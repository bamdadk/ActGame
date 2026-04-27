import os
import json
import re
from flask import Flask, render_template, request, redirect, url_for, session
from PyPDF2 import PdfReader

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_study_path'

# API keys are provided by the user via the upload form — no env vars needed.

# ── Shared LLM Prompt ────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert medical educator and question writer.
You will receive the full text extracted from a patient case report PDF.

Your job:
1. Read the text carefully and understand the clinical scenario.
2. Write a concise structured clinical brief (NOT a copy of the paper).
3. Extract or estimate patient vitals from the text.
4. Generate EXACTLY 10 multiple-choice questions that test understanding
   of the case. Each question must have 4 choices (A-D) and a correct_id.
   Questions should cover diagnosis, pathophysiology, treatment, prognosis,
   differential diagnosis, and clinical reasoning.

Respond with a raw JSON object ONLY (no markdown fences, no explanation).
The JSON must follow this exact schema:
{
    "case_id": "<short alphanumeric id>",
    "severity": "CRITICAL | URGENT | STABLE",
    "title": "<short descriptive title for the case>",
    "structured_brief": [
        {"section": "Patient History", "content": "<2-3 sentence summary of relevant history>"},
        {"section": "Clinical Presentation", "content": "<2-3 sentences on chief complaint & exam findings>"},
        {"section": "Diagnostic Findings", "content": "<1-2 sentences on labs, imaging, or key results>"}
    ],
    "vitals": {"hr": "110", "bp": "90/60", "o2": "88%", "temp": "38.2"},
    "parameters": [
        {"name": "Heart Rate",        "value": "110",   "unit": "bpm",  "icon": "favorite",       "color": "text-error"},
        {"name": "Blood Pressure",    "value": "90/60", "unit": "mmHg", "icon": "blood_pressure",  "color": "text-primary-fixed"},
        {"name": "Oxygen Saturation", "value": "88",    "unit": "%",    "icon": "pulmonology",     "color": "text-secondary-fixed"}
    ],
    "questions": [
        {
            "question": "...",
            "choices": [
                {"id": "A", "text": "..."},
                {"id": "B", "text": "..."},
                {"id": "C", "text": "..."},
                {"id": "D", "text": "..."}
            ],
            "correct_id": "A"
        }
    ]
}
The "questions" array MUST have EXACTLY 10 items.
Fill vitals with realistic values from the text (or reasonable estimates if not stated).
"""


# ── LLM Callers ──────────────────────────────────────────────────────────────

def _clean_json_response(text: str) -> str:
    """Strip markdown code fences the model might add."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


def call_openai(pdf_text: str, api_key: str) -> dict:
    """Call OpenAI GPT-4o-mini and return parsed JSON."""
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.4,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Here is the case report text:\n\n{pdf_text[:14000]}"},
        ],
    )
    raw = response.choices[0].message.content
    return json.loads(_clean_json_response(raw))


def call_gemini(pdf_text: str, api_key: str) -> dict:
    """Call Google Gemini and return parsed JSON."""
    from google import genai

    client = genai.Client(api_key=api_key)
    user_msg = f"{SYSTEM_PROMPT}\n\nHere is the case report text:\n\n{pdf_text[:14000]}"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_msg,
    )
    raw = response.text
    return json.loads(_clean_json_response(raw))


# ── Local Fallback (no API key) ──────────────────────────────────────────────

def extract_vitals(text):
    vitals = {"hr": "80", "bp": "120/80", "o2": "98%", "temp": "37.0"}
    hr = re.search(r'(?i)(hr|heart rate).*?(\d{2,3})', text)
    if hr: vitals["hr"] = hr.group(2)
    bp = re.search(r'(?i)(bp|blood pressure).*?(\d{2,3}\s*/\s*\d{2,3})', text)
    if bp: vitals["bp"] = bp.group(2)
    o2 = re.search(r'(?i)(o2|saturation|spo2|sat).*?(\d{2,3})\s*%', text)
    if o2: vitals["o2"] = o2.group(2) + "%"
    tmp = re.search(r'(?i)(temp|temperature).*?(\d{2}\.\d)', text)
    if tmp: vitals["temp"] = tmp.group(2)
    return vitals


def generate_local_fallback(pdf_text: str) -> dict:
    """Keyword-based fallback when no API key is available."""
    text_lower = pdf_text.lower()
    vitals = extract_vitals(pdf_text)

    cats = {
        "cardiology":  ["heart", "cardiac", "chest pain", "infarction", "arrhythmia", "ecg"],
        "respiratory": ["lung", "breath", "respiratory", "pneumonia", "cough", "wheeze"],
        "neurology":   ["brain", "stroke", "seizure", "headache", "consciousness", "gcs"],
    }
    scores = {c: sum(text_lower.count(k) for k in ks) for c, ks in cats.items()}
    best = max(scores, key=scores.get)

    sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', pdf_text) if len(s.split()) > 4]
    history      = " ".join(sentences[:2]) or "History not documented."
    presentation = " ".join(sentences[2:4]) or "Presented for evaluation."
    findings     = " ".join(sentences[4:6]) or "Pending results."

    title_map    = {"cardiology": "Cardiovascular Crisis", "respiratory": "Acute Respiratory Distress", "neurology": "Neurological Deficit"}
    severity_map = {"cardiology": "CRITICAL", "respiratory": "URGENT", "neurology": "CRITICAL"}

    questions = []
    for i in range(10):
        questions.append({
            "question": f"Question {i+1}: Based on the {best} findings, what is the best next step?",
            "choices": [
                {"id": "A", "text": "Immediate imaging (CT/MRI)"},
                {"id": "B", "text": "Administer pharmacological intervention"},
                {"id": "C", "text": "Discharge with outpatient follow-up"},
                {"id": "D", "text": "Consult specialist team"},
            ],
            "correct_id": "B",
        })

    return {
        "case_id": f"CASE-{len(pdf_text) % 9999}",
        "severity": severity_map.get(best, "URGENT"),
        "title": title_map.get(best, "General Medical Case"),
        "structured_brief": [
            {"section": "Patient History",        "content": history},
            {"section": "Clinical Presentation",  "content": presentation},
            {"section": "Diagnostic Findings",    "content": findings},
        ],
        "vitals": vitals,
        "parameters": [
            {"name": "Heart Rate",        "value": vitals["hr"],              "unit": "bpm",  "icon": "favorite",      "color": "text-error"},
            {"name": "Blood Pressure",    "value": vitals["bp"],              "unit": "mmHg", "icon": "blood_pressure", "color": "text-primary-fixed"},
            {"name": "Oxygen Saturation", "value": vitals["o2"].replace('%',''), "unit": "%",    "icon": "pulmonology",   "color": "text-secondary-fixed"},
        ],
        "questions": questions,
    }


# ── Main dispatcher ──────────────────────────────────────────────────────────

def generate_case_data(pdf_text: str, provider: str = None, api_key: str = None) -> dict:
    """Call the requested provider, then fall back to local extraction."""
    if api_key and provider:
        provider = provider.lower()
        if provider == 'openai':
            print("Using OpenAI GPT to generate case data...")
            try:
                return call_openai(pdf_text, api_key)
            except Exception as e:
                print(f"OpenAI call failed: {e}")
                raise
        elif provider == 'gemini':
            print("Using Google Gemini to generate case data...")
            try:
                return call_gemini(pdf_text, api_key)
            except Exception as e:
                print(f"Gemini call failed: {e}")
                raise

    print("No API key provided. Using local keyword-based fallback.")
    return generate_local_fallback(pdf_text)


# ── Flask Routes ─────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'case_report' not in request.files:
        return redirect(url_for('index'))

    file     = request.files['case_report']
    provider = request.form.get('provider', '').strip().lower()
    api_key  = request.form.get('api_key', '').strip()

    if file.filename == '':
        return redirect(url_for('index'))

    if file and file.filename.endswith('.pdf'):
        try:
            reader = PdfReader(file)
            extracted_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"

            case_data = generate_case_data(extracted_text, provider=provider, api_key=api_key)

            # Initialise quiz state
            session['case_data']       = case_data
            session['current_q_index'] = 0
            session['score']           = 0
            session['answers']         = []

            return redirect(url_for('mission_briefing'))
        except Exception as e:
            print(f"Error processing PDF: {e}")
            # Redirect back to index with an error flag so user can try again
            return redirect(url_for('index', error='api'))

    return "Invalid file format", 400


@app.route('/mission_briefing')
def mission_briefing():
    case_data = session.get('case_data')
    if not case_data:
        return redirect(url_for('index'))
    return render_template('mission_briefing.html', data=case_data)


@app.route('/multiple_choice_quest')
def multiple_choice_quest():
    case_data = session.get('case_data')
    q_index = session.get('current_q_index', 0)

    if not case_data or 'questions' not in case_data:
        return redirect(url_for('index'))

    if q_index >= len(case_data['questions']):
        return redirect(url_for('quest_results'))

    current_question = case_data['questions'][q_index]
    total_q = len(case_data['questions'])
    progress_percent = int(((q_index + 1) / total_q) * 100)

    return render_template(
        'multiple_choice_quest.html',
        question=current_question,
        q_index=q_index + 1,
        total_q=total_q,
        progress_percent=progress_percent,
    )


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    selected_id = request.form.get('choice_id')
    case_data = session.get('case_data')
    q_index = session.get('current_q_index', 0)

    if not case_data or q_index >= len(case_data['questions']):
        return redirect(url_for('index'))

    q = case_data['questions'][q_index]
    is_correct = (selected_id == q.get('correct_id'))
    if is_correct:
        session['score'] = session.get('score', 0) + 1

    # Record answer for the results breakdown
    answers = session.get('answers', [])
    answers.append({
        "q_num": q_index + 1,
        "question": q['question'],
        "selected": selected_id,
        "correct": q['correct_id'],
        "is_correct": is_correct,
    })
    session['answers'] = answers

    session['current_q_index'] = q_index + 1

    if session['current_q_index'] >= len(case_data['questions']):
        return redirect(url_for('quest_results'))

    return redirect(url_for('multiple_choice_quest'))


@app.route('/quest_results')
def quest_results():
    score = session.get('score', 0)
    case_data = session.get('case_data', {})
    answers = session.get('answers', [])
    total_q = len(case_data.get('questions', [])) if case_data else 10
    return render_template('quest_success.html', score=score, total=total_q, answers=answers)


@app.route('/quest_success')
def quest_success():
    return redirect(url_for('quest_results'))


@app.route('/open_ended_quest')
def open_ended_quest():
    return render_template('open_ended_quest.html')


@app.route('/clinically_energetic')
def clinically_energetic():
    return render_template('clinically_energetic.html')


@app.route('/quest_failure')
def quest_failure():
    return render_template('quest_failure.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)

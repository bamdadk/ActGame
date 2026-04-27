# ActGame Medical Study Path

An AI-powered, interactive medical case-study platform that turns any patient case report PDF into a structured clinical briefing and a 10-question multiple-choice quiz — scored in real time.

---

## Features

| Feature | Details |
|---|---|
| **PDF Upload** | Upload any patient case report PDF directly from the browser |
| **LLM-Driven Analysis** | Supports **OpenAI GPT-4o-mini** and **Google Gemini 2.5 Flash** |
| **Structured Clinical Brief** | Patient History · Clinical Presentation · Diagnostic Findings |
| **Vital Signs Dashboard** | Heart Rate, Blood Pressure, and Oxygen Saturation extracted from the document |
| **10-Question MCQ Quiz** | Auto-generated questions covering diagnosis, pathophysiology, treatment, and more |
| **Instant Scoring** | Live progress bar, per-answer feedback, and a final accuracy report |
| **Local Fallback** | Keyword-based case generation when no API key is supplied — no LLM required |
| **Zero Server Storage** | API key is entered in-browser per session and never stored on the server |

---

## Tech Stack

- **Backend** — [Flask](https://flask.palletsprojects.com/) (Python 3.10+)
- **PDF Parsing** — [PyPDF2](https://pypdf2.readthedocs.io/)
- **LLM Providers** — [OpenAI Python SDK](https://github.com/openai/openai-python) · [Google GenAI SDK](https://ai.google.dev/)
- **Frontend** — Vanilla HTML/CSS/JS · [Tailwind CSS](https://tailwindcss.com/) · Material Symbols icons
- **Templating** — Jinja2 (Flask built-in)

---

## Project Structure

```
stitch_medical_study_path/
├── app.py                         # Flask application & LLM dispatch logic
├── templates/
│   ├── index.html                 # Upload page — PDF + API key form
│   ├── mission_briefing.html      # Structured clinical brief & vitals dashboard
│   ├── multiple_choice_quest.html # Question-by-question MCQ interface
│   ├── quest_success.html         # Results page with score & answer breakdown
│   ├── quest_failure.html         # Error / failure state page
│   ├── open_ended_quest.html      # Open-ended question mode (extension)
│   └── clinically_energetic.html  # Supplementary educational content
├── requirements.txt               # Python dependencies
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/ActGame_medical_study_path.git
cd stitch_medical_study_path
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the development server

```bash
python app.py
```

Open your browser at **http://localhost:8080**.

---

## Usage

1. **Select** your AI provider — OpenAI or Google Gemini.
2. **Paste** your API key (or leave it blank to use the local fallback).
3. **Upload** a patient case report PDF via drag-and-drop or the file picker.
4. Click **Generate Questions** — the app extracts the text, calls the LLM, and redirects you to the **Mission Briefing**: a structured clinical brief with live vitals.
5. Click **Start Quiz** to begin the 10-question challenge.
6. After the last question, view your **Diagnostic Accuracy Report** with a full answer breakdown.

---

## API Keys

API keys are **never stored** on the server. They are submitted with the upload form, used for a single LLM call, and discarded when the request ends.

| Provider | Model used | Where to get a key |
|---|---|---|
| OpenAI | `gpt-4o-mini` | https://platform.openai.com/api-keys |
| Google Gemini | `gemini-2.5-flash` | https://aistudio.google.com/app/apikey |

---

## Local Fallback (no API key)

If no API key is provided, the app uses a keyword-based engine to:

- Detect the clinical specialty (cardiology, respiratory, neurology) from the PDF text.
- Extract vitals via regex patterns.
- Generate 10 placeholder MCQs appropriate to the detected specialty.

This mode is useful for testing the UI flow without incurring any API costs.

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## License

This project is licensed under the **MIT License** — see [`LICENSE`](LICENSE) for details.

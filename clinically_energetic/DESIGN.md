---
name: Clinically Energetic
colors:
  surface: '#0f131f'
  surface-dim: '#0f131f'
  surface-bright: '#353946'
  surface-container-lowest: '#0a0e1a'
  surface-container-low: '#171b28'
  surface-container: '#1b1f2c'
  surface-container-high: '#262a37'
  surface-container-highest: '#313442'
  on-surface: '#dfe2f3'
  on-surface-variant: '#b9cacb'
  inverse-surface: '#dfe2f3'
  inverse-on-surface: '#2c303d'
  outline: '#849495'
  outline-variant: '#3b494b'
  surface-tint: '#00dbe9'
  primary: '#dbfcff'
  on-primary: '#00363a'
  primary-container: '#00f0ff'
  on-primary-container: '#006970'
  inverse-primary: '#006970'
  secondary: '#f5fff2'
  on-secondary: '#003919'
  secondary-container: '#36ff8b'
  on-secondary-container: '#007238'
  tertiary: '#faf3ff'
  on-tertiary: '#3c0090'
  tertiary-container: '#e1d2ff'
  on-tertiary-container: '#7213ff'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#7df4ff'
  primary-fixed-dim: '#00dbe9'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#004f54'
  secondary-fixed: '#61ff97'
  secondary-fixed-dim: '#00e476'
  on-secondary-fixed: '#00210c'
  on-secondary-fixed-variant: '#005227'
  tertiary-fixed: '#e9ddff'
  tertiary-fixed-dim: '#d1bcff'
  on-tertiary-fixed: '#23005b'
  on-tertiary-fixed-variant: '#5700c9'
  background: '#0f131f'
  on-background: '#dfe2f3'
  surface-variant: '#313442'
typography:
  h1:
    fontFamily: Space Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  h2:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  h3:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-caps:
    fontFamily: Lexend
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
  stat-value:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 24px
  lg: 40px
  xl: 64px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
---

## Brand & Style

The design system is engineered to evoke the atmosphere of a high-stakes, futuristic medical laboratory merged with the adrenaline of a competitive arena. It targets medical professionals and students who require high precision but benefit from the engagement of gamification. The visual language balances professional clinical credibility with "neon-noir" energy.

The aesthetic utilizes **Glassmorphism** and **High-Contrast Bold** styles. This combination ensures that data feels layered and complex, yet accessible and urgent. UI elements should feel like holographic projections within a dark, sophisticated environment, utilizing translucency to maintain a sense of depth without cluttering the diagnostic workspace.

## Colors

The palette is anchored by a deep midnight blue base, providing a high-contrast foundation for "electric" accents. 

- **Primary (Electric Blue):** Used for interactive elements, primary actions, and "active" state indicators. It represents the "High-Tech" aspect of the system.
- **Secondary (Emerald Green):** Reserved for progress, success states, "streak" indicators, and health-related confirmations. It represents the "Medical/Vitality" aspect.
- **Tertiary (Cyber Purple):** Used sparingly for rare achievements or specialized data categories.
- **Neutral:** A range of dark navy tones used for structural depth. Surface containers utilize a semi-transparent hex with an alpha channel to facilitate the glassmorphism effect.

## Typography

This design system uses a triple-font approach to distinguish between navigation, data, and action.

- **Space Grotesk (Headlines):** Its geometric, technical character provides the "futuristic lab" feel. Large headers should be tightly tracked to feel impactful and urgent.
- **Inter (Body):** Used for all clinical descriptions and long-form study material to ensure maximum legibility and professional neutrality.
- **Lexend (Labels/Stats):** Chosen for its athletic, readable qualities to represent game mechanics like scores, timers, and progress percentages.

## Layout & Spacing

The layout follows a **Fluid Grid** model with a strict 8px rhythmic scale. Content is organized into modular cards that adapt to screen width, ensuring that data-heavy clinical views remain scannable.

- **Grid:** A 12-column system for desktop, collapsing to 4 columns for mobile.
- **Rhythm:** Use `md` (24px) for standard padding within containers. Use `lg` (40px) to separate distinct "quest" or "module" sections. 
- **Density:** Clinical data views can drop to `sm` (12px) spacing to maximize information density, while gamified splash screens should use `xl` (64px) to emphasize heroic elements.

## Elevation & Depth

Depth is achieved through **Glassmorphism** rather than traditional drop shadows. Surfaces do not "float" using darkness; they "glow" and "blur" to indicate hierarchy.

1.  **Level 0 (Floor):** Midnight blue background.
2.  **Level 1 (Default Container):** Semi-transparent dark navy with a 12px backdrop blur and a subtle 1px inner border (opacity 10%) to define the edges.
3.  **Level 2 (Active/Hover):** Increased transparency and a thin primary-colored outer glow (0px 0px 15px rgba(0, 240, 255, 0.3)).
4.  **Level 3 (Modals/Overlays):** 20px backdrop blur with a more pronounced border.

All containers should feel like glass panels catching the light from the neon accents.

## Shapes

The shape language is **Rounded**, avoiding the harshness of a pure military-tech look to keep the experience approachable and "energetic."

- **Standard Elements:** 0.5rem (8px) radius for buttons and input fields.
- **Feature Cards:** 1rem (16px) radius for module cards and glass containers.
- **Gamified Elements:** Progress bar caps and "Streak" badges should use the `rounded-xl` (1.5rem) or full pill-shape to feel more like game tokens than clinical forms.

## Components

### Buttons
- **Primary:** Solid Electric Blue with black text for maximum punch. High-gloss finish.
- **Secondary:** Outlined with a 1px Emerald Green border and subtle glow on hover.
- **Ghost:** Transparent background with white text, used for less critical navigation.

### Progress Bars & Streaks
- Progress bars should feature a "pulse" animation on the leading edge. 
- Use a dual-tone gradient (Primary to Secondary) to indicate "filling" energy.
- Streak indicators should use a flame icon paired with Emerald Green glow effects.

### Inputs & Cards
- **Input Fields:** Dark background with a bottom-only 2px border that "lights up" in Primary Blue when focused.
- **Cards:** Utilize the glassmorphic style. Headers within cards should have a subtle horizontal separator line using 5% white opacity.

### Feedback Elements
- **Success State:** Emerald Green text with a "Vitality" icon.
- **Critical State:** Electric Blue with a "Warning" amber pulse for high-stakes quiz questions.
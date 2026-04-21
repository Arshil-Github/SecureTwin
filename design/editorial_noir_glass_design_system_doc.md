# Editorial Noir Glass — SecureWealth Twin

## North Star: "Contextual Financial Intelligence"
SecureWealth Twin is a premium, AI-native financial companion. The design avoids traditional banking clichés in favor of an "Editorial Noir" aesthetic—combining high-contrast typography, deep glassmorphism, and intentional whitespace to make financial data feel like a high-end briefing rather than a spreadsheet.

---

## Visual Language

### 1. Color Palette
The palette is built on a "Solid Ink" foundation with high-visibility functional accents.

- **Surface (Ink Black):** `#080C14` — Solid, deep background for maximum contrast.
- **Surface Container (Glass):** `rgba(13, 20, 33, 0.4)` — Layered cards with `backdrop-blur-md`.
- **Primary (Electric Teal):** `#00E5C0` — Used for growth, health, and primary actions.
- **Secondary (Warm Ivory):** `#F2EDE4` — Primary text color; provides a premium, non-clinical feel.
- **Warning (Ember Amber):** `#FF9B3D` — For at-risk goals, budget alerts, and moderate friction.
- **Error (Deep Crimson):** `#E63946` — Reserved for high-risk blocks and critical wealth gaps.

### 2. Typography
A balance of geometric precision and editorial weight.

- **Headlines & Data Hero:** **Epilogue (Bold/Black)**
  - Tracking: `-0.02em` for large numbers.
  - Case: Uppercase for brand headers; Sentence case for narratives.
- **Body & Technical UI:** **Epilogue (Regular/Medium)**
  - Used for insights, labels, and micro-copy.
  - Emphasis: Bold for impact metrics.

### 3. Glassmorphism & Depth
- **Borders:** Every card uses a `1px` solid border: `rgba(255, 255, 255, 0.1)`.
- **Elevation:** No drop shadows. Depth is created through layer transparency and border definition.
- **Glow Effects:** Functional elements (charts, gauges, status pips) use subtle outer glows (e.g., `drop-shadow-[0_0_8px_rgba(0,229,192,0.4)]`) to signify "live" intelligence.

---

## Core Component Patterns

### 1. The Pulse Hero
The central net worth display features a glowing "Wealth Pulse" line. The line's amplitude reflects portfolio health—smooth waves for stability, jagged for volatility.

### 2. Focus Cards
Used for "Today's Focus." These are vertically stacked with 12px internal padding and 24px section spacing. They use left-accent borders (Teal or Amber) to denote priority.

### 3. Intelligence Grid
Non-traditional layout for portfolio health. Factors are displayed as asymmetrical tiles where size correlates to "Intelligence Weight."

### 4. Thinking Chat
The AI interface uses a "thinking" pulse (Twin Glyph) instead of standard typing indicators. Messages are framed in deep-layer glass cards with high-contrast Ivory text.

---

## Spatial System
- **Base Unit:** 4px
- **Screen Padding:** 24px (Ultra-generous for premium feel)
- **Section Gap:** 32px
- **Component Gap:** 16px

---

## Design Principles
1. **Emotion Before Information:** Lead with status (Health Score, Stress) before raw numbers.
2. **Numbers That Speak:** Every metric is accompanied by a plain-language narrative.
3. **Friction is a Feature:** Use the "Pause Mechanic" (5s countdown) for medium-risk actions instead of disruptive modals.

# SmartCompost Design System

> [!IMPORTANT]
> **Theme**: "Nature / Compost / Rétro"
> **Core Philosophy**: **STRICT PIXEL ART**. No anti-aliasing, no rounded corners, no emojis. Everything is built with CSS blocks or pixelated assets.

## 🎨 Palette (The "Compost Biosphere")

### Soils & Earth
- **Humus (Dark)**: `bg-[#3E2723]`
- **Active Soil (Mid)**: `bg-[#5D4037]`
- **Dry Soil (Light)**: `bg-[#795548]`
- **Clay (Argile)**: `bg-[#1E88E5]`

### Life & Indicators
- **Plant Green**: `bg-[#558B2F]` (Borders/Accents)
- **Warning Red**: `bg-red-500` (Heat/Danger)
- **Cold Blue**: `bg-blue-400` (Wet/Cold)
- **Gold/Highlight**: `bg-[#FFD700]`

## 📐 Pixel Art Rules (The "Commandments")

1.  **NO Rounded Corners**: `rounded-none` everywhere. Buttons, windows, bars must be sharp.
2.  **NO Emojis**: Use CSS-drawn icons (divs with absolute positioning) or pixel-art SVG/PNG.
    *   *Bad*: 🌡️, 💧, 🐛
    *   *Good*: `<Probe />`, `<Dial />`, Custom CSS Wriggler.
3.  **Thick Borders**: Use `border-2` or `border-4` to mimic retro game UI.
4.  **Shadows**: Hard shadows only. `shadow-[4px_4px_0_black]`. No soft blur.
5.  **Fonts**: `font-pixel` (VT323 or similar) for all text.

## 🧱 Key Components

### `<RetroWindow />`
The standard container for modals and details.
- **Background**: Dark Brown (`#3E2723`)
- **Border**: Thick Light Green (`#558B2F`)
- **Shadow**: Hard Black offset.

### Icons & Assets
- **Probe**: Pixel art metal spike for sensors.
- **Dial**: Analog circle (made of square pixels if possible, or sharp steps) for temperature.
- **Worms**:
    - **Anecic**: Stack of brown squares (Vertical).
    - **Endogeic**: Line of pink squares (Horizontal).

## 🎬 Animations
- **Movement**: Use `steps(n)` to simulate frame-by-frame animation. Avoid linear smoothing (`ease-in-out` is okay for accumulation, but movement should be jerky).
- **Particles**: 1px or 2px blocks moving in straight lines or discrete steps.

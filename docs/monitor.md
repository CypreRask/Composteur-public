# Web Monitor Documentation

## 🏗️ Architecture

The Web Monitor is a Svelte-based frontend (`/web-monitor/frontend`) communicating with a Python backend (`/web-monitor/backend`) via HTTP/WebSocket (or simple polling currently).

### 📁 Structure (`src/`)

*   `App.svelte`: Root orchestrator. Handles navigation (Monitor vs Learn), "God Mode", and global layout.
*   `styles/`: Contains tailwind setup and `font-pixel` definitions.

### 🌍 The "World" Components

These components simulate the physical ecosystem. They are "Data-Driven": they visually react to props like `temp`, `humidity`, `weather`.

1.  **`Surface.svelte`**
    *   *Role*: The visible top layer. Tree, Grass, Sky.
    *   *Logic*: Day/Night cycle, Rain rendering. Contains the `CompostCabin` placement.

2.  **`CompostCabin.svelte`** (The Core)
    *   *Role*: Representation of the physical compost bin.
    *   *Features*:
        - **Hardware**: Pixel-art sensors (`Probe`, `Dial`) reflecting real data.
        - **Layers**: 3 internal zones (Surface, Core, Bottom) showing the composting process stages.
        - **Interactivity**: Clickable zones to open "Microscope" details.

3.  **`Underground.svelte`**
    *   *Role*: The soil beneath.
    *   *Features*:
        - **Geology**: Procedural generation of rocks/fossils.
        - **Biology**: Worms (Anecic/Endogeic) moving autonomously.
        - **Cycles**: Visualizing Carbon/Nitrogen flux particles.

### 📊 The "Data" Components

1.  **`Hud.svelte`**
    *   *Role*: RPG-like overlay.
    *   *Features*: XP Bar, Level, Inventory (collected resources), Notifications.

2.  **`DataView.svelte`**
    *   *Role*: Scientific dashboard. Charts and precise metrics.

3.  **`LearnView.svelte` / `widgets/`**
    *   *Role*: Educational minigames (Arcade).
    *   *Games*:
        - **CompostSorter**: Sorting arcade game.
        - **CycleBuilder**: God-game simulation of compost phases.

## 🔌 Data Flow
1.  **Backend** (`main.py`) aggregates MQTT sensors -> JSON endpoint.
2.  **Frontend** (`App.svelte`) fetches JSON every N seconds.
3.  **Props**: Data is passed down: `App` -> `Surface`/`Underground` -> `CompostCabin`.

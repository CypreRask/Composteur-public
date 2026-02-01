# C/N Estimation Engine Implementation (Report V2)

- [x] **Analyze Report V2** <!-- id: 0 -->
    - [x] Compare V1 (Mass Balance) vs V2 (Ratio Trends) <!-- id: 1 -->
    - [x] Validate feasibility with current sensors (MQ + SCD41 + EC) <!-- id: 2 -->
- [x] **Architecture Design** <!-- id: 3 -->
    - [x] Create `implementation_plan.md` for the new pipeline <!-- id: 4 -->
    - [x] Define Python data structures (Pandas/Polars equivalent or lightweight lists) <!-- id: 5 -->
    - [x] Create V3 Technical Specification (`technical_specification_v3.md`) <!-- id: 17 -->
- [x] **Implementation: Core Logic (`heuristic_engine.py`)** <!-- id: 6 -->
    - [x] Implement `compute_indices` (R1, R2, R3, EC_norm) <!-- id: 7 -->
    - [x] Implement `detect_spikes` (Z-score/MAD) <!-- id: 8 -->
    - [x] Implement `apply_gating` (Anaerobic, Inactive, Mature) <!-- id: 9 -->
    - [x] Implement `compute_score` (Weighted Log Sum) <!-- id: 10 -->
    - [x] Prototype Digital Twin Trainer (`digital_twin_trainer.py`) <!-- id: 18 -->
- [x] **Integration** <!-- id: 11 -->
    - [x] Replace `physics_engine.py` usage in `main.py` <!-- id: 12 -->
    - [x] Connect to `ingest.py` (optional, for live processing) or `main.py` (on-read) <!-- id: 13 -->

- [x] **Frontend Update** <!-- id: 14 -->
    - [x] Update `DataView.svelte` to display the new Score (0-100) and Reliability Flags <!-- id: 15 -->
    - [ ] Update `Hud.svelte` or `Surface.svelte` if needed <!-- id: 16 -->

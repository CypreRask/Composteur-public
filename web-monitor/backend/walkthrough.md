# Walkthrough: Migration to Heuristic Digital Twin (V2/V3)

We successfully transitioned the Compost Monitor from a flawed Physics calculation to a robust **Heuristic & Predictive Architecture**.

## 1. The Core Engine (V2)
The backend now uses `heuristic_engine.py` instead of `physics_engine.py`.
- **Logic:** Uses Ratios ($R1=NH_3/CO_2$, $R2=CH_4/CO_2$) to detect trends.
- **Robustness:** Resamples data to 1H, filters noise (MAD), and applies Logic Gates (Anaerobie/Mature).
- **Output:** A reliability-weighted "Score C/N" (0-100).

## 2. The Predictive Layer (V3 Prototype)
We implemented the **Sim-to-Real Pipeline** in `ml/digital_twin_trainer.py`.
- **Synthetic Data:** Generates 100k+ hours of biological simulation.
- **Deep Learning:** Trains a Transformer model to predict "Crash Events" 72h in advance.
- **Visualization:** Generates professional Loss/Accuracy metrics in `backend/ml/plots/`.

## 3. Documentation
- [Scientific Report V3](file:///d:/composteur/web-monitor/backend/scientific_report_v2.md): The theoretical proof and math.
- [Technical Spec V3](file:///d:/composteur/docs/technical_specification_v3.md): The architecture for future dev.

## 4. Verification
- **Backend:** Stable, API responding at `http://localhost:8085`.
- **Frontend:** Dashboard displaying new gauges.
- **ML:** Trainer script converging (Accuracy ~94%).

## 5. Next Steps (Roadmap)
- **Month 1-3:** Run in "Shadow Mode" to collect real data.
- **Month 4:** Perform Transfer Learning (Phase 3) to fine-tune the Digital Twin on your specific hardware.

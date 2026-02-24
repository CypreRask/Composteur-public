# Architecture Specification: Hybrid Digital Twin for Predictive Composting (V3)

**Project:** Smart Compost Monitor  
**Date:** February 1, 2026  
**Status:** Conceptual Framework  
**Reference:** Internal Research "Kimi-V3"

---

## 1. Executive Summary
This document defines the "V3" architecture for the Compost Intelligence System. Moving beyond simple heuristics (V2), V3 implements a **Hybrid Mechanistic-Stochastic Digital Twin**. Its primary goal is not to curve-fit historical data, but to estimate the **Latent Biological State** of the pile to predict critical failure events (Anaerobia, Activity Crash) with a 72h-120h horizon.

## 2. Sensor Topology: Causes vs. Symptoms
A critical insight of V3 is the hierarchical classification of inputs. To prevent "learning artifacts," we distinguish between the *drivers* of the system and its *manifestations*.

### 2.1 Core Drivers (The "Causes") [High Reliability]
These sensors measure the physical boundary conditions that dictate biological possibility.
*   **Temperature ($T$):** Direct proxy for Metabolic Rate (Respiration/Degradation of $C_{fast}$).
*   **Humidity ($W$):** Key to Oxygen Transport (Diffusion coefficient $D_{O2} \propto f(W)$). Excess leads to pore clogging (Anaerobia).
*   **pH:** Determines the chemical equilibrium of Ammonia ($NH_3 \leftrightarrow NH_4^+$). High pH + High T = Volatilization Risk.
*   **EC (Conductivity):** Proxy for Mineralization (Salinity) and Humification. High EC can act as an inhibitor.

### 2.2 Gas Signatures (The "Symptoms") [Low Reliability / High Latency]
Gas sensors measure the *result* of biological activity, modified by transport delays.
*   **CO₂:** Aerobic Respiration (Lagged by diffusion).
*   **CH₄:** The primary signature of **Anaerobic Shifts** (Methanogenesis). Depends heavily on "anoxious pockets" fraction.
*   **NH₃:** Nitrogen saturation or C/N imbalance.
*   **CO:** Artifact/Trace signal, weighted weakly.

**Strategy:** The model must effectively "invert" the transport function: $Observation(t) = Transport(State(t-\delta)) + Noise$.

## 3. The Digital Twin Architecture

### 3.1 Latent State Vector ($\vec{x}_t$)
The Digital Twin estimates variables that cannot be directly measured but define the system's future trajectory:

*   $A(t)$: **Effective Microbial Activity** (Biomass active fraction).
*   $C_{fast}(t)$: **Bio-available Carbon** stock (Sugars/Cellulose).
*   $N_{avail}(t)$: **Mineralized Nitrogen** stock ($NH_4^+/NO_3^-$).
*   $W_{eff}(t)$: **Effective Saturation** (Pore occupancy).
*   $K_{O2}(t)$: **Aeration Capacity** (Estimated Porosity/Percolation).
*   $AnaFrac(t)$: **Anoxic Fraction** (0.0 to 1.0).

### 3.2 The Hybrid Model
The Twin operates in "Shadow Mode," updating its state $\vec{x}_t$ at each time step.

#### A. Mechanistic Core (The Physics)
defines the evolution of $\vec{x}_t$:
$$ \frac{dA}{dt} = \mu(T, W, pH) \cdot \frac{C_{fast}}{K_c + C_{fast}} - Decay $$
$$ \text{AnaFrac} = f(W_{eff}, K_{O2}) \quad (\text{if Demand } O_2 > \text{Supply } O_2) $$

#### B. Observation Layer (The Sensor Model)
Maps state to expected measurements (Inverse Problem):
$$ CO_{2,measured}(t) = \text{Diffuse}(A(t) \cdot \text{AerobicFrac}) + \epsilon_{drift} $$

### 3.3 Probabilistic Prediction (The Ensemble)
Instead of a single curve, the V3 system projects an **Ensemble of N=50 trajectories** into the future (J+5), sampling uncertainties in:
1.  Weather (Rain/Temp).
2.  Intervention (User limits).
3.  Model Error (Process Noise).

**Output:** Hazard Probability $P(E|t_{now})$
*   "Probability of Anaerobia > 50% in 48h"
*   "Probability of Activity Crash > 80% in 72h"

## 4. Implementation Strategy

### 4.1 Synthetic Training ("Sim-to-Real")
To train the ML components (Residual Correction & Hazard Function), we generate a massive synthetic dataset via **Domain Randomization**:
*   Simulate sensor drift (Offset/Gain walk).
*   Simulate membrane delays (1h - 48h).
*   Simulate heterogeneity (Spotty anaerobic pockets).
*   Simulate "External Events" (Turning, Adding Greens, Rain).

The ML model learns to map *noisy, delayed sensor history* to *clean latent state probabilities*.

### 4.2 The "What-If" Engine
By accessing the Latent State, the system can simulate counterfactuals:
*   *Action:* "Add 5kg Dry Matter (Browns)" $\rightarrow$ $W_{eff} \downarrow, K_{O2} \uparrow$.
*   *Prediction:* $P(Anaerobia)$ drops from 85% to 12%.
*   *Recommendation:* "Add Browns to prevent imminent crash."

## 5. Deployment Roadmap

### Phase 1: Robust Alerting (Current V2+)
*   Model: Heuristic Rules + Trend Detection (V2 Engine).
*   Output: Current State + Naive Trend (Linear).

### Phase 2: Shadow Twin (V3 Alpha)
*   Model: Mechanistic State Estimator running in real-time.
*   Output: Latent Variables displayed ($C_{fast}$ stock estimate), 5-day Projection.

### Phase 3: Neural Residuals (V3 Beta)
*   Model: Deep Learning trained on Synthetic Data corrects the Mechanistic Kernel.
*   Output: Predictive Maintenance, Sensor Fault Detection ("CO2 mismatch implies sensor failure").

## 6. Conclusion
The V3 Architecture represents a paradigm shift from "Monitoring" to "Management." By distinguishing drivers from symptoms and modelling the hidden biological state, the system transitions from a passive observer to an active, predictive expert system capable of guiding the user through the composting process with scientifically grounded foresight.

# 📱 Predicting Teen Mental Health Crisis via Phone Usage
**Project Type:** Classification (Random Forest) | **Client:** Health Insurance Provider

graph TD
    %% Styling Definitions
    classDef business fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef data fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    classDef model fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef deploy fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef value fill:#ffccbc,stroke:#d84315,stroke-width:2px,stroke-dasharray: 5 5;

    subgraph Phase1 [Phase 1: Business Understanding]
        A[<b>Goal</b>: Reduce Crisis Claims] --> B(Cost of Crisis: $2,673)
        B --> C(Cost of Prevention: $200)
        C --> D{Strategy: Optimize Recall}
    end

    subgraph Phase2 [Phase 2: Data Prep & Engineering]
        E[Raw Data: 3,000 Teens] --> F[Feature Engineering]
        F --> G(Usage-to-Sleep Ratio)
        F --> H(App Diversity / Switching)
        F --> I(Social Media Duration)
    end

    subgraph Phase3 [Phase 3: Modeling & Tuning]
        J[Random Forest Classifier] --> K{Threshold Tuning}
        K -- Default 0.5 --> L[Recall: 88% <br> Missed 12% of Risk]
        K -- <b>Tuned 0.40</b> --> M[<b>Recall: 92%</b> <br> Defensive Safety Net]
    end

    subgraph Phase4 [Phase 4: Deployment & ROI]
        M --> N{Is Risk > 40%?}
        N -- Yes --> O[Trigger Wellness Check]
        N -- No --> P[No Action]
        O --> Q[<b>Net Value Lift</b> <br> +$377,512 vs Baseline]
    end

    %% Connections
    D --> E
    I --> J
    
    %% Apply Styles
    class A,B,C,D business;
    class E,F,G,H,I data;
    class J,K,L,M model;
    class N,O,P deploy;
    class Q value;

## 🎯 Executive Summary
**The Problem:** Teen mental health crises are rising and expensive. A single "Crisis Episode" (e.g., ER visit, inpatient care) costs our insurer client **$2,673**. The current industry standard—flagging teens who use phones >5 hours/day—is reactive and fails to detect **34%** of high-risk cases.

**The Solution:** We built a **Random Forest Classifier** to predict "High-Risk" teens based on behavioral patterns (not just volume). Our model is optimized for **Recall (Safety)**, prioritizing the detection of at-risk teens over avoiding false alarms.

**The Impact:**
* **Recall Lift:** Improved detection rate from **66% (Status Quo) → 92% (Our Model)**.
* **Financial ROI:** On a test set of 600 teens, our model captured **$377,512** in net value over the baseline by preventing costly crisis episodes via early intervention ($200/teen).

---

## 👥 The Team (TMP 422 - Data & Decision Analytics)
| Name | Role | Responsibility |
|------|------|----------------|
| **Jeitī Trujillo** | Project Manager | Strategy, ROI analysis, stakeholder alignment, deck ownership. |
| **Octavio Gzain** | Technical Lead | Architecture decisions, GitHub repo management, code review. |
| **Aishwarya Mundada** | Lead Modeler | Algorithm selection (Random Forest), hyperparameter tuning. |
| **Chinmaiye Gandhi** | Data Engineer | Data cleaning, pipeline construction, feature engineering. |
| **Maya Parra** | Business Analyst | Unit economics, business value proposition, storytelling. |
| **Mohammad Ameen** | Quality Assurance | Error analysis, bias auditing, assumption testing. |

---

## 🔄 Project Lifecycle (CRISP-DM Methodology)

### **1. Business Understanding**
* **Objective:** Minimize the total cost of teen mental health claims.
* **Success Metric:** Net Value = `(True Positives * Savings) - (False Positives * Cost)`.
* **Constraint:** False Negatives (missed crises) are 13x more expensive than False Positives.

### **2. Data Understanding & Preparation (HW 3)**
* **Dataset:** 3,000 rows of teen behavioral data (Usage, Sleep, Grades, Social).
* **Audit Results:** Zero missing values; detected outliers in `Phone_Checks_Per_Day` (Max: 150+).
* **Feature Engineering:**
    * `Usage_to_Sleep_Ratio`: Measures sleep displacement.
    * `App_Diversity`: (Phone Checks / Apps Used Daily) – A proxy for "compulsive switching."
    * **Leakage Control:** Explicitly removed `Addiction_Level` (target) from the training set.

### **3. Modeling & Evaluation (HW 4)**
* **Model:** Random Forest Classifier (chosen for non-linear relationships and outlier robustness).
* **Tuning Strategy:** Applied **Threshold Tuning**. We lowered the decision boundary from **0.50 → 0.40** to create a "Defensive" model.
* **Performance:**
    * **Baseline (5-Hour Rule):

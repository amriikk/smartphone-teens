# 📱 Predicting Teen Mental Health Crisis via Phone Usage
**Project Type:** Classification (Random Forest) | **Client:** Health Insurance Provider

[Image of CRISP-DM process diagram]

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

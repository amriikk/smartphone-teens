# 📱 Predicting Teen Mental Health Crisis via Phone Usage

**Course:** TMP 422 - Data Mining & Analytics (Winter 2026)  
**Institution:** UC Santa Barbara  
**Status:** 🟢 Active (Week 4/10)  

## 📖 Executive Summary
**The Business Problem:** Reactive mental health care for teens is expensive and often too late. For insurers, a single "crisis episode" (e.g., ED visit or inpatient admission) costs an average of **$2,673**. By the time a claim is filed, the member's health has already deteriorated significantly.

**The Solution:** Acting as a Data Science Consulting Team, we are building a **Classification Model** to predict high-risk teens ("Crisis" vs. "Non-Crisis") based on daily phone usage patterns, sleep metrics, and social interaction data.

**The Impact:** Our goal is to shift from reactive claims coverage to preventative care. By achieving a target **Recall of 90%+**, we aim to trigger low-cost interventions (e.g., wellness coaching, parental alerts) *before* a clinical crisis occurs. This prioritizes minimizing false negatives, as missing a high-risk teen carries a much higher cost than flagging a healthy one.

---

## 👥 The Team
| Name | Role | Responsibility |
|------|------|----------------|
| **Jeiti Trujillo** | Project Manager | Timeline management, stakeholder alignment, deliverable ownership. |
| **Octavio Gzain** | Technical Lead | Architecture decisions, code review, GitHub repo management. |
| **Aishwarya Mundada** | Lead Modeler | Algorithm selection, hyperparameter tuning, model validation. |
| **Chinmaiye Gandhi** | Data Engineer | Data cleaning, pipeline construction, feature engineering. |
| **Maya Parra** | Business Analyst | Business value proposition, unit economics, storytelling. |
| **Mohammad Ameen** | Quality Assurance | Error analysis, bias auditing, assumption testing. |

---

## 📅 Project Timeline (CRISP-DM)
*This project follows the CRISP-DM methodology over a 10-week quarter.*

* **Phase 1: Business Understanding** (Weeks 1-3) ✅ **COMPLETED**
    * Defined scope: Crisis Prevention for Health Insurers.
    * Established Success Metric: 90% Recall to minimize risk of unflagged crisis events.
    * [Link to Pitch Deck (PDF)](deliverables/GroupHW1_PitchDeck.pdf)
* **Phase 2: Data Understanding & Preparation** (Weeks 4-5) 🚧 **IN PROGRESS**
    * Exploratory Data Analysis (EDA).
    * Data cleaning (handling nulls, outliers).
    * Feature engineering on usage metrics.
* **Phase 3: Modeling** (Weeks 6-7) ⏳ *Upcoming*
    * Model selection (Logistic Regression, Random Forest, etc.).
    * Training and Validation.
* **Phase 4: Evaluation** (Week 8) ⏳ *Upcoming*
    * Testing against success metrics (Recall/Precision trade-off).
    * Cost-Benefit Analysis using Unit Economics.
* **Phase 5: Deployment & Final Report** (Weeks 9-10) ⏳ *Upcoming*
    * Final "Client" Presentation.

---

## 📊 The Data
**Source:** [Kaggle: Teen Phone Addiction & Mental Health](https://www.kaggle.com/datasets/sumedh1507/teen-phone-addiction)  
**Size:** ~3,000 Records  

**Key Features:**
* **Predictors (Usage):** `Daily_Usage_Hours`, `Social_Interactions`, `Screen_Time_Before_Bed`, `Phone_Checks_Per_Day`.
* **Predictors (Context):** `Sleep_Hours`, `Academic_Performance`, `Parental_Control`.
* **Target Variables:** `Anxiety_Level` (Scale 0-10), `Depression_Level` (Scale 0-10).

---

## 🛠️ Tech Stack & Setup
This project uses **Python 3.x** and standard data science libraries.

**Installation:**
```bash
# Clone the repo
git clone [https://github.com/amriikk/smartphone-teens.git](https://github.com/amriikk/smartphone-teens.git)

# Install requirements (once file is created)
pip install -r requirements.txt
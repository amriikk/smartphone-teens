# 📱 Predicting Teen Mental Health Crisis via Phone Usage
**Project Type:** Classification (Random Forest) | **Client:** Health Insurance Provider

![CRISP-DM Framework](./images/CRISP-DM.png)

## 🎯 Executive Summary
**The Problem:** Teen mental health crises are rising and expensive. A single "Crisis Episode" (e.g., ER visit, inpatient care) costs our insurer client **$2,673**. The current industry standard—flagging teens who use phones >5 hours/day—is reactive and fails to detect **34%** of high-risk cases.

**The Solution:** We built a **Random Forest Classifier** to predict "High-Risk" teens based on behavioral patterns (not just volume). Our model is optimized for **Recall (Safety)**, prioritizing the detection of at-risk teens over avoiding false alarms.

**The Impact:**
* **Recall Lift:** Improved detection rate from **66% (Status Quo) → 92% (Our Model)**.
* **Financial ROI:** On a test set of 600 teens, our model captured **$377,512** in net value over the baseline by preventing costly crisis episodes via early intervention ($200/teen).

---

## 👥 The Team (TMP 422 - Data & Decision Analytics)

![Data Science Team](./images/team.png)

| Name | Role | Responsibility |
|------|------|----------------|
| [**Jeitī Trujillo**](https://www.linkedin.com/in/jeiti/) | Project Manager | Strategy, ROI analysis, stakeholder alignment, deck ownership. |
| [**Octavio Gzain**](https://www.linkedin.com/in/octavio-gzain/) | Technical Lead | Architecture decisions, GitHub repo management, code review. |
| [**Aishwarya Mundada**](https://www.linkedin.com/in/aishwarya-mundada/) | Lead Modeler | Algorithm selection (Random Forest), hyperparameter tuning. |
| [**Chinmaiye Gandhi**](https://www.linkedin.com/in/chinmaiye/) | Data Engineer | Data cleaning, pipeline construction, feature engineering. |
| [**Maya Parra**](https://www.linkedin.com/in/maya-parra/) | Business Analyst | Unit economics, business value proposition, storytelling. |
| [**Mohammad Ameen**](https://www.linkedin.com/in/mohammadmameen/) | Quality Assurance | Error analysis, bias auditing, assumption testing. |

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

---

## How to Run the Data Quality Report

This guide will help you run the data quality analysis script, even if you're not familiar with programming.

### What You'll Need

- A computer with macOS, Windows, or Linux
- Python 3.8 or newer installed on your computer

### Step-by-Step Instructions

#### 1. Open the Terminal (or Command Prompt)

**On Mac:**
- Press `Cmd + Space`, type "Terminal", and press Enter

**On Windows:**
- Press `Windows key`, type "Command Prompt" or "PowerShell", and press Enter

#### 2. Navigate to the Project Folder

Type the following command and press Enter (replace the path with where you saved this project):

```bash
cd /path/to/smartphone-teens
```

For example, if you downloaded it to your Documents folder:
- **Mac:** `cd ~/Documents/smartphone-teens`
- **Windows:** `cd C:\Users\YourName\Documents\smartphone-teens`

#### 3. Set Up the Environment (First Time Only)

Run these commands one at a time:

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### 4. Run the Data Quality Report

Make sure your virtual environment is activated (you should see `(venv)` at the start of your command line), then run:

**Mac/Linux:**
```bash
python data_quality_report.py teen_phone_addiction_dataset.csv
```

**Windows:**
```bash
python data_quality_report.py teen_phone_addiction_dataset.csv
```

#### 5. View the Report

After the script finishes, you'll see a summary in the terminal. A detailed HTML report will be created in the same folder called:

```
teen_phone_addiction_dataset_quality_report.html
```

**To open the report:** Double-click the HTML file, and it will open in your web browser.

### Running on Your Own Data

To analyze a different CSV file, just replace the filename:

```bash
python data_quality_report.py your_data_file.csv
```

### Troubleshooting

| Problem | Solution |
|---------|----------|
| `command not found: python3` | Python is not installed. Download it from [python.org](https://www.python.org/downloads/) |
| `No module named 'pandas'` | Run `pip install -r requirements.txt` again |
| `No such file or directory` | Make sure you're in the correct folder and the CSV file exists |

### What the Report Shows

The data quality report analyzes your dataset for:

- **Missing Values** - Cells with no data
- **Outliers** - Unusual values that might be errors
- **Duplicates** - Repeated rows
- **Data Types** - What kind of data each column contains
- **Categorical Values** - All unique values for text/category columns


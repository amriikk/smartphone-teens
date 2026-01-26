# 📱 Predicting Teen Mental Health Crisis via Phone Usage

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


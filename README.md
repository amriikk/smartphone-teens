# smartphone-teens
TMP Data Science Project

## Title

### Team:


#### Description



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




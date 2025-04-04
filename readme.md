<h1 align="center">Assignment_NITAllahabad_ScoreMe_20213027</h1>
<p align="center">
</p>

---

## 📌 Project Description  
This project extracts tables from **PDF files** and saves them into **Excel sheets**. It also includes functionality to generate sample PDFs containing **tabular data** for testing.

---

## 📑 Table of Contents  

- **Introduction**  
- **Features**  
- **Project Structure**  
- **Setup & Installation**  
- **Usage Instructions**  
- **Technology Stack**  
- **Troubleshooting**  
- **Contributors**  
- **Contact**  

---

## 🌟 Features  

✔ Extract **tables** from system-generated PDFs using `pdfplumber`.  
✔ Convert extracted tables into structured **Excel (`.xlsx`)** files.  
✔ Process **multiple PDFs** automatically from a folder.  
✔ Generate **sample PDF files** with tabular data for testing.  

---

## 📂 Project Structure  

├── sample1.pdf # Sample PDF for testing <br>
├── sample2.pdf # Additional sample PDF <br>
│── output_excel/ # Directory for extracted Excel files <br>
├── sample1.xlsx # Extracted tables from sample1.pdf<br>
├── sample2.xlsx # Extracted tables from sample2.pdf<br>
│── extract_tables.py # Script to extract tables from PDFs and save as Excel<br>
│── generate_file.py # Script to generate sample PDFs with tables<br>
│── requirements.txt # File containing required Python dependencies<br>
│── README.md # Project documentation<br>
└── .gitignore # Specifies files to ignore in version control<br>


---

## ⚙️ Setup & Installation  

### 🔹 Step 1: Clone the Repository  
        git clone https://github.com/akshatvermavi/assignment_nitallahabad_scoreme_20213027.git
        cd assignment_nitallahabad_scoreme_20213027

### 🔹 Step 2: Create a Virtual Environment (Recommended)
        python -m venv venv
        source venv/bin/activate   # macOS/Linux  
        venv\Scripts\activate      # Windows  
### 🔹 Step 3: Install Dependencies
        pip install -r requirements.txt

### 🔹 Generate Sample PDFs
        python generate_file.py

### 🔹 Extract Tables from PDFs
        python extract_tables.py
        
##   💻 Technology Stack

✔ Python <br>
✔ pdfplumber (Extracts tables from PDFs)<br>
✔ pandas (Converts extracted tables into Excel format)<br>
✔ fpdf (Generates PDFs with tabular data)<br>
✔ openpyxl (Saves Excel files)<br>
  

### To install all dependencies
    pip install -r requirements.txt
    
### 🐞 Troubleshooting
    choco install ghostscript  # Windows  
    brew install ghostscript   # macOS  

### Git Push Issues
    git pull --rebase origin main  
    git push -u origin main 

### 📧 Contact
🔹 **Author:** Akshat Verma  
🔗 **GitHub Profile:** [akshatvermavi](https://github.com/akshatvermavi)




          




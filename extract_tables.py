import pdfplumber
import pandas as pd
import re
from pdfminer.high_level import extract_text

def clean_text(text):
    """Remove illegal characters that OpenPyXL cannot process."""
    return re.sub(r"[^\x20-\x7E]", "", text)  # Keep only printable ASCII

def merge_broken_columns(row):
    """Merges broken column headers or values (e.g., 'BRANCH', 'NAME' → 'BRANCH NAME')."""
    merged_row = []
    skip_next = False

    for i in range(len(row) - 1):
        if skip_next:
            skip_next = False
            continue

        # If the next word should be merged, combine it
        if row[i + 1] != ":" and len(row[i]) < 10:  # Ignore colons and short values
            merged_row.append(f"{row[i]} {row[i + 1]}")
            skip_next = True
        else:
            merged_row.append(row[i])

    # Add last word if it wasn't merged
    if not skip_next:
        merged_row.append(row[-1])

    return merged_row

def extract_unbordered_tables(page):
    """Extracts unbordered tables by analyzing word spacing and line alignment."""
    words = page.extract_words()
    if not words:
        return None  # No text found

    lines = {}  # Group words by their y-coordinate
    for word in words:
        y_center = round(float(word["top"]))
        if y_center in lines:
            lines[y_center].append(word)
        else:
            lines[y_center] = [word]

    structured_table = []
    for y, line_words in sorted(lines.items()):
        row = [word["text"] for word in sorted(line_words, key=lambda x: x["x0"])]

        # Merge broken columns properly
        merged_row = merge_broken_columns(row)
        structured_table.append(merged_row)

    return structured_table if structured_table else None

def extract_structured_tables(pdf_path, writer):
    """Extracts structured tables using pdfplumber."""
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()

            # Extract bordered tables
            if tables:
                for idx, table in enumerate(tables, start=1):
                    df = pd.DataFrame(table).applymap(lambda x: clean_text(str(x)))
                    df.to_excel(writer, sheet_name=f"Page_{page_num}_Table_{idx}", index=False, header=False)

            # Extract unbordered tables
            unbordered_table = extract_unbordered_tables(page)
            if unbordered_table:
                df_unbordered = pd.DataFrame(unbordered_table)
                df_unbordered.to_excel(writer, sheet_name=f"Page_{page_num}_Unbordered", index=False, header=False)

def extract_tables_from_pdf(pdf_path, output_excel):
    """Extracts both text-based and structured tables and saves them in an Excel file."""
    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        extract_structured_tables(pdf_path, writer)

        # Extract raw text if needed
        raw_text = extract_text(pdf_path)
        df_text = pd.DataFrame([raw_text.split("\n")]).applymap(clean_text)
        df_text.to_excel(writer, sheet_name="Raw_Text", index=False, header=False)

    print(f"✅ Extraction completed. Check {output_excel}")

if __name__ == "__main__":
    input_pdf = "sample2.pdf"
    #input_pdf = "sample.pdf"
    input_pdf = "sample1.pdf"
    output_excel = "output2.xlsx"
    #output_excel = "output.xlsx"
    output_excel = "output1.xlsx"
    
    extract_tables_from_pdf(input_pdf, output_excel)

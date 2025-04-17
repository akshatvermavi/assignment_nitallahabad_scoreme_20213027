#This script extracts both bordered and unbordered tables, as well as raw text, from PDF files and saves
#them into an Excel file.

import pdfplumber   #pdfplumber: Used for extracting tables and text from PDFs.
import pandas as pd   #pandas: Facilitates data manipulation and storage in Excel format.
import re   #re: Provides regular expression operations for text cleaning.
from pdfminer.high_level import extract_text #extract_text: Extracts raw text from PDFs.

def clean_text(text):
    """Remove illegal characters that OpenPyXL cannot process."""
    #re.sub(pattern, replacement, text): This function searches for all occurrences of the pattern in 
    #text and replaces them with replacement
    return re.sub(r"[^\x20-\x7E]", "", text)  #Keep only printable ASCII
    #\x20 to \x7E: These are hexadecimal representations of ASCII characters ranging from space (' ') 
    # to tilde ('~'). This range includes all standard printable ASCII characters

def merge_broken_columns(row):#When you have a list and you want to add another item to its end, you use the append() method.
    """Merges broken column headers or values (e.g., 'BRANCH', 'NAME' → 'BRANCH NAME')."""
    merged_row = []   # list 
    skip_next = False # flag

    for i in range(len(row) - 1):  #for i in range(n + 1) eg. range(5) just means every number between 0 and 5
        #eg.  By using len(row) - 1, the range will generate indices from 0 to len(row) - 2.
        # example, range(2) would produce [0, 1].​  
        if skip_next:
            skip_next = False
            continue
            #Skips the rest of the code in the current loop iteration and moves to the next iteration.
        # If the next word should be merged, combine it
        if row[i + 1] != ":" and len(row[i]) < 10:  # Ignore colons and short values
        # if row[i+1] != ":" and len(row[i]) <10:
            merged_row.append(f"{row[i]} {row[i + 1]}") 
            # When you have a list and you want to add another item to its end, you use the append() method.
            skip_next = True
        else:
            merged_row.append(row[i])

    # Add last word if it wasn't merged
    if not skip_next:
        merged_row.append(row[-1])

    return merged_row

def extract_unbordered_tables(page):
    """Extracts unbordered tables by analyzing word spacing and line alignment."""
    #page: This is an object representing a single page of a PDF document, obtained using the pdfplumber library
    words = page.extract_words()
    #extract_words(): This is a method provided by pdfplumber that extracts individual words from the page
    if not words:
        return None  # return No text found in the page if there is no any word

    lines = {}  # Initializes an empty dictionary named lines, Group words by their y-coordinate
    for word in words:  # Iterates over each word extracted from the PDF page. 
        y_center = round(float(word["top"]))
        #Calculates the vertical position of the word by accessing its "top" attribute, 
        #which represents the distance from the top of the page to the top of the word's bounding box.
        if y_center in lines: #Checks if the calculated y_center value already exists as a key in the lines dictionary
            lines[y_center].append(word) #If the line already exists in the dictionary, appends the current word to the list of words on that line.
        else:
            lines[y_center] = [word]
            #If the line does not exist in the dictionary, it means this is the first word encountered on this line
    structured_table = []  #Initializes an empty list named structured_table.
    for y, line_words in sorted(lines.items()): #lines: This is a dictionary where each key is a y-coordinate (representing a line on the PDF
        row = [word["text"] for word in sorted(line_words, key=lambda x: x["x0"])]
        #row = [word["text"] for word in sorted(line_words, key=lambda x: x["x0"])]
        # Merge broken columns properly
        merged_row = merge_broken_columns(row)# Sorts the list of word dictionaries (line_words) based on the x-coordinate ("x0"), which represents the horizontal position 
        structured_table.append(merged_row)#This is a list comprehension that extracts the text content ("text") from each word dictionary in the sorted list.

    return structured_table if structured_table else None

def extract_structured_tables(pdf_path, writer):
    #Defines a function to extract both bordered and unbordered tables from a PDF and write them to an Excel file.
    """Extracts structured tables using pdfplumber."""
    with pdfplumber.open(pdf_path) as pdf:#Action: Opens the PDF file for processing using pdfplumber.
        for page_num, page in enumerate(pdf.pages, start=1):#Purpose: Loops through each page in the PDF.
            tables = page.extract_tables()
            #Function: Uses pdfplumber's extract_tables() method to extract tables with visible borders from the page.
            # Extract bordered tables
            if tables:
                for idx, table in enumerate(tables, start=1):
                    df = pd.DataFrame(table).applymap(lambda x: clean_text(str(x)))
                    df.to_excel(writer, sheet_name=f"Page_{page_num}_Table_{idx}", index=False, header=False)
                    #Check: Proceeds only if tables are found.
                    #Loop: Iterates through each extracted table.
                    #DataFrame Creation: Converts the table (a list of lists) into a pandas DataFrame.
                    #Cleaning: Applies the clean_text function to each cell to remove unwanted characters or formatting.
            # Extract unbordered tables
            unbordered_table = extract_unbordered_tables(page)
            #Function: Calls a custom function extract_unbordered_tables to handle tables without visible borders. This function likely uses text positioning to infer table structures.​
            if unbordered_table:
                df_unbordered = pd.DataFrame(unbordered_table)#Check: Proceeds only if an unbordered table is found.
                df_unbordered.to_excel(writer, sheet_name=f"Page_{page_num}_Unbordered", index=False, header=False)
                #DataFrame Creation: Converts the unbordered table into a pandas DataFrame.
                #Excel Writing: Writes the DataFrame to the Excel file with a sheet name indicating the page and that it's an unbordered table.
def extract_tables_from_pdf(pdf_path, output_excel):
    """Extracts both text-based and structured tables and saves them in an Excel file."""
    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        #Action: Initializes a context manager for writing to an Excel file using pandas' ExcelWriter.
        extract_structured_tables(pdf_path, writer)
        #Function Call: Invokes the extract_structured_tables function, which processes the PDF to extract tables and writes them to the Excel file using the provided writer.
        # Extract raw text if needed
        raw_text = extract_text(pdf_path) #Function Call: Uses the extract_text function to retrieve all textual content from the PDF.​
        df_text = pd.DataFrame([raw_text.split("\n")]).applymap(clean_text)
        #raw_text.split("\n"): Splits the raw text into a list of lines based on newline characters.
        df_text.to_excel(writer, sheet_name="Raw_Text", index=False, header=False)
        #Writing to Excel: Saves the cleaned raw text to a new sheet named "Raw_Text" in the Excel file.​

    print(f"✅ Extraction completed. Check {output_excel}")
    #Feedback: Prints a confirmation message indicating the extraction process is complete and specifies the location of the output Excel file
if __name__ == "__main__":
    #Purpose: This conditional checks whether the script is being run as the main program. If it is, the 
    #code block under this condition will execute. This is a common Python idiom to allow or prevent parts
    #of code from being run when the modules are imported.
    #Initially, input_pdf is set to "sample2.pdf".
    #The next line is commented out, so "sample.pdf" is not assigned.
    #Then, input_pdf is reassigned to "sample1.pdf".
    #Result: The final value of input_pdf is "sample1.pdf
    input_pdf = "sample2.pdf" 
    #input_pdf = "sample.pdf"
    input_pdf = "sample1.pdf"
    output_excel = "output2.xlsx"
    #output_excel = "output.xlsx"
    output_excel = "output1.xlsx"
    #Initially, output_excel is set to "output2.xlsx".
    #The next line is commented out, so "output.xlsx" is not assigned.
    #Then, output_excel is reassigned to "output1.xlsx".
    #Result: The final value of output_excel is "output1.xlsx".
    extract_tables_from_pdf(input_pdf, output_excel)

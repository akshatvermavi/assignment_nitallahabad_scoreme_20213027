# from fpdf import FPDF
# #Imports the FPDF class from the fpdf library, which is used to create PDF files
# import os
# #Imports the os module for interacting with the file system (e.g., creating directories).
# def create_pdf_with_table(filename, table_data, title):
#     #Defines a function that generates a PDF with a title and tabular data.
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
#     pdf.set_font("Arial", style='B', size=14)
    
#     # Title
#     pdf.cell(200, 10, title, ln=True, align='C')
#     pdf.ln(10)

#     pdf.set_font("Arial", size=10)
#     col_width = 40  # Adjust column width
#     row_height = 10  # Adjust row height

#     # Print table headers
#     pdf.set_font("Arial", style='B', size=10)
#     for header in table_data[0]:
#         pdf.cell(col_width, row_height, header, border=1, align='C')
#     pdf.ln(row_height)

#     # Print table rows
#     pdf.set_font("Arial", size=10)
#     for row in table_data[1:]:
#         for cell in row:
#             pdf.cell(col_width, row_height, cell, border=1, align='C')
#         pdf.ln(row_height)

#     pdf.output(filename)
#     print(f"✅ {filename} created successfully!")

# # Create an output folder
# os.makedirs("pdf_files", exist_ok=True)

# # Sample Table Data
# table_data1 = [
#     ["ID", "Name", "Age", "City"],
#     ["1", "Alice", "25", "New York"],
#     ["2", "Bob", "30", "Los Angeles"],
#     ["3", "Charlie", "35", "Chicago"]
# ]

# table_data2 = [
#     ["Product", "Category", "Price", "Stock"],
#     ["Laptop", "Electronics", "$1000", "50"],
#     ["Shoes", "Fashion", "$100", "200"],
#     ["Phone", "Electronics", "$800", "30"]
# ]

# # Generate Sample PDFs
# create_pdf_with_table("pdf_files/sample1.pdf", table_data1, "Employee Details")
# create_pdf_with_table("pdf_files/sample2.pdf", table_data2, "Product Inventory")

from fpdf import FPDF
#Imports the FPDF class from the fpdf library, which is used to create PDF files
import os
#Imports the os module for interacting with the file system (e.g., creating directories).
def create_pdf_with_table(filename, table_data, title):
    #Defines a function that generates a PDF with a title and tabular data.
    """
    Creates a PDF file with a title and a table.

    Parameters:
    - filename (str): Output path for the generated PDF
    - table_data (list of lists): Table data, where the first list is headers
    - title (str): Title to be displayed at the top of the PDF
    """
    pdf = FPDF()  # Initialize PDF document
    pdf.set_auto_page_break(auto=True, margin=15)  # Enable auto page breaks
    pdf.add_page()  # Add a new page
    pdf.set_font("Arial", style='B', size=14)  # Set font for title

    # Title
    pdf.cell(200, 10, title, ln=True, align='C')  # Add centered title
    pdf.ln(10)  # Line break for spacing

    # Table column width and row height
    col_width = 40
    row_height = 10

    # Print table headers in bold
    pdf.set_font("Arial", style='B', size=10)
    for header in table_data[0]:
        pdf.cell(col_width, row_height, header, border=1, align='C')
    pdf.ln(row_height)

    # Print table rows
    pdf.set_font("Arial", size=10)
    for row in table_data[1:]:
        for cell in row:
            pdf.cell(col_width, row_height, cell, border=1, align='C')
        pdf.ln(row_height)

    # Save PDF
    pdf.output(filename)
    print(f"✅ {filename} created successfully!")

# Ensure output folder exists
os.makedirs("pdf_files", exist_ok=True)

# Sample Table Data
table_data1 = [
    ["ID", "Name", "Age", "City"],
    ["1", "Alice", "25", "New York"],
    ["2", "Bob", "30", "Los Angeles"],
    ["3", "Charlie", "35", "Chicago"]
]

table_data2 = [
    ["Product", "Category", "Price", "Stock"],
    ["Laptop", "Electronics", "$1000", "50"],
    ["Shoes", "Fashion", "$100", "200"],
    ["Phone", "Electronics", "$800", "30"]
]

# Generate PDFs
create_pdf_with_table("pdf_files/sample1.pdf", table_data1, "Employee Details")
create_pdf_with_table("pdf_files/sample2.pdf", table_data2, "Product Inventory")

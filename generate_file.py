from fpdf import FPDF
import os

def create_pdf_with_table(filename, table_data, title):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=14)
    
    # Title
    pdf.cell(200, 10, title, ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=10)
    col_width = 40  # Adjust column width
    row_height = 10  # Adjust row height

    # Print table headers
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

    pdf.output(filename)
    print(f"✅ {filename} created successfully!")

# Create an output folder
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

# Generate Sample PDFs
create_pdf_with_table("pdf_files/sample1.pdf", table_data1, "Employee Details")
create_pdf_with_table("pdf_files/sample2.pdf", table_data2, "Product Inventory")

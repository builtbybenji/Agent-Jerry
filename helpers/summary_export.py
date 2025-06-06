from fpdf import FPDF
import os

def create_pdf_report(address, search_results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Property Summary Report", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Address: {address}", ln=True, align="L")
    pdf.ln(10)

    if not search_results:
        pdf.cell(200, 10, txt="No property listings found.", ln=True, align="L")
    else:
        for i, result in enumerate(search_results[:5], 1):
            title = result.get("title", "No Title")
            link = result.get("link", "")
            pdf.multi_cell(0, 10, txt=f"{i}. {title}\n{link}")
            pdf.ln(5)

    output_path = "/mnt/data/Property_Summary.pdf"
    pdf.output(output_path)
    return output_path

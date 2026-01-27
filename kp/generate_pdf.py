#!/usr/bin/env python3
"""
Generate PDF from HTML template using WeasyPrint
"""

from weasyprint import HTML, CSS
from pathlib import Path

def generate_pdf():
    template_path = Path(__file__).parent / "template.html"
    output_path = Path(__file__).parent / "WorkHere_КП.pdf"
    
    print("Генерация PDF...")
    
    # Read HTML
    html = HTML(filename=str(template_path))
    
    # Generate PDF
    html.write_pdf(str(output_path))
    
    print(f"✓ PDF создан: {output_path}")
    print(f"  Размер: {output_path.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    generate_pdf()

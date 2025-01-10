import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def excel_to_pdf_tab():
    def generate_pdf(data):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 750, "Excel Data to PDF")
        
        y_position = 730  
        
        c.setFont("Helvetica", 10)
        for idx, row in data.iterrows():
            line = ' | '.join([str(item) for item in row])
            c.drawString(50, y_position, line)
            y_position -= 15  
            if y_position < 50:  
                c.showPage()
                c.setFont("Helvetica", 10)
                y_position = 750
        
        c.save()
        buffer.seek(0)
        return buffer

    def handle_file(uploaded_file):
        df = pd.read_excel(uploaded_file)

        st.write("Data preview:")
        st.write(df.head())
        
        pdf_output = generate_pdf(df)

        return pdf_output

    st.markdown("#### Excel to PDF Converter")
    
    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx", key='excel_to_pdf')

    if uploaded_file:
        pdf_output = handle_file(uploaded_file)
        
        st.download_button(
            label="Download PDF",
            data=pdf_output,
            file_name="converted_data.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    excel_to_pdf_tab()

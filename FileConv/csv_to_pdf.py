import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO


def csv_to_pdf_tab():
    st.markdown("#### CSV to PDF Converter")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key='csv_to_pdf')

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        st.write("CSV File Preview:")
        st.dataframe(df)

        if st.button('Convert to PDF'):
            pdf_buffer = BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)

            c.setFont("Helvetica", 10)
            x_offset = 50
            y_offset = 750
            line_height = 14

            for idx, col_name in enumerate(df.columns):
                c.drawString(x_offset + idx * 120, y_offset, col_name)

            for row in df.itertuples(index=False):
                y_offset -= line_height
                for idx, value in enumerate(row):
                    c.drawString(x_offset + idx * 120, y_offset, str(value))

            c.save()

            pdf_buffer.seek(0)

            st.download_button(
                label="Download PDF",
                data=pdf_buffer,
                file_name="converted_file.pdf",
                mime="application/pdf"
            )

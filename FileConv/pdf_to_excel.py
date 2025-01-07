import streamlit as st
import pdfplumber
import pandas as pd
import io

def pdf_to_excel_tab():
    st.title("PDF to Excel Converter")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key='pdf_to_excel')

    if uploaded_file is not None:
        # Open the uploaded PDF file using pdfplumber
        with pdfplumber.open(uploaded_file) as pdf:
            # Try to extract the first page's table (if available)
            first_page = pdf.pages[0]
            table = first_page.extract_table()

            if table:
                # Convert the table to a pandas DataFrame
                df = pd.DataFrame(table[1:], columns=table[0])

                # Show a preview of the table (DataFrame)
                st.write("PDF Table Preview:")
                st.dataframe(df)

                # Convert the table to Excel when the user clicks the button
                if st.button('Convert to Excel'):
                    # Save the DataFrame to an Excel file in memory
                    excel_file = io.BytesIO()
                    df.to_excel(excel_file, index=False, engine='openpyxl')
                    excel_file.seek(0)  # Reset file pointer to the beginning

                    # Provide the Excel file for download
                    st.download_button(
                        label="Download Excel File",
                        data=excel_file,
                        file_name="converted_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.write("No table found on the first page of the PDF.")

# Running the function to handle PDF to Excel conversion
if __name__ == "__main__":
    pdf_to_excel_tab()

import streamlit as st
import pdfplumber
import pandas as pd

def pdf_to_csv_tab():
    st.markdown("#### PDF to CSV Converter")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key='pdf_to_csv')

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

                # Convert the table to CSV when the user clicks the button
                if st.button('Convert to CSV'):
                    # Convert the DataFrame to CSV
                    csv_data = df.to_csv(index=False)

                    # Provide the CSV file for download
                    st.download_button(
                        label="Download CSV File",
                        data=csv_data,
                        file_name="converted_data.csv",
                        mime="text/csv"
                    )
            else:
                st.write("No table found on the first page of the PDF.")

# Running the function to handle PDF to CSV conversion
if __name__ == "__main__":
    pdf_to_csv_tab()
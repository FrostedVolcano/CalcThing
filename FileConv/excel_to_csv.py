import streamlit as st
import pandas as pd

def excel_to_csv_tab():
    st.title("Excel to CSV Converter")

    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx", key='excel_to_csv')

    if uploaded_file is not None:
        # Read the Excel file using pandas
        df = pd.read_excel(uploaded_file)

        # Show a preview of the Excel data
        st.write("Excel File Preview:")
        st.dataframe(df)

        # Convert Excel to CSV when the user clicks the button
        if st.button('Convert to CSV'):
            # Generate the CSV filename by replacing '.xlsx' with '.csv'
            csv_file = uploaded_file.name.replace('.xlsx', '.csv')

            # Convert the DataFrame to CSV
            csv_data = df.to_csv(index=False)

            # Provide the CSV file for download
            st.download_button(
                label="Download CSV File",
                data=csv_data,
                file_name=csv_file,
                mime="text/csv"
            )

# Running the function to handle Excel to CSV conversion
if __name__ == "__main__":
    excel_to_csv_tab()

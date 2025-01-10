import streamlit as st
import pandas as pd

def csv_to_excel_tab():
    st.markdown("#### CSV to Excel Converter")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key='csv_to_excel')

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        st.write("CSV File Preview:")
        st.dataframe(df)
        
        if st.button('Convert to Excel'):
            excel_file = uploaded_file.name.replace('.csv', '.xlsx')
            df.to_excel(excel_file, index=False, engine='openpyxl')
            
            with open(excel_file, "rb") as f:
                st.download_button(
                    label="Download Excel File",
                    data=f,
                    file_name=excel_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

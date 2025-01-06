import streamlit as st
from posthog import Posthog
from current_divider import current_divider_tab
from voltage_divider import voltage_divider_tab
from wye_to_delta import wye_to_delta_tab
from delta_to_wye import delta_to_wye_tab


# Set page config first, before any other Streamlit commands
st.set_page_config(page_title="CalcThing", page_icon="logo.png", layout="wide")

st.markdown("""
<style>
    [data-testid="stDecoration"] {
        display: none;
    }
</style>
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
        max-width: 90%;
        margin-left: auto;
        margin-right: auto;
    }
</style>
""", unsafe_allow_html=True)

posthog = Posthog('phc_WqSMXohypdxpBdGEFrJBIcTwzn0f1yKauzKY6UbxJHg', host='https://us.i.posthog.com')
posthog = Posthog(api_key='phc_WqSMXohypdxpBdGEFrJBIcTwzn0f1yKauzKY6UbxJHg',host='https://phrevpro.vercel.app/ingest')

posthog.capture(
    'distinct_id',
    event='event_name',
    properties={
        '$process_person_profile': False})


st.header("CalcThing: Calculator for various things")
st.write("Visual Calculators for wye (Y) to delta (Δ) and delta (Δ) to wye (Y) circuits, voltage from voltage divider, current from parallel resistors, and many more coming!")

def main():
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Wye(Y) to Delta(Δ)", "Delta(Δ) to Wye(Y)", "Current Divider Rule", "Voltage Divider Rule"])
    
    # Render content based on active tab
    with tab1:
        wye_to_delta_tab()
    
    with tab2:
        delta_to_wye_tab()
        
    with tab3:
        current_divider_tab()
        
    with tab4:
        voltage_divider_tab()
    
if __name__ == "__main__":
    main()
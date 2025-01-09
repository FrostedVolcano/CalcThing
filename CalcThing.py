import streamlit as st
import streamlit.components.v1 as components
import gc
from posthog import Posthog
from streamlit_option_menu import option_menu
from streamlit_extras.buy_me_a_coffee import button

# Set page config first, before any other Streamlit commands
st.set_page_config(page_title="CalcThing", page_icon="logo.ico", layout="wide")

@st.fragment()
def top_bar():
    st.markdown("""
    <style>
        [data-testid="stDecoration"] {
            display: none;
        }
    </style>
    <style>
        .block-container {
            padding-top: 3rem;
            padding-bottom: 0rem;
            max-width: 90%;
            margin-left: auto;
            margin-right: auto;
        }
    </style>
    """, unsafe_allow_html=True)
top_bar()

posthog = Posthog('phc_79RpiYGOIeOrJuM1gdxQtT2aQHwltOyLPRd6V1ZrRq6', host='https://us.i.posthog.com')

# Only import modules when needed
@st.fragment()
def load_circuit_modules():
    import gc
    from Circuits.current_divider import current_divider_tab
    from Circuits.voltage_divider import voltage_divider_tab
    from Circuits.wye_to_delta import wye_to_delta_tab
    from Circuits.delta_to_wye import delta_to_wye_tab
    return current_divider_tab, voltage_divider_tab, wye_to_delta_tab, delta_to_wye_tab

@st.fragment()
def load_fileconv_modules():
    from FileConv.csv_to_excel import csv_to_excel_tab
    from FileConv.csv_to_pdf import csv_to_pdf_tab
    from FileConv.excel_to_pdf import excel_to_pdf_tab
    from FileConv.excel_to_csv import excel_to_csv_tab
    from FileConv.pdf_to_csv import pdf_to_csv_tab
    from FileConv.pdf_to_excel import pdf_to_excel_tab
    return csv_to_excel_tab, csv_to_pdf_tab, excel_to_pdf_tab, excel_to_csv_tab, pdf_to_csv_tab, pdf_to_excel_tab


def main():
    selected = option_menu(menu_title=None, options=["Home", "Circuits Page", "File Coverters"], icons= ["house", "activity", "file-earmark-bar-graph"], 
                           default_index=0,orientation="horizontal", menu_icon="cast")
    
    if selected == "Home":
        @st.fragment()
        def home():
            st.header("CalcThing: Calculators and File Converters for Engineering & Physics")
            st.write("#####")
            
            cl1, cl2 = st.columns(2, gap="large")
            with cl1:
                st.subheader("Circuits Page: Circuit Calculators and Converters with their schematics")
                st.write("""
                    - Delta (Δ) to Wye (Y) Circuits and vise versa.
                    - Calculate voltage divider circuit.
                    - Calculate current divider circuit.
                    - Calculate LED current limiter resistor values.
                     """)
            with cl2:
                st.subheader("File Converters: File Converters for popular engineering file formats")
                st.write("""
                    - Convert .csv files to .xlsx files.
                    - Convert .csv files to .pdf files.
                    - Convert .xlsx files to .csv files.
                    - Convert .csv files to .pdf files.
                    - Convert .pdf files to .csv files.
                    - Convert .pdf files to .xlsx files.
                    """)
        home()

    
    if selected == "Circuits Page":
        @st.fragment()
        def circuits():
            placeholder = st.empty()  # Add placeholder for dynamic content
            with placeholder.container():
                tab1, tab2, tab3, tab4 = st.tabs(["**Wye(Y) to Delta(Δ)**", "**Delta(Δ) to Wye(Y)**", "**Current Divider Rule**", "**Voltage Divider Rule**"])
                current_divider_tab, voltage_divider_tab, wye_to_delta_tab, delta_to_wye_tab = load_circuit_modules()
                with tab1:
                    wye_to_delta_tab()
                with tab2:
                    delta_to_wye_tab()
                with tab3:
                    current_divider_tab()
                with tab4:
                    voltage_divider_tab()
        circuits()
           
    if selected == "File Coverters":
        @st.fragment()
        def fileconv():
            placeholder = st.empty()
            with placeholder.container():
                tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["**CSV to Excel**","**Excel to CSV**", "**CSV to Pdf**", "**Pdf to CSV**", "**Excel to Pdf**", "**Pdf to Excel**"])
                csv_to_excel_tab, csv_to_pdf_tab, excel_to_pdf_tab, excel_to_csv_tab, pdf_to_csv_tab, pdf_to_excel_tab = load_fileconv_modules()
                with tab1:
                    csv_to_excel_tab()
                with tab2:
                    excel_to_csv_tab()
                with tab3:
                    csv_to_pdf_tab()
                with tab4:
                    pdf_to_csv_tab()
                with tab5:
                    excel_to_pdf_tab()
                with tab6:
                    pdf_to_excel_tab()
        fileconv()
        
main()

# button(username="calcthing", width=220, font_color="#FFDD00", coffee_color="#FFDD00", bg_color="#1c1c1c" )


       
# Keep this part at the end.
components.html("""
    <head>
    <script>
        !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
        posthog.init('phc_79RpiYGOIeOrJuM1gdxQtT2aQHwltOyLPRd6V1ZrRq6', {api_host: 'https://us.i.posthog.com'})
    </script>
    </head>
""")

@st.fragment()
def logos():
    st.markdown('''
        <head>
            <link rel="shortcut icon" href="logo.ico" type="image/x-icon">
            <link rel="icon" href="logo.ico" type="image/x-icon">
            <link rel="apple-touch-icon" sizes="180x180" href="logo_180x180.png">
            <link rel="icon" type="image/png" sizes="32x32" href="logo_32x32.png">
            <link rel="icon" type="image/png" sizes="16x16" href="logo_16x16.png">
            <meta property="og:image" content="logo_180x180.png">
        </head>
    ''', unsafe_allow_html=True)
logos()
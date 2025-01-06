import streamlit as st
from calculation import current_divider_rule, voltage_divider_rule
from diagram import draw_wye_circuit, draw_delta_circuit, draw_parallel_circuit, draw_series_circuit
import schemdraw
import schemdraw.elements as elm
import streamlit.components.v1 as com


# Set page config first, before any other Streamlit commands
st.set_page_config(page_title="CalcThing", page_icon="logo.png", layout="wide")

# CSS to hide Streamlit's default decoration and adjust padding
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
    }
</style>
""", unsafe_allow_html=True)


st.header("CalcThing: Calculator for various things")
st.write("Visual Calculators for wye (Y) to delta (Δ) and delta (Δ) to wye (Y) circuits, voltage from voltage divider, current from parallel resistors, and many more coming!")


def init_page():
    # Initialize session state for formulas if not exists
    if 'show_wye_formula' not in st.session_state:
        st.session_state.show_wye_formula = False
    if 'show_delta_formula' not in st.session_state:
        st.session_state.show_delta_formula = False

def display_wye_to_delta_formula():
    st.write("#")
    st.subheader("Formula used:")
    st.latex(r"R_a = \frac{R_1 R_2 + R_2 R_3 + R_3 R_1}{R_1}")
    st.latex(r"R_b = \frac{R_1 R_2 + R_2 R_3 + R_3 R_1}{R_2}")
    st.latex(r"R_c = \frac{R_1 R_2 + R_2 R_3 + R_3 R_1}{R_3}")

def display_delta_to_wye_formula():
    st.write("#")
    st.subheader("Formula used:")
    st.latex(r"R_1 = \frac{R_a R_b}{R_a + R_b + R_c}")
    st.latex(r"R_2 = \frac{R_b R_c}{R_a + R_b + R_c}")
    st.latex(r"R_3 = \frac{R_c R_a}{R_a + R_b + R_c}")

def wye_to_delta_tab():
    st.subheader("Wye (Y) to Delta (Δ) Circuit Converter")
    col1, col2 = st.columns(2, gap='large')
    
    with col1:
        st.write("######")
        st.write("Input Wye (Y) Resistor Values:")
        cols1, cols2, cols3 = st.columns(3)
        with cols1:
            res1 = st.number_input("Value of R1: ", min_value=0.0001, value=10.0, step=1.0, key="wye_res1")
        with cols2:
            res2 = st.number_input("Value of R2: ", min_value=0.0001, value=10.0, step=1.0, key="wye_res2")
        with cols3:
            res3 = st.number_input("Value of R3: ", min_value=0.0001, value=10.0, step=1.0, key="wye_res3")
        
        wye_circuit = draw_wye_circuit(res1, res2, res3)
        st.markdown(wye_circuit, unsafe_allow_html=True)
    
    with col2:
        denominator = res1 * res2 + res2 * res3 + res3 * res1
        resa = round((denominator / res1), 4)
        resb = round((denominator / res2), 4)
        resc = round((denominator / res3), 4)
        delta_circuit = draw_delta_circuit(resa, resb, resc)
    
        st.write("Delta Resistor Values:")
        st.write(f"Ra = {resa:.4f} Ω")
        st.write(f"Rb = {resb:.4f} Ω")
        st.write(f"Rc = {resc:.4f} Ω")
        st.markdown(delta_circuit, unsafe_allow_html=True)
    
    if st.button("Show/Hide Formula", key="wye_formula_button"):
        st.session_state.show_wye_formula = not st.session_state.show_wye_formula
    
    if st.session_state.show_wye_formula:
        display_wye_to_delta_formula()

def delta_to_wye_tab():
    st.subheader("Delta (Δ) to Wye (Y) Circuit Converter")
    col1, col2 = st.columns(2, gap='large')
    
    with col1:
        st.write("######")
        st.write("Input Delta (Δ) Resistor Values:")
        cols1, cols2, cols3 = st.columns(3)
        with cols1:
            r1 = st.number_input("Value of Ra: ", min_value=0.0001, value=30.0, step=1.0, key="delta_r1")
        with cols2:
            r2 = st.number_input("Value of Rb: ", min_value=0.0001, value=30.0, step=1.0, key="delta_r2")
        with cols3:
            r3 = st.number_input("Value of Rc: ", min_value=0.0001, value=30.0, step=1.0, key="delta_r3")
    
        delta_circuit = draw_delta_circuit(r1, r2, r3)
        st.markdown(delta_circuit, unsafe_allow_html=True)
    
    with col2:
        r_sum = r1 + r2 + r3
        ra = round((r1 * r2) / r_sum, 4)
        rb = round((r2 * r3) / r_sum, 4)
        rc = round((r3 * r1) / r_sum, 4)
    
        wye_circuit = draw_wye_circuit(ra, rb, rc)
        st.write("Wye (Y) Resistor Values:")
        st.write(f"R1 = {ra:.4f} Ω")
        st.write(f"R2 = {rb:.4f} Ω")
        st.write(f"R3 = {rc:.4f} Ω")
        st.markdown(wye_circuit, unsafe_allow_html=True)
    
    if st.button("Show/Hide Formula", key="delta_formula_button"):
        st.session_state.show_delta_formula = not st.session_state.show_delta_formula
    
    if st.session_state.show_delta_formula:
        display_delta_to_wye_formula()
        
def current_divider_tab():
    # Streamlit app title
    st.title("Interactive Current Divider Circuit")

    # Source-Voltage input
    current_inp = st.text_input("$Current$ $(A)$", value=str(10.0))
    try:
        current_inp = float(current_inp)  # Convert to float
    except ValueError:
        st.error("Invalid input for current. Please Enter a valid number.")
        current_inp = None

    # Initialize resistors in session state if not already initialized
    if 'resistances' not in st.session_state:
        st.session_state.resistances = [100.0, 100.0, 100.0]  # Default resistances (3 resistors of 100Ω)

    # Handle adding/removing resistors
    col1, col2 = st.columns(2)
    with col1:
        # Disable 'Add More Resistors' button when resistor count reaches 10
        add_resistor_clicked = st.button("Add More Resistors", key='1234')
    with col2:
        remove_resistor_clicked = st.button("Remove Last Resistors", key='2345')

    # Update the resistances list based on button clicks
    if add_resistor_clicked:
        st.session_state.resistances.append(100.0)  # Add a new resistor with a default value of 100Ω

    if remove_resistor_clicked:
        st.session_state.resistances.pop()  # Remove the last resistor

    gol1, gol2, gol3, gol4, gol5 = st.columns(5)
    # Display resistor inputs based on the current number of resistors
    gols = [gol1, gol2, gol3, gol4, gol5]  # Create a list of columns to alternate
    for i in range(len(st.session_state.resistances)):
        with gols[i % 5]:  # Modified Line: Alternate between 5 columns and cycle back to the first one
            resistor_value = st.text_input(
                label=f"$R_{{{i+1}}} \, (\Omega)$", 
                value=str(round(st.session_state.resistances[i], 2)), 
                key=f"resistor_{i}"  # Unique key to track each input widget
            )
            try:
                new_resistor_value = float(resistor_value)
                if new_resistor_value != st.session_state.resistances[i]:
                    st.session_state.resistances[i] = new_resistor_value
            except ValueError:
                st.error(f"Invalid input for resistance")

    result = current_divider_rule(current_inp, 'parallel', *st.session_state.resistances)

    img_buffer = draw_parallel_circuit(current_inp, len(st.session_state.resistances), st.session_state.resistances, result)
    st.image(img_buffer, caption=f"Parallel Circuit Diagram")

    if current_inp and st.session_state.resistances:  # Check if voltage and resistances are valid
        try:
            st.subheader("Results:")
            nol1, nol2, nol3, nol4, nol5 = st.columns(5)
            nols = [nol1, nol2, nol3, nol4, nol5]
            for i in range(len(result)):
                with nols[i % 5]:  # Alternate between left and right columns
                    st.write(f"$C-Flow$ $R_{{{i+1}}} \, (\Omega)$: {round(result[i], 2)} A")
                        
        except ValueError as e:
            st.error(f"Error: {e}")

def voltage_divider_tab():
    st.title("Interactive Voltage Divider Circuit")

    # Source-Voltage input
    voltage_inp = st.text_input("$Voltage$ $(V)$", value=str(10.0))
    try:
        voltage_inp = float(voltage_inp)  # Convert to float
    except ValueError:
        pass

    # Initialize resistors in session state if not already initialized
    if 'resistances' not in st.session_state:
        st.session_state.resistances = [100.0, 100.0, 100.0]  # Default resistances (3 resistors of 100Ω)

    # Handle adding/removing resistors
    col1, col2 = st.columns(2)
    with col1:
        # Disable 'Add More Resistors' button when resistor count reaches 10
        add_resistor_clicked = st.button("Add More Resistors", key='3456')
    with col2:
        remove_resistor_clicked = st.button("Remove Last Resistor", key='4567')

    # Update the resistances list based on button clicks
    if add_resistor_clicked:
        st.session_state.resistances.append(100.0)  # Add a new resistor with a default value of 100Ω

    if remove_resistor_clicked:
        st.session_state.resistances.pop()  # Remove the last resistor

    gol1, gol2, gol3, gol4, gol5 = st.columns(5)
    # Display resistor inputs based on the current number of resistors
    gols = [gol1, gol2, gol3, gol4, gol5]  # Create a list of columns to alternate
    for i in range(len(st.session_state.resistances)):
        with gols[i % 5]:  # Modified Line: Alternate between 5 columns and cycle back to the first one
            resistor_value = st.text_input(
                label=f"$R_{{{i+1}}} \, (\Omega)$", 
                value=str(round(st.session_state.resistances[i], 2)), 
                key=f"resistor_{i+len(st.session_state.resistances)+10}"  # Unique key to track each input widget
            )
            try:
                new_resistor_value = float(resistor_value)
                if new_resistor_value != st.session_state.resistances[i]:
                    st.session_state.resistances[i] = new_resistor_value
            except ValueError:
                pass

    result = voltage_divider_rule(voltage_inp, 'series', *st.session_state.resistances)

    img_buffer = draw_series_circuit(voltage_inp, len(st.session_state.resistances), st.session_state.resistances, result)
    st.image(img_buffer, caption=f"Series Circuit Diagram")

    if voltage_inp and st.session_state.resistances:  # Check if voltage and resistances are valid
        try:
            st.subheader("Results:")
            nol1, nol2, nol3, nol4, nol5 = st.columns(5)
            nols = [nol1, nol2, nol3, nol4, nol5]
            for i in range(len(result)):
                with nols[i % 5]:  # Alternate between left and right columns
                    st.write(f"$V-drop$ $R_{{{i+1}}} \, (\Omega)$: {round(result[i], 2)} V")
                    
        except ValueError as e:
            st.error(f"Error: {e}")

def add_tracking():
    com.html("""
    <head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XQQQ8NSB2Y"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-XQQQ8NSB2Y');
    </script>  
    <script>
        !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetGroupPropertiesForFlags resetPersonPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug getPageViewId".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
        posthog.init('phc_WqSMXohypdxpBdGEFrJBIcTwzn0f1yKauzKY6UbxJHg', {
            api_host:'https://us.i.posthog.com',
            person_profiles: 'identified_only'
        })
    </script>
    <script defer src="https://cloud.umami.is/script.js" data-website-id="cf7f0ed8-7e4e-4a27-8a02-c013fc8291b1"></script>
    </head>
    """, width=None, height=None)
    

def main():
    # Initialize the page
    init_page()
    
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

    # Add tracking scripts
    add_tracking()
    
if __name__ == "__main__":
    main()
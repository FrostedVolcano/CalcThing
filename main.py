import streamlit as st
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

def draw_wye_circuit(res1, res2, res3):
    """Draw Wye circuit with proper encoding handling"""
    d = schemdraw.Drawing()
    d.config(unit=3, color="#37bd95")
    center = d.add(elm.Dot())
    d.add(elm.Resistor().right().label(f"R1={res1:.4f}Ω", loc="top").label("x", loc="right"))
    d.add(elm.Resistor().theta(-120).at(center.start).label(f"R2={res2:.4f}Ω", loc="top").label("y", loc="left"))
    d.add(elm.Resistor().theta(120).at(center.start).label(f"R3={res3:.4f}Ω", loc="bottom").label("z", loc="left"))
    
    # Get SVG data and force UTF-8 encoding
    svg_data = d.get_imagedata('svg')
    if isinstance(svg_data, bytes):
        return svg_data.decode('utf-8', errors='ignore')
    return svg_data

def draw_delta_circuit(resa, resb, resc):
    """Draw Delta circuit with proper encoding handling"""
    d = schemdraw.Drawing()
    d.config(unit=5, color="#37bd95")
    start_point = (0, 0)
    r1 = d.add(elm.Resistor().up().at(start_point).label(f"Ra={resa:.4f}Ω", loc="top", ofst=.1).label("z", loc="right"))
    r2 = d.add(elm.Resistor().theta(-30).label(f"Rb={resb:.4f}Ω", loc="top", ofst=.3).label("x", loc="right"))
    r3 = d.add(elm.Resistor().theta(-150).label(f"Rc={resc:.4f}Ω", loc="bottom", ofst=.3).label("y", loc="left"))
    d.add(elm.Line().at(r3.end).to(r1.start))
    
    # Get SVG data and force UTF-8 encoding
    svg_data = d.get_imagedata('svg')
    if isinstance(svg_data, bytes):
        return svg_data.decode('utf-8', errors='ignore')
    return svg_data

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

def add_tracking():
    com.html("""
    <head>
    <!-- Google Site Verification -->
    <meta name="google-site-verification" content="UpK4x268-JAVGifEIIa0LG7x9OFnEFgoBqvRvdxio-E" />
    
    <!-- PostHog Analytics -->
    <script>
        !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetGroupPropertiesForFlags resetPersonPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug getPageViewId".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
        posthog.init('phc_WqSMXohypdxpBdGEFrJBIcTwzn0f1yKauzKY6UbxJHg', {
            api_host:'https://us.i.posthog.com',
            person_profiles: 'identified_only'
        })
    </script>
    
    <!-- Umami Analytics -->
    <script defer src="https://cloud.umami.is/script.js" data-website-id="cf7f0ed8-7e4e-4a27-8a02-c013fc8291b1"></script>
    </head>
    """, width=None, height=None)

def main():
    # Initialize the page
    init_page()
    
    # Create tabs
    tab1, tab2 = st.tabs(["Wye(Y) to Delta(Δ)", "Delta(Δ) to Wye(Y)"])
    
    # Render content based on active tab
    with tab1:
        wye_to_delta_tab()
    
    with tab2:
        delta_to_wye_tab()
    
    # Add tracking scripts
    add_tracking()

if __name__ == "__main__":
    main()
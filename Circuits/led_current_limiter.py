import streamlit as st
import schemdraw
from schemdraw import elements as elm

def draw_led_circuit(v, r, i, f):
    """Draw circuit with resistor, ammeter, LED, and battery"""
    d = schemdraw.Drawing()
    d.config(unit=2.5, color='#00cc00', bgcolor='none')
    p = d.add(elm.Battery().label(f"{v} V"))
    q = d.add(elm.Line().left().at(p.start))
    d.add(elm.Line().up().at(q.end))
    d.add(elm.Resistor().right().label(f"{r:.2f} Ω"))
    d.add(elm.MeterA().right().label(f"{i} mA"))
    d.add(elm.LED().right().label(f"{f} V"))  
    d.add(elm.Line().down())
    d.add(elm.Line().left())
    
    # Get SVG data with UTF-8 encoding
    svg_data = d.get_imagedata('svg')
    if isinstance(svg_data, bytes):
        return svg_data.decode('utf-8', errors='ignore')
    return svg_data

def calculate_resistance(v, f, i):
    """Calculate the required resistance"""
    if i > 0:  # Avoid division by zero
        return (v - f) / (i / 1000)  # Convert mA to A
    return 0

@st.fragment()
def show_formula():
    cl1, cl2 = st.columns(2)
    with cl1:
        st.markdown("### Formula for Calculations:")
        st.latex(r"R = \frac{V_s - V_f}{I_f}")
    with cl2:
        st.write("######")
        st.markdown("Where:")
        st.markdown(r"""
                    -  $R$ : Resistance \($\Omega$\)
                    -  $V_{s}$ : Source Voltage (V)
                    -  $V_{f}$ : LED Forward Voltage (V)
                    -  $I_{f}$ : LED Forward Current (A)
        """)


@st.fragment()
def led_current_limiter_tab():
    st.subheader("LED Current Limiting Circuit Calculator")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        v = st.number_input("Source Voltage (V)", value=5.0, min_value=0.0, step=1.0)
    with col2:
        f = st.number_input("LED Forward Voltage (V)", value=3.0, min_value=0.0, step=1.0)
    with col3:
        i = st.number_input("Limiting Current (mA)", value=20.0, min_value=0.0, step=1.0)
    with col4:
        st.write("######")

    # Calculate resistance
    r = calculate_resistance(v, f, i)

    # Create columns for output
    cols1, cols2 = st.columns(2)
    with cols1:
        st.write("######")
        led_circuit = draw_led_circuit(v, r, i, f)
        st.markdown(led_circuit, unsafe_allow_html=True)
    with cols2:
        st.write("#####")
        st.markdown("#### Results:")
        st.write(f"LED Forward Voltage: {f:.2f} V")
        st.write(f"Source Voltage: {v:.2f} V")
        st.write(f"Calculated Resistance: {r:.2f} Ω")
        st.write(f"Limiting Current: {i:.2f} mA")
        
    st.write("####")
    show_formula()

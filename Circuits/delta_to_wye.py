import streamlit as st
import schemdraw
import schemdraw.elements as elm

def draw_wye_circuit(res1, res2, res3):
    """Draw Wye circuit with proper encoding handling"""
    d = schemdraw.Drawing()
    d.config(unit=2.5, color="#00cc00", bgcolor='none')
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
    d.config(unit=4, color="#00cc00", bgcolor='none')
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

@st.cache_resource()
def display_delta_to_wye_formula():
    st.write("#")
    st.subheader("Formula used:")
    st.latex(r"R_1 = \frac{R_a R_b}{R_a + R_b + R_c}")
    st.latex(r"R_2 = \frac{R_b R_c}{R_a + R_b + R_c}")
    st.latex(r"R_3 = \frac{R_c R_a}{R_a + R_b + R_c}")



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
    
    display_delta_to_wye_formula()

import streamlit as st
import schemdraw
import schemdraw.elements as elm
from functools import lru_cache

# Cache SVG drawing functions
@st.cache_data
def draw_wye_circuit(res1, res2, res3):
    """Draw Wye circuit with caching"""
    d = schemdraw.Drawing()
    d.config(unit=2.5, color="#00cc00", bgcolor='none')
    
    center = d.add(elm.Dot())
    d.add(elm.Resistor().right().label(f"R1={res1:.4f}Ω", loc="top").label("x", loc="right"))
    d.add(elm.Resistor().theta(-120).at(center.start).label(f"R2={res2:.4f}Ω", loc="top").label("y", loc="left"))
    d.add(elm.Resistor().theta(120).at(center.start).label(f"R3={res3:.4f}Ω", loc="bottom").label("z", loc="left"))
    
    svg_data = d.get_imagedata('svg')
    return svg_data.decode('utf-8', errors='ignore') if isinstance(svg_data, bytes) else svg_data

@st.cache_data
def draw_delta_circuit(resa, resb, resc):
    """Draw Delta circuit with caching"""
    d = schemdraw.Drawing()
    d.config(unit=4, color="#00cc00", bgcolor='none')
    
    start_point = (0, 0)
    r1 = d.add(elm.Resistor().up().at(start_point).label(f"Ra={resa:.4f}Ω", loc="top", ofst=.1).label("z", loc="right"))
    r2 = d.add(elm.Resistor().theta(-30).label(f"Rb={resb:.4f}Ω", loc="top", ofst=.3).label("x", loc="right"))
    r3 = d.add(elm.Resistor().theta(-150).label(f"Rc={resc:.4f}Ω", loc="bottom", ofst=.3).label("y", loc="left"))
    d.add(elm.Line().at(r3.end).to(r1.start))
    
    svg_data = d.get_imagedata('svg')
    return svg_data.decode('utf-8', errors='ignore') if isinstance(svg_data, bytes) else svg_data

# Cache formula HTML
@st.cache_data
def get_formula_html():
    st.subheader("Formula used:")
    st.latex(r"R_a = \frac{R_1 R_2 + R_2 R_3 + R_3 R_1}{R_1}")
    st.latex(r"R_b = \frac{R_1 R_2 + R_2 R_3 + R_3 R_1}{R_2}")
    st.latex(r"R_c = \frac{R_1 R_2 + R_2 R_3 + R_3 R_1}{R_3}")

# Cache calculation function
@st.cache_data
def calculate_delta_values(res1, res2, res3):
    """Calculate Delta values from Wye values"""
    denominator = res1 * res2 + res2 * res3 + res3 * res1
    return (
        round(denominator / res1, 4),
        round(denominator / res2, 4),
        round(denominator / res3, 4)
    )

def wye_to_delta_tab():
    """Main tab function with optimized rendering"""
    st.markdown("#### Wye (Y) to Delta (Δ) Circuit Converter")
    
    # Use a container to reduce redraws
    with st.container():
        col1, col2 = st.columns(2, gap='large')
        
        # Input column
        with col1:
            st.write("######")
            st.write("**Input Wye (Y) Resistor Values:**")
            
            # Group inputs in a container
            with st.container():
                cols1, cols2, cols3 = st.columns(3)
                with cols1:
                    res1 = st.number_input("Value of R1: ", min_value=0.0001, value=10.0, step=1.0, key="wye_res1")
                with cols2:
                    res2 = st.number_input("Value of R2: ", min_value=0.0001, value=10.0, step=1.0, key="wye_res2")
                with cols3:
                    res3 = st.number_input("Value of R3: ", min_value=0.0001, value=10.0, step=1.0, key="wye_res3")
            
            # Draw Wye circuit
            wye_svg = draw_wye_circuit(res1, res2, res3)
            st.markdown(wye_svg, unsafe_allow_html=True)
        
        # Output column
        with col2:
            # Calculate values using cached function
            resa, resb, resc = calculate_delta_values(res1, res2, res3)
            
            # Display results
            st.markdown("**Delta (Δ) Resistor Values:**")
            
            # Group output values in a container
            with st.container():
                st.write(f"Ra = {resa:.4f} Ω")
                st.write(f"Rb = {resb:.4f} Ω")
                st.write(f"Rc = {resc:.4f} Ω")
            
            # Draw Delta circuit
            delta_svg = draw_delta_circuit(resa, resb, resc)
            st.markdown(delta_svg, unsafe_allow_html=True)
    
    # Display formula using cached HTML
    st.markdown(get_formula_html(), unsafe_allow_html=True)
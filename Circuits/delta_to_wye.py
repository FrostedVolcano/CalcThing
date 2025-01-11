import streamlit as st
import schemdraw
import schemdraw.elements as elm
from functools import lru_cache

# Cache SVG drawing functions since they're computationally expensive
@st.cache_data
def draw_wye_circuit(res1, res2, res3):
    """Draw Wye circuit with caching"""
    d = schemdraw.Drawing()
    d.config(unit=2.5, color="#00cc00", bgcolor='none')
    
    # Create circuit elements
    center = d.add(elm.Dot())
    d.add(elm.Resistor().right().label(f"R1={res1:.4f}Ω", loc="top").label("x", loc="right"))
    d.add(elm.Resistor().theta(-120).at(center.start).label(f"R2={res2:.4f}Ω", loc="top").label("y", loc="left"))
    d.add(elm.Resistor().theta(120).at(center.start).label(f"R3={res3:.4f}Ω", loc="bottom").label("z", loc="left"))
    
    # Get SVG data with encoding handling
    svg_data = d.get_imagedata('svg')
    return svg_data.decode('utf-8', errors='ignore') if isinstance(svg_data, bytes) else svg_data

@st.cache_data
def draw_delta_circuit(resa, resb, resc):
    """Draw Delta circuit with caching"""
    d = schemdraw.Drawing()
    d.config(unit=4, color="#00cc00", bgcolor='none')
    
    # Create circuit elements
    start_point = (0, 0)
    r1 = d.add(elm.Resistor().up().at(start_point).label(f"Ra={resa:.4f}Ω", loc="top", ofst=.1).label("z", loc="right"))
    r2 = d.add(elm.Resistor().theta(-30).label(f"Rb={resb:.4f}Ω", loc="top", ofst=.3).label("x", loc="right"))
    r3 = d.add(elm.Resistor().theta(-150).label(f"Rc={resc:.4f}Ω", loc="bottom", ofst=.3).label("y", loc="left"))
    d.add(elm.Line().at(r3.end).to(r1.start))
    
    # Get SVG data with encoding handling
    svg_data = d.get_imagedata('svg')
    return svg_data.decode('utf-8', errors='ignore') if isinstance(svg_data, bytes) else svg_data

# Cache formula display HTML
@st.cache_data
def get_formula_html():
    st.subheader("Formula used:")
    st.latex(r"R_1 = \frac{R_a R_b}{R_a + R_b + R_c}")
    st.latex(r"R_2 = \frac{R_b R_c}{R_a + R_b + R_c}")
    st.latex(r"R_3 = \frac{R_c R_a}{R_a + R_b + R_c}")

# Cache computation function
@st.cache_data
def calculate_wye_values(r1, r2, r3):
    """Calculate Wye values from Delta values"""
    r_sum = r1 + r2 + r3
    return (
        round((r1 * r2) / r_sum, 4),
        round((r2 * r3) / r_sum, 4),
        round((r3 * r1) / r_sum, 4)
    )

def delta_to_wye_tab():
    """Main tab function with optimized rendering"""
    st.markdown("#### Delta (Δ) to Wye (Y) Circuit Converter")
    
    # Use a container to reduce redraws
    with st.container():
        col1, col2 = st.columns(2, gap='large')
        
        # Input column
        with col1:
            st.write("######")
            st.write("**Input Delta (Δ) Resistor Values:**")
            
            # Group inputs in a single container
            with st.container():
                cols1, cols2, cols3 = st.columns(3)
                with cols1:
                    r1 = st.number_input("Value of Ra: ", min_value=0.0001, value=30.0, step=1.0, key="delta_r1")
                with cols2:
                    r2 = st.number_input("Value of Rb: ", min_value=0.0001, value=30.0, step=1.0, key="delta_r2")
                with cols3:
                    r3 = st.number_input("Value of Rc: ", min_value=0.0001, value=30.0, step=1.0, key="delta_r3")
            
            # Draw delta circuit
            delta_svg = draw_delta_circuit(r1, r2, r3)
            st.markdown(delta_svg, unsafe_allow_html=True)
        
        # Output column
        with col2:
            # Calculate values using cached function
            ra, rb, rc = calculate_wye_values(r1, r2, r3)
            
            # Display results
            st.markdown("**Wye (Y) Resistor Values:**")
            
            # Group output values in a container
            with st.container():
                st.write(f"R1 = {ra:.4f} Ω")
                st.write(f"R2 = {rb:.4f} Ω")
                st.write(f"R3 = {rc:.4f} Ω")
            
            # Draw wye circuit
            wye_svg = draw_wye_circuit(ra, rb, rc)
            st.markdown(wye_svg, unsafe_allow_html=True)
    
    # Display formula using cached HTML
    st.markdown(get_formula_html(), unsafe_allow_html=True)
import streamlit as st
import schemdraw
import schemdraw.elements as elm
from io import BytesIO

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
        }
</style>
""",
unsafe_allow_html=True)

st.header("Circuit Calculators:")

tab1, tab2 = st.tabs(["Wye(Y) to Delta(Δ)", " Delta(Δ) to Wye(Y)"])

with tab1:
    @st.fragment()
    def draw_wye_circuit(res1, res2, res3):
        with schemdraw.Drawing() as d:
            d.config(unit=3, color="#37bd95")
            center = d.add(elm.Dot())
            d.add(elm.Resistor().right().label(f"R1={res1:.4f}Ω", loc="top").label("x", loc="right"))
            d.add(elm.Resistor().theta(-120).at(center.start).label(f"R2={res2:.4f}Ω", loc="top").label("y", loc="left"))
            d.add(elm.Resistor().theta(120).at(center.start).label(f"R3={res3:.4f}Ω", loc="bottom").label("z", loc="left"))
        
            svg_content = d.get_imagedata('svg')
            return svg_content
           
    def draw_delta_circuit(resa, resb, resc):
        with schemdraw.Drawing() as d:
            d.config(unit=5, color="#37bd95")
            start_point = (0, 0)  # Coordinates for the starting point
            r1 = d.add(elm.Resistor().up().at(start_point).label(f"Ra={resa:.4f}Ω", loc="top", ofst=.1).label("z", loc="right"))
            r2 = d.add(elm.Resistor().theta(-30).label(f"Rb={resb:.4f}Ω", loc="top", ofst=.3).label("x", loc="right"))
            r3 = d.add(elm.Resistor().theta(-150).label(f"Rc={resc:.4f}Ω", loc="bottom", ofst=.3).label("y", loc="left"))
            d.add(elm.Line().at(r3.end).to(r1.start))  # Close the Delta loop
        
            svg_content = d.get_imagedata('svg')
            return svg_content
        
    st.subheader(" Wye (Y) to Delta (Δ) Circuit Converter")
        
    col1, col2 = st.columns(2, gap='large')

    with col1:
        st.write("######")
        st.write("Input Wye (Y) Resistor Values:")
        # Draw Wye circuit
        cols1, cols2, cols3 = st.columns(3)
        with cols1:
           res1 = st.number_input("Value of R1: ", min_value=0.0001, value=10.0, step=1.0)
        with cols2:
           res2 = st.number_input("Value of R2: ", min_value=0.0001, value=10.0, step=1.0)
        with cols3:
           res3 = st.number_input("Value of R3: ", min_value=0.0001, value=10.0, step=1.0)
            
        wye_circuit = draw_wye_circuit(res1, res2, res3)
        st.markdown(f'{wye_circuit.decode()}', unsafe_allow_html=True)
        
        st.write("#")
        st.subheader("Formula used:")
        st.latex(r"R_a = \frac{R_1 R_2 + R_2 R_3 + R_3 R_1}{R_1}")
        st.latex(r"R_b = \frac{R_1 R_2 + R_2 R_3 + R_3 R_1}{R_2}")
        st.latex(r"R_c = \frac{R_1 R_2 + R_2 R_3 + R_3 R_1}{R_3}")


    with col2:
        # Draw Delta circuit
        denominator = res1 * res2 + res2 * res3 + res3 * res1
        resa = round((denominator / res1), 4)
        resb = round((denominator / res2), 4)
        resc = round((denominator / res3), 4)
        delta_circuit = draw_delta_circuit(resa, resb, resc)
    
        st.write("Delta Resistor Values:")
        st.write(f"Ra = {resa:.4f} Ω")
        st.write(f"Rb = {resb:.4f} Ω")
        st.write(f"Rc = {resc:.4f} Ω")
        st.markdown(f'{delta_circuit.decode()}', unsafe_allow_html=True)
        
        


with tab2:
    @st.fragment()
    def draw_delta_circuit(r1, r2, r3):
        with schemdraw.Drawing() as d:
            d.config(unit=5, color="#37bd95")
            start_point = (0, 0)  # Coordinates for the starting point
            r1_draw = d.add(elm.Resistor().up().at(start_point).label(f"Ra={r1:.4f}Ω", loc="top", ofst=.1).label("z", loc="right"))
            r2_draw = d.add(elm.Resistor().theta(-30).label(f"Rb={r2:.4f}Ω", loc="top", ofst=.3).label("x", loc="right"))
            r3_draw = d.add(elm.Resistor().theta(-150).label(f"Rc={r3:.4f}Ω", loc="bottom", ofst=.3).label("y", loc="left"))
            d.add(elm.Line().at(r3_draw.end).to(r1_draw.start))  # Close the Delta loop
        
            svg_content = d.get_imagedata('svg')
            return svg_content
        
    def draw_wye_circuit(ra, rb, rc):
        with schemdraw.Drawing() as d:
            d.config(unit=3, color="#37bd95")
            center = d.add(elm.Dot())
            d.add(elm.Resistor().right().label(f"R1={ra:.4f}Ω", loc="top").label("x", loc="right"))
            d.add(elm.Resistor().theta(-120).at(center.start).label(f"R2={rb:.4f}Ω", loc="top").label("y", loc="left"))
            d.add(elm.Resistor().theta(120).at(center.start).label(f"R3={rc:.4f}Ω", loc="bottom").label("z", loc="left"))
        
            
            svg_content = d.get_imagedata('svg')
            return svg_content
        
    st.subheader("Delta (Δ) to Wye (Y) Circuit Converter")

    col1, col2 = st.columns(2, gap='large')

    with col1:
        st.write("######")
        # Input Delta resistor values
        st.write("Input Delta (Δ) Resistor Values:")
        cols1, cols2, cols3 = st.columns(3)
        with cols1:
            r1 = st.number_input("Value of Ra: ", min_value=0.0001, value=30.0, step=1.0)
        with cols2:
            r2 = st.number_input("Value of Rb: ", min_value=0.0001, value=30.0, step=1.0)
        with cols3:
            r3 = st.number_input("Value of Rc: ", min_value=0.0001, value=30.0, step=1.0)
    
        # Draw Delta circuit
        delta_circuit = draw_delta_circuit(r1, r2, r3)
        st.markdown(f'{delta_circuit.decode()}', unsafe_allow_html=True)
        
        st.write("#")
        st.subheader("Formula used:")
        st.latex(r"R_1 = \frac{R_a R_b}{R_a + R_b + R_c}")
        st.latex(r"R_2 = \frac{R_b R_c}{R_a + R_b + R_c}")
        st.latex(r"R_3 = \frac{R_c R_a}{R_a + R_b + R_c}")

    with col2:
        # Calculate Wye resistor values
        r_sum = r1 + r2 + r3
        ra = round((r1 * r2) / r_sum, 4)
        rb = round((r2 * r3) / r_sum, 4)
        rc = round((r3 * r1) / r_sum, 4)
    
        # Draw Wye circuit
        wye_circuit = draw_wye_circuit(ra, rb, rc)
        st.write("Wye (Y) Resistor Values:")
        st.write(f"R1 = {ra:.4f} Ω")
        st.write(f"R2 = {rb:.4f} Ω")
        st.write(f"R3 = {rc:.4f} Ω")
        st.markdown(f'{wye_circuit.decode()}', unsafe_allow_html=True)
    
        
         
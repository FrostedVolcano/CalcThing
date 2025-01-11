import streamlit as st
import schemdraw
import schemdraw.elements as elm
from functools import lru_cache
import numpy as np

@st.fragment
def current_divider_tab():
    # Helper functions with caching
    @lru_cache(maxsize=128)
    def eq_resistance(resistances: tuple) -> float:
        return 1.0 / np.sum(1.0 / np.array(resistances))
    
    @lru_cache(maxsize=128)
    def calculate_currents(current: float, resistances: tuple) -> tuple:
        resistance_all = eq_resistance(resistances)
        return tuple((current * resistance_all) / r for r in resistances)
    
    def draw_parallel_circuit(_current: float, _resistances: list, _currents: list) -> str:
        # Remove caching to allow dynamic updates
        d = schemdraw.Drawing()
        d.config(unit=2.5, color='#00cc00', bgcolor='none')
        
        # Add current source
        C = d.add(elm.sources.SourceI().up().label(f'{_current:.2f}A'))
        
        # Create parallel connection lines
        previous_resistor_end_top = C.end
        L_mid = d.add(elm.Line().at(C.start).down())
        previous_resistor_end_below = L_mid.end
        
        # Create resistors and lines in parallel
        for i, (resistance, current) in enumerate(zip(_resistances, _currents)):
            L_top = d.add(elm.Line().right().at(previous_resistor_end_top).linewidth(2))
            R = d.add(elm.Resistor().down().at(L_top.end).linewidth(2).label(f'{resistance:.2f}Ω'))
            d.add(elm.sources.MeterA().down().at(R.end).label(f'{current:.2f}A'))
            L_bottom = d.add(elm.Line().right().at(previous_resistor_end_below).linewidth(2))
            
            previous_resistor_end_top = L_top.end
            previous_resistor_end_below = L_bottom.end
        
        svg_data = d.get_imagedata('svg')
        return svg_data.decode('utf-8', errors='ignore') if isinstance(svg_data, bytes) else svg_data

    # Initialize session state
    if 'resistances' not in st.session_state:
        st.session_state.resistances = [100.0, 100.0, 100.0]

    # Main UI
    st.markdown("#### Current Divider Circuit")
    
    # Current input
    try:
        current = float(st.text_input("$Current$ $(A)$", value="10.0"))
    except ValueError:
        st.error("Invalid input for current. Please enter a valid number.")
        return
    
    # Resistor controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add More Resistors", key='add_resistor'):
            st.session_state.resistances.append(100.0)
    with col2:
        if st.button("Remove Last Resistor", key='remove_resistor') and len(st.session_state.resistances) > 1:
            st.session_state.resistances.pop()
    
    # Resistor inputs
    columns = st.columns(5)
    updated_resistances = []
    valid_inputs = True
    
    for i, resistance in enumerate(st.session_state.resistances):
        with columns[i % 5]:
            try:
                value = float(st.text_input(
                    f"$R_{{{i+1}}} \, (\Omega)$",
                    value=f"{resistance:.2f}",
                    key=f"resistor_{i}"
                ))
                updated_resistances.append(value)
            except ValueError:
                st.error(f"Invalid input for R_{i+1}")
                valid_inputs = False
                break
    
    # Calculate and display results only if all inputs are valid
    if valid_inputs and updated_resistances:
        # Update session state
        st.session_state.resistances = updated_resistances
        
        # Convert to tuple for caching
        resistances_tuple = tuple(updated_resistances)
        
        # Calculate currents using cached function
        currents = list(calculate_currents(current, resistances_tuple))
        
        # Draw circuit diagram - now updates dynamically
        img_buffer = draw_parallel_circuit(current, updated_resistances, currents)
        st.image(img_buffer, caption="Parallel Circuit Diagram")
        
        # Display results
        st.subheader("Results:")
        result_columns = st.columns(5)
        for i, current_value in enumerate(currents):
            with result_columns[i % 5]:
                st.write(f"$C-Flow$ $R_{{{i+1}}} \, (\Omega)$: {current_value:.2f} A")
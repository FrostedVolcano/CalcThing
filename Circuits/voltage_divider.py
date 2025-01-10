import streamlit as st
import schemdraw
import schemdraw.elements as elm

def eq_resistance(connection_type, *args):
    if connection_type == 'series':
        return sum(args)
    elif connection_type == 'parallel':
        total_reci = sum(1 / r for r in args)
        return 1/total_reci
    else:
        raise ValueError("Invalid connection type. Choose 'series' or 'parallel'.")

def voltage_divider_rule(voltage, connection_type='series', *resistance):
    """ Takes input voltage, connection_type and all the resistances.

    """
    
    resistance_all = eq_resistance('series', *resistance)
    
    if connection_type == 'series':
            voltage_drop = [(voltage * r) / resistance_all for r in resistance]
            return voltage_drop
    elif connection_type == 'parallel':
            voltage_drop = [voltage for _ in resistance]
            return voltage_drop
    else:
        raise ValueError("Invalid connection type.")

def draw_series_circuit(voltage, resistor_count, resistances, voltages):
    d = schemdraw.Drawing()
    d.config(unit=2.5, color='#00cc00', bgcolor='none')

    # Add a voltage source
    V = d.add(elm.SourceV().up().label(f'{round(voltage, 2)}V'))
    # Line going right from the top of the voltage source
    L1 = d.add(elm.Line().right().at(V.end).linewidth(2))
    L2 = d.add(elm.Line().right().at(V.start).linewidth(2))

    # Resistor(s)
    previous_resistor_end = L1.end  # To connect subsequent resistors
    previous_line_end = V.start
    for i in range(resistor_count):
        # Create a new resistor in series with its current value from user input
        R = d.add(elm.Resistor().right().at(previous_resistor_end).linewidth(2).label(f'{round(resistances[i], 2)}Ω'))
        previous_resistor_end = R.end  # Update the end for the next resistor
        if i != resistor_count - 1:
            d.add(elm.sources.MeterV().down().label(f'{round(voltages[i], 2)}'))
            d.add(elm.Ground())

    # Add horizontal lines between resistors
    for i in range(resistor_count + 2):
        L = d.add(elm.Line().right().at(previous_line_end).linewidth(2))
        previous_line_end = L.end

    L3 = d.add(elm.Line().right().at(previous_resistor_end).linewidth(2))
    L5 = d.add(elm.Line().up().at(previous_line_end).linewidth(2))

    # Get SVG data and handle encoding
    svg_data = d.get_imagedata('svg')
    if isinstance(svg_data, bytes):
        return svg_data.decode('utf-8', errors='ignore')
    return svg_data


@st.fragment()
def voltage_divider_tab():
    st.subheader("Voltage Divider Circuit")

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

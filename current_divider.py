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

def current_divider_rule(current, connection_type='parallel', *resistance):
    resistance_all = eq_resistance('parallel', *resistance)

    if connection_type == 'series':
        return current
    elif connection_type == 'parallel':
        current_each = [(current * resistance_all) / r for r in resistance]
        return current_each
    else:
        raise ValueError("Invalid Connection Type.")

def draw_parallel_circuit(current, resistor_count, resistances, currents):
    d = schemdraw.Drawing()
    d.config(unit=3, color='#ff6600')

    # Add a current source
    C = d.add(elm.sources.SourceI().up().label(f'{round(current, 2)}A'))

    # Create the parallel connection lines
    previous_resistor_end_top = C.end
    L_mid = d.add(elm.Line().at(C.start).down())

    previous_resistor_end_below = L_mid.end
    # Create resistors and lines in parallel
    for i in range(resistor_count):
        # Create a new horizontal line for the resistor at the top
        L_top = d.add(elm.Line().right().at(previous_resistor_end_top).linewidth(2))
        
        # Place the resistor and label it with its value
        R = d.add(elm.Resistor().down().at(L_top.end).linewidth(2).label(f'{round(resistances[i], 2)}Ω'))
        Ammeter = d.add(elm.sources.MeterA().down().at(R.end).label(f'{round(currents[i], 2)}A'))

        # Create a line back to the bottom node
        L_bottom = d.add(elm.Line().right().at(previous_resistor_end_below).linewidth(2))

        # Update the end points for the next resistor
        previous_resistor_end_top = L_top.end
        previous_resistor_end_below = L_bottom.end

    # Get SVG data and handle encoding
    svg_data = d.get_imagedata('svg')
    if isinstance(svg_data, bytes):
        return svg_data.decode('utf-8', errors='ignore')
    return svg_data
    


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

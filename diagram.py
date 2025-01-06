import schemdraw
import schemdraw.elements as elm

def draw_series_circuit(voltage, resistor_count, resistances, voltages):
    d = schemdraw.Drawing()
    d.config(unit=3, color='#ff6600')

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

def draw_parallel_circuit(current, resistor_count, resistances, currents):
    d = schemdraw.Drawing()
    d.config(unit=3, color='#3366ff')

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
    

def draw_wye_circuit(res1, res2, res3):
    """Draw Wye circuit with proper encoding handling"""
    d = schemdraw.Drawing()
    d.config(unit=3, color="#00cc00")
    center = d.add(elm.Dot())
    d.add(elm.Resistor().right().label(f"R1={res1:.4f}Ω", loc="top").label("x", loc="right"))
    d.add(elm.Resistor().theta(-120).at(center.start).label(f"R2={res2:.4f}Ω", loc="top").label("y", loc="left"))
    d.add(elm.Resistor().theta(120).at(center.start).label(f"R3={res3:.4f}Ω", loc="bottom").label("z", loc="left", ofst=.2))
    
    # Get SVG data and force UTF-8 encoding
    svg_data = d.get_imagedata('svg')
    if isinstance(svg_data, bytes):
        return svg_data.decode('utf-8', errors='ignore')
    return svg_data

def draw_delta_circuit(resa, resb, resc):
    """Draw Delta circuit with proper encoding handling"""
    d = schemdraw.Drawing()
    d.config(unit=5, color="#00cc00")
    start_point = (0, 0)
    r1 = d.add(elm.Resistor().up().at(start_point).label(f"Ra={resa:.4f}Ω", loc="top").label("z", loc="right", ofst=.2))
    r2 = d.add(elm.Resistor().theta(-30).label(f"Rb={resb:.4f}Ω", loc="top", ofst=.3).label("x", loc="right"))
    r3 = d.add(elm.Resistor().theta(-150).label(f"Rc={resc:.4f}Ω", loc="bottom", ofst=.3).label("y", loc="left"))
    d.add(elm.Line().at(r3.end).to(r1.start))
    
    # Get SVG data and force UTF-8 encoding
    svg_data = d.get_imagedata('svg')
    if isinstance(svg_data, bytes):
        return svg_data.decode('utf-8', errors='ignore')
    return svg_data

def resistance_(voltage, current):
    try:
        return float(voltage/current)
    except ZeroDivisionError:
        print("Infinite Resistance")


def voltage(current, resistance):
    return float(current * resistance)


def current(voltage, resistance):
    try:
        return float(voltage/resistance)
    except ZeroDivisionError:
        print("Zero Current")


def ohms_law():
    user_action = input("Find Voltage (V) or Current (I) or Resistance (R)")

    if 'V' | 'v' in user_action:
        current = float(input("Enter i: "))
        resistance = float(input("Enter r: "))
        return voltage(current, resistance)
    
    elif 'I' | 'i' in user_action:
        voltage = float(input("Enter v: "))
        resistance = float(input("Enter r: "))
        return current(voltage, resistance)
    
    elif 'R' | 'r' in user_action:
        current = float(input("Enter i: "))
        voltage = float(input("Enter v: "))
        return resistance(voltage, current)
    else:
        print("Invalid choice")


def kvl_check(*args):
    if sum(args) == 0:
        return True
    else:
        return False


def kcl_check(*args):
    if sum(args) == 0:
        return True
    else:
        return False


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


def current_divider_rule(current, connection_type='parallel', *resistance):
    resistance_all = eq_resistance('parallel', *resistance)

    if connection_type == 'series':
        return current
    elif connection_type == 'parallel':
        current_each = [(current * resistance_all) / r for r in resistance]
        return current_each
    else:
        raise ValueError("Invalid Connection Type.")


def delta_wye(a, b, c):
    sum_r = sum(a,b,c)
    r1 = (b*c)/sum_r
    r2 = (c*a)/sum_r
    r3 = (a*b)/sum_r
    return [r1, r2, r3]

def wye_delta(r1, r2, r3):
    sum_r = (r1*r2) + (r2*r3) + (r3*r1)
    a = sum_r / r1
    b = sum_r / r2
    c = sum_r / r3

    return [a, b, c]

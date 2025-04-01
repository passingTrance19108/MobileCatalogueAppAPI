ALLOWED_NETWORKS = {"GSM", "HSPA", "LTE", "3G", "4G", "5G"}

def validate_serial_number(serial_number):
    if not (len(serial_number) == 11 and serial_number.isalnum()):
        raise ValueError("Serial number must be exactly 11 alphanumeric characters.")
    return serial_number

def validate_imei(imei):
    if not (len(imei) == 15 and imei.isdigit()):
        raise ValueError("IMEI must be exactly 15 digits.")
    return imei

def validate_model(model):
    if not (len(model) >= 2 and model.isalnum()):
        raise ValueError("Model must be alphanumeric and at least 2 characters long.")
    return model

def validate_brand(brand):
    if not (len(brand) >= 2 and brand.isalpha()):
        raise ValueError("Brand must contain only letters and be at least 2 characters long.")
    return brand

def validate_network_technologies(network_technologies):
    if not (isinstance(network_technologies, list) and network_technologies):
        raise ValueError("Network technologies must be provided as a non-empty list.")
    if not all(tech in ALLOWED_NETWORKS for tech in network_technologies):
        raise ValueError(f"Network technologies must be among: {', '.join(ALLOWED_NETWORKS)}.")
    return ",".join(network_technologies)

def validate_number_of_cameras(number_of_cameras):
    if not (isinstance(number_of_cameras, int) and 1 <= number_of_cameras <= 3):
        raise ValueError("Number of cameras must be an integer between 1 and 3.")
    return number_of_cameras

def validate_number_of_cores(number_of_cores):
    if not (isinstance(number_of_cores, int) and number_of_cores >= 1):
        raise ValueError("Number of cores must be an integer greater than or equal to 1.")
    return number_of_cores

def validate_weight(weight):
    if not (isinstance(weight, int) and weight > 0):
        raise ValueError("Weight must be a positive integer (in grams).")
    return weight

def validate_battery_capacity(battery_capacity):
    if not (isinstance(battery_capacity, int) and battery_capacity > 0):
        raise ValueError("Battery capacity must be a positive integer (in mAh).")
    return battery_capacity

def validate_cost(cost):
    if not (isinstance(cost, (int, float)) and cost > 0):
        raise ValueError("Cost must be a positive number (in euros).")
    return float(cost)
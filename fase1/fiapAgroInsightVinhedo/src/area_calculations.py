def calculate_rectangular_area(width_meters, length_meters):
    return width_meters * length_meters

def calculate_grape_row_count(width_meters, row_spacing_meters):
    return int(width_meters / row_spacing_meters)

def calculate_total_row_length(row_count, length_meters):
    return row_count * length_meters

def calculate_grape_area(width_meters, length_meters):
    return calculate_rectangular_area(width_meters, length_meters)
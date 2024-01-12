
import re
import math

def parse_input(input_data):
    # Parse the input data from the text
    wafer_diameter = int(re.search(r'WaferDiameter:(\d+)', input_data).group(1))
    die_size = tuple(map(int, re.search(r'DieSize:(\d+)x(\d+)', input_data).groups()))
    die_shift_vector = tuple(map(int, re.search(r'DieShiftVector:\(([^)]+)\)', input_data).group(1).split(',')))
    reference_die = tuple(map(int, re.search(r'ReferenceDie:\(([^)]+)\)', input_data).group(1).split(',')))
    
    return wafer_diameter, die_size, die_shift_vector, reference_die
'''
def generate_wafer_map(wafer_diameter, die_size, die_shift_vector, reference_die):
    die_width, die_height = die_size
    shift_x, shift_y = die_shift_vector
    ref_die_x, ref_die_y = reference_die
    
    # Calculate the number of dies that fit horizontally and vertically
    radius = wafer_diameter / 2
    num_dies_horizontal = (2 * radius) // die_width
    num_dies_vertical = (2 * radius) // die_height
    
    wafer_map = []
    num_dies_horizontal = int(num_dies_horizontal)
    num_dies_vertical = int(num_dies_vertical)
    # Generate the wafer map
    for i in range(-num_dies_vertical//2, num_dies_vertical//2 + 1):
        for j in range(-num_dies_horizontal//2, num_dies_horizontal//2 + 1):
            # Calculate the die's center position
            llc_x = j * die_width + shift_x
            llc_y = i * die_height + shift_y

            lrc_x = j* die_width + shift_x + die_width
            lrc_y = i*die_height + shift_y + die_height

            ulc_x = llc_x + die_height
            ulc_y = llc_y + die_height

            urc_x = lrc_x + die_height
            urc_y = lrc_y + die_height
            

            # Check if the die's center is within the wafer
            if (llc_x**2 + llc_y**2) <= radius**2 or (lrc_x**2 + lrc_y**2 <= radius**2) or (ulc_x**2 + ulc_y**2 <= radius**2) or (urc_x**2 + urc_y**2 <= radius**2):
                wafer_map.append(((j + ref_die_x, i + ref_die_y), (round(llc_x, 4), round(llc_y, 4))))
    
    return wafer_map
'''
def generate_wafer_map(params):
    wafer_diameter = params['WaferDiameter']
    die_width, die_height = params['DieSize']
    shift_x, shift_y = params['DieShiftVector']
    ref_die_x, ref_die_y = params['ReferenceDie']
    
    radius = wafer_diameter / 2.0
    num_dies_horizontal = int(math.ceil(wafer_diameter / die_width))
    num_dies_vertical = int(math.ceil(wafer_diameter / die_height))
    
    die_positions = []
    
    # Calculate the reference die bottom left corner based on center
    ref_die_blc_x = ref_die_x - die_width / 2 + shift_x
    ref_die_blc_y = ref_die_y - die_height / 2 + shift_y
    
    # Loop through each potential die position
    for i in range(-num_dies_vertical // 2, num_dies_vertical // 2 + 1):
        for j in range(-num_dies_horizontal // 2, num_dies_horizontal // 2 + 1):
            die_blc_x = ref_die_blc_x + j * die_width
            die_blc_y = ref_die_blc_y + i * die_height
            
            # Check if the die is at least partially inside the wafer
            if (die_blc_x + die_width > -radius and die_blc_x < radius and
                die_blc_y + die_height > -radius and die_blc_y < radius):
                die_index = (j, i)
                die_positions.append((die_index, (round(die_blc_x, 4), round(die_blc_y, 4))))
    
    return die_positions

def write_output(filename, wafer_map):
    with open(filename, 'w') as file:
        for die_index, coordinates in wafer_map:
            file.write(f"{die_index}:{coordinates}\n")

# Path to the uploaded input file
input_filename = "C:\HackathonKLA\KLA-Hackathon\Milestone2\Input\Testcase1.txt" # This should be the actual path to the input file

# Read the input file
with open(input_filename, 'r') as file:
    input_data = file.read()

# Parse the input data
parameters = parse_input(input_data)

# Generate the wafer map
wafer_map = generate_wafer_map(parameters)
# Path to the output file
output_filename = 'milestone2output.txt'

# Write the wafer map to the output file
write_output(output_filename, wafer_map)

'''
# Importing required libraries
import re
import math

# Define the function to parse the input data
def parse_input(input_data):
    parameters = {
        'WaferDiameter': int(re.search(r'WaferDiameter:(\d+)', input_data).group(1)),
        'DieSize': tuple(map(int, re.search(r'DieSize:(\d+)x(\d+)', input_data).groups())),
        'DieShiftVector': tuple(map(int, re.search(r'DieShiftVector:\(([^)]+)\)', input_data).group(1).split(','))),
        'ReferenceDie': tuple(map(int, re.search(r'ReferenceDie:\(([^)]+)\)', input_data).group(1).split(',')))
    }
    return parameters

# Define the function to generate the wafer map
def generate_wafer_map(params):
    # Unpack parameters
    diameter = params['WaferDiameter']
    die_width, die_height = params['DieSize']
    shift_x, shift_y = params['DieShiftVector']
    ref_die_x, ref_die_y = params['ReferenceDie']
    radius = diameter / 2

    # Initialize wafer map list
    wafer_map = []

    # Calculate number of dies that fit within the diameter
    num_dies_x = int(math.ceil((radius * 2) / die_width))
    num_dies_y = int(math.ceil((radius * 2) / die_height))

    # Calculate the range for the grid
    range_x = num_dies_x // 2
    range_y = num_dies_y // 2

    # Loop through each potential die location
    for i in range(-range_y, range_y + 1):
        for j in range(-range_x, range_x + 1):
            # Calculate the lower left corner of the die
            ll_x = (j + ref_die_x) * die_width + shift_x - radius
            ll_y = (i + ref_die_y) * die_height + shift_y - radius

            # Check if the die is at least partially inside the wafer's circular area
            if (ll_x < radius and ll_y < radius) and \
               (ll_x + die_width > -radius and ll_y + die_height > -radius):
                # Add the die to the wafer map with coordinates rounded to 4 decimal places
                wafer_map.append(((j, i), (round(ll_x, 4), round(ll_y, 4))))

    return wafer_map

# Define the function to write the wafer map to a file
def write_output_to_file(wafer_map, filename):
    with open(filename, 'w') as file:
        for die_index, ll_corner in wafer_map:
            file.write(f"{die_index}:{ll_corner}\n")

# Test input data
input_data = """
WaferDiameter:300
DieSize:30x30
DieShiftVector:(0,0)
ReferenceDie:(15,15)
"""
input_filename = "C:\HackathonKLA\KLA-Hackathon\Milestone2\Input\Testcase1.txt" # This should be the actual path to the input file

# Read the input file
with open(input_filename, 'r') as file:
    input_data = file.read()

# Parse the input data
wafer_diameter, die_size, die_shift_vector, reference_die = parse_input(input_data)


# Parse the input data to get the parameters
params = parse_input(input_data)

# Generate the wafer map including partial dies
wafer_map = generate_wafer_map(params)

# Define the output file name
output_filename = 'milestone2output.txt'

# Write the wafer map to the output file
write_output_to_file(wafer_map, output_filename)

# Provide the output file name for download
output_filename
'''
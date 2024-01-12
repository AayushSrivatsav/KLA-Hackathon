import math

def read_input_file(filename):

    with open(filename, 'r') as file:
        lines = file.readlines()

    parameters = {}
    for line in lines:
        key, value = line.strip().split(':')
        parameters[key] = int(value)
    
    return parameters['WaferDiameter'], parameters['NumberOfPoints'], parameters['Angle']

def generate_points_on_line(diameter, num_points, angle):
    angle_rad = math.radians(angle)
    distance_between_points = diameter / (num_points - 1)
    
    # Calculate the offset to start from one end of the diameter
    offset = (num_points - 1) / 2
    print(offset)
    points = []
    for i in range(num_points):
        x = (i - offset) * distance_between_points * math.cos(angle_rad)
        y = (i - offset) * distance_between_points * math.sin(angle_rad)
        points.append((x, y))
    
    return points

def write_points_to_file(points, filename):
    with open(filename, "w") as file:
        for point in points:
            file.write(f"({point[0]:.1f},{point[1]:.1f})\n")


input_filename = "C:\\HackathonKLA\\KLA-Hackathon\\Input\\Testcase1.txt"
diameter, num_points, angle = read_input_file(input_filename)
points = generate_points_on_line(diameter, num_points, angle)
output_filename = "points.txt"
write_points_to_file(points, output_filename)

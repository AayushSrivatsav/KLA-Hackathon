import math

def read_input_file(filename):

    with open(filename, 'r') as file:
        lines = file.readlines()

    parameters = {}
    for line in lines:
        key, value = line.strip().split(':')
        parameters[key] = int(value)
    
    return parameters['WaferDiameter'], parameters['NumberOfPoints'], parameters['Angle']

def generate_points_on_diameter(diameter, num_points, angle):

    angle_rad = math.radians(angle)
    # The total number of segments is num_points - 1
    distance_between_points = diameter / (num_points - 1)
    
    # Calculate the offset from the origin for the first point
    offset = (num_points - 1) / 2 * distance_between_points

    points = []
    for i in range(num_points):
        # Calculate the position of the point on the line
        distance_from_origin = i * distance_between_points - offset
        x = distance_from_origin * math.cos(angle_rad)
        y = distance_from_origin * math.sin(angle_rad)
        # Round the coordinates to 4 decimal places
        points.append((round(x, 4), round(y, 4)))
    
    return points

def write_points_to_file(points, filename):
    with open(filename, "w") as file:
        for point in points:
            file.write(f"({point[0]:.4f},{point[1]:.4f})\n")


input_filename = "C:\\HackathonKLA\\KLA-Hackathon\\Input\\Testcase2.txt"
diameter, num_points, angle = read_input_file(input_filename)
points = generate_points_on_diameter(diameter, num_points, angle)
output_filename = "points2.txt"
print(points)
write_points_to_file(points, output_filename)

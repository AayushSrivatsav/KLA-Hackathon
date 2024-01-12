import math
import sys

class WaferMapGenerator:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.wafer_diameter = None
        self.die_size = None
        self.die_shift_vector = None
        self.reference_die = None
        self.wafer_radius = None
        self.visited = []

    def read_input(self):
        with open(self.input_file, 'r') as file:
            lines = file.readlines()

        inp_dict = {}
        for line in lines:
            key, value = line.split(":")
            value = value.strip()
            if 'x' in value:
                inp_dict[key] = tuple(map(int, value.split("x")))
            elif ',' in value:
                value = value.strip("()")
                inp_dict[key] = tuple(map(int, value.split(",")))
            else:
                inp_dict[key] = int(value)
        
        self._unpack_input(inp_dict)

    def _unpack_input(self, inp_dict):
        self.wafer_diameter = inp_dict["WaferDiameter"]
        self.die_size = inp_dict["DieSize"]
        self.die_shift_vector = inp_dict["DieShiftVector"]
        self.reference_die = inp_dict["ReferenceDie"]
        self.wafer_radius = self.wafer_diameter / 2

    def calculate_die_positions(self):
        x_die, y_die = self.die_size
        x_ref, y_ref = self.reference_die
        x_shift, y_shift = self.die_shift_vector

        ref_die_blc = [x_ref - x_die / 2, y_ref - y_die / 2]
        start_point = [ref_die_blc[0] + x_shift, ref_die_blc[1] + y_shift]

        self._die_num(start_point[0], start_point[1], 0, 0)

    def _die_num(self, x_curr, y_curr, x_pos, y_pos):
        self.visited.append((x_pos, y_pos))
        corners = [(x_curr, y_curr), (x_curr + self.die_size[0], y_curr), 
                   (x_curr, y_curr + self.die_size[1]), (x_curr + self.die_size[0], y_curr + self.die_size[1])]

        if any(math.dist([0, 0], corner) < self.wafer_radius for corner in corners):
            self._write_output(x_pos, y_pos, x_curr, y_curr)
            self._explore_neighboring_dies(x_curr, y_curr, x_pos, y_pos)
        else:
            return

    def _explore_neighboring_dies(self, x_curr, y_curr, x_pos, y_pos):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            if (x_pos + dx, y_pos + dy) not in self.visited:
                self._die_num(x_curr + dx * self.die_size[0], y_curr + dy * self.die_size[1], x_pos + dx, y_pos + dy)

    def _write_output(self, x_pos, y_pos, x_curr, y_curr):
        with open(self.output_file, 'a') as file:
            file.write(f"({x_pos},{y_pos}):({x_curr},{y_curr})\n")

    def generate_map(self):
        self.read_input()
        self.calculate_die_positions()

# Set the recursion limit higher for deep recursion
sys.setrecursionlimit(20000)

# Create an instance of the class and generate the wafer map
wafer_map_generator = WaferMapGenerator("C:\HackathonKLA\KLA-Hackathon\Milestone2\Input\Testcase4.txt", "milestone2output4.txt")
wafer_map_generator.generate_map()

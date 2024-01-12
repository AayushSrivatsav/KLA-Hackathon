
import math
import sys

sys.setrecursionlimit(20000)
#open the input file
inp= open("C:\HackathonKLA\KLA-Hackathon\Milestone2\Input\Testcase4.txt",'r')
out= open("milestone2output4check.txt",'w')

#read the input content into a dictionary
lines=inp.readlines()
input_dict = dict()

for line in lines:
    input_list=line.split(":")
    input_list[1]=input_list[1].split("\n")[0]
    if len(input_list[1].split("x"))==2:
        input_list[1]=input_list[1].split("x")
        input_list[1][0]=int(input_list[1][0])
        input_list[1][1]=int(input_list[1][1])
    elif len(input_list[1].split(","))==2:
        input_list[1]=input_list[1].split(",")
        input_list[1][0]=int(input_list[1][0].split("(")[1])
        input_list[1][1]=int(input_list[1][1].split(")")[0])
    else:
        input_list[1]=int(input_list[1])

    input_dict[input_list[0]]=input_list[1]
    

print(input_dict)

#initial setup to start calculations
x_die=input_dict["DieSize"][0]
y_die=input_dict["DieSize"][1]

x_ref=input_dict["ReferenceDie"][0]
y_ref=input_dict["ReferenceDie"][1]

x_shift=input_dict["DieShiftVector"][0]
y_shift=input_dict["DieShiftVector"][1]

initial_point=(0,0)
wafer_diameter=input_dict["WaferDiameter"]
wafer_radius=wafer_diameter/2


ref_die_point=[x_ref,y_ref]   #center of reference die
start_point=[ref_die_point[0]-(x_die/2),ref_die_point[1]-(y_die/2)]
if (x_shift>x_die and y_shift>y_die):
    start_point = [ref_die_point[0] - x_shift - (x_die/2), ref_die_point[1] -y_shift - (y_die/2)]

visited=[]

def die_num(x_curr,y_curr,x_pos,y_pos):

    visited.append([x_pos,y_pos])
    left_dist=math.dist([0,0],[x_curr,y_curr])
    right_dist=math.dist([0,0],[x_curr+x_die,y_curr])
    top_dist=math.dist([0,0],[x_curr,y_curr+y_die])
    top_right_dist=math.dist([0,0],[x_curr+x_die,y_curr+y_die])



    if left_dist<wafer_radius or right_dist<wafer_radius or top_dist<wafer_radius or top_right_dist<wafer_radius:

        out.write("("+str(x_pos)+","+str(y_pos)+"):("+str(x_curr)+","+str(y_curr)+")\n")
        if [x_pos-1,y_pos] not in visited:
            die_num(x_curr-x_die,y_curr,x_pos-1,y_pos)
        if [x_pos+1,y_pos] not in visited:
            die_num(x_curr+x_die,y_curr,x_pos+1,y_pos)
        if [x_pos,y_pos-1] not in visited:
            die_num(x_curr,y_curr-y_die,x_pos,y_pos-1)
        if [x_pos,y_pos+1] not in visited:
            die_num(x_curr,y_curr+y_die,x_pos,y_pos+1)
    else:
        return

die_num(start_point[0],start_point[1],0,0)

inp.close()
out.close()



#!/usr/bin/env python3

from sys import argv, exit, stderr
import math

# ---- check the validity of the args
def check_validity_args(argv):

    for i in range(1, 8):
        arg = argv[i]
        for j in range(len(arg)):
            if arg[0] != '-' and (ord(arg[j]) < 48 or ord(arg[j]) > 57) and (arg[j] != '.' and 0 < j < len(arg)):
                print ("Syntax error: argument(s) must be integer or float", file=stderr)
                exit(0)
    if int(argv[7]) != float(argv[7]) or int(argv[7]) < 0 :
        print ("Syntax error: argument(s) must be integer (positive or null)", file=stderr)
        exit(0)

# ---- check validity of calc (division by zero) ----
def check_validity_calc(norm_speed_vector):
    if norm_speed_vector == 0:
        print ("Impossible : division by zero\n(the two points are merged)", file=stderr)
        exit(0)

# ---- first error checks ----
def check_error_part_1(argv):
    if (len(argv) < 2):
        print("Syntax error: Invalid number of arguments", file=stderr)
        exit(0)
    elif argv[1] == '-h' and len(argv) == 2:
        print ('USAGE')
        print ('      ./101pong x0 y0 z0 x1 y1 z1 n\n')
        print ('DESCRIPTION')
        print ('       x0   ball abscissa at time t - 1')
        print ('       y0   ball ordinate at time t - 1')
        print ('       z0   ball altitude at time t - 1')
        print ('       x1   ball abscissa at time t')
        print ('       y1   ball ordinate at time t')
        print ('       z1   ball altitude at time t')
        print ('       n    time shift (greater than or equal to zero, integer)')
        exit(0)
    elif len(argv) != 8 :
        print("Syntax error: Invalid number of arguments", file=stderr)
        exit(0)

#.----.second.error.checks.----
def check_error_part_2(vector, norm_speed_vector, point) :
    if vector[2] == 0 or (point[2] > 0 and vector[2] > 0) or (point[2] < 0 and vector[2] < 0) :
        print ("The ball won't reach the bat.")
        exit(0)
    elif norm_speed_vector == 0 :
        print ("The ball won't reach the bat.")
        exit(0)

# ---- calc vector ----
def calc_vect(x0, y0, z0, x1, y1, z1) :
    vect_x = x1 - x0
    vect_y = y1 - y0
    vect_z = z1 - z0
    vect = [vect_x, vect_y, vect_z]
    return (vect)

# ---- calc the final position of the ball (at t + n)
def calc_final_ball_pos(x1, y1, z1, speed_vector, n):
    end_pos_x = x1 + (n * speed_vector[0])
    end_pos_y = y1 + (n * speed_vector[1])
    end_pos_z = z1 + (n * speed_vector[2])
    end_pos = [end_pos_x, end_pos_y, end_pos_z]
    return (end_pos)

# ---- calc norm of vector ----
def calc_norm(vector) :
    squared_x = vector[0]**2
    squared_y = vector[1]**2
    squared_z = vector[2]**2
    norm = math.sqrt(squared_x + squared_y + squared_z)
    return (norm)

# ---- calc cos ----
def calc_angle_with_cos(adjacent_side, hypotenuse) :
    if hypotenuse != 0 :
        cos = adjacent_side / hypotenuse
        angle = math.acos(cos)
        angle = round(angle * 180 / math.pi, 2)
        return (angle)

# ---- print values correctly ----
def print_values(val_arr) :
    print ("(", end='')
    for i in range(3) :
        val_print = float(val_arr[i])
        val_print = round(val_print, 2)
        if (val_print * 100 % 10) == 0 :
            print(str(val_print)+"0", end='')
        else :
            print(str(val_print), end ='')
        if i == 2 :
            print(")");
        else :
            print(", ", end='')

# ---- print angle value ----
def print_angle(angle) :
    angle = round(angle*100, 2)
    if (angle % 10) == 0 :
        print(str(angle /100)+"0 degrees")
    else :
        print(str(angle / 100), "degrees")

# ---- declaration of the coordinates ----
check_error_part_1(argv)
check_validity_args(argv)

x0 = float(argv[1])
y0 = float(argv[2])
z0 = float(argv[3])
x1 = float(argv[4])
y1 = float(argv[5])
z1 = float(argv[6])

n = int(argv[7])
# ---- end coordinates declaration ----

# ---- main zone ----
point = [x1, y1, z1]
speed_vector = calc_vect(x0, y0, z0, x1, y1, z1,)
norm_speed_vector = calc_norm(speed_vector)

projected_vector = calc_vect(x0, y0, 0, x1, y1, 0)
norm_projected_vector = calc_norm(projected_vector)

alpha = calc_angle_with_cos(norm_projected_vector, norm_speed_vector)
angle = alpha

end_coordinates = calc_final_ball_pos(x1, y1, z1, speed_vector, n)

check_validity_calc(norm_speed_vector)

# ---- Print result zone ----
print ("The velocity vector of the ball is:")
print_values (speed_vector)
print ("At time t + "+str(n)+", ball coordinates will be :")
print_values (end_coordinates)
check_error_part_2(speed_vector, norm_speed_vector, point)
print ("The incidence angle is:")
print_angle(angle)

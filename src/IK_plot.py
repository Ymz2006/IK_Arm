import math

import sympy as sp
from sympy import simplify
from sympy.matrices import Matrix
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def rotx(q):
    r = Matrix([
    [1., 0., 0.],
    [0., math.cos(q), -math.sin(q)],
    [0., math.sin(q), math.cos(q)]])
    return r

def roty(q):
    sq, cq = math.sin(q), math.cos(q)
    r = Matrix([
    [ cq, 0., sq],
    [ 0., 1., 0.],
    [-sq, 0., cq]])
    return r

def rotz(q):
    sq, cq = math.sin(q), math.cos(q)
    r = Matrix([
    [cq,-sq, 0.],
    [sq, cq, 0.],
    [0., 0., 1.]])
    return r


def plot_coordinate_frame(ax, origin, rotation_matrix, num, length=0.1):
    # Define the unit vectors in the frame (x, y, z)
    x_axis = rotation_matrix @ np.array([1, 0, 0])
    y_axis = rotation_matrix @ np.array([0, 1, 0])
    z_axis = rotation_matrix @ np.array([0, 0, 1])

    # Plot the axes
    ax.quiver(origin[0], origin[1], origin[2], x_axis[0], x_axis[1], x_axis[2], length=length, color='r', label='X')
    ax.quiver(origin[0], origin[1], origin[2], y_axis[0], y_axis[1], y_axis[2], length=length, color='g', label='Y')
    ax.quiver(origin[0], origin[1], origin[2], z_axis[0], z_axis[1], z_axis[2], length=length, color='b', label='Z')

    # Add labels to the axes
    ax.text(origin[0] + x_axis[0] * length * 1.1, origin[1] + x_axis[1] * length * 1.1,
            origin[2] + x_axis[2] * length * 1.1, 'X' + str(num), color='r')
    ax.text(origin[0] + y_axis[0] * length * 1.1, origin[1] + y_axis[1] * length * 1.1,
            origin[2] + y_axis[2] * length * 1.1, 'Y' + str(num), color='g')
    ax.text(origin[0] + z_axis[0] * length * 1.1, origin[1] + z_axis[1] * length * 1.1,
            origin[2] + z_axis[2] * length * 1.1, 'Z' + str(num), color='b')



def get_hypotenuse(a, b):
    # calculate the longest side given the two shorter sides
    # of a right triangle using pythagorean theorem
    return math.sqrt(a * a + b * b)

def get_cosine_law_angle(a, b, c):
    # given all sides of a triangle a, b, c
    # calculate angle gamma between sides a and b
    cos_gamma = (a*a + b*b - c*c) / (2*a*b)
    sin_gamma = math.sqrt(1 - cos_gamma * cos_gamma)
    gamma = math.atan2(sin_gamma, cos_gamma)
    return gamma



mpl.use('TkAgg')  # or can use 'TkAgg', whatever you have/prefer
theta1 = sp.Symbol('t1')
theta2 = sp.Symbol('t2')
theta3 = sp.Symbol('t3')
theta4 = sp.Symbol('t4')
theta5 = sp.Symbol('t5')
theta6 = sp.Symbol('t6')

#dh parameters
alpha_dh = {
    0: 0,
    1: 0,
    2: -math.pi/2,
    3: 0,
    4: -math.pi/2,
    5: math.pi/2,
    6: -math.pi/2
}

a_dh = {
    0: 0,
    1: 0,
    2: 0.35,
    3: 1.25,
    4: 0,
    5: 0,
    6: 0
}
d_dh = {
    0: 0,
    1: 0.75,
    2: 0,
    3: 0,
    4: 1.5,
    5: 0, #try it?
    6: 0
}
theta_dh = {
    0: 0,
    1: theta1,
    2: theta2 - sp.pi/2,
    3: theta3,
    4: theta4,
    5: theta5,
    6: theta6
}



def transformation_mat(i):
    return Matrix([[sp.cos(theta_dh[i]), -sp.sin(theta_dh[i]), 0, a_dh[i]],
                      [sp.sin(theta_dh[i]) * sp.cos(alpha_dh[i]), sp.cos(theta_dh[i]) * sp.cos(alpha_dh[i]), -sp.sin(alpha_dh[i]), -d_dh[i]*sp.sin(alpha_dh[i])],
                      [sp.sin(theta_dh[i]) * sp.sin(alpha_dh[i]), sp.cos(theta_dh[i]) * sp.sin(alpha_dh[i]), sp.cos(alpha_dh[i]), d_dh[i] * sp.cos(alpha_dh[i])],
                      [0,0,0,1],
                      ] )



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
origin = np.array([0, 0, 0])

# Set axis limits
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])

rotation_matrix = np.eye(3)

# Plot coordinate frame at the origin
# plot_coordinate_frame(ax, origin, rotation_matrix,1)

ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')


#origin_augmented = np.array([[0], [0], [0],[1]])
T01 = transformation_mat(1)#.subs(theta1,0)
T12 = transformation_mat(2)#.subs(theta1,0)
T23 = transformation_mat(3)#.subs(theta1,0)
T34 = transformation_mat(4)#.subs(theta1,0)
T45 = transformation_mat(5)#.subs(theta1,0)
T56 = transformation_mat(6)#.subs(theta1,0)

print(T34)
print(T45)
print(T56)

T03 = simplify(T01 * T12 * T23)
R03 = T03[:3, :3]
R03T = R03.T


T36 = simplify(T34 * T45 * T56)
R36 = T36[:3, :3]


target_xyz = np.array([0.7,0.5,0.5])
target_dir = np.array([0,1,0])

R0g_eval = rotx(target_dir[0]) * roty(target_dir[1]) * rotz(target_dir[2])


def get_wrist_center(gripper_point, R0g, dg = 0):
    xg, yg, zg = gripper_point
    nx, ny, nz = R0g[0, 2], R0g[1, 2], R0g[2, 2]
    xw = xg - dg * nx
    yw = yg - dg * ny
    zw = zg - dg * nz
    return xw, yw, zw

wrist_pos = get_wrist_center(target_xyz,R0g_eval)
print("wrist_pos" + str(wrist_pos))

def get_first_three_angles(wrist_center):
    x, y, z = wrist_center
    a1, a2, a3 = a_dh[2], a_dh[3], a_dh[4]
    d1, d4 = d_dh[1], d_dh[4]
    l = get_hypotenuse(d4,-a3)
    phi = math.atan2(d4, -a3)


    x_prime = get_hypotenuse(x, y)
    mx = x_prime - a1
    my = z - d1
    m = get_hypotenuse(mx, my)
    alpha = math.atan2(my, mx)
    gamma = get_cosine_law_angle(l, a2, m)
    beta = get_cosine_law_angle(m, a2, l)


    q1 = math.atan2(y, x)
    q2 = math.pi/2 - beta - alpha
    q3 = -(gamma - phi)
    return q1, q2, q3


c1,c2,c3 = get_first_three_angles(wrist_pos)


# origin = np.array([0,0,0,0])
# T01_evaluated = T01.subs(theta1,c1)
# frame1 = np.dot(T01_evaluated,origin)
#
# plot_coordinate_frame(ax,frame1,rotation_matrix,3)
#
# T02 = (T01 * T12).subs(theta1,c1)
# T02.subs(theta2,c2)

def get_last_three_angles(R):
    sin_q4 = R[2, 2]
    cos_q4 = -R[0, 2]
    sin_q5 = math.sqrt(R[0, 2]**2 + R[2, 2]**2)
    cos_q5 = R[1, 2]
    sin_q6 = -R[1, 1]
    cos_q6 = R[1, 0]
    q4 = math.atan2(sin_q4, cos_q4)
    q5 = math.atan2(sin_q5, cos_q5)
    q6 = math.atan2(sin_q6, cos_q6)
    return q4, q5, q6


R03T_eval = R03T.evalf(
    subs = {
        theta1: c1,
        theta2: c2,
        theta3: c3,
    }
)

R06 = R03 * R36
R36_eval = R03T_eval * R0g_eval
c4, c5, c6 = get_last_three_angles(R36_eval)


angles_sub = {
    theta1: c1,
    theta2: c2,
    theta3: c3,
    theta4: c4,
    theta5: c5,
    theta6: c6
}
origin_augmented = np.array([0.0,0.0,0.0,1.0]).transpose()

T01_eval = T01.subs(angles_sub)
T12_eval = T12.subs(angles_sub)
T23_eval = T23.subs(angles_sub)
T34_eval = T34.subs(angles_sub)
T45_eval = T45.subs(angles_sub)
T56_eval = T56.subs(angles_sub)

T02_eval = T01_eval @ T12_eval
T03_eval = T02_eval @ T23_eval
T04_eval = T03_eval @ T34_eval
T05_eval = T04_eval @ T45_eval
T06_eval = T05_eval @ T56_eval



p1 = (T01_eval @ origin_augmented) [:3]
p2 = (T02_eval @ origin_augmented) [:3]
p3 = (T03_eval @ origin_augmented) [:3]
p4 = (T04_eval @ origin_augmented) [:3]
p5 = (T05_eval @ origin_augmented) [:3]
p6 = (T06_eval @ origin_augmented) [:3]

print(p1)
print(p2)
print(p3)
print(p4)
print(p5)
print(p6)

R06 = np.array(T06_eval[:3, :3])


plot_coordinate_frame(ax, p1, rotation_matrix,1, length=0.1)
# plot_coordinate_frame(ax, p2, rotation_matrix,2, length=0.1)
# plot_coordinate_frame(ax, p3, rotation_matrix,3, length=0.1)
# plot_coordinate_frame(ax, p4, rotation_matrix,4, length=0.1)
# plot_coordinate_frame(ax, p5, rotation_matrix,5, length=0.1)
plot_coordinate_frame(ax, p6, R06,6, length=0.1)




ax.plot([0, p1[0]], [0, p1[1]], [0, p1[2]], color='b', marker='o')
ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='b', marker='o')
ax.plot([p2[0], p3[0]], [p2[1], p3[1]], [p2[2], p3[2]], color='b', marker='o')
ax.plot([p3[0], p4[0]], [p3[1], p4[1]], [p3[2], p4[2]], color='b', marker='o')
ax.plot([p4[0], p5[0]], [p4[1], p5[1]], [p4[2], p5[2]], color='b', marker='o')
ax.plot([p5[0], p6[0]], [p5[1], p6[1]], [p5[2], p6[2]], color='b', marker='o')








plt.show()

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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


# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define the origin and rotation matrix for the coordinate frame
origin = np.array([0, 0, 0])

theta = np.pi / 4  # 45 degrees
rotation_matrix = np.array([
    [np.cos(theta), -np.sin(theta), 0],
    [np.sin(theta), np.cos(theta), 0],
    [0, 0, 1]
])


# Plot the coordinate frame
plot_coordinate_frame(ax, origin, rotation_matrix, num=1, length=1)

# Set plot limits and labels
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the plot
plt.show()
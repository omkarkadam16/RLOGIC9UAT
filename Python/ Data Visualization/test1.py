# Example: Plotting a Linear Relationship with Matplotlib

# importing the required libraries
import matplotlib.pyplot as plt
import numpy as np

"""matplotlib.pyplot as plt: A popular plotting library in Python used for creating static, animated, and interactive visualizations.

numpy as np: A library for numerical operations, especially with arrays."""

# define data values
x = np.array([1, 2, 3, 4])  # X-axis points
y = x  # Y-axis points

plt.scatter(x, y)

plt.plot(x, y)  # Plots the points (x, y) on a 2D line chart
plt.show()  # Displays the plot window with the chart

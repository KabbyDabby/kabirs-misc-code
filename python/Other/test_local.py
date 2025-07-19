import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Define the hexagon ---
def hexagon_vertices(center, radius, num_points=6):
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)
    return np.column_stack((x, y))

# --- Collision Detection Function ---
def distance_point_to_segment(point, segment_start, segment_end):
    """Calculates the distance from a point to a line segment."""
    px, py = point
    x1, y1 = segment_start
    x2, y2 = segment_end
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return np.sqrt((px - x1)**2 + (py - y1)**2)
    t = ((px - x1) * dx + (py - y1) * dy) / (dx**2 + dy**2)
    t = max(0, min(1, t))  # Clamp t to [0, 1]
    closest_x = x1 + t * dx
    closest_y = y1 + t * dy
    return np.sqrt((px - closest_x)**2 + (py - closest_y)**2)

# --- Animation Setup ---
# Hexagon parameters
center = (0, 0)
radius = 2
# Ball parameters
ball_radius = 0.2
# Initial ball position and velocity
initial_position = (0.5, 1.0)  # Initial x, y
initial_velocity = (1.0, 0.0)  # Initial vx, vy
gravity = -0.1  # Downward acceleration

# Create the figure and axes
fig, ax = plt.subplots()
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')

# Initial ball position
ball = plt.plot(initial_position[0], initial_position[1], 'ro', markersize=ball_radius * 20)[0]
# Initialize hexagon vertices
hexagon = hexagon_vertices(center, radius)

# Hexagon edges for collision detection
edges = []
for i in range(len(hexagon)):
    edges.append((hexagon[i], hexagon[(i + 1) % len(hexagon)]))

# Rotation angle
rotation_angle = 0.0
rotation_speed = 0.05

# Animation function
def animate(frame):
    global rotation_angle, initial_position  # Access global variables

    # Update rotation angle
    rotation_angle += rotation_speed

    # Update ball position and velocity
    vx, vy = initial_velocity
    vy += gravity
    x, y = initial_position
    x += vx
    y += vy
    initial_position = (x, y)  # Update global initial_position

    # Collision detection
    for edge in edges:
        segment_start, segment_end = edge
        distance = distance_point_to_segment(initial_position, segment_start, segment_end)
        if distance < ball_radius:
            # Reverse velocity component perpendicular to the edge
            dx = segment_end[0] - segment_start[0]
            dy = segment_end[1] - segment_start[1]
            edge_length = np.sqrt(dx**2 + dy**2)
            if edge_length > 0:  #Avoid division by zero
                edge_normal_x = dy / edge_length
                edge_normal_y = -dx / edge_length
                dot_product = vx * edge_normal_x + vy * edge_normal_y
                vx -= 2 * dot_product * edge_normal_x
                vy -= 2 * dot_product * edge_normal_y

    # Update the plot
    ball.set_data(initial_position[0], initial_position[1])

    return ball,

# Create the animation
ani = animation.FuncAnimation(fig, animate, blit=True)
plt.show()
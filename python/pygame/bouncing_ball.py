import pygame
import sys
import math
import numpy as np
import random


# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize sound mixer

# Constants
WIDTH, HEIGHT = 1000, 1000
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
PINK = (255, 192, 203)
LIME = (0, 255, 0)
TEAL = (0, 128, 128)
NAVY = (0, 0, 128)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)

# List of all available colors (excluding default colors)
COLLISION_COLORS = [GREEN, YELLOW, PURPLE, ORANGE, CYAN, MAGENTA, PINK, LIME, TEAL, NAVY, MAROON, OLIVE]

# Ball properties
BALL_RADIUS = 10
BALL_MASS = 1
BALL_SPEED = 10  # Initial speed

# Shape properties
SHAPE_RADIUS = 214  # Scaled down from 300 for new window size
SHAPE_CENTER = (WIDTH // 2, HEIGHT // 2)
ROTATION_SPEED = 0.02  # radians per frame
SHAPE_SPEED = 6  # Initial speed for shape movement
MOVE_SPEED = 0.2  # Arrow key velocity adjustment (decreased from 2.0)

# Load sound effect
collision_sound = pygame.mixer.Sound("clack_fx.mp3")

def get_num_sides():
    while True:
        try:
            n = int(input("Enter the number of sides for the shape (3 or more for polygon, less than 3 for circle): "))
            return n
        except ValueError:
            print("Please enter a valid integer.")

def get_num_balls():
    while True:
        try:
            n = int(input("Enter the number of balls: "))
            if n > 0:
                return n
            print("Please enter a positive integer.")
        except ValueError:
            print("Please enter a valid integer.")

class Ball:
    def __init__(self, x, y, radius, velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = velocity
        self.mass = BALL_MASS
        self.color = RED  # Default color

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def get_shape_vertices(center, radius, rotation, num_sides):
    if num_sides < 3:
        # For circle, return points for smooth drawing
        points = []
        for i in range(36):  # 36 points for smooth circle
            angle = rotation + (2 * math.pi * i / 36)
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((x, y))
        return points
    else:
        # For polygon
        vertices = []
        for i in range(num_sides):
            angle = rotation + (2 * math.pi * i / num_sides)
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            vertices.append((x, y))
        return vertices

def get_wall_velocity(center, collision_point, rotation_speed):
    # Calculate the wall's velocity at the collision point
    # This is the tangential velocity of a point rotating around the center
    radius_vector = np.array([collision_point[0] - center[0], collision_point[1] - center[1]])
    # Rotate radius vector 90 degrees to get tangential direction
    tangential = np.array([-radius_vector[1], radius_vector[0]])
    # Normalize and scale by rotation speed
    if np.linalg.norm(tangential) > 0:
        tangential = tangential / np.linalg.norm(tangential)
    return tangential * rotation_speed * np.linalg.norm(radius_vector)

def line_intersection(p1, p2, ball_pos, ball_radius):
    # Vector from p1 to p2
    line_vec = np.array([p2[0] - p1[0], p2[1] - p1[1]])
    line_length = np.linalg.norm(line_vec)
    line_unit = line_vec / line_length

    # Vector from p1 to ball
    ball_vec = np.array([ball_pos[0] - p1[0], ball_pos[1] - p1[1]])

    # Project ball vector onto line
    projection = np.dot(ball_vec, line_unit)
    projection = max(0, min(line_length, projection))
    closest_point = p1 + line_unit * projection

    # Distance from ball to closest point on line
    distance = np.linalg.norm(np.array(ball_pos) - closest_point)

    if distance <= ball_radius:
        # Calculate normal vector (perpendicular to line)
        normal = np.array([-line_unit[1], line_unit[0]])
        # Ensure normal points inward by checking dot product with vector from center to ball
        center_to_ball = np.array([ball_pos[0] - SHAPE_CENTER[0], ball_pos[1] - SHAPE_CENTER[1]])
        if np.dot(normal, center_to_ball) < 0:
            normal = -normal
        return closest_point, normal
    return None, None

def vertex_collision(vertex, ball_pos, ball_radius):
    # Check if ball is colliding with a vertex
    distance = np.linalg.norm(np.array(ball_pos) - np.array(vertex))
    if distance <= ball_radius:
        # Calculate normal vector (from vertex to ball)
        normal = np.array([ball_pos[0] - vertex[0], ball_pos[1] - vertex[1]])
        if np.linalg.norm(normal) > 0:
            normal = normal / np.linalg.norm(normal)
        return vertex, normal
    return None, None

def reflect_velocity(velocity, normal):
    # Normalize the normal vector
    normal = normal / np.linalg.norm(normal)
    
    # Calculate reflection
    dot_product = np.dot(velocity, normal)
    reflection = velocity - 2 * dot_product * normal
    
    return reflection

def check_ball_collision(ball1, ball2):
    # Calculate distance between balls
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.sqrt(dx*dx + dy*dy)
    
    # Check if balls are colliding
    if distance < ball1.radius + ball2.radius:
        # Calculate normal vector
        nx = dx / distance
        ny = dy / distance
        
        # Calculate relative velocity
        dvx = ball2.velocity[0] - ball1.velocity[0]
        dvy = ball2.velocity[1] - ball1.velocity[1]
        
        # Calculate relative velocity in terms of the normal direction
        velocity_along_normal = dvx * nx + dvy * ny
        
        # Do not resolve if velocities are separating
        if velocity_along_normal > 0:
            return False
        
        # Calculate impulse scalar
        restitution = 1.0  # Perfectly elastic collision
        j = -(1 + restitution) * velocity_along_normal
        j /= 1/ball1.mass + 1/ball2.mass
        
        # Apply impulse
        impulse_x = j * nx
        impulse_y = j * ny
        
        ball1.velocity[0] -= impulse_x / ball1.mass
        ball1.velocity[1] -= impulse_y / ball1.mass
        ball2.velocity[0] += impulse_x / ball2.mass
        ball2.velocity[1] += impulse_y / ball2.mass
        
        # Move balls apart to prevent sticking
        overlap = (ball1.radius + ball2.radius - distance) / 2
        ball1.x -= overlap * nx
        ball1.y -= overlap * ny
        ball2.x += overlap * nx
        ball2.y += overlap * ny
        
        return True
    return False

def is_point_in_shape(point, vertices):
    # Ray casting algorithm to check if point is inside polygon
    x, y = point
    inside = False
    n = len(vertices)
    p1x, p1y = vertices[0]
    for i in range(1, n + 1):
        p2x, p2y = vertices[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def get_nearest_point_inside_shape(ball_pos, shape_center, shape_radius, vertices):
    # Unpack positions
    ball_x, ball_y = ball_pos
    center_x, center_y = shape_center
    
    # Calculate vector from center to ball
    dx = ball_x - center_x
    dy = ball_y - center_y
    distance = math.sqrt(dx*dx + dy*dy)
    
    if distance == 0:
        return (center_x, center_y)
    
    # Calculate point on shape boundary in the same direction
    boundary_x = center_x + (dx / distance) * shape_radius
    boundary_y = center_y + (dy / distance) * shape_radius
    
    # Calculate inward vector
    inward_dx = center_x - boundary_x
    inward_dy = center_y - boundary_y
    inward_length = math.sqrt(inward_dx*inward_dx + inward_dy*inward_dy)
    
    if inward_length == 0:
        return (boundary_x, boundary_y)
    
    # Move point slightly inward
    inward_x = boundary_x + (inward_dx / inward_length) * (BALL_RADIUS * 1.1)
    inward_y = boundary_y + (inward_dy / inward_length) * (BALL_RADIUS * 1.1)
    
    return (inward_x, inward_y)

def main():
    # Get number of sides and balls from user
    num_sides = get_num_sides()
    num_balls = get_num_balls()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Bouncing Balls in Spinning {'Circle' if num_sides < 3 else f'{num_sides}-gon'}")
    clock = pygame.time.Clock()

    # Create balls
    balls = []
    for i in range(num_balls):
        angle = 2 * math.pi * i / num_balls
        velocity = [BALL_SPEED * math.cos(angle), BALL_SPEED * math.sin(angle)]
        ball = Ball(SHAPE_CENTER[0], SHAPE_CENTER[1], BALL_RADIUS, velocity)
        ball.color = RED  # Set initial color
        balls.append(ball)
    
    rotation = 0
    is_spinning = True  # Initially spinning
    shape_center = list(SHAPE_CENTER)  # Make center mutable
    shape_offset = [0, 0]  # Track how far the shape has moved from center
    shape_color = BLUE  # Default shape color
    
    # Initialize shape velocity with random direction
    initial_angle = random.uniform(0, 2 * math.pi)
    shape_velocity = [SHAPE_SPEED * math.cos(initial_angle), SHAPE_SPEED * math.sin(initial_angle)]

    def reset():
        nonlocal rotation, is_spinning, shape_center, shape_offset, shape_velocity, shape_color
        # Reset shape position
        shape_center = list(SHAPE_CENTER)
        shape_offset = [0, 0]
        # Reset rotation
        rotation = 0
        # Reset spinning state
        is_spinning = True
        # Reset shape velocity with new random direction
        initial_angle = random.uniform(0, 2 * math.pi)
        shape_velocity = [SHAPE_SPEED * math.cos(initial_angle), SHAPE_SPEED * math.sin(initial_angle)]
        # Reset shape color
        shape_color = BLUE
        # Reset balls
        for i, ball in enumerate(balls):
            angle = 2 * math.pi * i / num_balls
            velocity = [BALL_SPEED * math.cos(angle), BALL_SPEED * math.sin(angle)]
            ball.x = SHAPE_CENTER[0]
            ball.y = SHAPE_CENTER[1]
            ball.velocity = velocity
            ball.color = RED

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_spinning = not is_spinning  # Toggle spinning state
                elif event.key == pygame.K_r:
                    reset()  # Reset to initial state

        # Handle continuous key presses for velocity adjustment
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            shape_velocity[0] -= MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            shape_velocity[0] += MOVE_SPEED
        if keys[pygame.K_UP]:
            shape_velocity[1] -= MOVE_SPEED
        if keys[pygame.K_DOWN]:
            shape_velocity[1] += MOVE_SPEED

        # Update shape position based on velocity
        shape_center[0] += shape_velocity[0]
        shape_center[1] += shape_velocity[1]

        # Bounce shape off screen edges
        if shape_center[0] - SHAPE_RADIUS < 0:
            shape_center[0] = SHAPE_RADIUS
            shape_velocity[0] = abs(shape_velocity[0])
            shape_color = random.choice(COLLISION_COLORS)  # Change to random color on wall collision
        elif shape_center[0] + SHAPE_RADIUS > WIDTH:
            shape_center[0] = WIDTH - SHAPE_RADIUS
            shape_velocity[0] = -abs(shape_velocity[0])
            shape_color = random.choice(COLLISION_COLORS)
        if shape_center[1] - SHAPE_RADIUS < 0:
            shape_center[1] = SHAPE_RADIUS
            shape_velocity[1] = abs(shape_velocity[1])
            shape_color = random.choice(COLLISION_COLORS)
        elif shape_center[1] + SHAPE_RADIUS > HEIGHT:
            shape_center[1] = HEIGHT - SHAPE_RADIUS
            shape_velocity[1] = -abs(shape_velocity[1])
            shape_color = random.choice(COLLISION_COLORS)

        # Update rotation if spinning
        if is_spinning:
            rotation += ROTATION_SPEED
        
        # Get shape vertices
        vertices = get_shape_vertices(shape_center, SHAPE_RADIUS, rotation, num_sides)
        
        # Update all balls
        for ball in balls:
            # Store previous position
            prev_x, prev_y = ball.x, ball.y
            
            # Update ball position
            ball.update()
            # Move ball with shape
            ball.x += shape_velocity[0]
            ball.y += shape_velocity[1]

            # Check if ball is outside shape (with buffer zone)
            if not is_point_in_shape((ball.x, ball.y), vertices):
                # Check if ball is significantly outside (more than 1.15x radius)
                distance_from_center = math.sqrt((ball.x - shape_center[0])**2 + (ball.y - shape_center[1])**2)
                if distance_from_center > SHAPE_RADIUS * 1.15:  # Tightened from 1.25 to 1.15
                    # Calculate vector from center to ball
                    dx = ball.x - shape_center[0]
                    dy = ball.y - shape_center[1]
                    distance = math.sqrt(dx*dx + dy*dy)
                    
                    if distance > 0:
                        # Move ball inward by 16x ball radius (increased from 8x)
                        ball.x = shape_center[0] + (dx / distance) * (SHAPE_RADIUS - BALL_RADIUS * 16)
                        ball.y = shape_center[1] + (dy / distance) * (SHAPE_RADIUS - BALL_RADIUS * 16)
                    
                    # Reverse velocity
                    ball.velocity = [-v for v in ball.velocity]
                    
                    # Normalize velocity to maintain constant speed
                    velocity_magnitude = BALL_SPEED
                    current_magnitude = math.sqrt(ball.velocity[0]**2 + ball.velocity[1]**2)
                    if current_magnitude > 0:
                        ball.velocity = [v * (velocity_magnitude / current_magnitude) for v in ball.velocity]
                continue

            # Check for collisions with shape edges and vertices
            collision_occurred = False
            for i in range(len(vertices)):
                p1 = vertices[i]
                p2 = vertices[(i + 1) % len(vertices)]
                
                # Check for edge collision
                intersection_point, normal = line_intersection(
                    p1, p2, (ball.x, ball.y), ball.radius
                )
                
                # Check for vertex collision
                vertex_point, vertex_normal = vertex_collision(
                    p1, (ball.x, ball.y), ball.radius
                )
                
                if (intersection_point is not None or vertex_point is not None) and not collision_occurred:
                    collision_occurred = True
                    # Move ball back to previous position
                    ball.x, ball.y = prev_x, prev_y
                    
                    # Use the appropriate normal for reflection
                    if intersection_point is not None:
                        reflection_normal = normal
                    else:
                        reflection_normal = vertex_normal
                    
                    # Calculate new velocity with reflection
                    ball.velocity = reflect_velocity(ball.velocity, reflection_normal)
                    
                    # Move ball in new direction
                    ball.update()
                    # Move ball with shape
                    ball.x += shape_velocity[0]
                    ball.y += shape_velocity[1]
                    
                    # Change ball color on collision
                    ball.color = random.choice(COLLISION_COLORS)
                    
                    # Play collision sound at full volume
                    collision_sound.set_volume(1.0)
                    collision_sound.play()
                    
                    # Ensure velocity magnitude remains constant
                    velocity_magnitude = BALL_SPEED
                    current_magnitude = math.sqrt(ball.velocity[0]**2 + ball.velocity[1]**2)
                    if current_magnitude > 0:
                        ball.velocity = [v * (velocity_magnitude / current_magnitude) for v in ball.velocity]

        # Check for ball-ball collisions
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                if check_ball_collision(balls[i], balls[j]):
                    # Change colors of both balls on collision
                    balls[i].color = random.choice(COLLISION_COLORS)
                    balls[j].color = random.choice(COLLISION_COLORS)
                    # Play collision sound at 25% volume
                    collision_sound.set_volume(0.25)
                    collision_sound.play()

        # Draw everything
        screen.fill(BLACK)
        
        # Draw shape
        if num_sides < 3:
            pygame.draw.circle(screen, shape_color, (int(shape_center[0]), int(shape_center[1])), SHAPE_RADIUS, 2)
        else:
            pygame.draw.polygon(screen, shape_color, vertices, 2)
        
        # Draw balls
        for ball in balls:
            ball.draw(screen)
        
        # Update window title to show controls
        pygame.display.set_caption(
            f"Bouncing Balls in {'Spinning' if is_spinning else 'Static'} {'Circle' if num_sides < 3 else f'{num_sides}-gon'} (SPACE: toggle spin, ARROWS: adjust velocity, R: reset)"
        )
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main() 
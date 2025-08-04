import math
import random
import sys

import pygame

# Initialize pygame and its sound system
pygame.init()
pygame.mixer.init()

# Load default sound effects
DEFAULT_COLLISION_SOUND = pygame.mixer.Sound("gunshot.mp3")
CANNON_COLLISION_SOUND = pygame.mixer.Sound("cannon_sound.mp3")
NUKE_FALLING_SOUND = pygame.mixer.Sound("nuke_falling.mp3")
NUKE_EXPLOSION_SOUND = pygame.mixer.Sound("nuke_explosion.mp3")

# Game messages
GAME_TITLE = "EURO UNESSAY"
GAME_SUBTITLE = "CHOOSE A LEVEL TO GET STARTED"
LEVEL_1_WIN_MESSAGE = "COUNTRY {winner} WINS THE WAR!"
LEVEL_2_WIN_MESSAGE = "COUNTRY {winner} WINS THE WAR!"
LEVEL_3_WIN_MESSAGE = "COUNTRY {winner} WINS THE WAR!"
LEVEL_4_WIN_MESSAGE = "BOTH COUNTRIES LOSE DUE TO MUTUALLY ASSURED DESTRUCTION"
LEVEL_1_RESTART_MESSAGE = "PRESS R TO PLAY AGAIN OR PRESS SPACE TO EXIT"
LEVEL_2_RESTART_MESSAGE = "PRESS R TO PLAY AGAIN OR PRESS SPACE TO EXIT"
LEVEL_3_RESTART_MESSAGE = "PRESS R TO PLAY AGAIN OR PRESS SPACE TO EXIT"
LEVEL_4_RESTART_MESSAGE = "PRESS R TO WATCH AGAIN OR PRESS SPACE TO EXIT"
LEVEL_1_SPACE_MESSAGE = """Firearms were introduced into Europe from Asia in the 1380s,
marking the transition from purely melee combat to slightly
ranged combat---only 'slightly' because guns were still very
inaccurate, meaning one had to be close to their target to shoot them.
In this game, the curved paddles represent soldiers, while the ball
represents bullets that the soldiers are shooting. When a bullet makes
contact with a soldier, the bullet will bounce off and the soldier will
be killed. If the bullet makes contact with either the left or right edge
of the screen, the other side will win 'the battle' and the game will
reset. The first country to win three battles wins the war.
[PRESS SPACE TO BEGIN]
"""
LEVEL_2_SPACE_MESSAGE = """Cannons were first introduced into Europe in 1572 in Venice.
However, they were only popularized in their mobile variant by Swedish 
King Gustavus Adolphus in the Swedish Phase of the Thirty Years' War
beginning in 1630. Cannons changed European warfare because they 
could take out dozens of soldiers at once and also destroy the 
more elaborate fortifications that were being developed over time.
A second, larger ball has now been added into play to represent a 
cannonball---this ball moves slower than bullets, but can take out
two soldiers at a time. Also during this time, standing militaries
began expanding and becoming more organized. Thus, each country now
 has more total soldiers.
[PRESS SPACE TO BEGIN]
"""
LEVEL_3_SPACE_MESSAGE = """Machine guns were invented by Hiram S. Maxim in 1884, and were
first put to heavy use during WWI (which was one of the main reasons
trench warfare was so prevalent). Machine guns could fire dozens of
rounds per second, causing absolutely devastating losses to the other
side. To represent the machine gun, there will now be 2 bullets in
play instead of 1, and they will now move slightly faster.
Additionally, tanks were invented by British inventors Walter Gordon
Wilson and William Tritton to solve stalemates in trench warfare.
Tanks shot larger, more powerful bullets than normal firearms and
replaced the cannon. The larger ball now represents a bullet shot
from a tank rather than a cannonball – as such, it now moves faster.
Finally, army sizes greatly increased during WWI due to mass
conscription and militarism, so both sides now have more soldiers.
[PRESS SPACE TO BEGIN]
"""
LEVEL_4_SPACE_MESSAGE = """The atomic bomb was developed during WWII in the US during the
Manhattan Project, and was used at Hiroshima and Nagasaki in Japan
to end the war's Pacific front. The first atomic bombs were already
the most destructive weapons ever created, but since then, they have
become more than 1000x more destructive, and thousands exist across
the world, mostly split between the US and Russia as a result of the
arms race in the Cold War. Play the simulation to see what modern
atomic bombs would do to a population.
[PRESS SPACE TO BEGIN].
"""

# Game constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
PADDLE_WIDTH = 6  # Decreased from 10
PADDLE_HEIGHT = 60
PADDLE_SPEED = 10


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)

        # Draw text
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False


class GameState:
    START_SCREEN = 0
    GAME = 1
    PAUSED = 2
    WIN = 3
    BATTLE_WIN = 4
    LEVEL_4_ANIMATION = 5  # New state for level 4 animation


class Ball:
    def __init__(self, x, y, radius, color, speed, collision_sound=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.collision_cooldown = 0
        self.collision_sound = (
            collision_sound if collision_sound else DEFAULT_COLLISION_SOUND
        )
        self.reset()

    def reset(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.collision_cooldown = 0

        # Convert degrees to radians and choose between two ranges
        # -45 to 45 degrees or -135 to 135 degrees
        if random.random() < 0.5:
            # First range: -45 to 45 degrees
            angle = random.uniform(-math.pi / 4, math.pi / 4)
        else:
            # Second range: -135 to 135 degrees
            angle = random.uniform(3 * math.pi / 4, 5 * math.pi / 4)

        self.velocity_x = self.speed * math.cos(angle)
        self.velocity_y = self.speed * math.sin(angle)

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        # Decrease collision cooldown if it's active
        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1

    def check_paddle_collision(self, paddle, level=None):
        # Skip collision check if cooldown is active
        if self.collision_cooldown > 0:
            return False

        # Calculate distance between ball center and curve center
        dx = self.x - paddle.center_x
        dy = self.y - paddle.center_y
        distance = math.sqrt(dx * dx + dy * dy)

        # Use a constant hitbox buffer, but larger for level 3
        CONSTANT_HITBOX_BUFFER = (
            7.5 if level == 3 else 5
        )  # 50% larger buffer for level 3
        min_distance = paddle.curve_radius
        max_distance = paddle.curve_radius + paddle.width + CONSTANT_HITBOX_BUFFER

        if min_distance <= distance <= max_distance:
            # Calculate the angle of the ball relative to the curve center
            angle = math.atan2(dy, dx)
            if angle < 0:
                angle += 2 * math.pi

            # Check if the ball is within the visible angle range
            if paddle.is_left:
                # For left paddle, check if angle is in [2π-visible_angle_range, 2π] or [0, visible_angle_range]
                if not (
                    angle >= 2 * math.pi - paddle.visible_angle_range
                    or angle <= paddle.visible_angle_range
                ):
                    return False
            else:
                # For right paddle, check if angle is in [π-visible_angle_range, π+visible_angle_range]
                if not (
                    math.pi - paddle.visible_angle_range
                    <= angle
                    <= math.pi + paddle.visible_angle_range
                ):
                    return False

            # Calculate the normal vector (from curve center to ball center)
            normal_x = dx / distance
            normal_y = dy / distance

            # For left paddle, normal should point left
            # For right paddle, normal should point right
            if (paddle.is_left and normal_x > 0) or (
                not paddle.is_left and normal_x < 0
            ):
                # Play collision sound
                self.collision_sound.play()

                # Reflect velocity across normal vector
                dot_product = self.velocity_x * normal_x + self.velocity_y * normal_y
                self.velocity_x = self.velocity_x - 2 * dot_product * normal_x
                self.velocity_y = self.velocity_y - 2 * dot_product * normal_y

                # Normalize and scale to maintain constant speed
                speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
                self.velocity_x = (self.velocity_x / speed) * self.speed
                self.velocity_y = (self.velocity_y / speed) * self.speed

                # Set collision cooldown to 10 frames
                self.collision_cooldown = 10
                return True

        return False

    def check_wall_collision(self):
        if self.y - self.radius <= 0 or self.y + self.radius >= WINDOW_HEIGHT:
            self.velocity_y *= -1
            self.y = max(self.radius, min(WINDOW_HEIGHT - self.radius, self.y))

        # Remove automatic reset, let the win screen handle it
        if self.x - self.radius <= 0 or self.x + self.radius >= WINDOW_WIDTH:
            return True
        return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


class Paddle:
    def __init__(self, x, y, width, height, color, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.curve_radius = height * 2
        self.is_left = x < WINDOW_WIDTH // 2
        self.visible_angle_range = math.pi / 10
        self.start_x = x  # Store initial x position
        self.start_y = y  # Store initial y position

        # Calculate the center of the circle (closer to screen)
        if self.is_left:
            self.center_x = x - self.curve_radius * 0.5
        else:
            self.center_x = x + self.curve_radius * 0.5
        self.center_y = y + height / 2

    def reset(self):
        """Reset paddle to its starting position"""
        self.y = self.start_y
        self.center_y = self.y + self.height / 2

    def is_point_in_visible_range(self, x, y):
        """Check if a point is within the visible angle range of the paddle"""
        # Calculate angle of point relative to center
        dx = x - self.center_x
        dy = y - self.center_y
        angle = math.atan2(dy, dx)

        # Normalize angle to [0, 2π]
        if angle < 0:
            angle += 2 * math.pi

        if self.is_left:
            # For left paddle, check if angle is in [2π-visible_angle_range, 2π] or [0, visible_angle_range]
            return (
                angle >= 2 * math.pi - self.visible_angle_range
                or angle <= self.visible_angle_range
            )
        else:
            # For right paddle, check if angle is in [π-visible_angle_range, π+visible_angle_range]
            return (
                math.pi - self.visible_angle_range
                <= angle
                <= math.pi + self.visible_angle_range
            )

    def move(self, up=True):
        if up:
            self.y -= self.speed
        else:
            self.y += self.speed

        if self.y < 0:
            self.y = 0
        if self.y + self.height > WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - self.height

        # Update center_y when paddle moves
        self.center_y = self.y + self.height / 2

    def draw(self, screen):
        # Calculate the visible portion of the curve
        if self.is_left:
            # For left paddle, show rightmost portion of circle
            start_angle = (
                -math.pi / 10
            )  # Reduced angle range to show ~10% of circumference
            end_angle = math.pi / 10
            arc_rect = (
                self.center_x - self.curve_radius,
                self.center_y - self.curve_radius,
                self.curve_radius * 2,
                self.curve_radius * 2,
            )
        else:
            # For right paddle, show leftmost portion of circle
            start_angle = math.pi - math.pi / 10
            end_angle = math.pi + math.pi / 10
            arc_rect = (
                self.center_x - self.curve_radius,
                self.center_y - self.curve_radius,
                self.curve_radius * 2,
                self.curve_radius * 2,
            )

        # Draw the curved surface
        pygame.draw.arc(
            screen, self.color, arc_rect, start_angle, end_angle, int(self.width)
        )

    def get_curve_point(self, y):
        """Calculate the x position of the curve at a given y position"""
        # Calculate how far y is from the center, normalized to [-1, 1]
        y_offset = (y - self.center_y) / self.curve_radius
        # Clamp to valid range
        y_offset = max(-1, min(1, y_offset))
        # Calculate x offset using circle equation: x = sqrt(1 - y^2)
        x_offset = math.sqrt(1 - y_offset * y_offset)

        if self.is_left:
            return self.center_x + (x_offset * self.curve_radius)
        else:
            return self.center_x - (x_offset * self.curve_radius)

    def get_normal_vector(self, y):
        """Calculate the normal vector at a given y position on the curve"""
        # For a circle, the normal vector points from the center to the point
        y_offset = (y - self.center_y) / self.curve_radius
        y_offset = max(-1, min(1, y_offset))

        # Calculate the normal vector (pointing outward from the curve)
        if self.is_left:
            return (-math.sqrt(1 - y_offset * y_offset), y_offset)
        else:
            return (math.sqrt(1 - y_offset * y_offset), y_offset)


class BattleMessage:
    def __init__(self):
        self.text = ""
        self.alpha = 255
        self.timer = 0
        self.duration = 120  # 2 seconds at 60 FPS

    def show(self, winner):
        self.text = f"COUNTRY {winner} WON THE BATTLE"
        self.alpha = 255
        self.timer = self.duration

    def update(self):
        if self.timer > 0:
            self.timer -= 1
            self.alpha = int((self.timer / self.duration) * 255)
            return True
        return False

    def draw(self, screen):
        if self.timer > 0:
            font = pygame.font.Font(None, 48)
            text = font.render(self.text, True, (255, 255, 255))
            text.set_alpha(self.alpha)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 50))
            screen.blit(text, text_rect)


class PaddleChain:
    def __init__(self, is_left, num_paddles=8):
        self.is_left = is_left
        self.paddles = []
        self.num_paddles = num_paddles
        self.paddle_height = PADDLE_HEIGHT
        self.paddle_width = PADDLE_WIDTH
        self.paddle_spacing = 5  # Added spacing between paddles
        self.total_height = (self.paddle_height * num_paddles) + (
            self.paddle_spacing * (num_paddles - 1)
        )
        self.start_y = (WINDOW_HEIGHT - self.total_height) // 2
        self.removed_paddles = set()  # Track removed paddles by their index

        # Create the chain of paddles
        for i in range(num_paddles):
            x = 50 if is_left else WINDOW_WIDTH - 50 - self.paddle_width
            y = self.start_y + (i * (self.paddle_height + self.paddle_spacing))
            self.paddles.append(
                Paddle(
                    x,
                    y,
                    self.paddle_width,
                    self.paddle_height,
                    (255, 255, 255),
                    PADDLE_SPEED,
                )
            )

    @classmethod
    def create_for_level(cls, is_left, level):
        if level in [3, 4]:  # Both level 3 and 4 use the same paddle configuration
            # For level 3/4: smaller paddles, more of them, adjusted centers
            num_paddles = 24  # Slightly reduced from 26 for better gameplay balance
            paddle_height = PADDLE_HEIGHT * 0.5  # 50% of normal height
            paddle_width = PADDLE_WIDTH * 0.5  # 50% of normal width
            paddle_spacing = 0  # No spacing between paddles for a continuous wall

            # Create chain with base configuration
            chain = cls(is_left, num_paddles)

            # Update chain properties
            chain.paddle_height = paddle_height
            chain.paddle_width = paddle_width
            chain.paddle_spacing = paddle_spacing
            chain.total_height = (paddle_height * num_paddles) + (
                paddle_spacing * (num_paddles - 1)
            )
            chain.start_y = (WINDOW_HEIGHT - chain.total_height) // 2

            # Adjust paddle properties
            for i, paddle in enumerate(chain.paddles):
                paddle.width = paddle_width
                paddle.height = paddle_height
                # Move center much closer to screen edge to maintain visible position
                if is_left:
                    paddle.center_x = paddle.x - paddle.curve_radius * 0.1  # 90% closer
                else:
                    paddle.center_x = paddle.x + paddle.curve_radius * 0.1  # 90% closer
                paddle.curve_radius = paddle_height * 1.5  # Reduced curve radius
                paddle.center_y = paddle.y + paddle_height / 2

                # Update paddle position
                paddle.y = chain.start_y + (i * (paddle_height + paddle_spacing))
                paddle.center_y = paddle.y + paddle_height / 2

            return chain
        elif level == 2:
            # For level 2: smaller paddles, more of them
            num_paddles = 15
            paddle_height = PADDLE_HEIGHT * 0.7  # 70% of normal height
            paddle_width = PADDLE_WIDTH * 0.7  # 70% of normal width
            paddle_spacing = 2  # Reduced spacing to fit more paddles

            # Create chain with base configuration
            chain = cls(is_left, num_paddles)

            # Update chain properties
            chain.paddle_height = paddle_height
            chain.paddle_width = paddle_width
            chain.paddle_spacing = paddle_spacing
            chain.total_height = (paddle_height * num_paddles) + (
                paddle_spacing * (num_paddles - 1)
            )
            chain.start_y = (WINDOW_HEIGHT - chain.total_height) // 2

            # Adjust paddle properties
            for i, paddle in enumerate(chain.paddles):
                paddle.width = paddle_width
                paddle.height = paddle_height
                # Move center closer to screen
                if is_left:
                    paddle.center_x = paddle.x - paddle.curve_radius * 0.3  # 30% closer
                else:
                    paddle.center_x = paddle.x + paddle.curve_radius * 0.3  # 30% closer
                paddle.curve_radius = (
                    paddle_height * 2
                )  # Adjust curve radius for new height
                paddle.center_y = paddle.y + paddle_height / 2

                # Update paddle position
                paddle.y = chain.start_y + (i * (paddle_height + paddle_spacing))
                paddle.center_y = paddle.y + paddle_height / 2

            return chain
        else:
            # Normal configuration for level 1
            return cls(is_left)

    def move(self, up=True):
        # Check if any non-removed paddle would hit the boundary
        if up:
            for i, paddle in enumerate(self.paddles):
                if i not in self.removed_paddles and paddle.y <= 0:
                    return
        else:
            for i, paddle in enumerate(self.paddles):
                if (
                    i not in self.removed_paddles
                    and paddle.y + paddle.height >= WINDOW_HEIGHT
                ):
                    return

        # Move all paddles together
        for paddle in self.paddles:
            paddle.move(up)

    def reset(self):
        # Reset all paddles to their starting positions and restore removed paddles
        self.removed_paddles.clear()
        for i, paddle in enumerate(self.paddles):
            paddle.y = self.start_y + (i * (self.paddle_height + self.paddle_spacing))
            paddle.center_y = paddle.y + self.paddle_height / 2

    def draw(self, screen):
        for i, paddle in enumerate(self.paddles):
            if i not in self.removed_paddles:
                paddle.draw(screen)

    def check_collision(self, ball, level=None):
        for i, paddle in enumerate(self.paddles):
            if i not in self.removed_paddles and ball.check_paddle_collision(
                paddle, level
            ):
                self.removed_paddles.add(i)  # Remove the paddle after collision
                return True
        return False

    def get_visible_paddle_count(self):
        return self.num_paddles - len(self.removed_paddles)

    def get_adjacent_paddles(self, paddle_index):
        """Returns the indices of adjacent paddles in the original chain"""
        adjacent = []
        if paddle_index > 0 and (paddle_index - 1) not in self.removed_paddles:
            adjacent.append(paddle_index - 1)
        if (
            paddle_index < self.num_paddles - 1
            and (paddle_index + 1) not in self.removed_paddles
        ):
            adjacent.append(paddle_index + 1)
        return adjacent

    def get_nearest_adjacent(self, paddle_index, ball_x, ball_y):
        """Returns the index of the nearest adjacent paddle to the ball"""
        adjacent = self.get_adjacent_paddles(paddle_index)
        if not adjacent:
            return None

        min_distance = float("inf")
        nearest_index = None

        for adj_index in adjacent:
            paddle = self.paddles[adj_index]
            # Calculate distance from ball to paddle center
            dx = ball_x - paddle.center_x
            dy = ball_y - paddle.center_y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < min_distance:
                min_distance = distance
                nearest_index = adj_index

        return nearest_index


class CannonBall(Ball):
    def __init__(self, x, y, color, collision_sound=None):
        # Double radius, 30% faster than original cannon ball speed
        super().__init__(
            x,
            y,
            radius=12,
            color=color,
            speed=6.5,
            collision_sound=CANNON_COLLISION_SOUND,
        )  # Original 5 * 1.3

    def check_paddle_collision(self, paddle_chain, level=None):
        """Override the collision check for cannon ball to handle adjacent paddle destruction"""
        for i, paddle in enumerate(paddle_chain.paddles):
            if i not in paddle_chain.removed_paddles:
                # Check collision with this paddle
                if super().check_paddle_collision(paddle, level):
                    # Remove the hit paddle
                    paddle_chain.removed_paddles.add(i)

                    # Get adjacent paddles
                    adjacent = paddle_chain.get_adjacent_paddles(i)

                    if len(adjacent) == 1:
                        # If only one adjacent paddle, remove it
                        paddle_chain.removed_paddles.add(adjacent[0])
                    elif len(adjacent) == 2:
                        # If two adjacent paddles, remove the nearest one
                        nearest = paddle_chain.get_nearest_adjacent(i, self.x, self.y)
                        if nearest is not None:
                            paddle_chain.removed_paddles.add(nearest)

                    return True
        return False


class ExplosionParticle:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = (255, 255, 255)
        self.speed = speed
        self.velocity_x = speed * math.cos(angle)
        self.velocity_y = speed * math.sin(angle)

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def is_off_screen(self):
        return (
            self.x < -self.radius
            or self.x > WINDOW_WIDTH + self.radius
            or self.y < -self.radius
            or self.y > WINDOW_HEIGHT + self.radius
        )

    def check_paddle_collision(self, paddle, level=None):
        # Calculate distance between ball center and curve center
        dx = self.x - paddle.center_x
        dy = self.y - paddle.center_y
        distance = math.sqrt(dx * dx + dy * dy)

        # Use a constant hitbox buffer, but larger for level 3
        CONSTANT_HITBOX_BUFFER = 7.5 if level == 3 else 5
        min_distance = paddle.curve_radius
        max_distance = paddle.curve_radius + paddle.width + CONSTANT_HITBOX_BUFFER

        if min_distance <= distance <= max_distance:
            # Calculate the angle of the ball relative to the curve center
            angle = math.atan2(dy, dx)
            if angle < 0:
                angle += 2 * math.pi

            # Check if the ball is within the visible angle range
            if paddle.is_left:
                # For left paddle, check if angle is in [2π-visible_angle_range, 2π] or [0, visible_angle_range]
                if not (
                    angle >= 2 * math.pi - paddle.visible_angle_range
                    or angle <= paddle.visible_angle_range
                ):
                    return False
            else:
                # For right paddle, check if angle is in [π-visible_angle_range, π+visible_angle_range]
                if not (
                    math.pi - paddle.visible_angle_range
                    <= angle
                    <= math.pi + paddle.visible_angle_range
                ):
                    return False

            # Calculate the normal vector (from curve center to ball center)
            normal_x = dx / distance
            normal_y = dy / distance

            # For left paddle, normal should point left
            # For right paddle, normal should point right
            if (paddle.is_left and normal_x > 0) or (
                not paddle.is_left and normal_x < 0
            ):
                return True

        return False


class AnimatedSymbol:
    def __init__(self, x, y, circle_radius):
        self.x = x
        self.y = y
        self.base_circle_radius = circle_radius
        self.circle_radius = circle_radius * 2
        self.plus_radius = self.circle_radius * 1.6
        self.rotation = 45
        self.trapezoid_color = (0, 255, 0)
        self.line_thickness = 24
        self.taper_ratio = 0.4
        self.colors = [(255, 255, 255), (255, 255, 0), (255, 165, 0), (255, 0, 0)]
        self.font = pygame.font.Font(None, int(self.circle_radius * 0.5))
        self.animation_time = 2.5
        self.animation_start_time = None
        self.is_animating = False
        self.explosion_particles = []
        self.has_exploded = False
        self.explosion_start_time = None
        self.animation_complete = False

    def start_animation(self):
        print("Starting animation")  # Debug print
        self.animation_start_time = pygame.time.get_ticks()
        self.is_animating = True
        self.has_exploded = False
        self.explosion_particles = []
        self.explosion_start_time = None
        self.animation_complete = False
        self.circle_radius = (
            self.base_circle_radius * 4.5
        )  # Start at 1.5x larger than before
        self.plus_radius = self.circle_radius * 1.6
        self.font = pygame.font.Font(None, int(self.circle_radius * 0.5))
        NUKE_FALLING_SOUND.play()

    def create_explosion(self):
        if self.has_exploded:
            return

        print("Creating explosion")  # Debug print
        self.has_exploded = True
        self.explosion_start_time = pygame.time.get_ticks()
        num_particles = 160
        speed = 7.2

        NUKE_EXPLOSION_SOUND.play()

        for i in range(num_particles):
            angle = (2 * math.pi * i) / num_particles
            self.explosion_particles.append(
                ExplosionParticle(self.x, self.y, angle, speed)
            )

    def update(
        self, left_paddle_chain=None, right_paddle_chain=None, current_level=None
    ):
        if self.animation_complete:
            return True

        if self.is_animating:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.animation_start_time) / 1000.0

            if elapsed_time >= self.animation_time:
                print(f"Falling animation complete after {elapsed_time:.2f} seconds")
                self.create_explosion()
                self.is_animating = False
            else:
                progress = elapsed_time / self.animation_time
                # Use an even gentler ease-out function: 1 - (1-t)^1.3
                # This will make the shrinking decelerate more gradually
                ease_out_progress = 1 - (1 - progress) ** 1.3
                # Start at 4.5 (1.5x larger than before) and end at 0.5
                current_scale = 4.5 - (ease_out_progress * 4.0)
                self.circle_radius = self.base_circle_radius * current_scale
                self.plus_radius = self.circle_radius * 1.6
                self.font = pygame.font.Font(None, int(self.circle_radius * 0.5))

        if self.explosion_start_time:
            current_time = pygame.time.get_ticks()
            elapsed_explosion_time = (current_time - self.explosion_start_time) / 1000.0
            print(f"Explosion time: {elapsed_explosion_time:.2f} seconds")

            if elapsed_explosion_time >= 3.0:  # Changed from 5.0 to 3.0 seconds
                print("3 seconds elapsed, transitioning to win screen")
                self.animation_complete = True
                return True

        if self.explosion_particles:
            # Update and check collisions for each particle
            for particle in self.explosion_particles:
                particle.update()

                if left_paddle_chain:
                    for i, paddle in enumerate(left_paddle_chain.paddles):
                        if (
                            i not in left_paddle_chain.removed_paddles
                            and particle.check_paddle_collision(paddle, current_level)
                        ):
                            left_paddle_chain.removed_paddles.add(i)

                if right_paddle_chain:
                    for i, paddle in enumerate(right_paddle_chain.paddles):
                        if (
                            i not in right_paddle_chain.removed_paddles
                            and particle.check_paddle_collision(paddle, current_level)
                        ):
                            right_paddle_chain.removed_paddles.add(i)

            # Remove particles that are off screen
            self.explosion_particles = [
                p for p in self.explosion_particles if not p.is_off_screen()
            ]

        return False

    def draw(self, screen):
        if not self.has_exploded:
            # Draw the nuke symbol
            plus_size = int(self.plus_radius * 2)
            plus_surface = pygame.Surface((plus_size, plus_size), pygame.SRCALPHA)

            def create_tapered_rect(start_x, start_y, length, direction):
                end_thickness = self.line_thickness * self.taper_ratio
                if direction == "up":
                    points = [
                        (start_x - self.line_thickness / 2, start_y),
                        (start_x + self.line_thickness / 2, start_y),
                        (start_x + end_thickness / 2, start_y - length),
                        (start_x - end_thickness / 2, start_y - length),
                    ]
                elif direction == "down":
                    points = [
                        (start_x - self.line_thickness / 2, start_y),
                        (start_x + self.line_thickness / 2, start_y),
                        (start_x + end_thickness / 2, start_y + length),
                        (start_x - end_thickness / 2, start_y + length),
                    ]
                elif direction == "left":
                    points = [
                        (start_x, start_y - self.line_thickness / 2),
                        (start_x - length, start_y - end_thickness / 2),
                        (start_x - length, start_y + end_thickness / 2),
                        (start_x, start_y + self.line_thickness / 2),
                    ]
                else:  # right
                    points = [
                        (start_x, start_y - self.line_thickness / 2),
                        (start_x + length, start_y - end_thickness / 2),
                        (start_x + length, start_y + end_thickness / 2),
                        (start_x, start_y + self.line_thickness / 2),
                    ]
                return points

            center_x = plus_size // 2
            center_y = plus_size // 2
            arm_length = plus_size // 2

            directions = ["up", "down", "left", "right"]
            for direction in directions:
                points = create_tapered_rect(center_x, center_y, arm_length, direction)
                pygame.draw.polygon(plus_surface, self.trapezoid_color, points)

            rotated_plus = pygame.transform.rotate(plus_surface, self.rotation)
            rotated_rect = rotated_plus.get_rect(center=(self.x, self.y))
            screen.blit(rotated_plus, rotated_rect)

            pygame.draw.circle(
                screen, self.colors[0], (self.x, self.y), self.circle_radius
            )

            current_radius = self.circle_radius
            for color in self.colors[1:]:
                current_radius = int(current_radius * 0.5)
                pygame.draw.circle(screen, color, (self.x, self.y), current_radius)

            text = "NUKE"
            start_angle = math.pi * 0.7
            end_angle = math.pi * 0.3
            angle_step = (start_angle - end_angle) / (len(text) - 1)

            for angle_offset in [0, math.pi]:
                for i, char in enumerate(text):
                    angle = start_angle - (i * angle_step) + angle_offset
                    char_x = self.x + math.cos(angle) * (self.circle_radius * 0.75)
                    char_y = self.y - math.sin(angle) * (self.circle_radius * 0.75)
                    char_surface = self.font.render(char, True, (0, 0, 0))
                    char_surface = pygame.transform.rotate(
                        char_surface, math.degrees(angle - math.pi / 2)
                    )
                    char_rect = char_surface.get_rect(center=(char_x, char_y))
                    screen.blit(char_surface, char_rect)

        # Draw explosion particles
        for particle in self.explosion_particles:
            particle.draw(screen)


pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong Game")

# Create buttons for level selection
button_width = 120
button_height = 50
button_spacing = 20
total_buttons_width = (button_width * 4) + (button_spacing * 3)
start_x = (WINDOW_WIDTH - total_buttons_width) // 2
buttons = []
# Define button colors for each level
button_colors = [
    ((0, 150, 0), (0, 200, 0)),  # Level 1: Green
    ((200, 200, 0), (255, 255, 0)),  # Level 2: Yellow
    ((255, 140, 0), (255, 165, 0)),  # Level 3: Orange
    ((200, 0, 0), (255, 0, 0)),  # Level 4: Red
]
for i in range(4):
    x = start_x + (button_width + button_spacing) * i
    y = WINDOW_HEIGHT // 2 + 50
    buttons.append(
        Button(
            x,
            y,
            button_width,
            button_height,
            f"LVL {i+1}",
            button_colors[i][0],
            button_colors[i][1],
            (255, 255, 255),
        )
    )

# Initialize game variables
battle_message = BattleMessage()
country1_battles = 0
country2_battles = 0
current_level = 1
ball = None  # Will be initialized based on level
left_paddle_chain = None  # Will be initialized based on level
right_paddle_chain = None  # Will be initialized based on level
show_nuke = False  # Flag to control nuke visibility in level 4


def create_ball_for_level(level):
    if level == 3:
        return [
            CannonBall(
                x=WINDOW_WIDTH // 2, y=WINDOW_HEIGHT // 2, color=(255, 255, 255)
            ),
            Ball(
                x=WINDOW_WIDTH // 2,
                y=WINDOW_HEIGHT // 2,
                radius=6,
                color=(255, 255, 255),
                speed=10.5,  # 5% faster than normal (10 * 1.05)
            ),
            Ball(
                x=WINDOW_WIDTH // 2,
                y=WINDOW_HEIGHT // 2,
                radius=6,
                color=(255, 255, 255),
                speed=10.5,  # 5% faster than normal
            ),
        ]
    elif level == 2:
        return [
            CannonBall(
                x=WINDOW_WIDTH // 2, y=WINDOW_HEIGHT // 2, color=(255, 255, 255)
            ),
            Ball(
                x=WINDOW_WIDTH // 2,
                y=WINDOW_HEIGHT // 2,
                radius=6,
                color=(255, 255, 255),
                speed=10,
            ),
        ]
    elif level == 4:
        return []  # No balls for level 4
    else:
        return [
            Ball(
                x=WINDOW_WIDTH // 2,
                y=WINDOW_HEIGHT // 2,
                radius=6,
                color=(255, 255, 255),
                speed=10,
            )
        ]


def initialize_game_for_level(level):
    global ball, left_paddle_chain, right_paddle_chain
    ball = create_ball_for_level(level)
    left_paddle_chain = PaddleChain.create_for_level(is_left=True, level=level)
    right_paddle_chain = PaddleChain.create_for_level(is_left=False, level=level)


# Initialize for level 1
initialize_game_for_level(1)

# Initialize the animated symbol
animated_symbol = AnimatedSymbol(
    WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 45
)  # Increased from 30 to 45

running = True
clock = pygame.time.Clock()
game_state = GameState.START_SCREEN


def draw_start_screen():
    screen.fill((0, 0, 0))

    # Draw title
    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render(GAME_TITLE, True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)

    # Draw subtitle
    subtitle_font = pygame.font.Font(None, 48)
    subtitle_text = subtitle_font.render(GAME_SUBTITLE, True, (255, 255, 255))
    subtitle_rect = subtitle_text.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    )
    screen.blit(subtitle_text, subtitle_rect)

    # Draw buttons
    for button in buttons:
        button.draw(screen)


def draw_game():
    screen.fill((0, 0, 0))

    # Draw game elements if we're in the GAME state or LEVEL_4_ANIMATION state
    if game_state in [GameState.GAME, GameState.LEVEL_4_ANIMATION]:
        # Draw all balls (if any)
        for b in ball:
            b.draw(screen)
        left_paddle_chain.draw(screen)
        right_paddle_chain.draw(screen)

    # Draw the animated symbol for level 4 only when show_nuke is True
    if current_level == 4 and show_nuke:
        animated_symbol.draw(screen)

    if game_state == GameState.PAUSED:
        # Draw "Press Space to begin" text
        font = pygame.font.Font(None, 48)
        space_message = {
            1: LEVEL_1_SPACE_MESSAGE,
            2: LEVEL_2_SPACE_MESSAGE,
            3: LEVEL_3_SPACE_MESSAGE,
            4: LEVEL_4_SPACE_MESSAGE,
        }[current_level]

        # Split message into lines and render each line
        lines = space_message.split("\n")
        line_surfaces = [font.render(line, True, (255, 255, 255)) for line in lines]

        # Calculate total height of all lines
        total_height = sum(surface.get_height() for surface in line_surfaces)
        line_spacing = 10  # Space between lines
        total_height += line_spacing * (len(lines) - 1)

        # Calculate starting y position to center the entire block of text
        current_y = WINDOW_HEIGHT // 2 - total_height // 2

        # Draw each line
        for surface in line_surfaces:
            text_rect = surface.get_rect(centerx=WINDOW_WIDTH // 2, top=current_y)
            screen.blit(surface, text_rect)
            current_y += surface.get_height() + line_spacing


def draw_battle_counter(screen, country1_battles, country2_battles):
    # Only show battle counter for levels 1-3
    if current_level != 4:
        font = pygame.font.Font(None, 36)
        text = font.render(
            f"BATTLES: {country1_battles} - {country2_battles}", True, (255, 255, 255)
        )
        text_rect = text.get_rect(topright=(WINDOW_WIDTH - 20, 20))
        screen.blit(text, text_rect)

    # Draw remaining soldiers/population count
    soldier_font = pygame.font.Font(None, 24)
    # Use different multiplier for level 3 and 4
    if current_level == 4:
        soldier_multiplier = 1000000  # 10 times level 3's multiplier
        label = "POPULATION"
    elif current_level == 3:
        soldier_multiplier = 100000
        label = "SOLDIERS"
    else:
        soldier_multiplier = 10000
        label = "SOLDIERS"
    left_text = soldier_font.render(
        f"{label}: {left_paddle_chain.get_visible_paddle_count() * soldier_multiplier}",
        True,
        (255, 255, 255),
    )
    right_text = soldier_font.render(
        f"{label}: {right_paddle_chain.get_visible_paddle_count() * soldier_multiplier}",
        True,
        (255, 255, 255),
    )
    left_rect = left_text.get_rect(topleft=(20, 20))
    # Adjust y position for right text based on level
    right_y = 20 if current_level == 4 else 50
    right_rect = right_text.get_rect(topright=(WINDOW_WIDTH - 20, right_y))
    screen.blit(left_text, left_rect)
    screen.blit(right_text, right_rect)


def draw_win_screen(winner, is_level_4=False):
    screen.fill((0, 0, 0))

    # Draw win message
    font = pygame.font.Font(None, 48)
    if is_level_4:
        win_text = font.render(LEVEL_4_WIN_MESSAGE, True, (255, 255, 255))
    else:
        win_text = font.render(
            LEVEL_1_WIN_MESSAGE.format(winner=winner), True, (255, 255, 255)
        )
    win_rect = win_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    screen.blit(win_text, win_rect)

    # Draw instructions
    instruction_font = pygame.font.Font(None, 36)
    instruction_text = instruction_font.render(
        LEVEL_4_RESTART_MESSAGE if is_level_4 else LEVEL_1_RESTART_MESSAGE,
        True,
        (255, 255, 255),
    )
    instruction_rect = instruction_text.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
    )
    screen.blit(instruction_text, instruction_rect)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if game_state == GameState.WIN:
                    game_state = GameState.PAUSED
                    country1_battles = 0
                    country2_battles = 0
                elif game_state == GameState.LEVEL_4_ANIMATION:
                    # Restart the animation in level 4
                    animated_symbol.start_animation()
                initialize_game_for_level(current_level)
            elif event.key == pygame.K_SPACE:
                if game_state == GameState.PAUSED:
                    if current_level == 4:
                        game_state = GameState.LEVEL_4_ANIMATION
                        show_nuke = True
                        animated_symbol.start_animation()
                    else:
                        game_state = GameState.GAME
                elif game_state == GameState.WIN:
                    game_state = GameState.START_SCREEN
            elif event.key == pygame.K_ESCAPE:
                # Reset game state and return to main menu
                game_state = GameState.START_SCREEN
                country1_battles = 0
                country2_battles = 0
                show_nuke = False
                # Reset the game board
                initialize_game_for_level(current_level)
        elif game_state == GameState.START_SCREEN:
            for i, button in enumerate(buttons):
                if button.handle_event(event):
                    current_level = i + 1
                    game_state = GameState.PAUSED
                    country1_battles = 0
                    country2_battles = 0
                    show_nuke = False  # Reset nuke visibility when changing levels
                    initialize_game_for_level(current_level)

    if game_state == GameState.START_SCREEN:
        draw_start_screen()
    else:
        if game_state == GameState.GAME:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                left_paddle_chain.move(up=True)
            if keys[pygame.K_s]:
                left_paddle_chain.move(up=False)
            if keys[pygame.K_UP]:
                right_paddle_chain.move(up=True)
            if keys[pygame.K_DOWN]:
                right_paddle_chain.move(up=False)

            # Move and check collisions for all balls
            for b in ball:
                b.move()
                if b.check_wall_collision():
                    winner = 2 if b.x - b.radius <= 0 else 1
                    if winner == 1:
                        country1_battles += 1
                    else:
                        country2_battles += 1

                    if country1_battles >= 3 or country2_battles >= 3:
                        game_state = GameState.WIN
                    else:
                        battle_message.show(winner)
                        game_state = GameState.BATTLE_WIN
                        initialize_game_for_level(current_level)
                    break  # Exit the loop if a point is scored

                # Use the appropriate collision check based on ball type
                if isinstance(b, CannonBall):
                    b.check_paddle_collision(left_paddle_chain, current_level)
                    b.check_paddle_collision(right_paddle_chain, current_level)
                else:
                    left_paddle_chain.check_collision(b, current_level)
                    right_paddle_chain.check_collision(b, current_level)
        elif game_state == GameState.LEVEL_4_ANIMATION:
            if animated_symbol.update(
                left_paddle_chain, right_paddle_chain, current_level
            ):
                print("Transitioning to win screen")  # Debug print
                game_state = GameState.WIN
                country1_battles = 3  # Set to 3 to ensure country 1 wins
                country2_battles = 0

        if game_state == GameState.WIN:
            draw_win_screen(1 if country1_battles >= 3 else 2, current_level == 4)
        else:
            draw_game()
            draw_battle_counter(screen, country1_battles, country2_battles)
            if battle_message.update():
                battle_message.draw(screen)
                if game_state == GameState.BATTLE_WIN:
                    game_state = GameState.GAME

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

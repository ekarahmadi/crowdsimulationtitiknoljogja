import pygame
import random
import sys
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions (keeping it 16:9 ratio)
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random Walk with Constrained Coordinates")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Boundary margins (reduced)
MARGIN = 0

# Total time to reach the end point (in seconds)
TOTAL_TIME = ([10, 15, 20])

# Interval to generate nodes (in milliseconds)
GENERATE_INTERVAL = 1000
current_time_text = 'MORNING'

# Load background image
full_background_image = pygame.image.load(r"image\Layout Based.png")
full_bg_width, full_bg_height = full_background_image.get_size()

full_background_image_display_morning = pygame.image.load(r"image\Layout Pagi.png")
full_bg_width_display_morning, full_bg_height_display_morning = full_background_image_display_morning.get_size()

full_background_image_display_day = pygame.image.load(r"image\Layout Siang.png")
full_bg_width_display_day, full_bg_height_display_day = full_background_image_display_day.get_size()

full_background_image_display_night = pygame.image.load(r"image\Layout Malam.png")
full_bg_width_display_night, full_bg_height_display_night = full_background_image_display_night.get_size()

# Determine the portion to clip for 16:9 ratio centered view
clip_width = min(full_bg_width, int(full_bg_height * (16 / 9)))
clip_height = min(full_bg_height, int(full_bg_width / (16 / 9)))

# Calculate the top-left corner for the centered clip
clip_x = (full_bg_width - clip_width) // 2
clip_y = (full_bg_height - clip_height) // 2

# Clip the background image to maintain the 16:9 ratio
background_image = full_background_image.subsurface((clip_x, clip_y, clip_width, clip_height))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

background_image_display_morning = full_background_image_display_morning.subsurface((clip_x, clip_y, clip_width, clip_height))
background_image_display_morning = pygame.transform.scale(background_image_display_morning, (WIDTH, HEIGHT))

background_image_display_day = full_background_image_display_day.subsurface((clip_x, clip_y, clip_width, clip_height))
background_image_display_day = pygame.transform.scale(background_image_display_day, (WIDTH, HEIGHT))

background_image_display_night = full_background_image_display_night.subsurface((clip_x, clip_y, clip_width, clip_height))
background_image_display_night = pygame.transform.scale(background_image_display_night, (WIDTH, HEIGHT))

# Load particle images
particle_image1 = pygame.image.load(r"image\woman.png")
particle_image1 = pygame.transform.scale(particle_image1, (20, 20))

particle_image2 = pygame.image.load(r"image\man.png")
particle_image2 = pygame.transform.scale(particle_image2, (20, 20))

current_background = background_image_display_morning

# Define start, middle, and end points

# Start points
right_up_start_point = [(1920, 620)]
right_down_start_point = [(1920, 740)]
left_up_start_point = [(0, 385), (0, 410), (0, 455)]
left_down_start_point = [(0, 600), (0, 627)]
up_right_start_point = [(1050, 0)]
up_left_start_point = [(935, 0), (935, 0)]
down_right_start_point = [(890, 1080), (960, 1080)]
down_left_start_point = [(718, 1080), (745, 1080)]

all_start_points_arrays = [
    right_up_start_point,
    right_down_start_point,
    left_up_start_point,
    left_down_start_point,
    up_right_start_point,
    up_left_start_point,
    down_right_start_point,
    down_left_start_point
]

# Middle points
left_up_middle_point = [(845, 490)]
right_up_middle_point = [(989, 500)]
right_down_middle_point = [(971, 733)]
left_down_middle_point = [(783, 688)]

all_middle_points_arrays = [
    right_up_middle_point,
    right_down_middle_point,
    left_up_middle_point,
    left_down_middle_point,
]

# Crowd Points
supersemar_crowd_points = [(767, 750)]
istana_crowd_points = [(980, 750)]

all_crowd_points_arrays = [
    supersemar_crowd_points,
    istana_crowd_points
]

# End points
right_up_end_point = [(1920, 595)]
right_down_end_point = [(1920, 740)]
left_up_end_point = [(0, 390)]
left_down_end_point = [(0, 640)]
up_right_end_point = [(1075, 0)]
up_left_end_point = [(925, 0)]
down_right_end_point = [(925, 1080)]
down_left_end_point = [(750, 1080)]

all_end_points_arrays = [
    right_up_end_point,
    right_down_end_point,
    left_up_end_point,
    left_down_end_point,
    up_right_end_point,
    up_left_end_point,
    down_right_end_point,
    down_left_end_point
]

# Counters for man and woman
man_count = 0
woman_count = 0

# Total counters for generated nodes
total_man_generated = 0
total_woman_generated = 0

# Node class
class Node:
    def __init__(self, start_pos, middle_pos, crowd_pos, end_pos, total_time, image, visited_crowd):
        self.start_pos = start_pos
        self.pos = list(start_pos)
        self.middle_pos = middle_pos
        self.crowd_pos = crowd_pos
        self.end_pos = end_pos
        self.total_time = total_time
        self.time_elapsed = 0
        self.image = image
        self.rect = self.image.get_rect(center=start_pos)
        self.finished = False  # Flag to check if the node reached the end
        self.pos_before_gray = list(start_pos)
        self.visited_crowd = visited_crowd  # Flag to check if the node has visited the crowd point
        self.calculate_velocity()

    def calculate_velocity(self):
        # Calculate velocities for different segments
        self.velocity1 = [(self.middle_pos[0] - self.start_pos[0]) / (self.total_time / 3),
                          (self.middle_pos[1] - self.start_pos[1]) / (self.total_time / 3)]
         
        if self.visited_crowd:
            # Middle to crowd
            self.velocity2 = [(self.crowd_pos[0] - self.middle_pos[0]) / (self.total_time / 3),
                              (self.crowd_pos[1] - self.middle_pos[1]) / (self.total_time / 3)]
            # Crowd to end
            self.velocity3 = [(self.end_pos[0] - self.crowd_pos[0]) / (self.total_time / 3),
                              (self.end_pos[1] - self.crowd_pos[1]) / (self.total_time / 3)]
        else:
            # Middle to end
            self.velocity2 = [(self.end_pos[0] - self.middle_pos[0]) / (2 * self.total_time / 3),
                              (self.end_pos[1] - self.middle_pos[1]) / (2 * self.total_time / 3)]

    # def find_new_start_point(self):
    #     """
    #     Find a new start and middle point for the node.
    #     """
    #     new_start_pos = random.choice([point for array in all_start_points_arrays for point in array])
    #     new_middle_pos = random.choice([point for array in all_middle_points_arrays for point in array])
    #     self.pos = list(new_start_pos)
    #     self.start_pos = new_start_pos
    #     self.middle_pos = new_middle_pos
    #     self.time_elapsed = 0
    #     self.calculate_velocity()
    #     self.rect = self.image.get_rect(center=new_start_pos)

    def find_return_path(self):
        """
        Find a return path from the current position to the middle point.
        """
        dx = self.middle_pos[0] - self.pos[0]
        dy = self.middle_pos[1] - self.pos[1]
        
        length = math.sqrt(dx ** 2 + dy ** 2)
        if length != 0:
            dx /= length
            dy /= length
        
        distance = 20  # Adjust this value as needed
        new_x = self.pos[0] + dx * distance
        new_y = self.pos[1] + dy * distance
        
        return [self.pos, (new_x, new_y)]

    def update(self, dt):
        if not self.finished:
            if self.time_elapsed < self.total_time:
                if self.time_elapsed < self.total_time / 3:
                    # Move towards the middle point
                    self.pos[0] += self.velocity1[0] * dt
                    self.pos[1] += self.velocity1[1] * dt
                elif self.visited_crowd and self.time_elapsed < 2 * self.total_time / 3:
                    # Move towards the crowd point
                    self.pos[0] += self.velocity2[0] * dt
                    self.pos[1] += self.velocity2[1] * dt
                elif self.visited_crowd:
                    # Move towards the end point from the crowd point
                    self.pos[0] += self.velocity3[0] * dt
                    self.pos[1] += self.velocity3[1] * dt
                else:
                    # Move towards the end point directly from the middle point
                    self.pos[0] += self.velocity2[0] * dt
                    self.pos[1] += self.velocity2[1] * dt

                # Add a random walk component
                self.pos[0] += random.uniform(-1, 1)
                self.pos[1] += random.uniform(-1, 1)

                # Check if the background color at the new position is gray
                # if 0 <= int(self.pos[0]) < WIDTH and 0 <= int(self.pos[1]) < HEIGHT:
                #     bg_color = background_image.get_at((int(self.pos[0]), int(self.pos[1])))
                #     if bg_color != (217, 217, 217):  # If not gray, node is outside the gray zone
                #         # Set the current position as the new start point
                #         self.start_pos = list(self.pos)
                #         # Reset the node to find a new path
                #         # self.find_new_start_point()
                #         return
                #     else:
                #         # Store the last position before hitting gray
                #         self.pos_before_gray = list(self.pos)

                # Constrain coordinates within the boundary margins
                self.pos[0] = max(MARGIN, min(self.pos[0], WIDTH - MARGIN))
                self.pos[1] = max(MARGIN, min(self.pos[1], HEIGHT - MARGIN))

                # Update rect position
                self.rect.center = (int(self.pos[0]), int(self.pos[1]))
                self.time_elapsed += dt
            else:
                self.finished = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Function to generate a single node at random start, middle, and end points
def generate_node():
    global total_man_generated, total_woman_generated, man_count, woman_count # Use the global total counters

    total_time = random.choice(TOTAL_TIME)
    
    probabilities_start = [0.1, 0.1, 0.03, 0.03, 0.03, 0.05, 0.05, 0.05, 0.025, 0.025, 0.125, 0.125, 0.125, 0.125]
    start_pos = random.choices([point for array in all_start_points_arrays for point in array], weights=probabilities_start, k=1)[0]
    
    # Determine the appropriate middle point based on the start position
    if start_pos in right_up_start_point:
        middle_pos = random.choice(right_up_middle_point)
    elif start_pos in right_down_start_point:
        middle_pos = random.choice(right_down_middle_point)
    elif start_pos in left_up_start_point:
        middle_pos = random.choice(left_up_middle_point)
    elif start_pos in left_down_start_point:
        middle_pos = random.choice(left_down_middle_point)
    elif start_pos in up_right_start_point:
        middle_pos = random.choice(right_up_middle_point)
    elif start_pos in up_left_start_point:
        middle_pos = random.choice(left_up_middle_point)
    elif start_pos in down_right_start_point:
        middle_pos = random.choice(right_down_middle_point)
    elif start_pos in down_left_start_point:
        middle_pos = random.choice(left_down_middle_point)
    else:
        middle_pos = (WIDTH // 2, HEIGHT // 2)  # Default to the center if not found
        
    # Determine the appropriate end point based on the middle position
    if middle_pos in right_up_middle_point:
        end_pos = random.choice(up_right_end_point + right_up_end_point + left_up_end_point + down_right_end_point)
    elif middle_pos in right_down_middle_point:
        end_pos = random.choice(right_down_end_point + up_right_end_point + left_down_end_point + down_right_end_point)
    elif middle_pos in left_up_middle_point:
        end_pos = random.choice(up_left_end_point + left_up_end_point + down_left_end_point + right_up_end_point)
    elif middle_pos in left_down_middle_point:
        end_pos = random.choice(left_down_end_point + down_left_end_point + right_down_end_point + up_left_end_point)
    else:
        end_pos = (WIDTH // 2, HEIGHT // 2)  # Default to the center if not found

    choices = [True, False]
    probabilities = [0.7, 0.3]
    visit_crowd = random.choices(choices, weights=probabilities, k=1)[0]
    
    choices_gender = [particle_image1, particle_image2]
    probabilities_gender = [0.45, 0.55]
    image = random.choices(choices_gender, weights=probabilities_gender, k=1)[0] # Randomly select an image
    
    # Determine the crowd position based on the middle position
    if visit_crowd:
        if middle_pos in right_up_middle_point or middle_pos in right_down_middle_point:
            crowd_pos = random.choice(istana_crowd_points)
        else:
            crowd_pos = random.choice(supersemar_crowd_points)
        
        
        if crowd_pos in istana_crowd_points:
            end_pos = random.choice(up_right_end_point+right_down_end_point+down_right_end_point)
        else:
            end_pos = random.choice(left_down_end_point+down_left_end_point+up_left_end_point)
            
    
    # Randomly decide whether to visit the crowd point


    # Increment the total generated counters
    if image == particle_image1:
        total_woman_generated += 1
        woman_count += 1
    else:
        total_man_generated += 1
        man_count += 1   
    node = Node(start_pos, middle_pos, crowd_pos if visit_crowd else None, end_pos, total_time, image, visit_crowd)
    return node
# Function to get the current counts of generated nodes
def get_generated_counts():
    return total_man_generated, total_woman_generated


def morning_button():
    global GENERATE_INTERVAL, current_time_text, current_background
    GENERATE_INTERVAL = 1000
    current_time_text = 'MORNING'
    current_background = background_image_display_morning

def daylight_button():
    global GENERATE_INTERVAL, current_time_text, current_background
    GENERATE_INTERVAL = 300
    current_time_text = 'DAYLIGHT'
    current_background = background_image_display_day

def night_button():
    global GENERATE_INTERVAL, current_time_text, current_background
    GENERATE_INTERVAL = 48
    current_time_text = 'NIGHT'
    current_background = background_image_display_night

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.action = action
        self.is_hovered = False

    def draw(self, surface):
        if self.is_hovered:
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.SysFont(None, 36)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def click(self):
        if self.action:
            self.action()

buttons = [
    Button(1150, 990, 200, 50, "MORNING", (102, 194, 255),(78, 136, 202), morning_button),
    Button(1360, 990, 200, 50, "DAYLIGHT", (255, 153, 102), (240, 99, 55),daylight_button),
    Button(1570, 990, 200, 50, "NIGHT", (102, 102, 153), (72, 79, 150),night_button),
]

# Main function
def main():
    global man_count, woman_count  # Use the global counters
    clock = pygame.time.Clock()
    nodes = []  # List to store nodes
    last_generate_time = 0  # Initialize last generate time

    while True:
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    button.is_hover(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_hovered:
                        button.click()


        # Generate a single node at the specified interval
        if current_time - last_generate_time > GENERATE_INTERVAL:
            nodes.append(generate_node())
            last_generate_time = current_time  # Update last generate time

        # Update node positions
        total_man, total_woman = get_generated_counts()
        
        dt = clock.get_time() / 1000  # Delta time in seconds
        for node in nodes[:]:
            node.update(dt)
            if node.finished:
                if node.image == particle_image1:
                    woman_count -= 1
                else:
                    man_count -= 1
                nodes .remove(node)
         # Remove node after it reaches the end

        # Draw background
        screen.blit(current_background, (0, 0))

        # Draw nodes
        for node in nodes:
            node.draw(screen)
        
        for button in buttons:
            button.draw(screen)

        # Display counts
        font = pygame.font.SysFont("American Captain", 30)
        font_small = pygame.font.SysFont("American Captain", 15)
        font_time = pygame.font.SysFont("American Captain", 36)

        # Display total generated counts
        
        total_man_text = font.render(f'Total Pengunjung Pria: {man_count}', True, (255,162,0))
        total_woman_text = font.render(f'Total Pengunjung Wanita: {woman_count}', True, (32,165,249))
        
        pria_text = font_small.render(f'PRIA', True, (255,255,255))
        wanita_text = font_small.render(f'WANITA', True, (255,255,255))
        # time_text = font_time.render(f'{current_time_text}', True, (255,255,255))

        screen.blit(total_man_text, (57, 52))
        screen.blit(total_woman_text, (57, 115))
        screen.blit(pria_text, (250, 1003))
        screen.blit(wanita_text, (250, 1043))
        pygame.draw.rect(screen, (255,162,0), (64, 1060 - man_count*1.3, 50, 20000))
        pygame.draw.rect(screen, (32,165,249), (134, 1060 - woman_count*1.3, 50, 20000))
        pygame.draw.rect(screen, (255,162,0), (224, 1000, 20, 20))
        pygame.draw.rect(screen, (32,165,249), (224, 1040, 20, 20))
        # screen.blit(time_text, (1680, 50))

        pygame.display.flip()
        clock.tick(60)  # Limit the frame rate to 60 FPS

if __name__ == "__main__":
    main()

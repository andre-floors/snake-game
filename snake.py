import pygame
import settings

class Node:
    def __init__(self, position):
        self.position = position  # (x, y)
        self.next = None

class Snake:
    def __init__(self, init_positions):
        self.head = Node(init_positions[0])
        current = self.head
        for pos in init_positions[1:]:
            current.next = Node(pos)
            current = current.next

        self.direction = 'RIGHT'
        self.should_grow = False
        self.growth_pending = 0

        snake_color = settings.settings["snake_color"]

        # Dynamically load snake's images based on selected color
        def load_snake_image(part):
            img = pygame.image.load(f"assets/images/snake/snake-{part}-{snake_color}.png").convert_alpha()
            return pygame.transform.scale(img, (25, 25))

        self.head_img = load_snake_image("head")
        self.body_img = load_snake_image("body")
        self.tail_img = load_snake_image("tail")

    def get_positions(self):
        positions = []
        current = self.head
        while current:
            positions.append(current.position)
            current = current.next
        return positions

    def move(self, direction):
        head_x, head_y = self.head.position
        if direction == 'UP':
            new_head = (head_x, head_y - 1)
        elif direction == 'DOWN':
            new_head = (head_x, head_y + 1)
        elif direction == 'LEFT':
            new_head = (head_x - 1, head_y)
        elif direction == 'RIGHT':
            new_head = (head_x + 1, head_y)

        new_node = Node(new_head)
        new_node.next = self.head
        self.head = new_node

        # Only remove tail if we're not growing
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            current = self.head
            while current.next and current.next.next:
                current = current.next
            current.next = None

    def set_direction(self, key):
        key_map = {
            pygame.K_w: 'UP',
            pygame.K_UP: 'UP',
            pygame.K_s: 'DOWN',
            pygame.K_DOWN: 'DOWN',
            pygame.K_a: 'LEFT',
            pygame.K_LEFT: 'LEFT',
            pygame.K_d: 'RIGHT',
            pygame.K_RIGHT: 'RIGHT'
        }

        opposite = {
            'UP': 'DOWN',
            'DOWN': 'UP',
            'LEFT': 'RIGHT',
            'RIGHT': 'LEFT'
        }

        new_direction = key_map.get(key)
        if new_direction and new_direction != opposite.get(self.direction):
            self.direction = new_direction

    def direction_between(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2:
            return 'UP' if y1 < y2 else 'DOWN'
        elif y1 == y2:
            return 'LEFT' if x1 < x2 else 'RIGHT'

    def is_collision(self):
        head_x, head_y = self.head.position
        # Grid boundaries (30 cols x 26 rows)
        if head_x < 1 or head_x > 30 or head_y < 1 or head_y > 26:
            return True
        return False

    def is_self_collision(self):
        head_pos = self.head.position
        current = self.head.next  # skip the head

        while current:
            if current.position == head_pos:
                return True
            current = current.next

        return False
    
    def get_body_image(self, prev_pos, current_pos, next_pos):
        dir_from_prev = self.direction_between(prev_pos, current_pos)
        dir_to_next = self.direction_between(current_pos, next_pos)

        # Straight line
        if dir_from_prev == dir_to_next:
            if dir_from_prev == 'UP':
                return pygame.transform.rotate(self.body_img, 90)
            elif dir_from_prev == 'DOWN':
                return pygame.transform.rotate(self.body_img, -90)
            elif dir_from_prev == 'LEFT':
                return pygame.transform.rotate(self.body_img, 180)
            else:
                return self.body_img  # RIGHT, no rotation

        # Corner – no rotation needed since the image is pre-aligned
        return self.body_img

    def get_tail_image(self, prev_pos, tail_pos):
        tail_dir = self.direction_between(tail_pos, prev_pos)
        rotations = {
            'UP': -90,
            'DOWN': 90,
            'LEFT': 0,
            'RIGHT': 180
        }
        angle = rotations.get(tail_dir, 0)
        return pygame.transform.rotate(self.tail_img, angle)

    def get_head_image(self, direction):
        rotations = {
            'UP': 90,
            'DOWN': -90,
            'LEFT': 180,
            'RIGHT': 0
        }
        angle = rotations.get(direction, 0)
        return pygame.transform.rotate(self.head_img, angle)
    
    def grow(self, amount=1):
        self.growth_pending += amount
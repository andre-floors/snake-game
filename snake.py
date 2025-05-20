import pygame

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

        # Load and scale images
        self.head_img = pygame.image.load("assets/snake_head.png").convert()
        self.head_img.set_colorkey((255, 255, 255))
        self.head_img = pygame.transform.scale(self.head_img, (25, 25))

        self.body_img = pygame.image.load("assets/snake_body.png").convert()
        self.body_img.set_colorkey((255, 255, 255))
        self.body_img = pygame.transform.scale(self.body_img, (25, 25))

        self.body_corner_img = pygame.image.load("assets/snake_corner_body.png").convert()
        self.body_corner_img.set_colorkey((255, 255, 255))
        self.body_corner_img = pygame.transform.scale(self.body_corner_img, (25, 25))

        self.tail_img = pygame.image.load("assets/snake_tail.png").convert()
        self.tail_img.set_colorkey((255, 255, 255))
        self.tail_img = pygame.transform.scale(self.tail_img, (25, 25))

            # Linked list setup
        self.head = Node(init_positions[0])
        current = self.head
        for pos in init_positions[1:]:
            current.next = Node(pos)
            current = current.next

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

        # remove the tail
        current = self.head
        while current.next and current.next.next:
            current = current.next
        current.next = None

    def set_direction(self, key):
        key_map = {
            pygame.K_w: 'UP',
            pygame.K_s: 'DOWN',
            pygame.K_a: 'LEFT',
            pygame.K_d: 'RIGHT'
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

    def get_body_image(self, prev_pos, current_pos, next_pos):
        dir_from_prev = self.direction_between(prev_pos, current_pos)
        dir_to_next = self.direction_between(current_pos, next_pos)

        # Straight line
        if dir_from_prev == dir_to_next:
            if dir_from_prev in ['UP', 'DOWN']:
                return pygame.transform.rotate(self.body_img, 90)
            elif dir_from_prev == 'LEFT':
                return pygame.transform.rotate(self.body_img, 180)
            else:
                return self.body_img  # RIGHT, no flip

        print(f"Prev Dir: {dir_from_prev}, Next Dir: {dir_to_next}")
        
        # Corners
        # Mapping corner image rotations
        corner_angles = {
            ('DOWN', 'RIGHT'): 0,
            ('RIGHT', 'DOWN'): 180,
            ('LEFT', 'DOWN'): 270,
            ('DOWN', 'LEFT'): 90,
            ('UP', 'LEFT'): 180,
            ('LEFT', 'UP'): 0,
            ('RIGHT', 'UP'): 90,
            ('UP', 'RIGHT'): 270,
        }   

        # Check both orders
        angle = corner_angles.get((dir_from_prev, dir_to_next))
        if angle is None:
            angle = corner_angles.get((dir_to_next, dir_from_prev), 0)

        return pygame.transform.rotate(self.body_corner_img, angle)

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
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next = None

class Snake:
    def __init__(self):
        self.head = Node(5, 5)  # Initial position
        self.tail = self.head

    def move(self, dx, dy):
        # Shift all nodes to follow the head
        pass

    def grow(self):
        # Add new node at the tail
        pass

    def check_collision(self):
        # Check if head collides with body
        pass
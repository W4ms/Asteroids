from constants import *
import pygame
from shot import Shot # Make sure your Shot class in shot.py is also named 'Shot'
from circleshape import CircleShape # Assuming CircleShape is your base class

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0.0 # Initialize the shoot_timer
        self.velocity = pygame.Vector2(0, 0) # Initialize velocity
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def shoot(self):
        # Prevent shooting if the timer is greater than 0
        if self.shoot_timer > 0:
            return None # Cannot shoot yet

        # If we can shoot, reset the timer
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN

        # Calculate the starting position and direction for the shot
        forward_vector = pygame.Vector2(0, 1).rotate(self.rotation)
        shot_start_pos = self.position + forward_vector * (self.radius + SHOT_RADIUS + 1) # Offset to start outside player
        return Shot(shot_start_pos.x, shot_start_pos.y, self.rotation)

    
    def update(self, dt, is_accelerating=False): # Added is_accelerating parameter
        # Decrease the shoot timer
        if self.shoot_timer > 0:
            self.shoot_timer -= dt
            if self.shoot_timer < 0:
                self.shoot_timer = 0

        # Movement logic
        if is_accelerating:
            # Calculate the forward direction based on rotation
            forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)
            self.velocity += forward_direction * PLAYER_ACCELERATION * dt
        else:
            # Optional: Apply friction/deceleration if not accelerating
            # This makes the ship slow down over time
            self.velocity *= (1 - PLAYER_FRICTION * dt)
            if self.velocity.length_squared() < 0.01: # Stop if very slow
                self.velocity = pygame.Vector2(0, 0)

        # Apply velocity to position
        self.position += self.velocity * dt

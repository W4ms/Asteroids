# In your asteroid.py file
import random
import pygame # You'll likely need this
from circleshape import CircleShape
from constants import ASTEROID_SPEED, ASTEROID_RADIUS, ASTEROID_MIN_RADIUS # Make sure you import these!

class Asteroid(CircleShape):
    # Now it takes x, y, rotation, AND radius!
    def __init__(self, x, y, rotation, radius):
        super().__init__(x, y, radius) # Pass the radius to CircleShape's init
        self.rotation = rotation # Store its current rotation if needed for drawing/spin
        # Calculate velocity based on rotation and speed
        # You might want to randomize asteroid speed a bit too!
        self.velocity = pygame.Vector2(0, ASTEROID_SPEED).rotate(rotation)

    def update(self, dt):
        self.position += self.velocity * dt
        # You'll likely need boundary wrapping for asteroids here
        # or logic to remove/respawn them if they go off-screen.

    def draw(self, screen):
        # Example: draw a white circle
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
        # You might want to draw a more complex shape later!



    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS: 
            return []
        random_angle = random.uniform(20, 50)
        velocity1 = self.velocity.rotate(random_angle)
        velocity2 = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        velocity2 *= 1.2
        velocity1 *= 1.2
        rotation1 = self.rotation + random_angle
        rotation2 = self.rotation - random_angle
        new_asteroid_1 = Asteroid(self.position.x, self.position.y, rotation1, new_radius)
        new_asteroid_2 = Asteroid(self.position.x, self.position.y, rotation2, new_radius)
        new_asteroid_1.velocity = velocity1
        new_asteroid_2.velocity = velocity2
        return [new_asteroid_1, new_asteroid_2]


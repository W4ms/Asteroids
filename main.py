import pygame
import sys
import random

# Import your custom classes and constants
from constants import * # Make sure all necessary constants are here
from player import Player
from shot import Shot
from asteroid import Asteroid # Make sure you have this file and class

def main():
    pygame.init()

    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids Game")

    # Game objects initialization (Order matters!)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # <-- Player initialized here!
    all_shots = []
    all_asteroids = [] # <-- Asteroid list initialized here!

    # Asteroid Spawning Logic (Correctly placed and executed once at the start)
    for _ in range(ASTEROID_COUNT):
        # Spawn them randomly within the screen, but not too close to the player
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        
        # Ensure asteroid isn't spawned directly on top of the player
        # This is a simple check, more robust collision check might be needed
        distance_to_player = pygame.Vector2(x, y).distance_to(player.position)
        if distance_to_player < (player.radius + ASTEROID_RADIUS + 50): # Add some buffer
            # If too close, adjust position or skip this asteroid for now
            # For simplicity, we'll re-randomize or just ignore if it's a very small chance
            # A better approach for many asteroids is to re-roll until a safe spot is found.
            x = random.randint(0, SCREEN_WIDTH) # Simple re-roll if too close
            y = random.randint(0, SCREEN_HEIGHT)

        initial_rotation = random.uniform(0, 360) # Random initial direction (angle)
        
        # Assuming Asteroid.__init__(self, x, y, rotation, radius)
        all_asteroids.append(Asteroid(x, y, initial_rotation, ASTEROID_RADIUS))

    # Flags for continuous input (movement and rotation)
    is_accelerating_forward = False
    is_accelerating_backward = False # Not used in player.update by default for this lesson
    is_rotating_left = False
    is_rotating_right = False

    running = True
    clock = pygame.time.Clock()

    # --- Main Game Loop ---
    while running:
        dt = clock.tick(60) / 1000.0 # Time since last frame in seconds

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle KEYDOWN events (when a key is pressed down)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    is_accelerating_forward = True
                if event.key == pygame.K_s:
                    is_accelerating_backward = True # You'd need to add logic for this in Player.update
                if event.key == pygame.K_a:
                    is_rotating_left = True
                if event.key == pygame.K_d:
                    is_rotating_right = True
                if event.key == pygame.K_SPACE:
                    new_shot = player.shoot() # Player's shoot method handles cooldown
                    if new_shot: # Only add if a shot was actually created (not on cooldown)
                        all_shots.append(new_shot)
            
            # Handle KEYUP events (when a key is released)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    is_accelerating_forward = False
                if event.key == pygame.K_s:
                    is_accelerating_backward = False
                if event.key == pygame.K_a:
                    is_rotating_left = False
                if event.key == pygame.K_d:
                    is_rotating_right = False

        # --- Update Game Objects ---

        # Update player's rotation based on input flags
        if is_rotating_left:
            player.rotate(-dt)
        if is_rotating_right:
            player.rotate(dt)

        # Update player's position and shoot cooldown
        # This call should happen once per frame, passing the appropriate acceleration state
        player.update(dt, is_accelerating_forward)

        # Update all active shots
        active_shots = [] # Create a new list for shots that are still active
        for shot in all_shots:
            shot.update(dt)
            # Simple check to remove shots that go off-screen
            if 0 < shot.position.x < SCREEN_WIDTH and 0 < shot.position.y < SCREEN_HEIGHT:
                active_shots.append(shot)
        all_shots = active_shots # Replace old list with new list of active shots

        # Update all active asteroids
        # You'll likely want to wrap their positions if they go off-screen
        for asteroid in all_asteroids:
            asteroid.update(dt)
            # Example: Wrap around screen boundaries
            if asteroid.position.x < 0:
                asteroid.position.x = SCREEN_WIDTH
            elif asteroid.position.x > SCREEN_WIDTH:
                asteroid.position.x = 0
            if asteroid.position.y < 0:
                asteroid.position.y = SCREEN_HEIGHT
            elif asteroid.position.y > SCREEN_HEIGHT:
                asteroid.position.y = 0
        asteroids_to_remove = []
        shots_to_remove = []
        new_asteroids = []
        for asteroid in all_asteroids:
            for shot in all_shots:
                distance = asteroid.position.distance_to(shot.position)
                if distance < asteroid.radius + shot.radius:
                    asteroids_to_remove.append(asteroid)
                    shots_to_remove.append(shot)
                    split_result = asteroid.split()
                    new_asteroids.extend(split_result)
        for asteroid in asteroids_to_remove:
            if asteroid in all_asteroids:
                all_asteroids.remove(asteroid)
        all_asteroids.extend(new_asteroids)
        for shot in shots_to_remove:
              if shot in all_shots:
                  all_shots.remove(shot)
        # --- Drawing ---

        for asteroid in all_asteroids:
            distance = asteroid.position.distance_to(player.position)
            if distance < asteroid.radius + player.radius:
                running = False  # End the game if the player is hit


        # Fill the background
        screen.fill("black")

        # Draw player
        player.draw(screen)

        # Draw all shots
        for shot in all_shots:
            shot.draw(screen)
        
        # Draw all asteroids
        for asteroid in all_asteroids:
            asteroid.draw(screen)
        
        # Update the full display surface to the screen
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

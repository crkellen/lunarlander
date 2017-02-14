import pygame
import random
from vec2d import Vec2d

pygame.init()

WIDTH = 800
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

BACKGROUND_COLOR = (0, 0, 0)
LANDER_COLOR = (0, 255, 0)

FONT = pygame.font.SysFont('monospace', 15)

#Main Screen for drawing
DRAW_SCREEN = pygame.Surface((WIDTH,HEIGHT))
DRAW_SCREEN.fill(BACKGROUND_COLOR)
PLAYER_SCREEN = pygame.Surface((WIDTH, HEIGHT))
PLAYER_SCREEN.fill(BACKGROUND_COLOR)

#Time Variables
CLOCK = pygame.time.Clock()
TIMESTEPS = 0

#Vectors
THRUST_UP = Vec2d(0,-2)
THRUST_RIGHT = Vec2d(1,0)
THRUST_LEFT = Vec2d(-1,0)

class Lander:
	def __init__(self, isAlive = True, pos = Vec2d(0,0), vel = Vec2d(0,0)):
		self.isAlive = isAlive
		self.pos = pos
		self.vel = vel
		self.acc = Vec2d(0,1)
	
	def move_self(self, dt):
		self.pos += self.vel * dt + .5 * self.acc * dt * dt
		
	def add_force(self, force, dt):
		self.vel += force * dt
		if self.vel.x > 3:
			self.vel.x = 3
		if self.vel.y > 4:
			self.vel.x = 4
		
	def draw_self(self, surface):
		pygame.draw.rect(surface, LANDER_COLOR, pygame.Rect(self.pos.x, self.pos.y, 20, 20), 5)

def update_positions(dt):
	if PLAYER.isAlive == True:
		PLAYER.move_self(dt)
	
def handle_events():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				PLAYER.add_force(THRUST_UP, 1)
			if event.key == pygame.K_a:
				PLAYER.add_force(THRUST_LEFT, 1)
			if event.key == pygame.K_d:
				PLAYER.add_force(THRUST_RIGHT, 1)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				PLAYER.add_force(-THRUST_UP, 1)
			if event.key == pygame.K_a:
				PLAYER.add_force(-THRUST_LEFT, 1)
			if event.key == pygame.K_d:
				PLAYER.add_force(-THRUST_RIGHT, 1)
				
def update_screen():
	WINDOW.blit(DRAW_SCREEN, (0, 0))
	PLAYER_SCREEN.fill(BACKGROUND_COLOR)
	if PLAYER.isAlive == True:
		PLAYER.draw_self(PLAYER_SCREEN)
	WINDOW.blit(PLAYER_SCREEN, (0,0))
	pygame.display.flip()

def update_time():
	global TIMESTEPS
	TIMESTEPS += 1
	CLOCK.tick(60)	
	
	
def game_loop():
	while True:
		handle_events()
		update_positions(1)
		update_screen()
		update_time()	

#Player Object
PLAYER = Lander(True, Vec2d(400,300), Vec2d(0,0))
		
def main():
	pygame.display.set_caption('Lunar Lander')
	game_loop()
	
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e
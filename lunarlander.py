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
DONE = False

#Main Screen for drawing
DRAW_SCREEN = pygame.Surface((WIDTH,HEIGHT))
DRAW_SCREEN.fill(BACKGROUND_COLOR)
PLAYER_SCREEN = pygame.Surface((WIDTH, HEIGHT))
PLAYER_SCREEN.fill(BACKGROUND_COLOR)

#Time Variables
CLOCK = pygame.time.Clock()
TIMESTEPS = 0

#Vectors
THRUST_UP = Vec2d(0,-.02)
THRUST_RIGHT = Vec2d(.01,0)
THRUST_LEFT = Vec2d(-.01,0)
GRAVITY = Vec2d(0,0.01)

#Vector Bools
ADD_THRUST_UP = False
ADD_THRUST_LEFT = False
ADD_THRUST_RIGHT = False

#Velocity Text
VELX_LABEL = FONT.render('Velocity X: ', 1, (255, 255, 0))
VELY_LABEL = FONT.render('Velocity Y: ', 1, (255, 255, 0))

class Lander:
	def __init__(self, isAlive = True, pos = Vec2d(0,0), vel = Vec2d(0,0)):
		self.isAlive = isAlive
		self.pos = pos
		self.vel = vel
		self.acc = Vec2d(0,0)
	
	def move_self(self, dt):
		self.pos += self.vel * dt + .5 * self.acc * dt * dt
		
	def add_force(self, force, dt):
		self.vel += force * dt
		if self.vel.x > 2:
			self.vel.x = 2
		elif self.vel.x < -2:
			self.vel.x = -2;
		if self.vel.y > 2:
			self.vel.y = 2
		elif self.vel.y < -2:
			self.vel.y = -2
		
	def draw_self(self, surface):
		pygame.draw.rect(surface, LANDER_COLOR, pygame.Rect(self.pos.x, self.pos.y, 20, 20), 5)
	
def handle_events():
	global ADD_THRUST_UP, ADD_THRUST_LEFT, ADD_THRUST_RIGHT, DONE
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			DONE = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				ADD_THRUST_UP = True
			if event.key == pygame.K_a:
				ADD_THRUST_LEFT = True
			if event.key == pygame.K_d:
				ADD_THRUST_RIGHT = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				ADD_THRUST_UP = False
			if event.key == pygame.K_a:
				ADD_THRUST_LEFT = False
			if event.key == pygame.K_d:
				ADD_THRUST_RIGHT = False
				
def update_positions(dt):
	if PLAYER.isAlive == True:
		PLAYER.move_self(dt)
				
def update_force(dt):
	if ADD_THRUST_UP == True:
		PLAYER.add_force(THRUST_UP, dt)
	if ADD_THRUST_LEFT == True:
		PLAYER.add_force(THRUST_LEFT, dt)
	if ADD_THRUST_RIGHT == True:
		PLAYER.add_force(THRUST_RIGHT, dt)
	PLAYER.add_force(GRAVITY, dt)				

def update_labels():
	global VELX_LABEL, VELY_LABEL
	VELX_LABEL = FONT.render('Velocity X: {:.2f}'.format(PLAYER.vel.x), 1, (255, 255, 0))
	VELY_LABEL = FONT.render('Velocity Y: {:.2f}'.format(PLAYER.vel.y), 1, (255, 255, 0))
	
def update_screen():
	WINDOW.blit(DRAW_SCREEN, (0, 0))
	PLAYER_SCREEN.fill(BACKGROUND_COLOR)
	if PLAYER.isAlive == True:
		PLAYER.draw_self(PLAYER_SCREEN)
	WINDOW.blit(PLAYER_SCREEN, (0,0))
	WINDOW.blit(VELX_LABEL, (0,0))
	WINDOW.blit(VELY_LABEL, (0,10))
	pygame.display.flip()

def update_time():
	global TIMESTEPS
	TIMESTEPS += 1
	CLOCK.tick(60)	
	
def game_loop():
	while not DONE:
		handle_events()
		update_positions(1)
		update_force(1)
		update_labels()
		update_screen()
		update_time()	

#Player Object
PLAYER = Lander(True, Vec2d(400,300), Vec2d(0,0))
		
def main():
	global FONT
	pygame.display.set_caption('Lunar Lander')
	game_loop()
	
	del FONT
	pygame.display.quit()
	pygame.quit()
	
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e
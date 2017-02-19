import pygame
import random
from vec2d import Vec2d

pygame.init()

WIDTH = 800
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

BACKGROUND_COLOR = (0, 0, 0)
LANDER_COLOR = (0, 255, 0)
PLATFORM_COLOR = (0, 0, 255)
WALL_COLOR = (255, 0, 0)

FONT = pygame.font.SysFont('monospace', 15)
DONE = False   #Game Loop
EXIT = False   #End Screen Loop
PLAYER_WIN = False #True if player successfully lands

#Scoring Variables
FUEL = 500
SCORE = 0

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
ACCX_LABEL = FONT.render('Acceleration X: ', 1, (255, 255, 0))
ACCY_LABEL = FONT.render('Acceleration Y: ', 1, (255, 255, 0))

#Score Text
FUEL_LABEL = FONT.render('FUEL: {}'.format(FUEL), 1, (255, 255, 0))
TIME_LABEL = FONT.render('TIME: {}'.format(TIMESTEPS), 1, (255, 255, 0))
SCORE_LABEL = FONT.render('SCORE: {}'.format(SCORE), 1, (255, 255, 0))

#End Screen Text
YOU_WIN_LABEL = FONT.render('You successfully completed the mission!', 1, (255, 255, 0))
YOU_LOSE_LABEL = FONT.render('You failed to complete the mission!', 1, (255, 255, 0))
REPLAY_LABEL = FONT.render('Press R to play again!', 1, (255, 255, 0))

class Lander:
	def __init__(self, isAlive = True, pos = Vec2d(0,0), vel = Vec2d(0,0)):
		self.isAlive = isAlive
		self.pos = pos
		self.vel = vel
		self.acc = Vec2d(0,0)
		self.pRect = pygame.Rect(self.pos.x, self.pos.y, 20, 20)
	
	def move_self(self, dt):
		self.pos += self.vel * dt + .5 * self.acc * dt * dt
		
	def add_force(self, force):
		self.acc += force
		
	def draw_self(self, surface):
		self.pRect = pygame.Rect(self.pos.x, self.pos.y, 20, 20)
		pygame.draw.rect(surface, LANDER_COLOR, self.pRect, 1)
	
class Platform:
	def __init__(self, pos = Vec2d(0,0), threshold = Vec2d(1,1)):
		self.pos = pos
		self.threshold = threshold
		self.lowerHalf = pygame.Rect(self.pos.x, self.pos.y+2, 20, 8)
		self.landingPad = pygame.Rect(self.pos.x+5, self.pos.y, 10, 2)
	
	def draw_self(self, surface):
		pygame.draw.rect(surface, LANDER_COLOR, self.landingPad, 1)
		pygame.draw.rect(surface, (0,255,255), self.lowerHalf, 1)
		
class Wall:
	def __init__(self, bounds = pygame.Rect(0,0,1,1)):
		self.bounds = bounds
		
	def draw_self(self, surface):
		pygame.draw.rect(surface, WALL_COLOR, self.bounds, 1)
	
def reset_game():
	global DONE, TIMESTEPS, GOAL, FUEL, SCORE
	
	GOAL = Platform(Vec2d(random.randint(100,700), random.randint(100,500)), Vec2d(1,1))
	
	PLAYER.pos = Vec2d(400,300)
	PLAYER.vel = Vec2d(0,0)
	PLAYER.acc = Vec2d(0,0)
	PLAYER.isAlive = True
	
	FUEL = 500
	TIMESTEPS = 0
	SCORE = 0
	
	PLAYER_WIN = False
	TIMESTEPS = 0
	
	DONE = False
	#This actually is probably a bad idea so figure this out later
	game_loop()

def handle_events():
	global ADD_THRUST_UP, ADD_THRUST_LEFT, ADD_THRUST_RIGHT, DONE, EXIT
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			DONE = True
			EXIT = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				DONE = True
				EXIT = True
			if event.key == pygame.K_r:
				reset_game()
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
				
def update_force():
	global FUEL
	if ADD_THRUST_UP == True:
		PLAYER.add_force(THRUST_UP)
		FUEL -= .2
	if ADD_THRUST_LEFT == True:
		PLAYER.add_force(THRUST_LEFT)
		FUEL -= .1
	if ADD_THRUST_RIGHT == True:
		PLAYER.add_force(THRUST_RIGHT)
		FUEL -= .1
	PLAYER.add_force(GRAVITY)				

def update_labels():
	global ACCX_LABEL, ACCY_LABEL, FUEL_LABEL, TIME_LABEL
	ACCX_LABEL = FONT.render('Acceleration X: {:.2f}'.format(PLAYER.acc.x), 1, (255, 255, 0))
	ACCY_LABEL = FONT.render('Acceleration Y: {:.2f}'.format(PLAYER.acc.y), 1, (255, 255, 0))
	FUEL_LABEL = FONT.render('FUEL: {}'.format(int(FUEL)), 1, (255, 255, 0))
	TIME_LABEL = FONT.render('TIME: {}'.format(int(TIMESTEPS/60)), 1, (255, 255, 0))
	
def check_collision(): #ALL OF THE PLAYER_WIN = False LINES ARE NOT NEEDED
	global DONE, PLAYER_WIN, SCORE, SCORE_LABEL
	#If player collides with the top(Landing Pad)
	if PLAYER.pRect.colliderect(GOAL.landingPad):
		if PLAYER.acc.x < GOAL.threshold.x and PLAYER.acc.y < GOAL.threshold.y:
			if PLAYER.acc.x > -GOAL.threshold.x and PLAYER.acc.y > -GOAL.threshold.y:
				print('YOU WIN BUDDY')
				PLAYER_WIN = True
				SCORE = FUEL * 2
				SCORE += 10000 / TIMESTEPS
				SCORE_LABEL = FONT.render('SCORE: {}'.format(int(SCORE)), 1, (255, 255, 0))
				DONE = True
			else:
				print('YOU DIED BUDDY 2')
				PLAYER_WIN = False
				DONE = True
		else:
			print('YOU DIED BUDDY')
			PLAYER_WIN = False
			DONE = True
	#If player collides with any other part of the Platform
	if PLAYER.pRect.colliderect(GOAL.lowerHalf):
		print('YOU DIED BUDDY 3')
		PLAYER_WIN = False
		DONE = True
	#If player collides with any wall
	for wall in WALLS:
		if PLAYER.pRect.colliderect(wall.bounds):
			print('YOU DIED BUDDY 4')
			PLAYER_WIN = False
			DONE = True
	#If player runs out of fuel
	if FUEL <= 0:
		PLAYER_WIN = False
		DONE = True
	
def update_screen():
	WINDOW.blit(DRAW_SCREEN, (0, 0))	
	PLAYER_SCREEN.fill(BACKGROUND_COLOR)
	
	for wall in WALLS:
		wall.draw_self(PLAYER_SCREEN)
		
	GOAL.draw_self(PLAYER_SCREEN)
	
	if PLAYER.isAlive == True:
		PLAYER.draw_self(PLAYER_SCREEN)
		
	WINDOW.blit(PLAYER_SCREEN, (0,0))
	WINDOW.blit(ACCX_LABEL, (0,0))
	WINDOW.blit(ACCY_LABEL, (0,15))
	WINDOW.blit(FUEL_LABEL, (0,30))
	WINDOW.blit(TIME_LABEL, (0,45))
	
	if DONE == True:
		if PLAYER_WIN == True:
			WINDOW.blit(YOU_WIN_LABEL, (250,200))
			WINDOW.blit(SCORE_LABEL, (250,230))
		else:
			WINDOW.blit(YOU_LOSE_LABEL, (250,200))
		WINDOW.blit(REPLAY_LABEL, (250,215))
	
	pygame.display.flip()

def update_time():
	global TIMESTEPS
	TIMESTEPS += 1
	CLOCK.tick(60)	
	
def end_screen():
	update_screen()
	
def game_loop():
	while not DONE:
		handle_events()
		update_positions(1)
		update_force()
		update_labels()
		check_collision()
		update_screen()
		update_time()
	while not EXIT:
		handle_events()
		end_screen()
		CLOCK.tick(60)

#Player Object
PLAYER = Lander(True, Vec2d(400,300), Vec2d(0,0))
#Goal Object
GOAL = Platform(Vec2d(random.randint(100,700), random.randint(100,500)), Vec2d(1,1))
#Wall Object - Top, Bot, Left, Right
WALLS = [Wall(pygame.Rect(0,0,800,1)), Wall(pygame.Rect(0,599,800,1)), Wall(pygame.Rect(0,0,1,600)), Wall(pygame.Rect(799,0,1,600))]
		
def main():
	global FONT
	pygame.display.set_caption('Lunar Lander')
	game_loop()
	
	del FONT
	pygame.display.quit()
	pygame.quit()
	
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e
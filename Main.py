import pygame
import random
import os
from pygame import mixer
from spritesheet import SpriteSheet
from inimigo import Inimigo

# inicar o pygame
mixer.init()
pygame.init()

#Dimensoes da tela 
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

#janela do game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pokémon Jump')

#FrameRate do jogo
clock = pygame.time.Clock()
FPS = 70

#importando a musica e o som do jogo
pygame.mixer.music.load('assets/musicas_Pokemon.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1, 0.0)
jump_fx = pygame.mixer.Sound('assets/jump.mp3')
jump_fx.set_volume(0.4)
death_fx = pygame.mixer.Sound('assets/death.mp3')
death_fx.set_volume(0.3)


#variaveis do jogo
SCROLL_THRESH = 200
GRAVITY = 1
MAX_PLATFORMS = 10
scroll = 0
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0

if os.path.exists('score.txt'):
	with open('score.txt', 'r') as file:
		high_score = int(file.read())
else:
	high_score = 0

#pegando as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL = (153, 217, 234)

#fonte da letra
font_small = pygame.font.SysFont('assets/8-BIT WONDER.TTF', 30)
font_big = pygame.font.SysFont('assets/8-BIT WONDER.TTF', 24)

#importando as imagens
pokemon_image = pygame.image.load('assets/172.png').convert_alpha()
bg_image = pygame.image.load('assets/nuvens.png').convert_alpha()
platform_image = pygame.transform.scale(pygame.image.load('assets/ven.png'),(700,800))
#charizard spritesheet
charizard_sheet_img = pygame.image.load('assets/teste10.png').convert_alpha()
charizard_sheet = SpriteSheet(charizard_sheet_img)
#funcao para escrever o texto na tela 
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#funcao para escrever informacoes na tela
def draw_panel():
	pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
	pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)
	draw_text('Pontuação: ' + str(score), font_small, WHITE, 0, 0)


#funcao para desenhar a tela de fundo
def draw_bg(bg_scroll):
	screen.blit(bg_image, (0, 0 + bg_scroll))
	screen.blit(bg_image, (0, -600 + bg_scroll))

#player class
class Player():
	def __init__(self, x, y):
		self.image = pygame.transform.scale(pokemon_image, (45, 45))
		self.width = 25
		self.height = 40
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = (x, y)
		self.vel_y = 0
		self.flip = False

	def move(self):
		#resetando as  variaveis
		scroll = 0
		dx = 0
		dy = 0

		#teclas
		key = pygame.key.get_pressed()
		if key[pygame.K_a]:
			dx = -10
			self.flip = True
		if key[pygame.K_d]:
			dx = 10
			self.flip = False

		#gravidade
		self.vel_y += GRAVITY
		dy += self.vel_y

		#fazendo com que o boneco não saia da teela
		if self.rect.left + dx < 0:
			dx = -self.rect.left
		if self.rect.right + dx > SCREEN_WIDTH:
			dx = SCREEN_WIDTH - self.rect.right


		#colisao com as plataformas
		for platform in platform_group:
			#collision in the y direction
			if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				#check if above the platform
				if self.rect.bottom < platform.rect.centery:
					if self.vel_y > 0:
						self.rect.bottom = platform.rect.top
						dy = 0
						self.vel_y = -20
						jump_fx.play()
#verifciar se o jogador chegou no topo da tela
		if self.rect.top <= SCROLL_THRESH:
			#if player is jumping
			if self.vel_y < 0:
				scroll = -dy
		self.rect.x += dx
		self.rect.y += dy + scroll
		
		
		#update mask
		self.mask = pygame.mask.from_surface(self.image)

		return scroll

	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))

#platform class
class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, height, moving):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(platform_image, (height, 40))
		self.moving = moving
		self.move_counter = random.randint(0, 50)
		self.direction = random.choice([-1, 1])
		self.speed = random.randint(1, 2)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, scroll):
		#moving platform side to side if it is a moving platform
		if self.moving == True:
			self.move_counter += 1
			self.rect.x += self.direction * self.speed

		#change platform direction if it has moved fully or hit a wall
		if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
			self.direction *= -1
			self.move_counter = 0

		#update platform's vertical position
		self.rect.y += scroll

		#check if platform has gone off the screen
		if self.rect.top > SCREEN_HEIGHT:
			self.kill()

#player instance
pokemon = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

#create sprite groups
platform_group = pygame.sprite.Group()
inimigo_group = pygame.sprite.Group()

#plataforma inicial
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
platform_group.add(platform)

#game loop
run = True
while run:

	clock.tick(FPS)

	if game_over == False:
		scroll = pokemon.move()

		#draw background
		bg_scroll += scroll
		if bg_scroll >= 600:
			bg_scroll = 0
		draw_bg(bg_scroll)

		#generate platforms
		if len(platform_group) < MAX_PLATFORMS:
			p_w = random.randint(40, 60)
			p_x = random.randint(0, SCREEN_WIDTH - p_w)
			p_y = platform.rect.y - random.randint(80, 120)
			p_type = random.randint(1, 2)
			if p_type == 1 and score > 500:
				p_moving = True
			else:
				p_moving = False
			platform = Platform(p_x, p_y, p_w, p_moving)
			platform_group.add(platform)

		#update platforms
		platform_group.update(scroll)

		#generate enemies
		if len(inimigo_group) == 0 and score > 1650:
			inimigo = Inimigo(SCREEN_WIDTH, 150, charizard_sheet, 2.0)
			inimigo_group.add(inimigo)

		#update enemies
		inimigo_group.update(scroll, SCREEN_WIDTH)

		#update score
		if scroll > 0:
			score += scroll

		#draw line at previous high score
		pygame.draw.line(screen, WHITE, (0, score - high_score + SCROLL_THRESH), (SCREEN_WIDTH, score - high_score + SCROLL_THRESH), 3)
		draw_text('HIGH SCORE', font_small, WHITE, SCREEN_WIDTH - 130, score - high_score + SCROLL_THRESH)

		#draw sprites
		platform_group.draw(screen)
		inimigo_group.draw(screen)
		pokemon.draw()

		#draw panel
		draw_panel()

		#check game over
		if pokemon.rect.top > SCREEN_HEIGHT:
			game_over = True
			death_fx.play()
		#check for collision with enemies
		if pygame.sprite.spritecollide(pokemon, inimigo_group, False):
			if pygame.sprite.spritecollide(pokemon, inimigo_group, False, pygame.sprite.collide_mask):
				game_over = True
				death_fx.play()
	else:
		if fade_counter < SCREEN_WIDTH:
			fade_counter += 5
			for y in range(0, 6, 2):
				pygame.draw.rect(screen, BLACK, (0, y * 100, fade_counter, 100))
				pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, (y + 1) * 100, SCREEN_WIDTH, 100))
		else:
			draw_text('GAME OVER!', font_big, WHITE, 130, 200)
			draw_text('PONTUAÇÃO: ' + str(score), font_big, WHITE, 130, 250)
			draw_text('PRESSIONE ESPACO PARA JOGAR DE NOVO', font_big, WHITE, 15, 400)
			#update high score
			if score > high_score:
				high_score = score
				with open('score.txt', 'w') as file:
					file.write(str(high_score))
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE]:
				#reset variables
				game_over = False
				score = 0
				scroll = 0
				fade_counter = 0
				#reposition pokemon
				pokemon.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
				#reset enemies
				inimigo_group.empty()
				#reset platforms
				platform_group.empty()
				#create starting platform
				platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
				platform_group.add(platform)


	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			#update high score
			if score > high_score:
				high_score = score
				with open('score.txt', 'w') as file:
					file.write(str(high_score))
			run = False


	#update display window
	pygame.display.update()



pygame.quit()

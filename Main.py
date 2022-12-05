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
pygame.mixer.music.play(0, 0.5)
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

#funcao para excrever informacoes na tela
def draw_panel():
	pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
	pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)
	draw_text('SCORE: ' + str(score), font_small, WHITE, 0, 0)


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
		

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

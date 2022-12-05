import pygame
import random

class Inimigo(pygame.sprite.Sprite):
	def __init__(self, SCREEN_WIDTH, y, sprite_sheet, scale):
		pygame.sprite.Sprite.__init__(self)
		#define variables
		self.animation_list = []
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()
		self.direction = random.choice([-1, 1])
		if self.direction == 1:
			self.flip = True
		else:
			self.flip = False
      
    #numero de sprites do charizard
		animation_steps = 1
		for animation in range(animation_steps):
			image = sprite_sheet.get_image(animation, 20 ,20, scale, (0, 0, 0))
			image = pygame.transform.flip(image, self.flip, False)
			image.set_colorkey((0, 0, 0))
			self.animation_list.append(image)

import pygame


# Button class
class Button():
	def __init__(self, x, y, text, text_rgb, hover_text_rgb, font, scale, surface):
		text_img = font.render(text, True, text_rgb, (255,0,0))
		hover_text_img = font.render(text, True, hover_text_rgb, (255,0,0))
		surface.blit(text_img, (x, y))
		width = text_img.get_width()
		height = text_img.get_height()
		self.text_img = pygame.transform.scale(text_img, (int(width * scale), int(height * scale)))
		self.hover_text_img = pygame.transform.scale(hover_text_img, (int(width * scale), int(height * scale)))
		self.rect = self.text_img.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False


	def draw(self, surface):
		action = False

		# get mouse position
		pos = pygame.mouse.get_pos()

		# check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			surface.blit(self.hover_text_img, (self.rect.x, self.rect.y))
			pygame.display.update()
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
		else:
			surface.blit(self.text_img, (self.rect.x, self.rect.y))
			pygame.display.update()


		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		return action

# Button_area class (for overlaying a rectangle button on pokecard)
class Button_card():
	def __init__(self, x, y, img, hover_colourRGBA, surface):
		self.hover_colourRGBA = hover_colourRGBA
		self.hover_img = (x, y, img.get_width(), img.get_height())
		self.img = img
		self.rect = self.img.get_rect()
		self.rect.topleft = x, y
		self.clicked = False


	def draw(self, surface):
		action = False

		# get mouse position
		pos = pygame.mouse.get_pos()

		# check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			pygame.draw.rect(surface, self.hover_colourRGBA, (self.hover_img), 13, 15)
			pygame.display.update()
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
		else:
			pygame.draw.rect(surface, (255, 225, 101), (self.hover_img), 13, 15)  # matches yellow border
			pygame.display.update()

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		return action
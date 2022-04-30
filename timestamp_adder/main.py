import pygame
import audioUtils
from audioWindow import AudioWindow

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode([1000, 300])
m = audioUtils.musicPlayer('./ogg/Fearless--Mr. Perfectly Fine.ogg')
a = AudioWindow(screen, m)



running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:	
			a.handleKeyDownEvent(event)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if AudioWindow.WIN_RECT.collidepoint(event.pos) and event.button == 1:
				a.handleLeftClickEvent(event)
			elif AudioWindow.WIN_RECT.collidepoint(event.pos) and (event.button == 4 or event.button == 5):
				a.handleScrollEvent(event)


	screen.fill((255, 255, 255))
	a.draw()

	pygame.display.flip()

pygame.mixer.quit()
pygame.quit()
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
			#pass the event to the AudioWindow
			a.handleEvent(event)
			


	print(f"position: {m.get_pos()}")

	screen.fill((255, 255, 255))
	a.draw()

	pygame.display.flip()

pygame.mixer.quit()
pygame.quit()
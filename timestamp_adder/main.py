# Simple pygame program

# Import and initialize the pygame library
import pygame
import audioUtils
pygame.init()
pygame.mixer.init()

# Set up the drawing window
screen = pygame.display.set_mode([1000, 300])

m = audioUtils.musicPlayer('./ogg/Fearless--Mr. Perfectly Fine.ogg')

# print(f"The length of the sound is {sound.get_length()}")
# Run until the user asks to quit
running = True
while running:
	# Did the user click the window close button?
	print(f"position: {m.get_pos()}")
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.mixer.quit()
			running = False
		elif event.type == pygame.KEYDOWN:
			print(f'key: {event.key}')
			if event.key == pygame.K_SPACE:
				if not m.is_paused:
					m.pause()
				else:
					m.unpause()
			elif event.key == 101:  # 101 is the 'e' key
				m.set_pos(270)
			elif event.key == 102: #'f' key
				m.set_pos(170)
			elif event.key == 103: #'g' key
				print(f"position: {m.get_pos()}")
			elif event.key == 114:  # 114 is the 'r' key
				print(pygame.mixer.music.get_pos())

	# Fill the background with white
	screen.fill((255, 255, 255))

	# Draw a solid blue circle in the center
	pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

	# Flip the display
	pygame.display.flip()

# Done! Time to quit.
pygame.quit()
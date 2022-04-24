import pygame

class AudioWindow:
	XMIN = 50
	YMIN = 50
	XMAX = 950
	YMAX = 150
	WIN_WIDTH = XMAX - XMIN
	WIN_HEIGHT = YMAX - YMIN
	WIN_RECT = pygame.Rect(XMIN, YMIN, WIN_WIDTH, WIN_HEIGHT)

	def __init__(self, screen, musicPlayer):
		self.screen = screen
		self.musicPlayer = musicPlayer
	def draw(self):
		m = self.musicPlayer
		pygame.draw.rect(self.screen, (0,0,0), AudioWindow.WIN_RECT)
		x_coord = (m.get_pos()/m.length)* AudioWindow.WIN_WIDTH + AudioWindow.XMIN
		pygame.draw.line(self.screen, (255, 0,0), (x_coord, AudioWindow.YMIN), (x_coord, AudioWindow.YMAX))

	def handleKeyDownEvent(self, event):
		m = self.musicPlayer
		if event.key == pygame.K_SPACE:
			if not m.is_paused:
				m.pause()
			else:
				m.unpause()
	def handleLeftClickEvent(self, event):
		m = self.musicPlayer
		x = event.pos[0]
		XMIN, WIN_WIDTH = AudioWindow.XMIN, AudioWindow.WIN_WIDTH
		m.set_pos((x-XMIN)/WIN_WIDTH * m.length)
		
		
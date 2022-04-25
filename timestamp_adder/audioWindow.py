import pygame

class AudioWindow:
	XMIN = 50
	YMIN = 50
	XMAX = 950
	YMAX = 150
	WIN_WIDTH = XMAX - XMIN
	WIN_HEIGHT = YMAX - YMIN
	WIN_RECT = pygame.Rect(XMIN, YMIN, WIN_WIDTH, WIN_HEIGHT)
	MAXSCALE = 5
	SCROLL_UNIT = 0.068

	def __init__(self, screen, musicPlayer):
		self.screen = screen
		self.musicPlayer = musicPlayer

		self.scale = 1
		# scale is a variable which is always at least 1. Bigger numbers mean more zoomed in.
		self.window_start_pos = 0
		#the position, in milliseconds, of the start of the window.
	def draw(self):
		m = self.musicPlayer
		pygame.draw.rect(self.screen, (0,0,0), AudioWindow.WIN_RECT)
		x_coord = self.convertTimeFactorToScreenPos(m.get_pos()/m.length)
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
		m.set_pos(self.convertScreenPosToTimeFactor(x) * m.length)
	def handleScrollEvent(self, event):
		if event.button == 4:
			#zoom in
			if self.scale < AudioWindow.MAXSCALE:
				self.scale += AudioWindow.SCROLL_UNIT
		elif event.button == 5:
			#zoom out
			if self.scale > 1:
				self.scale -= AudioWindow.SCROLL_UNIT
	def convertTimeFactorToScreenPos(self, time_factor):
		# input as a proportion: 0 meaning start of song, 1 meaning end of song
		# this function uses self.scale and self.window_start_pos to calculate a position.
		return ((time_factor - self.window_start_pos)* self.scale)* AudioWindow.WIN_WIDTH + AudioWindow.XMIN
	def convertScreenPosToTimeFactor(self, screen_pos):
		return (screen_pos - AudioWindow.XMIN)/(self.scale * AudioWindow.WIN_WIDTH) + self.window_start_pos
	
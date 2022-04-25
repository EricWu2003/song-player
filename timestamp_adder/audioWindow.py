import pygame

class AudioWindow:
	XMIN = 50
	YMIN = 50
	XMAX = 950
	YMAX = 150
	XMID = (XMIN + XMAX)/2
	WIN_WIDTH = XMAX - XMIN
	WIN_HEIGHT = YMAX - YMIN
	WIN_RECT = pygame.Rect(XMIN, YMIN, WIN_WIDTH, WIN_HEIGHT)

	MAXSCALE = 100
	SCROLL_FACTOR = 1.07

	def __init__(self, screen, musicPlayer):
		self.screen = screen
		self.musicPlayer = musicPlayer

		self.scale = 1

		self.timestamps = list(range(0, int(self.musicPlayer.length), 5000))
	def draw(self):
		pygame.draw.rect(self.screen, (0,0,0), AudioWindow.WIN_RECT)
		pygame.draw.line(self.screen, (255,0,0), (AudioWindow.XMID, AudioWindow.YMIN), (AudioWindow.XMID, AudioWindow.YMAX))
		for t in self.timestamps:
			x_coord = self.convertTimeToScreenPos(t)
			pygame.draw.line(self.screen, (0,255,0), (x_coord, AudioWindow.YMIN), (x_coord, AudioWindow.YMAX))

	def convertTimeToScreenPos(self, time):
		#time input in milliseconds
		delta = (time - self.musicPlayer.get_pos())/self.musicPlayer.length * (AudioWindow.WIN_WIDTH/2)
		delta *= self.scale
		return AudioWindow.XMID + delta

	def convertScreenPosToTime(self, screen_pos):
		return (screen_pos - AudioWindow.XMID) * self.musicPlayer.length/ ((AudioWindow.WIN_WIDTH/2) * self.scale) + self.musicPlayer.get_pos()


	def handleKeyDownEvent(self, event):
		m = self.musicPlayer
		if event.key == pygame.K_SPACE:
			if not m.is_paused:
				m.pause()
			else:
				m.unpause()

	def handleLeftClickEvent(self, event):
		# set the position of the music player to whereever the user clicked,
		# if the click is within the range of the music
		new_pos = self.convertScreenPosToTime(event.pos[0])
		print(new_pos)
		if 0 < new_pos and new_pos < self.musicPlayer.length:
			self.musicPlayer.set_pos(new_pos)

	def handleScrollEvent(self, event):
		if event.button == 4:
			#zoom in
			if self.scale < AudioWindow.MAXSCALE:
				self.scale *= AudioWindow.SCROLL_FACTOR
		elif event.button == 5:
			#zoom out
			if self.scale > 1:
				self.scale /= AudioWindow.SCROLL_FACTOR

		
		
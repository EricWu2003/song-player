import pygame
import json
from os.path import exists


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

	def __init__(self, screen, musicPlayer, lyrics, export_path):
		self.screen = screen
		self.musicPlayer = musicPlayer

		self.scale = 1

		self.timestamps = [0]
		self.bigFont = pygame.font.Font('freesansbold.ttf', 32)
		self.smallFont = pygame.font.Font('freesansbold.ttf', 17)
		self.lyrics = lyrics
		self.export_path = export_path
		if exists(export_path):
			print("Importing timestamps from previous save")
			with open(export_path) as f:
				self.timestamps = [i[0] for i in json.load(f)]
		self.dragRects = []
		self.dragIndices = []
		self.dragIndex = -1 # a dragIndex of -1 means nothing is being dragged
		self.dragLimits = (None, None)
	def draw(self):
		pygame.draw.rect(self.screen, (0,0,0), AudioWindow.WIN_RECT)

		min_time_to_draw = self.convertScreenPosToTime(AudioWindow.XMIN)
		max_time_to_draw = self.convertScreenPosToTime(AudioWindow.XMAX)

		self.dragRects = []
		self.dragIndices = []
		for index,t in enumerate(self.timestamps):
			if t < min_time_to_draw:
				continue
			if t > max_time_to_draw:
				break
			x_coord = self.convertTimeToScreenPos(t)
			pygame.draw.line(self.screen, (0,255,0), (x_coord, AudioWindow.YMIN), (x_coord, AudioWindow.YMAX))
			size = (15,20)
			dragRect = pygame.Rect((x_coord - size[0]/2, AudioWindow.YMIN, 
				size[0], size[1]))
			self.dragRects.append(dragRect)
			self.dragIndices.append(index)
			pygame.draw.rect(self.screen, (0,255,255), dragRect)
		pygame.draw.line(self.screen, (255,0,0), (AudioWindow.XMID, AudioWindow.YMIN), (AudioWindow.XMID, AudioWindow.YMAX))
		
		currWordIndex = self.getCurrWordIndex()
		currWordText = self.bigFont.render(self.lyrics[currWordIndex], True, (0,0,0))
		self.screen.blit(currWordText, (AudioWindow.XMIN,0))
		
		nextFewWords = " ".join(self.lyrics[currWordIndex:currWordIndex+20])
		nextFewWordsText = self.smallFont.render(nextFewWords, True, (0,0,0))
		self.screen.blit(nextFewWordsText, (AudioWindow.XMIN, AudioWindow.YMAX))


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
		elif event.key == pygame.K_RSHIFT: #if the right shift key is pressed
			
			if self.getCurrWordIndex() == len(self.lyrics) - 1:
				# If we are at the end of the lyrics
				return
			if self.getCurrWordIndex() < len(self.timestamps)-1:
				# If we are somewhere in the middle
				return
			self.timestamps.append(self.musicPlayer.get_pos())
		elif event.key == pygame.K_e: #if the 'e' key is pressed
			self.exportTimestamps()

	def handleLeftClickEvent(self, event):
		# set the position of the music player to whereever the user clicked,
		# if the click is within the range of the music
		for index, rect in zip(self.dragIndices, self.dragRects):
			if rect.collidepoint(event.pos) and self.musicPlayer.is_paused:
				self.dragIndex = index
				min_limit = 0 if index == 0 else self.timestamps[index-1]
				max_limit = self.musicPlayer.length if index == len(self.timestamps) - 1 else self.timestamps[index+1]
				self.dragLimits = (min_limit, max_limit)
				return
		new_pos = self.convertScreenPosToTime(event.pos[0])
		# print(new_pos)
		if 0 < new_pos and new_pos < self.musicPlayer.length:
			self.musicPlayer.set_pos(new_pos)

	def handleMouseMotionEvent(self, event):
		if self.dragIndex == -1:
			return
		position = self.convertScreenPosToTime(event.pos[0])
		position = max(self.dragLimits[0], position)
		position = min(self.dragLimits[1], position)
		self.timestamps[self.dragIndex] = position
	
	def handleMouseUpEvent(self, event):
		self.dragIndex = -1
		self.dragLimits = (None, None)

	def handleScrollEvent(self, event):
		if event.button == 4:
			#zoom in
			if self.scale < AudioWindow.MAXSCALE:
				self.scale *= AudioWindow.SCROLL_FACTOR
		elif event.button == 5:
			#zoom out
			if self.scale > 1:
				self.scale /= AudioWindow.SCROLL_FACTOR

	def getCurrWordIndex(self):
		currPos = self.musicPlayer.get_pos()
		for index, timestamp in enumerate(self.timestamps):
			if timestamp > currPos:
				return index - 1
		return len(self.timestamps) - 1
	
	def exportTimestamps(self):
		print(f"exporting to {self.export_path} ...")
		with open(self.export_path, 'w') as f:
			obj = list(zip(self.timestamps, self.lyrics))
			f.write(json.dumps(obj, indent = 2))
		print("Done exporting.")
	
	def deleteAllTimestampsAfterCursor(self):
		currPos = self.musicPlayer.get_pos()
		self.timestamps = [x for x in self.timestamps if x < currPos]
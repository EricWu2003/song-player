import pygame
import audioUtils
from audioWindow import AudioWindow
import json

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode([1000, 300])

ALBUM = "Fearless"
SONG = "Don't You"
pygame.display.set_caption(f'{ALBUM}--{SONG}')

m = audioUtils.musicPlayer(f'./ogg/{ALBUM}--{SONG}.ogg')

with open(f'./lyrics-compiled/{ALBUM}--{SONG}.txt') as f:
	lyrics = json.load(f)['words']
a = AudioWindow(screen, m, lyrics, f'./timestamp_adder/timestamps/{ALBUM}--{SONG}.json')

deleteButtonFont = pygame.font.Font('freesansbold.ttf', 22)
deleteButtonWords = deleteButtonFont.render("Click to delete all timestamps after cursor", True, (0,0,0))
deleteButtonRect = pygame.Rect((100, 200, 100, 22))

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
			elif deleteButtonRect.collidepoint(event.pos) and event.button == 1:
				a.deleteAllTimestampsAfterCursor()

		elif event.type == pygame.MOUSEMOTION:
			a.handleMouseMotionEvent(event)
		elif event.type == pygame.MOUSEBUTTONUP:
			a.handleMouseUpEvent(event)


	screen.fill((255, 255, 255))

	screen.blit(deleteButtonWords, deleteButtonRect)

	a.draw()

	pygame.display.flip()

pygame.mixer.quit()
pygame.quit()
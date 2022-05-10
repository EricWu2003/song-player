import pygame
import json
import os
from timestamp_adder.audioUtils import musicPlayer


def play(album, song, startWordIndex, endWordIndex):
	pygame.display.set_caption(f'{album}--{song}')
	with open(f'./timestamp_adder/timestamps/{album}--{song}.json') as f:
		timestamps = [x[0] for x in json.load(f)]
	
	musicPlayer.playPortion(f'./ogg/{album}--{song}.ogg', timestamps[startWordIndex], timestamps[endWordIndex])

def searchByCharacter(characterStr):
	songs = []
	song_names = []

	timestamp_dir = "./timestamp_adder/timestamps"
	for filename in os.listdir(timestamp_dir):
		filepath = os.path.join(timestamp_dir, filename)
		if os.path.isfile(filepath) and filepath.endswith('.json'):
			with open(filepath) as f:
				songs.append(json.load(f))
				song_names.append((filename.strip(".json").partition("--")[0],filename.strip(".json").partition("--")[2]))
	
	results=  []
	for songIndex, song in enumerate(songs):
		for searchIndex in range(0, len(song) - len(characterStr) + 1):
			if all([song[searchIndex+d][1].lower().startswith(characterStr[d]) for d in range(0, len(characterStr))]):
				results.append({"song":song_names[songIndex], "index":searchIndex})

searchByCharacter("mpf")

# play("Fearless", "Mr. Perfectly Fine", 403, 407)

for index in (1, 91, 129, 232, 270, 364, 403):
	play("Fearless", "Mr. Perfectly Fine", index, index + 3)
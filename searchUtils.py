import pygame
import json
import os
from timestamp_adder.audioUtils import musicPlayer


def play(song_obj):
	album, song = song_obj["song"]
	startWordIndex = song_obj["index"]
	endWordIndex = startWordIndex + song_obj["length"]
	pygame.display.set_caption(f'{album}--{song}')
	with open(f'./timestamp_adder/timestamps/{album}--{song}.json') as f:
		timestamps = [x[0] for x in json.load(f)]
	
	musicPlayer.playPortion(f'./ogg/{album}--{song}.ogg', timestamps[startWordIndex], timestamps[endWordIndex])

def searchByCharacter(characterStr):
	# Takes in a character string and returns a list of results of songs which match that character string.
	# A result contains the starting index and length of the match.
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
				results.append({"song":song_names[songIndex], "index":searchIndex, "length":len(characterStr)})
	return results

def searchByCharacterRange(begin, end):
	start_results = searchByCharacter(begin)
	end_results = searchByCharacter(end)
	results = []
	for start_res in start_results:
		for end_res in [x for x in end_results if x['song'] == start_res['song']]:
			if end_res["index"] < start_res["index"] + start_res["length"]:
				# Filter out any instances of overlapping start_res and end_res
				continue
			results.append({"song":start_res['song'], "index":start_res["index"], "length": end_res["index"] + end_res["length"] - start_res["index"]})
	return results

if __name__ == "__main__":
	print("running as main")


import json
import os
from os.path import join

raw_lyric_dir = "lyric-guessing-game/lyrics"
comp_lyric_dir = "lyric-guessing-game/lyrics-compiled"
working_dir = "/Users/ericwu/Desktop/song-player"

def read_file(FILE_IN):

	words = []
	with open(FILE_IN, 'r') as f:
		for currLine, line in enumerate(f.readlines()):
			currLine += 1
			line = line.strip()
			#skip blank lines
			if line == "":
				continue
			#process song section labels:
			if line.startswith("["):
				if not line.endswith("]"):
					print(f"conversion error on {FILE_IN}")
					return f"Missing closing bracket expected on line {currLine}."
				continue

			#check for inappropriate use of dashes: only double dashes are allowed
			# if "-" in line.replace("--", "") or "---" in line:
			# 	return f"Bad use of dashes on line {currLine}."
			
			
			filteredLine = ""
			for char in line:
				if char in ('"', "'", "(", ")", ",", "."): #we filter out these characters
					continue
				filteredLine += char
			words += list(filteredLine.split())
			words += list(line.split(' '))
			
	
	return words

os.chdir(working_dir)
os.chdir(raw_lyric_dir)
# album_titles = [name.partition("_")[2] for name in os.listdir(".") if os.path.isdir(name)]
album_titles = [name for name in os.listdir(".") if os.path.isdir(name)]

os.chdir(working_dir)
all_lyrics = {}
for album in album_titles:
	os.chdir(join(working_dir, raw_lyric_dir, album))
	for path in os.listdir("."):
		if not os.path.isfile(path):
			continue
		print(album, path)

	album_formatted = album.partition("_")[2]
	name = os.path.splitext(path.partition("_")[2])[0]
	all_lyrics[f"{album_formatted}--{name}"] = read_file(path)
os.chdir(working_dir)
os.chdir(comp_lyric_dir)
with open("lyrics.json", "w") as f:
	f.write(json.dumps(all_lyrics))


print("DONE")

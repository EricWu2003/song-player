import json
import os

f1 = "lyrics/Fearless--Mr. Perfectly Fine.txt"
f2 = "lyrics-compiled/Fearless--Mr. Perfectly Fine.txt"
lyrics_dir = "./lyrics"
lyrics_out_dir = "./lyrics-compiled"

def read_file(FILE_IN):

	words = []
	sections = {}
	currSection = None
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
					return f"Missing closing bracket expected on line {currLine}."
				sectionName = line[1:-1]

				if sectionName in sections.keys():
						return f"Duplicate section on line {currLine}."

				if currSection is not None:
					#if we have a currSection that we need to close:
					sections[currSection].append(len(words))
				sections[sectionName] = [len(words)]
				currSection = sectionName
				continue
			#check for inappropriate use of dashes: only double dashes are allowed
			if "-" in line.replace("--", "") or "---" in line:
				return f"Bad use of dashes on line {currLine}."
			
			
			filteredLine = ""
			for char in line:
				if char.isalnum() or char == " " or char == "-":
					filteredLine += char
			words += list(filteredLine.split(' '))
			
	
	return {"words":words, "sections":sections}
def convertLyrics(fin, fout):
	with open(fout, 'w') as f:
		f.write(json.dumps(
			read_file(fin), indent=4
		))

for filename in os.listdir(lyrics_dir):
	fin = os.path.join(lyrics_dir, filename)
	fout = os.path.join(lyrics_out_dir, filename)
	if os.path.isfile(fin) and filename.endswith('txt'):
		convertLyrics(fin, fout)

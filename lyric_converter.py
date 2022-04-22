from asyncore import read
import json


f1 = "lyrics/Fearless--Mr. Perfectly Fine.txt"
f2 = "lyrics-compiled/Fearless--Mr. Perfectly Fine.txt"


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
                    return f"Missing closing bracket expected on line {currLine}"
                sectionName = line[1:-1]
                if currSection is not None:
                    sections[currSection].append(len(words))
                sections[sectionName] = [len(words)]
                currSection = sectionName
                continue
            #check for inappropriate use of dashes: only double dashes are allowed
            if "-" in line.replace("--", ""):
                return f"Bad use of dashes on line {currLine}"
            
            filteredLine = ""
            for char in line:
                if char.isalnum() or char == " " or char == "-":
                    filteredLine += char
            words += list(filteredLine.split(' '))
            
    
    return words, sections
        
print(read_file(f1))
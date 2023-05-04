#!/usr/bin/env python3.10

# to run this script: ./import_es_ja_script.py -es spanish* -ja textmap_ja*
# Doesn't work? Drag and drop the files into the command line window manually then


import sys
import re
from typing import Dict,List,Any, Union, Literal, Tuple

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def printWarn(text:str):
	print(bcolors.WARNING + text + bcolors.ENDC)
	
def printError(text:str):
	print(bcolors.FAIL + text + bcolors.ENDC)
	
def printOK(text:str):
	print(bcolors.OKGREEN + text + bcolors.ENDC)

# It's unnecessary to know the character since we're matching by exact text
def getQuoteNoCharacter(line:str) -> List[str]:
	return re.findall(r"(?=[\"'])(?:\"[^\"\\]*(?:\\[\s\S][^\"\\]*)*\")",line)

def isARenpyCommand(line:str):
	cmnds = ['call','scene','play','stop','with','show','hide','while','jump','$']
	l = line.lstrip()
	for cmd in cmnds:
		if l.startswith(cmd+' '):
			return True
	return False

def keyOrNone(d:dict,k:Any) -> Union[Any,None]:
	try:
		return d[k]
	except:
		return None

def findIndent(s:str) -> int:
	for i in range(len(s)):
		if s[i]!=" ":
			return i
	return 0

# Considering the values stored in mapping are the same,
# wouldn't some kind of linked list or a list of indexes to
# the lines make more sense?
class MappingStruct:
	
	def __init__(self,language:str="??") -> None:

		self.mapping:Dict[str,str] = {}
		self.mapping_by_line:Dict[int,str] = {}
		self.mapping_choices:Dict[str,str] = {}
		self.language=language

def parseSpanishLines(spanishFiles:List[str])->MappingStruct:

	lang_es = MappingStruct("es")
	for arg_num in range(1,len(spanishFiles)):
		if 'choice' in spanishFiles[arg_num]:
			continue
		with open(spanishFiles[arg_num],'r') as f:
			printOK("Parsing "+spanishFiles[arg_num])
			lines = f.readlines()
			scrMapping=-1
			for i in range(len(lines)):
				line = lines[i]
				if line.startswith("# game/script"):
					scrMapping = int(line.rsplit(":")[-1])
				elif line.startswith("    #"):
					eng = getQuoteNoCharacter(line)
					if len(eng)==0:
						printWarn("[es] Invalid line while parsing: "+line.strip())
						#print(line[i+1])
					else:
						eng=eng[-1]
						tl = getQuoteNoCharacter(lines[i+1])
						if len(tl)>0:
							lang_es.mapping[eng]=tl[-1]
							lang_es.mapping_by_line[scrMapping]=tl[-1]
						else:
							printWarn("[es] Line had no translation!")
							print(lines[i+1].strip())
						
					#print(eng+"\t"+tl)
	print("Indexed "+str(len(lang_es.mapping))+" translated lines.")

	for fileName in spanishFiles:
		if 'choice' in fileName:
			with open(fileName,'r') as f:
				lines = f.readlines()
				print("Read "+str(len(lines))+" choice lines")
				OLD = ""
				for i in range(len(lines)):
					l = lines[i].strip()
					if l.startswith("old"):
						OLD = getQuoteNoCharacter(l)[0][1:-1]
						#print(OLD)
					elif l.startswith("new"):
						lang_es.mapping_choices[OLD]=getQuoteNoCharacter(l)[0]
			break
	return lang_es

def parseJapaneseLines(japaneseFiles:List[str])->MappingStruct:
	lang_ja = MappingStruct("ja")

	for fileName in japaneseFiles:
		with open(fileName,'r') as f:
			printOK("Parsing "+fileName)
			lines = f.readlines() #who needs good programming anyways?
			for l in lines:
				if l.startswith("#"):
					continue
				en,ja = l.split("\t")
				#Japanese translator does not know how escape characters work
				ja = ja.replace("\\「","「").replace("\\」","」")
				if "\\" in ja or "\"" in ja:
					printWarn("[ja] Invalid line while parsing: "+ja)
					continue
				if en.startswith("%"):
					lang_ja.mapping_choices[en.lstrip("% ")] = ja.lstrip("% ").rstrip()
				else:
					#DO NOT STRIP MAPPING KEYS!
					lang_ja.mapping[en] = ja.strip()
	#for k,v in lang_ja.mapping.items():
	#	print(k +" = "+v)
	#assert lang_ja.mapping["An ocean of nothingness…"]
	return lang_ja

if __name__=="__main__":
	import argparse

	parser = argparse.ArgumentParser(description="Import stuff into renpy script.rpy")
	parser.add_argument('--spanish','-es' , type=str, nargs='*',
                    help='The spanish files to import. Duh.')
	parser.add_argument('--japanese','-ja',type=str, nargs="*",
		help="The Japanese files to import. Duh."
	)
	args = parser.parse_args()
	print(args.spanish)
	print(args.japanese)

	
	lang_es = parseSpanishLines(args.spanish)
	lang_ja = parseJapaneseLines(args.japanese)
	#sys.exit(0)

	with open("script_orig.rpy",'r') as readFile:
		with open('script_cust.rpy', 'w') as writeFile:
			lineNumber = 1
			while True:
				line = readFile.readline()
				if line: #If no more lines, line is falsy (Since a blank line still has \r\n)
					if line.startswith("label"):
						label =line[6:-1]
						printOK(f"--- Entered section {label} ---")
						#if label == "day_one:":
						#	sys.exit(-1)
					elif isARenpyCommand(line) or line.strip().startswith("#"):
						pass
					elif line.startswith("    "):
						if line[-2] == ":": #If this is a branch choice
							beginQuote = line.find('"')+1
							if beginQuote>0:
								endQuote = line.find('"',beginQuote)
								txt = line[beginQuote:endQuote]
								#print(txt)
								if txt in lang_es.mapping_choices:
									line = line[:endQuote+1]+" ("+lang_es.mapping_choices[txt]+") "+line[endQuote+1:]

									if txt in lang_ja.mapping_choices:
										endTuple = line.rfind(")")
										if endTuple!=-1:
											line = line[:endTuple]+", \""+lang_ja.mapping_choices[txt]+"\""+line[endTuple:]
									else:
										printWarn("["+lang_ja.language+"] No translation for choice "+txt)
								else:
									printWarn("["+lang_es.language+"] No translation for choice "+txt)
								#pass
						else:
							dialogue = getQuoteNoCharacter(line)
							if len(dialogue)>0:
								translatedDialogue = keyOrNone(lang_es.mapping,dialogue[-1])
								if not translatedDialogue: #try again
									translatedDialogue = keyOrNone(lang_es.mapping_by_line,lineNumber)
								if translatedDialogue:
									indent = findIndent(line)
									#If no speaker, have to edit it to support translation
									#We have to specifically check if there's only one arg in the script because two args in renpy means speaker and then text
									if line[4]=="\"" and len(dialogue)<2:
										#-1 to cut off line break
										line = " "*indent + "tl None "+line[indent:-1]+" "+translatedDialogue+"\n"
									elif line[4]!="t": #Else we can insert normally
										#Cut off \n, then put it back at the end.
										line = " "*indent + "tl "+line[indent:-1] + " "+translatedDialogue+"\n"
									

									#Do Japanese after because the "tl" opcode is already inserted
									#We have to cut off the " character too, because spanish has it and japanese doesn't
									translated_ja = keyOrNone(lang_ja.mapping,dialogue[-1][1:-1])
									if translated_ja:
										#Cut off \n, add it back at the end
										line = line[:-1]+" \""+translated_ja+"\"\n"
									else:
										printWarn("[ja] No translation for text "+dialogue[-1])
								else:
									printWarn("[es] No translation for text "+dialogue[-1])


					writeFile.write(line)
					lineNumber+=1
				else:
					break


# Copyleft 2023 Amaryllis
# 
# This program is free software: you can redistribute it and/or modify it under the 
# terms of the GNU Lesser General Public License as published by the Free Software 
# Foundation, either version 2 of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied warranty of MERCHANTABILITY or 
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for 
# more details.
# 
# You should have received a copy of the GNU Lesser General Public License along with 
# this program. If not, see <https://www.gnu.org/licenses/>. 
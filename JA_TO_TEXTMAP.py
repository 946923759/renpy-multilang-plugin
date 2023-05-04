#!/usr/bin/env python3.10

import sys
import re
from typing import Dict,List,Any, Union, Literal, Tuple
from import_es_ja_script import printError, printOK, printWarn
import import_es_ja_script as rpyUtils
#import argparse

#parser = argparse.ArgumentParser(description="Verify script errors or dump textmap.tsv.")

def idxOrBlank(l:list,idx:int)->str:
	try:
		return l[idx]
	except:
		return ''

LINES:Dict[str,List[str]] = {
	'NO_LABEL':[]
}
ORIG_LINES:Dict[str,List[str]] = {
	'NO_LABEL':[]
}
for arg_num in range(1,len(sys.argv)):
	with open(sys.argv[arg_num],'r') as f:
		printOK("Parsing "+sys.argv[arg_num])
		lines = f.readlines()
		curSection = "NO_LABEL"
		for i in range(len(lines)):
			line = lines[i].strip()
			if line and not line.startswith("#"):
				line = line.replace("”",'"')
				#print(line)
				#sys.exit(-1)
				
				if line.startswith("label"):
					curSection=line.rsplit(' ',1)[-1][:-1]
					print("--- entered section "+curSection+" ---")
					continue
				elif line.endswith(":") or rpyUtils.isARenpyCommand(line):
					#print("Skipping command "+line)
					continue
				
				dialogue = rpyUtils.getQuoteNoCharacter(line)
				
				if len(dialogue)>0:
					txt = dialogue[-1]
					if "[" in line:
						txt = "% "+txt
					if curSection not in LINES:
						LINES[curSection] = []
					LINES[curSection].append(txt)
				elif ":" in line or "[" in line: #Probably a choice
					#print("Renpy choice? "+line)
					pass
				#else:
				#	print("Ignoring incorrect formatting at line "+str(i+1)+": "+line)

#sys.exit(-1)

with open("script_orig.rpy",'r') as readFile:
	curSection = "NO_LABEL"
	while True:
		line = readFile.readline()
		if line: #If no more lines, line is falsy (Since a blank line still has \r\n)
			if line.startswith("label"):
				curSection = line[6:-2]
				print("--- Entered section "+line[6:-2]+" ---")
			elif rpyUtils.isARenpyCommand(line):
				pass
			elif line.startswith("    "):
				if line[-2] == ":": #Choice
					beginQuote = line.find('"')+1
					if beginQuote>0:
						endQuote = line.find('"',beginQuote)
						txt = line[beginQuote:endQuote]
						if curSection not in ORIG_LINES:
							ORIG_LINES[curSection] = []
						ORIG_LINES[curSection].append("% "+txt)
				else:
					dialogue = rpyUtils.getQuoteNoCharacter(line)
					if len(dialogue)>0:
						if curSection not in ORIG_LINES:
							ORIG_LINES[curSection] = []
						ORIG_LINES[curSection].append(dialogue[-1])
		else:
			break

with open("textmap_ja.tsv",'w') as writeFile:
	writeFile.write("ENGLISH\tJAPANESE")
	for label in LINES:
		if label=="NO_LABEL" and len(LINES[label])==0: #Skip this section if it's empty.
			continue
		elif label not in ORIG_LINES:
			printError("Label mismatch between JA and EN script.")
			printError("Missing "+label+" from EN script.")
		else:
			writeFile.write("\n# --- "+label+" ---")

			enLines = ORIG_LINES[label]
			jaLines = LINES[label]
			for i in range(max(len(enLines),len(jaLines))):
				l1 = idxOrBlank(enLines,i)
				l2 = idxOrBlank(jaLines,i)
				writeFile.write("\n"+l1+"\t"+l2)

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
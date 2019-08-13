import os
import re

space_patten = re.compile(r'(\s+)?.*')
blank_line = re.compile(r'^(\s+|\t+)?$')

lines = []

def build_index(file):
    with open(r"d:\my_program\tools\py\ssh.py",encoding='utf-8') as f:
        lines = [ x for x in f ]

def getWhiteSpaces(line):
    spaces = 0
    m = space_patten.match(line)
    if m and m.group(1):
        spaces = len(m.group(1))
    return spaces

def getEnd(startNum):
    line = lines[startNum-1]
    startSpace = getWhiteSpaces(line)
    for i in range(startNum, len(lines)):
        if lines[i].strip().startswith('#') or blank_line.match(lines[i]):
            continue
        if getWhiteSpaces(lines[i]) <= startSpace:
            break
    i -= 1
    while True:
        if lines[i].strip().startswith('#'):
            i -= 1
            continue
        if blank_line.match(lines[i]):
            i -= 1
        else:
            break
    endNum = i + 1
    return startNum,endNum

print(getEnd(8))
print(getEnd(51))
print(getEnd(102))
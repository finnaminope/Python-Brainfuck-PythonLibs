#!/usr/bin/python
#
# Brainfuck Interpreter
# Copyright 2011 Sebastian Kaspari
#
# Usage: ./brainfuck.py [FILE]

import sys
import getch

def execute(filenameIn):
  f = open(filenameIn, "r")
  evaluate(f.read())
  f.close()


def evaluate(code):
  code     = cleanup(list(code))
  bracemap = buildbracemap(code)

  cells, codeptr, cellptr, codeExecList, queue = [0], 0, 0, [], []
  while codeptr < len(code):
    command = code[codeptr]

    if not comment:
      if command == ">":
        cellptr += 1
        if cellptr == len(cells): cells.append(0)

      if command == "<":
        cellptr = 0 if cellptr <= 0 else cellptr - 1

      if command == "+":
        cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

      if command == "-":
        cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

      if command == "/":
        filename = sys.argv[1]
        print("Program Trace (ID: " + str(cellptr) + "-" + str(cells[cellptr]) + "-" + str(codeptr) + ") At " + str(codeptr) + " in " + filename + ". This Trace Was Not Called Because of An Error In The Program.")
        print("This is the Program Code That Was Executed: ")
        for item in codeExecList:
          print(item, end="")

      if command == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
      if command == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
      if command == ".": sys.stdout.write(chr(cells[cellptr]))
      if command == ",": cells[cellptr] = ord(getch.getch())
    
      codeptr += 1
      codeExecList.append(command)

    if command == "(": comment = True
    if command == ")": comment = False


def cleanup(code):
  return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-', '/', 'i', 'o'], code))


def buildbracemap(code):
  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "[": temp_bracestack.append(position)
    if command == "]":
      start = temp_bracestack.pop()
      bracemap[start] = position
      bracemap[position] = start
  return bracemap


def main():
    filename = sys.argv[1]
    if len(sys.argv) == 2: execute(filename)
    else: print("Usage:", sys.argv[0], "filename")

if __name__ == "__main__": main()


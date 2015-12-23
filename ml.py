#!/usr/bin/env python2

"""A Mijnlieff implementation for the commandline written in python.

Mijnlieff is created by Andy Hopwood. He has no previous knowledge of this
program and did not give me explicit permission to create this.
"""

board = [ [ ' ', ' ', ' ', ' '],
          [ ' ', '#', '#', ' '],
          [ ' ', '#', '#', ' '],
          [ ' ', ' ', ' ', ' '] ]
tiles = [
  {'pusher': 2, 'puller': 2, 'diagonal': 2, 'straight': 2},
  {'pusher': 2, 'puller': 2, 'diagonal': 2, 'straight': 2}
]
placed = [[], []]

def printBoard():
  print " ---- Board ----"
  for row in board:
    print '|',
    for point in row:
      print str(point), '|',
    print "\n ---------------"

def isValid(x, y):
  return board[y][x] == ' ';

def adjacentDiag(x1, y1, x2, y2):
  """Adjacency including diagonals."""
  if 1 >= x1 - x2 >= -1 and 1 >= y1 - y2 >= -1:
    return True

  return False

def diag(x1, y1, x2, y2):
  """Tests for direct diagonalness."""
  if abs(x1 - x2) == abs(y1 - y2):
    return True

  return False

def test(command, x1, y1, x2, y2):
  if command == 'pusher':
    return adjacentDiag(x1, y1, x2, y2)
  elif command == 'puller':
    return not adjacentDiag(x1, y1, x2, y2)
  elif command == 'straight':
    return not (x1 == x2 or y1 == y2)
  elif command == 'diagonal':
    return not diag(x1, y1, x2, y2)
  else:
    return False

def abbrev(command):
  if command == 'pusher':
    return 'p'
  elif command == 'puller':
    return 'u'
  elif command == 'straight':
    return 's'
  elif command == 'diagonal':
    return 'd'
  else:
    return False

light = True

def getTurn(text):
  if light:
    text = '\033[107m\033[30m' + text
  else:
    text = '\033[40m\033[39m' + text

  return text + '\033[0m'

def hasTiles(command):
  """Method to check the tiles."""
  return tiles[light][command] >= 1

def useTile(command):
  """Method to decrement a tile."""
  if not hasTiles(command):
    print 'can\'t drecrment tile for', command

  tiles[light][command] -= 1

def run(command, x, y):
  for ycoord, row in enumerate(board):
    for xcoord, point in enumerate(row):
      if board[ycoord][xcoord] in ['#', ' ']:
        if test(command, x, y, xcoord, ycoord):
          board[ycoord][xcoord] = '#'
        else:
          board[ycoord][xcoord] = ' '

  board[y][x] = getTurn(abbrev(command))
  placed[light].append([x, y])
  useTile(command)

def blocked():
  for row in board:
    for point in row:
      if point == ' ':
        return False

  for y, row in enumerate(board):
    for x, point in enumerate(row):
      if point == '#':
        board[y][x] = ' '

  return True

def score(player):
  """Method to score the board based on what's out there."""
  for point in played[player]:
    pass

def gameEnd():
  return len(placed[True]) == 8 or len(placed[False]) == 8

inp = ''
ending = False 

while True:
  printBoard()
  print getTurn(('Light' if light else 'Dark') + '\'s turn!')
  inp = raw_input('Coordinates: ')

  if inp == 'exit':
    break
  if inp == 'tiles':
    print tiles[light]
    continue
  if inp == 'scores':
    print 'Light:', score(True)
    print 'Dark:', scores(False)

  split = inp.split(' ')
  try:
    command = split[0]
    x = int(split[1])
    y = int(split[2])
  except (IndexError, ValueError) as e :
    print inp, 'is not a valid input.'
    continue

  if not isValid(x, y):
    print str(x), str(y), 'are not valid coordinates.'
    continue

  if not abbrev(command):
    print command, 'is not a valid command.'
    continue

  if not hasTiles(command):
    print 'You have no more', command, 'tiles.'
    continue

  run(command, x, y)

  if ending:
    print 'Game is over.'
    break

  ending = gameEnd()

  if not blocked():
    light = not light

printBoard()

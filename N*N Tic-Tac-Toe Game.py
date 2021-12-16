import datetime
import random
from enum import Enum
import seaborn as sns; sns.set();

import numpy as np
from tabulate import tabulate as tb

# GLOBAL VARIABLES
user, ticAI, empty, timer = "X", "O", "_", 3


class TicTacToeState(Enum):
  draw, progress, x, o = "Draw", "In Progress", "X", "O"


# FEW CLASSES TO HANDLE EXCEPTION ERRORS/RULE VIOLATIONS
# when user move is not a digit
class NotDigit(Exception):
  pass


# when user move is a digit higher than allowable cell positions
class BeyondCellBoundaries(Exception):
  pass


# when user enters a move in an already filled cell
class FilledCell(Exception):
  pass


class TicBoard:
  def __init__(self, size):
    self.size = size
    self.board = [["_" for _ in range(size)] for _ in range(size)]
    self.finalMove = None

  def getFinalMove(self):
    return self.finalMove

  # Display TicTacToe
  def displayBoard(self):
    print("Board Filled With Numbers is Reference Board")
    referenceboard = np.arange(self.size**2).reshape(self.size, -1)
    for x in range(self.size):
      for y in range(self.size):
        if y < self.size - 1:
          print(referenceboard[x][y], end="|")
        else:
          print(referenceboard[x][y], end="")
      print()

    print(tb(self.board, tablefmt="fancy_grid"))

  def getEntireRow(self, nr):
    return self.board[nr]

  def getEntireCol(self, nc):
    return [r[nc] for r in self.board]

  #Using 0-indexing this gets the cell user selects and converts it to board cell.
  def getCell(self, cell):
    r, c = cell // self.size, cell % self.size
    return r, c

  def getEntireDiagonals(self):
    y, d1, d2 = 0, [self.board[x][x] for x in range(self.size)], []
    for x in list(range(self.size)[::-1]):  # check here
      d2.append(self.board[x][y])
      y += 1
    return d1, d2

  def getPrimaryDiag(self):
    return [self.board[x][x] for x in range(self.size)]

  def isOnPrimaryDiag(self, cell):
    return cell % (self.size + 1) == 0

  def getAltDiag(self):
    y, d2 = 0, []
    for x in list(range(self.size)[::-1]):  # check here
      d2.append(self.board[x][y])
      y += 1
    return d2

  def isOnAltDiag(self, cell):
    return cell % (self.size - 1) == 0

  def tickNothing(self, cell):
    r, c = self.getCell(cell)
    self.board[r][c] = "_"

  def tickUser(self, cell):
    self.finalMove = cell
    r, c = self.getCell(cell)
    self.board[r][c] = "X"

  def tickAI(self, cell):
    self.finalMove = cell
    r, c = self.getCell(cell)
    self.board[r][c] = "O"

  def isLineFilledSame(self, check, m):
    return all(i == m for i in check)

  def isCellEmpty(self, cell):
    r, c = self.getCell(cell)
    return self.board[r][c] == "_"


class TicTacToe:
  def __init__(self, gameSize, dtimer, users, simulate):
    self.numusers = users
    self.tGame = TicBoard(gameSize)
    self.gameSize = gameSize
    self.usernames = [' '] * users
    self.turn = None
    self.whoStartsGame()
    self.bestM = 0
    self.AIFirstMove = None
    self.dtimer = dtimer
    self.simulate = simulate

  def getUsername(self):
    accumulator = 1
    while accumulator <= self.numusers:
      try:
        if self.simulate == False:
          userN = input("Welcome to TicTacToe Game, Please Enter Player " + str(accumulator) + " Name: ")
        elif self.simulate == True:
          userN = "RandomPlayer"
        if userN is None:
          raise ValueError("Kindly enter your name")
        self.usernames[accumulator - 1] = userN
        accumulator += 1
      except ValueError as i:
        print(i)

  def getUserTick(self):
    while True:
      try:
        if self.simulate == False:
          userM = int(input(self.usernames[self.turn] + " kindly pick a cell to make your move: "))
        elif self.simulate == True:
          print("Random Player is making move...")
          userM = int(np.random.choice(self.computeValidMoves()))
        if not isinstance(userM, int):
          raise NotDigit("Integer Digits Only")
        if not self.tGame.isCellEmpty(userM):
          raise FilledCell("Cell already ticked, please tick another")
        if not (0 <= userM <= (self.gameSize ** 2 - 1)):
          raise BeyondCellBoundaries("You are ticking outside cell boundaries, please tick again")
        return userM
      except(NotDigit, FilledCell, BeyondCellBoundaries) as i:
        print(i)
      except Exception:
        print("Invalid Move")

  def whoStartsGame(self):
    whostarts = np.random.choice(["user", "AI"])
    if whostarts == "user":
      self.turn = 0
      print("After a coinflip, User will be making First Move")
    else:
      self.AIFirstMove, self.turn = random.randrange(self.tGame.size ** 2), 1
      print("After a coinflip, AI will be making First Move")

  def checkDraw(self):
    for cell in range(self.tGame.size ** 2):
      if self.tGame.isCellEmpty(cell): return False
    return True

  def checkWin(self, move):
    m = ""
    if move % 2 == 0:
      m = user
    else:
      m = ticAI
    finalM = self.tGame.getFinalMove()
    r, c = self.tGame.getCell(finalM)
    if self.tGame.isLineFilledSame(self.tGame.getEntireRow(r), m) or self.tGame.isLineFilledSame(
        self.tGame.getEntireCol(c), m):
      return True
    if self.tGame.isOnPrimaryDiag(finalM) and self.tGame.isLineFilledSame(self.tGame.getPrimaryDiag(), m):
      return True
    if self.tGame.isOnAltDiag(finalM) and self.tGame.isLineFilledSame(self.tGame.getAltDiag(), m):
      return True
    return False

  def checkTicTacToeState(self):
    if self.checkDraw(): return "Draw"
    if self.checkWin(0): return "X"
    if self.checkWin(1): return "O"
    return "In Progress"

  def computeValidMoves(self):
    valid = []
    for cell in range(self.tGame.size ** 2):
      if self.tGame.isCellEmpty(cell): valid.append(cell)
    return valid

  # THIS METHOD TAKES CARE OF THE GAME
  def BeginGame(self):
    self.getUsername()
    while True:
      self.tGame.displayBoard()
      self.turn %= 2
      if self.turn % 2 == 0:
        userM = self.getUserTick()
        self.tGame.tickUser(userM)
      else:
        print("AI is ticking a cell........ in ", str(self.dtimer), " seconds")
        if self.AIFirstMove is not None:
          aiM = self.AIFirstMove
          self.AIFirstMove = None
        else:
          aiM = self.iterativeDeepening()
        self.tGame.tickAI(aiM)
      currentResult = self.checkTicTacToeState()
      if currentResult != "In Progress":
        self.tGame.displayBoard()
        if currentResult == "Draw":
          print("GAME ENDED: DRAW!!!")
        else:
          if self.turn % 2 == 0:
            print("GAME ENDED: ", self.usernames[self.turn], "WON!!!")
          else:
            print("GAME ENDED: AI WON, YOU LOST!!!")
        break
      self.turn += 1

    # THIS IS THE PART WHERE WE UTILIZE AI SEARCH STRATEGIES SUCH AS MINIMAX AND ITERATIVE DEEPENING

  def checkLine(self, line):
    return line.count("O"), line.count("X"), line.count("_")

  def getLinePoints(self, line):
    aiPoints, userPoints, emptyPoints = self.checkLine(line)
    points = 0
    if aiPoints == 0 and userPoints != 0:
      points += -(10 ** (userPoints - 1))
    if userPoints == 0 and aiPoints != 0:
      if aiPoints == self.tGame.size:
        points += 11 ** (aiPoints - 1)
      points += 10 ** (aiPoints - 1)
    return points

  def evaluateBoard(self):
    points, d = 0, self.tGame.getEntireDiagonals()
    for cell in range(self.tGame.size):
      points += self.getLinePoints(self.tGame.getEntireRow(cell))
      points += self.getLinePoints(self.tGame.getEntireCol(cell))
    for cell in range(2):
      points += self.getLinePoints(d[cell])
    return points

  def minimax(self, height, Max, alpha, beta, start, maxtime):
    allmoves, points, cell = self.computeValidMoves(), self.evaluateBoard(), None
    if datetime.datetime.now() - start >= maxtime:
      self.timeOver = True
    if not allmoves or height == 0 or self.timeOver:
      currentResult = self.checkTicTacToeState()
      if currentResult == "X":
        return -10 ** (self.tGame.size + 1), cell
      elif currentResult == "O":
        return 10 ** (self.tGame.size + 1), cell
      elif currentResult == "Draw":
        return 0, cell
      return points, cell

    if Max==True:
      for x in allmoves:
        self.tGame.tickAI(x)
        points, temp = self.minimax(height - 1, not Max, alpha, beta, start, maxtime)
        if points > alpha:
          alpha = points
          cell, self.bestM = x, x
        self.tGame.tickNothing(x)
        if beta <= alpha: break
      return alpha, cell

    else:
      for x in allmoves:
        self.tGame.tickUser(x)
        points, temp = self.minimax(height - 1, not Max, alpha, beta, start, maxtime)
        if points < beta:
          beta = points
          cell, self.bestM = x, x
        self.tGame.tickNothing(x)
        if alpha >= beta: break
      return beta, cell

  def iterativeDeepening(self):
    height, cell, self.timeOver = 1, None, False
    beginT = datetime.datetime.now()
    endT = beginT + datetime.timedelta(0, self.dtimer)
    while True:
      runtime = datetime.datetime.now()
      if runtime >= endT:
        break
      maxi, cell = self.minimax(height, False, -10000000, 10000000, runtime, endT - runtime)
      height += 1
    if cell == None:
      cell = self.bestM
    return cell


game = TicTacToe(4, 1, 1, False)
game.BeginGame()

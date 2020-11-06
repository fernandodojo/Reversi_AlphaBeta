# Reversi
# Integrantes: Fernando Henrique F. Leite, Emily Juliana
# MINMAX PODA ALPHA-BETA
import random
import sys
import math

global max_depth
max_depth = 2

def drawBoard(board):
	# Essa funcao desenha o tabuleiro
	HLINE = '  +---+---+---+---+---+---+---+---+'
	VLINE = '  |   |   |   |   |   |   |   |   |'

	print('    1   2   3   4   5   6   7   8')
	print(HLINE)

	for y in range(8):
		print(VLINE)
		print(y+1, end=' ')
		for x in range(8):
			print('| %s' % (board[x][y]), end=' ')
		print('|')
		print(VLINE)
		print(HLINE)

def resetBoard(board):
	#Essa funcao esvazia o tabuleiro
	for x in range(8):
		for y in range(8):
			board[x][y] = ' '
	# Pecas iniciais:
	board[3][3] = 'X'
	board[3][4] = 'O'
	board[4][3] = 'O'
	board[4][4] = 'X'

def getNewBoard():
	# Criar um tabuleiro novo
	board = []
	for i in range(8):
		board.append([' '] * 8)
	return board

def isValidMove(board, tile, xstart, ystart):
	# Retorna False se o movimento em xstart, ystart é invalido
	# Se o movimento é valido, retorna uma lista de casas que devem ser viradas após o movimento
	if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
		return False
	board[xstart][ystart] = tile
	if tile == 'X':
		otherTile = 'O'
	else:
		otherTile = 'X'
	tilesToFlip = []
	for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
		x, y = xstart, ystart
		x += xdirection # first step in the direction
		y += ydirection # first step in the direction
		if isOnBoard(x, y) and board[x][y] == otherTile:
			x += xdirection
			y += ydirection
			if not isOnBoard(x, y):
				continue
			while board[x][y] == otherTile:
				x += xdirection
				y += ydirection
				if not isOnBoard(x, y):
					break
			if not isOnBoard(x, y):
				continue
			if board[x][y] == tile:
				while True:
					x -= xdirection
					y -= ydirection
					if x == xstart and y == ystart:
						break
					tilesToFlip.append([x, y])
	board[xstart][ystart] = ' '
	if len(tilesToFlip) == 0:
		return False
	return tilesToFlip

def isOnBoard(x, y):
	# Retorna True se a casa está no tabuleiro.
	return x >= 0 and x <= 7 and y >= 0 and y <=7

def getBoardWithValidMoves(board, tile):
	# Retorna um tabuleiro com os movimentos validos
	dupeBoard = getBoardCopy(board)
	for x, y in getValidMoves(dupeBoard, tile):
		dupeBoard[x][y] = '.'
	return dupeBoard

def getValidMoves(board, tile):
	# Retorna uma lista de movimentos validos
	validMoves = []
	for x in range(8):
		for y in range(8):
			if isValidMove(board, tile, x, y) != False:
				validMoves.append([x, y])
	return validMoves

def getScoreOfBoard(board):
	# Determina o score baseado na contagem de 'X' e 'O'.
	xscore = 0
	oscore = 0
	for x in range(8):
		for y in range(8):
			if board[x][y] == 'X':
				xscore += 1
			if board[x][y] == 'O':
				oscore += 1
	return {'X':xscore, 'O':oscore}

"""def enterPlayerTile():
	# Permite que o player escolha ser X ou O
	tile = ''
	while not (tile == 'X' or tile == 'O'):
		print('Escolha suas peças: X ou O?')
		tile = input().upper()
	if tile == 'X':
		return ['X', 'O']
	else:
	  return ['O', 'X']"""

"""
Função modificada de forma que o player1 não necessite escolher sua peça, sendo
o padrão a peça X.
Função original comentada acima.
"""
def enterPlayerTile():
	# Permite que o player escolha ser X ou O
	tile = ''
	while not (tile == 'X' or tile == 'O'):
		print('Escolha suas peças: X ou O?')
		#tile = input().upper()
		tile = 'X'
	if tile == 'X':
		return ['X', 'O']
	else:
	  return ['O', 'X']

def whoGoesFirst():
	# Escolhe aleatóriamente quem começa.
	if random.randint(0, 1) == 0:
		return 'computer'
	else:
		return 'player'

def playAgain():
	# Retorna True se o player quer jogar novamente
	print('Quer jogar novamente? (yes ou no)')
	return input().lower().startswith('y')

def makeMove(board, tile, xstart, ystart):
	# Coloca a peça no tabuleiro em xstart, ystart, e as peças do oponente
	# Retorna False se for um movimento invalido
	tilesToFlip = isValidMove(board, tile, xstart, ystart)
	if tilesToFlip == False:
		return False
	board[xstart][ystart] = tile
	for x, y in tilesToFlip:
		board[x][y] = tile
	return True

def getBoardCopy(board):
	# Faz uma cópia do tabuleiro e retorna a cópia
	dupeBoard = getNewBoard()
	for x in range(8):
		for y in range(8):
			dupeBoard[x][y] = board[x][y]
	return dupeBoard

def isOnCorner(x, y):
	# Retorna True se a posição x, y é um dos cantos do tabuleiro
	return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

"""def getPlayerMove(board, playerTile):
	# Permite que o player insira sua jogada
	DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
	while True:
		print('Insira seu movimento, ou insira quit para sair do jogo, ou hints para ativar/desativar dicas.')
		move = input().lower()
		if move == 'quit':
			return 'quit'
		if move == 'hints':
			return 'hints'
		if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
			x = int(move[0]) - 1
			y = int(move[1]) - 1
			if isValidMove(board, playerTile, x, y) == False:
			  print('Essa não é uma jogada válida')
			  continue
			else:
			  break
		else:
			print('Essa não é uma jogada válida, digite o valor de x (1-8), depois o valor de y (1-8).')
			print('Por exemplo, 81 será o canto superior direito.')
	return [x, y]
"""

"""
Função modificada de forma que o player1 simula implementação inicial da IA,
onde este executa sempre a jogada que ganha mais pontos no momento atual.
Função original comentada acima.
"""
def getPlayerMove(board, playerTile):
	# Permite ao computador executar seu movimento
	possibleMoves = getValidMoves(board, playerTile)
	# randomiza a ordem dos possíveis movimentos
	random.shuffle(possibleMoves)
	# se for possivel, joga no canto
	for x, y in possibleMoves:
		if isOnCorner(x, y):
			return [x, y]
	# Escolhe a jogada que resulta em mais pontos
	bestScore = -1
	for x, y in possibleMoves:
		dupeBoard = getBoardCopy(board)
		makeMove(dupeBoard, playerTile, x, y)
		score = getScoreOfBoard(dupeBoard)[playerTile]
		if score > bestScore:
			bestMove = [x, y]
			bestScore = score
	return bestMove

def getComputerMove(board, computerTile, playerTile):
	# Permite ao computador executar seu movimento
	possibleMoves = getValidMoves(board, computerTile)
	#print(possibleMoves)
	# randomiza a ordem dos possíveis movimentos
	#random.shuffle(possibleMoves)
	# se for possivel, joga no canto
	for x, y in possibleMoves:
		if isOnCorner(x, y):
			return [x, y]
	# Escolhe a jogada que resulta em mais pontos
	bestScore = -math.inf
	for x, y in possibleMoves:
		#print("####################################BEGIN####################################\nX = {}, Y = {}:".format(x, y))
		dupeBoard = getBoardCopy(board)
		makeMove(dupeBoard, computerTile, x, y)
		#score = getScoreOfBoard(dupeBoard)[computerTile]
		score = MinMax(dupeBoard, 0, max_depth, True, computerTile, playerTile, -math.inf, math.inf)
		if score > bestScore:
			bestMove = [x, y]
			bestScore = score
			print("\n\nBEST_MOVE:", bestMove)
			print("BEST_SCORE:", bestScore, "\n\n")
	return bestMove

def MinMax(board, depth, max_depth, isMaximizing, computerTile, playerTile, alpha, beta):
	possibleMoves_ia = getValidMoves(board, computerTile)
	possibleMoves_player = getValidMoves(board, playerTile)

	if depth == max_depth or not possibleMoves_ia or not possibleMoves_player:
		if isMaximizing:
			return getScoreOfBoard(board)[computerTile]
		else:
			return getScoreOfBoard(board)[playerTile]

	# Escolhe a jogada que resulta em mais
	if isMaximizing:
		possibleMoves = getValidMoves(board, computerTile)
		#print(possibleMoves)
		bestScore = -math.inf
		for x, y in possibleMoves:
			#print("X = {}, Y = {}:".format(x, y))
			dupeBoard = getBoardCopy(board)
			makeMove(dupeBoard, computerTile, x, y)
			#score = getScoreOfBoard(dupeBoard)[computerTile]
			score = MinMax(dupeBoard, depth+1, max_depth, False, computerTile, playerTile, alpha, beta)
			#if score > bestScore:
				#bestScore = score
			bestScore = max(bestScore, score)
			alpha = max(alpha, score)
			# Alpha_Beta
			if beta <= alpha:
				break
		#print("MAX_BEST_AI_SCORE:{}, DEPTH:{}".format(bestScore, depth))
		return bestScore
	else:
		possibleMoves = getValidMoves(board, playerTile)
		#print(possibleMoves)
		bestScore = math.inf
		for x, y in possibleMoves:
			#print("X = {}, Y = {}:".format(x, y))
			dupeBoard = getBoardCopy(board)
			makeMove(dupeBoard, playerTile, x, y)
			#score = getScoreOfBoard(dupeBoard)[playerTile]
			score = MinMax(dupeBoard, depth+1, max_depth, True, computerTile, playerTile, alpha, beta)
			#if score < bestScore:
			#	bestScore = score
			bestScore = min(bestScore, score)
			beta = min(beta, bestScore)
			# Alpha_Beta
			if beta <= alpha:
				break
		#print("MIN_BEST_PLAYER_ SCORE:{}, DEPTH:{}".format(bestScore, depth))
		return bestScore

def showPoints(playerTile, computerTile):
	# Mostra o score atual
	scores = getScoreOfBoard(mainBoard)
	print('Player1: %s ponto(s). \nComputador: %s ponto(s).' % (scores[playerTile], scores[computerTile]))

print('Welcome to Reversi!')
while True:
	# Reseta o jogo e o tabuleiro
	mainBoard = getNewBoard()
	resetBoard(mainBoard)
	playerTile, computerTile = enterPlayerTile()
	showHints = False
	turn = whoGoesFirst()
	print('O ' + turn + ' começa o jogo.')
	while True:
		if turn == 'player':
			# Player's turn.
			if showHints:
				validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
				drawBoard(validMovesBoard)
			else:
				drawBoard(mainBoard)
			showPoints(playerTile, computerTile)
			move = getPlayerMove(mainBoard, playerTile)
			if move == 'quit':
				print('Obrigado por jogar!')
				sys.exit() # terminate the program
			elif move == 'hints':
				showHints = not showHints
				continue
			else:
				makeMove(mainBoard, playerTile, move[0], move[1])
			if getValidMoves(mainBoard, computerTile) == []:
				break
			else:
				turn = 'computer'
		else:
			# Computer's turn.
			drawBoard(mainBoard)
			showPoints(playerTile, computerTile)
			"""

			input('Pressione Enter para ver a jogada do computador.')
			x, y = getComputerMove(mainBoard, computerTile)
			"""
			"""
			modificado para não possibilitar jogada do player1 com intervenção
			do usuário, além de passar como parametro o valor da peça do player1
			para utilização pelo min_max
			Código original comentado acima.
			"""
			x, y = getComputerMove(mainBoard, computerTile, playerTile)
			makeMove(mainBoard, computerTile, x, y)
			if getValidMoves(mainBoard, playerTile) == []:
				break
			else:
				turn = 'player'
	# Mostra o resultado final.
	drawBoard(mainBoard)
	scores = getScoreOfBoard(mainBoard)
	print('X: %s ponto(s) \nO: %s ponto(s).' % (scores['X'], scores['O']))
	if scores[playerTile] > scores[computerTile]:
		print('Você venceu o computador por %s ponto(s)! \nParabéns!' % (scores[playerTile] - scores[computerTile]))
	elif scores[playerTile] < scores[computerTile]:
		print('Você perdeu!\nO computador venceu você por %s ponto(s).' % (scores[computerTile] - scores[playerTile]))
	else:
		print('Empate!')
	if not playAgain():
		break

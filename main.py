import json
    
whiteMove = 0
blackMove = 1
emptySquare = '.'
whitePawn = 'P'
blackPawn = 'p'
whiteKing = 'K'
blackKing = 'k'
whiteQueen = 'Q'
blackQueen = 'q'
blackNextTwoSquare = 20
whiteNextTwoSquare = -1 * blackNextTwoSquare

pawnSquares = whitePawn + blackPawn
    
class Chess:
	def __init__(self, filename):
		with open(filename) as f:
			self.__dict__ = json.loads(f.read())
			self.board = list('         \n' * 2 + ' ' + ''.join([
				emptySquare * int(c) if c.isdigit() else c
				for c in self.fen.split()[0].replace('/', '\n ')
			]) + '\n' + '         \n' * 2)
			self.side = whiteMove if self.fen.split()[1] == 'w' else blackMove

	def generate_moves(self):
		move_list = []

		for square in range(len(self.board)):
			piece = self.board[square]
			if piece not in ' .\n' and self.colors[piece] == self.side:
				for offset in self.directions[piece]:
					target_square = square
					while True:
						target_square += offset
						captured_piece = self.board[target_square]

						# Skip the move if it is out of the board
						if captured_piece in ' \n': break

						# Prevent to capture own pieces
						if self.colors[captured_piece] == self.side: break

						if captured_piece in pawnSquares:
							# Prevent pawns to move diagonal if the square is empty
							if offset in [9,11,-9,-11] and captured_piece == emptySquare: break
							# Prevent pawns to move next 1 or 2 square if the square is not empty
							if offset in [10,20,-10,-20] and captured_piece != emptySquare: break


						# White pawn can not move directly with 2 square if the next square is not empty
						if piece == whitePawn and offset == whiteNextTwoSquare:
							## If the pawn moving first time
							if square not in self.rank_2: break
							if self.board[square - 10] != emptySquare: break

						# Black pawn can not move directly with 2 square if the next square is not empty
						if piece == blackPawn and offset == blackNextTwoSquare:
							## If the pawn moving first time
							if square not in self.rank_7: break
							if self.board[square + 10] != emptySquare: break

						if captured_piece in [blackKing, whiteKing]: return []

						move_list.append({
							'source': square, 'target': target_square,
							'piece': piece, 'captured': captured_piece,
						})

						# Move the piece to square and replace it previous square
						self.board[target_square] = piece
						self.board[square] = emptySquare
						#print(''.join([' ' + cs.pieces[p] for p in ''.join(cs.board)]), cs.side);

						# Put it back
						self.board[target_square] = captured_piece
						self.board[square] = piece
						#print(''.join([' ' + cs.pieces[p] for p in ''.join(cs.board)]), cs.side);

						# Validating the captured piece after moving if we captured opposite
						if self.colors[captured_piece] == self.side ^ 1: break
						if piece in 'PpNnKk': break
		return move_list

	def make_move(self, move):
		self.board[move['target']] = move['piece']
		self.board[move['source']] = emptySquare
		if move['piece'] == whitePawn and move['source'] in self.rank_7: self.board[move['target']] = whiteQueen
		if move['piece'] == blackPawn and move['source'] in self.rank_2: self.board[move['target']] = blackQueen
		self.print()
		self.side ^=1


	def take_back(self, move):
		self.board[move['target']] = move['captured']
		self.board[move['source']] = move['piece']
		self.print()
		self.side ^=1

	def print(self):
		print(''.join([' ' + cs.pieces[p] for p in ''.join(cs.board)]), cs.side); input()


cs = Chess('settings.json')
#print(''.join([' ' + cs.pieces[p] for p in ''.join(cs.board)]), cs.side)

for move in cs.generate_moves():
	cs.make_move(move)
	cs.take_back(move)
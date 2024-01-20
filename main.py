import json
    
whitePlay = 0
blackPlay = 1
    
class Chess:
	def __init__(self, filename):
		with open(filename) as f:
			self.__dict__ = json.loads(f.read())
			self.board = list('         \n' * 2 + ' ' + ''.join([
				'.' * int(c) if c.isdigit() else c
				for c in self.fen.split()[0].replace('/', '\n ')
			]) + '\n' + '         \n' * 2)
			self.side = whitePlay if self.fen.split()[1] == 'w' else blackPlay


cs = Chess('settings.json')
print(''.join([' ' + cs.pieces[p] for p in ''.join(cs.board)]), cs.side)
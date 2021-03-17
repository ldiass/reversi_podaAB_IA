import random
import sys
sys.path.append('..')
from common import board


class Node(object):
    def __init__(self, estado, cor):
        self.estado = estado
        self.cor=cor
        self.acao = (0,0)
        self.pontos = 0
        self.movimentos = []
        self.caminho = []
        self.oponente=estado.opponent(self.cor)

    def add_move(self, new_node):
        self.move.append(new_node)

    def __str__(self):
        return str(self.estado) + ": " + str(self.custo)

    def make_move(self):
        """
        Returns a random move from the list of possible ones
        Primeiro elemento eh o numero da coluna e o segunda da linha [0,7]
        :return: (int, int)
        """
        self.movimentos = self.estado.legal_moves(self.cor)
        return random.choice(self.movimentos) if len(self.movimentos) > 0 else (-1, -1)

    def encontrar_pecas(self):
        """
        Retorna uma lista com a posicao das pecas em
        '........\n........\n........\n........\n........\n........\n........\n........\n'
        :return: [[aliada],[inimigas]]
        """
        aliadas=[]
        tabuleiroStr=str(self.estado)
        for charPos in range(len(tabuleiroStr)):
            if(tabuleiroStr[charPos]==self.cor):
                aliadas.append(charPos)
        return aliadas

    def calcula_pontos(self):
        aliadas= self.encontrar_pecas()

        #Nao fazer um alg guloso pela captura
        self.pontos = self.pontos + 1*len(aliadas)

        # Pontuar a reducao de jogadas do adv
        self.pontos = self.pontos - 1.5 * len(self.movimentos)

        #20 pts por quinas:0,7,70,77
        adjquina_fixa = [1, 6, 10, 6,15, 16, 54, 55, 64, 60, 61, 69]
        adjquina = [1, 6, 10, 6,15, 16, 54, 55, 64, 60, 61, 69]
        quinas=[0, 7, 63, 71]
        for pos in aliadas:
            for i in range(4):
            	if(quinas[i] in aliadas):
            		#remove as 3 posicoes do C adjacente a quina preenchida
            		adjquina=list(set(adjquina)-set(adjquina_fixa[i*3:(i*3+4)]))
	                self.pontos=self.pontos+20

        # -20 pela regiao adjacente a quina (borda C)
        adjquina = [1, 6, 10, 6,15, 16, 54, 55, 64, 60, 61, 69]
        for pos in aliadas:
            if (pos in adjquina):
                self.pontos = self.pontos - 20

        #10 pts por bordas -C
        # [2:5],[18+i*09<46],[25+i*09<53],[65:68]
        for pos in aliadas:
            if (pos > 1 and pos<6):
                self.pontos = self.pontos + 10
            elif (pos > 64 and pos < 69):
                self.pontos = self.pontos + 10
            elif(pos>17 and (pos-18)%9==0 and pos<46):
                self.pontos = self.pontos + 10
            elif(pos >24 and (pos - 25) % 9== 0 and pos < 53):
                self.pontos = self.pontos + 10

        #-5 pts pela regiao adjacente as bordas centrais
	adj_bordas_centrais = [12,13,28,37,33,42,57,58]
        for pos in aliadas:
            if (pos in adj_bordas_centrais):
                self.pontos = self.pontos - 5


if __name__ == '__main__':
    b = board.from_file(sys.argv[1])
    #Codificar a cor q vem do servidor em formato 'black' p/ "B" e o msm p/ white
    color = board.Board.WHITE if sys.argv[2] == 'white' else board.Board.BLACK
    node=Node(b,color)
    f = open('move.txt', 'w')
    f.write('%d,%d' % node.make_move())
    f.close()

import random
import sys

sys.path.append('..')
from common import board


class Node(object):
    def __init__(self, estado, cor):
        self.estado = estado
        self.cor = cor
        self.acao = (0, 0)
        self.oponente = estado.opponent(self.cor)
        # variavel para impor limite de profundidade
        self.iter = 10

    def make_move(self):

        v_atual = -999999
        jogada_max = (-1, -1)
        movimentos_legais = self.estado.legal_moves(self.cor)

        if (len(movimentos_legais) > 0):
            for i in movimentos_legais:
                tabuleiro = self.estado
                tabuleiro.process_move(i, self.cor)
                v = self.valorMAX(tabuleiro, -999999, 999999, 1)
                if (v_atual < v):
                    jogada_max = i
                    v_atual = v
            print (self.calcula_pontos(tabuleiro, self.cor))
            return jogada_max
        else:
            return (-1, -1)

    def valorMAX(self, tabuleiro, alpha, beta, iter):

        movimentos_legais = self.estado.legal_moves(self.oponente)
        if (iter == self.iter or len(movimentos_legais) == 0):
            return self.calcula_pontos(tabuleiro, self.cor)

        else:
            for i in movimentos_legais:
                tabuleiro_novo = tabuleiro
                tabuleiro_novo.process_move(i, self.oponente)
                v = self.valorMIN(tabuleiro_novo, alpha, beta, iter + 1)
                alpha_novo = max(alpha, v)
                if (beta < alpha_novo):
                    return alpha_novo
            return alpha

    def valorMIN(self, tabuleiro, alpha, beta, iter):

        movimentos_legais = self.estado.legal_moves(self.cor)
        if (iter == self.iter or len(movimentos_legais) == 0):
            return self.calcula_pontos(tabuleiro, self.oponente)

        else:
            for i in movimentos_legais:
                tabuleiro_novo = tabuleiro
                tabuleiro_novo.process_move(i, self.cor)
                v = self.valorMAX(tabuleiro_novo, alpha, beta, iter + 1)
                beta_novo = min(beta, v)
                if (alpha > beta_novo):
                    return beta_novo
            return beta

    def encontrar_pecas(self, tabuleiro, cor):
        """
        Retorna uma lista com a posicao das pecas em
        '........\n........\n........\n........\n........\n........\n........\n........\n'
        :return: [[aliada],[inimigas]]
        """
        aliadas = []
        tabuleiroStr = str(tabuleiro)
        for charPos in range(len(tabuleiroStr)):
            if (tabuleiroStr[charPos] == cor):
                aliadas.append(charPos)
        return aliadas

    def calcula_pontos(self, tabuleiro, cor):
        pontos=0
        #Referencias p/ heuristica:
        #http://play-othello.appspot.com/files/Othello.pdf
        #https://bonaludo.com/2017/01/04/how-to-win-at-othello-part-1-strategy-basics-stable-discs-and-mobility/

        aliadas = self.encontrar_pecas(tabuleiro, cor)

        # Nao fazer um alg guloso pela captura
        pontos = pontos + 2 * len(aliadas)

        # Pontuar a reducao de jogadas do adv
        pontos = pontos - 4 * len(tabuleiro.legal_moves(cor))

        # 50 pts por quinas:0,7,70,77
        adjquina_fixa = [1, 6, 10, 6, 15, 16, 54, 55, 64, 60, 61, 69]
        adjquina = [1, 6, 10, 6, 15, 16, 54, 55, 64, 60, 61, 69]
        quinas = [0, 7, 63, 71]
        for pos in aliadas:
            for i in range(4):
                if (quinas[i] in aliadas):
                    # remove as 3 posicoes do C adjacente a quina preenchida
                    adjquina = list(set(adjquina) - set(adjquina_fixa[i * 3:(i * 3 + 4)]))
                    pontos = pontos + 150

        # -20 pela regiao adjacente a quina (borda C)        
        for pos in aliadas:
            if (pos in adjquina):
                pontos = pontos - 30

        # 10 pts por bordas -C
        # [2:5],[18+i*09<46],[25+i*09<53],[65:68]
        for pos in aliadas:
            if (pos > 1 and pos < 6):
                pontos = pontos + 10
            elif (pos > 64 and pos < 69):
                pontos = pontos + 10
            elif (pos > 17 and (pos - 18) % 9 == 0 and pos < 46):
                pontos = pontos + 10
            elif (pos > 24 and (pos - 25) % 9 == 0 and pos < 53):
                pontos = pontos + 10

        # -5 pts pela regiao adjacente as bordas centrais
        adj_bordas_centrais = [12, 13, 28, 37, 33, 42, 57, 58]
        for pos in aliadas:
            if (pos in adj_bordas_centrais):
                pontos = pontos - 5
        return pontos

if __name__ == '__main__':
    b = board.from_file(sys.argv[1])
    # Codificar a cor q vem do servidor em formato 'black' p/ "B" e o msm p/ white
    color = board.Board.WHITE if sys.argv[2] == 'white' else board.Board.BLACK
    node = Node(b, color)
    f = open('move.txt', 'w')
    f.write('%d,%d' % node.make_move())
    f.close()

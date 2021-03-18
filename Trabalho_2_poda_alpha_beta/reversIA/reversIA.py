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
        #variavel para impor limite de profundidade
        self.iter = 3

#    def add_movimentos(self):
        #Usar funcoes definidas no board para executar os movimentos de movimentos
        #Nao tenho ctz se aqui vai o oponente msm, mas faz sentido os proximos movimentos serem do oposto
#       coordenada_movimentos=self.estado.legal_moves(self.oponente)
        #Criar a lista de estados a partir da lista de movimentos, instanciar novos nodos e colocar na arvore
        #self.movimentos = 
#        self.move.movimentos(new_node)

#    def __str__(self):
#        return str(self.estado) + ": " + str(self.custo)

    def make_move(self):

        v_atual = -999999
        jogada_max = (-1, -1)
        movimentos_legais = self.estado.legal_moves(self.cor)
		
        if(len(movimentos_legais) > 0):
            for i in movimentos_legais:
                tabuleiro = self.estado
                tabuleiro.process_move(i,self.cor)
                v = self.valorMAX(tabuleiro,-999999,999999,1)
                if(v_atual < v):   
                    jogada_max = i
                    v_atual = v
            return jogada_max
        else:
            return (-1, -1)

    def valorMAX(self,tabuleiro,alpha,beta,iter):

        movimentos_legais = self.estado.legal_moves(self.oponente)
        if(iter == self.iter or len(movimentos_legais) == 0):
            self.calcula_pontos(tabuleiro)
            utilidade = self.pontos
            self.pontos = 0
            return utilidade
        else:
            for i in movimentos_legais:
                tabuleiro_novo = tabuleiro
                tabuleiro_novo.process_move(i,self.oponente)
                v = self.valorMIN(tabuleiro_novo,alpha,beta,iter+1)
                alpha_novo = max(alpha,v)
                if(beta < alpha_novo):
                    return alpha_novo
            return alpha

    def valorMIN(self,tabuleiro,alpha,beta,iter):

        movimentos_legais = self.estado.legal_moves(self.cor)
        if(iter == self.iter or len(movimentos_legais) == 0):
            self.calcula_pontos(tabuleiro)
            utilidade = self.pontos
            self.pontos = 0
            return utilidade
        else:
            for i in movimentos_legais:
                tabuleiro_novo = tabuleiro
                tabuleiro_novo.process_move(i,self.cor)
                v = self.valorMAX(tabuleiro_novo,alpha,beta,iter+1)
                beta_novo = min(beta,v)
                if(alpha > beta_novo):
                    return beta_novo
            return beta

    def encontrar_pecas(self,tabuleiro):
        """
        Retorna uma lista com a posicao das pecas em
        '........\n........\n........\n........\n........\n........\n........\n........\n'
        :return: [[aliada],[inimigas]]
        """
        aliadas=[]
        tabuleiroStr=str(tabuleiro)
        for charPos in range(len(tabuleiroStr)):
            if(tabuleiroStr[charPos]==self.cor):
                aliadas.append(charPos)
        return aliadas

    def calcula_pontos(self,tabuleiro):
        aliadas= self.encontrar_pecas(tabuleiro)

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

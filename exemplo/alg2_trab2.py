import random
import pygame
import sys

# Inicializando o Pygame
pygame.init()

# Dimensões da janela e da carta
LARGURA, ALTURA = 1400, 800
LARG_CARTA, ALT_CARTA = 85, 120
ESP_LATERAL, ESP_VERTICAL = 90, 70

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 128, 0)
AZUL = (0, 0, 255)
CINZA_CLARO = (200, 200, 200)

# Limites
MAX_PILHAS = 10
LIM_CARTAS = 15
MAX_SUBPILHA = 5

# Mapas de valores e naipes
NAIPES = {0: '♠', 1: '♣', 2: '♥', 3: '♦'}
VALORES = {1: 'A', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K'}
NAIPE_PRETO = (0, 1)
NAIPE_VERMELHO = (2, 3)

# Fonte personalizada para corrigir os símbolos dos naipes
FONTE_CARTA = pygame.font.Font(pygame.font.match_font("arial"), 30)  # Altere aqui para carregar outra fonte!

class Carta:
    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe

    def desenha(self, x, y, destaque=False):
        desenhar_carta(tela, x, y, self.valor, self.naipe, destaque)

def desenhar_carta(superficie, x, y, valor, naipe, destaque):
    cor = PRETO if naipe in NAIPE_PRETO else VERMELHO
    pygame.draw.rect(superficie, BRANCO, (x, y, LARG_CARTA, ALT_CARTA), border_radius=10)
    pygame.draw.rect(superficie, AZUL if destaque else PRETO, (x, y, LARG_CARTA, ALT_CARTA), 3, border_radius=10)
    texto_valor = FONTE_CARTA.render(VALORES[valor], True, cor)
    texto_naipe = FONTE_CARTA.render(NAIPES[naipe], True, cor)
    superficie.blit(texto_valor, (x + 10, y + 10))
    superficie.blit(texto_naipe, (x + 10, y + 40))

def valida_movimento(origem, destino):
    """Valida movimento de uma carta única."""
    if not origem or len(destino) >= LIM_CARTAS:
        return False
    carta_origem = origem[-1]
    carta_destino = destino[-1] if destino else None
    if carta_destino:
        return (
            carta_origem.valor + 1 == carta_destino.valor and
            cores_alternadas(carta_origem, carta_destino)
        )
    return True

def cores_alternadas(c1, c2):
    """Verifica se as cores das cartas são alternadas."""
    return (c1.naipe in NAIPE_PRETO and c2.naipe in NAIPE_VERMELHO) or \
           (c1.naipe in NAIPE_VERMELHO and c2.naipe in NAIPE_PRETO)

def valida_subpilha(origem, subpilha, destino):
    """Valida movimento de uma subpilha."""
    if len(subpilha) > MAX_SUBPILHA or len(destino) + len(subpilha) > LIM_CARTAS:
        return False
    for i in range(len(subpilha) - 1):
        if not (
            subpilha[i].valor + 1 == subpilha[i + 1].valor and
            cores_alternadas(subpilha[i], subpilha[i + 1])
        ):
            return False
    return valida_movimento([subpilha[-1]], destino)

def valida_recolhimento(carta, pilha_recolhimento):
    """Valida movimento para pilhas de recolhimento."""
    if not pilha_recolhimento:
        return carta.valor == 1  # Aceita apenas o Ás inicialmente.
    return carta.valor == pilha_recolhimento[-1].valor + 1 and carta.naipe == pilha_recolhimento[-1].naipe

def print_pilha(pilha, x, y, destaque=False):
    """Desenha as cartas de uma pilha na tela."""
    for i, carta in enumerate(pilha):
        carta.desenha(x, y + i * ESP_VERTICAL, destaque and i == len(pilha) - 1)

# Preparação do jogo
baralho = [Carta(valor, naipe) for valor in range(1, 14) for naipe in range(4)]
random.shuffle(baralho)
pilhas = [[baralho.pop() for _ in range(5)] for _ in range(MAX_PILHAS)]
pilhas_recolhimento = [[] for _ in range(4)]

# Loop principal
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo de Cartas')
rodando = True
origem = None
subpilha_selecionada = []

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos
            cx = x // ESP_LATERAL
            if 0 <= cx < MAX_PILHAS:
                if origem is None:
                    origem = cx
                    subpilha_selecionada = pilhas[origem][-MAX_SUBPILHA:]
                else:
                    destino = cx
                    if valida_movimento(pilhas[origem], pilhas[destino]):
                        pilhas[destino].append(pilhas[origem].pop())
                    elif valida_subpilha(pilhas[origem], subpilha_selecionada, pilhas[destino]):
                        pilhas[destino].extend(subpilha_selecionada)
                        pilhas[origem] = pilhas[origem][:-len(subpilha_selecionada)]
                    origem = None
                    subpilha_selecionada = []
            elif MAX_PILHAS <= cx < MAX_PILHAS + 4:  # Pilhas de recolhimento
                indice_recolhimento = cx - MAX_PILHAS
                if origem is not None and valida_recolhimento(pilhas[origem][-1], pilhas_recolhimento[indice_recolhimento]):
                    pilhas_recolhimento[indice_recolhimento].append(pilhas[origem].pop())
                    origem = None

    tela.fill(CINZA_CLARO)
    for i, pilha in enumerate(pilhas):
        print_pilha(pilha, ESP_LATERAL * i, 100, destaque=(origem == i))
    for i, pilha_recolhimento in enumerate(pilhas_recolhimento):
        print_pilha(pilha_recolhimento, ESP_LATERAL * (MAX_PILHAS + i), 50)

    pygame.display.flip()

pygame.quit()
sys.exit()

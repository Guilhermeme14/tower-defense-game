import pygame
import math
import random
from enum import Enum

pygame.init()

# Constantes
LARGURA = 1200
ALTURA = 700
FPS = 60

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (34, 139, 34)
VERDE_ESCURO = (0, 100, 0)
MARROM = (139, 69, 19)
CINZA = (128, 128, 128)
VERMELHO = (220, 20, 60)
AZUL = (30, 144, 255)
AMARELO = (255, 215, 0)
ROXO = (138, 43, 226)
LARANJA = (255, 140, 0)


class TipoTorre(Enum):
    BASICA = 1
    RAPIDA = 2
    SNIPER = 3


class Inimigo:
    def __init__(self, caminho, vida, velocidade, recompensa, tipo=1):
        self.caminho = caminho
        self.indice_caminho = 0
        self.x, self.y = caminho[0]
        self.vida_max = vida
        self.vida = vida
        self.velocidade = velocidade
        self.recompensa = recompensa
        self.tipo = tipo
        self.raio = 8 + tipo * 2
        self.cor = self.obter_cor()
        self.inimigos = []
        self.inimigos_fila = []

    def obter_cor(self):
        cores = [VERMELHO, LARANJA, ROXO, (255, 0, 255)]
        return cores[min(self.tipo - 1, len(cores) - 1)]

    def mover(self):
        if self.indice_caminho < len(self.caminho) - 1:
            alvo_x, alvo_y = self.caminho[self.indice_caminho + 1]
            dx = alvo_x - self.x
            dy = alvo_y - self.y
            dist = math.sqrt(dx ** 2 + dy ** 2)

            if dist < self.velocidade:
                self.indice_caminho += 1
                if self.indice_caminho < len(self.caminho):
                    self.x, self.y = self.caminho[self.indice_caminho]
            else:
                self.x += (dx / dist) * self.velocidade
                self.y += (dy / dist) * self.velocidade
            return True
        return False

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)
        pygame.draw.circle(tela, PRETO, (int(self.x), int(self.y)), self.raio, 2)

        # Barra de vida
        largura_barra = self.raio * 2
        altura_barra = 4
        x_barra = self.x - largura_barra // 2
        y_barra = self.y - self.raio - 8

        pygame.draw.rect(tela, PRETO, (x_barra - 1, y_barra - 1, largura_barra + 2, altura_barra + 2))
        proporcao_vida = self.vida / self.vida_max
        pygame.draw.rect(tela, VERDE, (x_barra, y_barra, largura_barra * proporcao_vida, altura_barra))

    def receber_dano(self, dano):
        self.vida -= dano
        return self.vida <= 0


class Projetil:
    def __init__(self, x, y, alvo, dano, velocidade=8, cor=AMARELO):
        self.x = x
        self.y = y
        self.alvo = alvo
        self.dano = dano
        self.velocidade = velocidade
        self.cor = cor
        self.raio = 4

    def mover(self):
        if self.alvo and self.alvo.vida > 0:
            dx = self.alvo.x - self.x
            dy = self.alvo.y - self.y
            dist = math.sqrt(dx ** 2 + dy ** 2)

            if dist < self.velocidade + 5:  # Aumenta a tolerância de colisão
                return True

            self.x += (dx / dist) * self.velocidade
            self.y += (dy / dist) * self.velocidade
            return False
        return None  # Retorna None se alvo não existe

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)
        pygame.draw.circle(tela, PRETO, (int(self.x), int(self.y)), self.raio, 1)


class Torre:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.nivel = 1
        self.cooldown = 0
        self.alvo = None

        # Configurações por tipo
        if tipo == TipoTorre.BASICA:
            self.alcance = 120
            self.dano = 20
            self.taxa_tiro = 30
            self.cor = AZUL
            self.custo = 100
            self.nome = "Básica"
        elif tipo == TipoTorre.RAPIDA:
            self.alcance = 100
            self.dano = 8
            self.taxa_tiro = 10
            self.cor = LARANJA
            self.custo = 150
            self.nome = "Rápida"
        elif tipo == TipoTorre.SNIPER:
            self.alcance = 200
            self.dano = 50
            self.taxa_tiro = 60
            self.cor = ROXO
            self.custo = 200
            self.nome = "Sniper"


    def melhorar(self):
        self.nivel += 1
        self.dano = int(self.dano * 1.5)
        self.alcance += 15
        return int(self.custo * 0.7)

    def encontrar_alvo(self, inimigos):
        alvos_no_alcance = []
        for inimigo in inimigos:
            dist = math.sqrt((inimigo.x - self.x) ** 2 + (inimigo.y - self.y) ** 2)
            if dist <= self.alcance:
                alvos_no_alcance.append((inimigo, inimigo.indice_caminho))

        if alvos_no_alcance:
            alvos_no_alcance.sort(key=lambda x: x[1], reverse=True)
            return alvos_no_alcance[0][0]
        return None

    def atirar(self, inimigos):
        if self.cooldown <= 0:
            self.alvo = self.encontrar_alvo(inimigos)
            if self.alvo:
                self.cooldown = self.taxa_tiro
                return Projetil(self.x, self.y, self.alvo, self.dano, cor=self.cor)
        return None

    def atualizar(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def desenhar(self, tela, selecionada=False):
        # Base da torre
        pygame.draw.circle(tela, CINZA, (self.x, self.y), 18)
        pygame.draw.circle(tela, self.cor, (self.x, self.y), 15)
        pygame.draw.circle(tela, PRETO, (self.x, self.y), 15, 2)

        # Alcance ao selecionar
        if selecionada:
            s = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.cor, 30), (self.x, self.y), self.alcance)
            pygame.draw.circle(s, (*self.cor, 100), (self.x, self.y), self.alcance, 2)
            tela.blit(s, (0, 0))

        # Nível
        fonte = pygame.font.Font(None, 20)
        texto = fonte.render(str(self.nivel), True, BRANCO)
        tela.blit(texto, (self.x - texto.get_width() // 2, self.y - texto.get_height() // 2))


class Jogo:
    def __init__(self):
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Tower Defense")
        self.relogio = pygame.time.Clock()

        self.dinheiro = 400
        self.vidas = 20
        self.onda = 0
        self.inimigos = []
        self.torres = []
        self.projeteis = []

        self.torre_selecionada = None
        self.tipo_torre_construir = None

        self.tempo_proxima_onda = 0
        self.inimigos_por_spawn = 0
        self.delay_spawn = 0

        # Caminho dos inimigos
        self.caminho = [
            (50, 100), (200, 100), (200, 300), (400, 300),
            (400, 150), (600, 150), (600, 400), (800, 400),
            (800, 200), (1000, 200), (1000, 500), (1150, 500)
        ]

        # Áreas onde não pode construir
        self.areas_bloqueadas = []
        for i in range(len(self.caminho) - 1):
            x1, y1 = self.caminho[i]
            x2, y2 = self.caminho[i + 1]
            self.areas_bloqueadas.append((min(x1, x2) - 30, min(y1, y2) - 30,
                                          abs(x2 - x1) + 60, abs(y2 - y1) + 60))

    def pode_construir(self, x, y):
        # Verifica se está muito perto do caminho
        for bx, by, bw, bh in self.areas_bloqueadas:
            if bx < x < bx + bw and by < y < by + bh:
                return False

        # Verifica se está muito perto de outra torre
        for torre in self.torres:
            dist = math.sqrt((torre.x - x) ** 2 + (torre.y - y) ** 2)
            if dist < 40:
                return False

        return 0 < x < LARGURA and 50 < y < ALTURA - 150

    def iniciar_onda(self):
        self.onda += 1
        num_inimigos = 5 + self.onda * 3

        self.inimigos_fila = []

        if self.onda < 3:
            tipos = [1]
        elif self.onda < 6:
            tipos = [1, 1, 2]
        elif self.onda < 10:
            tipos = [1, 2, 2, 3]
        else:
            tipos = [1, 2, 3, 4]

        for _ in range(num_inimigos):
            tipo = random.choice(tipos)
            vida = 50 * tipo * (1 + self.onda * 0.3)
            velocidade = 1.5 + tipo * 0.3
            recompensa = 10 * tipo + self.onda * 2

            inimigo = Inimigo(self.caminho, vida, velocidade, recompensa, tipo)
            self.inimigos_fila.append(inimigo)

        self.delay_spawn = 20

    def atualizar(self):
        # Spawn gradual de inimigos
        if self.inimigos_fila:
            self.delay_spawn -= 1
            if self.delay_spawn <= 0:
                self.inimigos.append(self.inimigos_fila.pop(0))
                self.delay_spawn = 20

        # Atualizar inimigos
        for inimigo in self.inimigos[:]:
            if not inimigo.mover():
                self.inimigos.remove(inimigo)
                self.vidas -= 1

        # Atualizar torres
        for torre in self.torres:
            torre.atualizar()
            projetil = torre.atirar(self.inimigos)
            if projetil:
                self.projeteis.append(projetil)

        # Atualizar projéteis
        for projetil in self.projeteis[:]:
            resultado = projetil.mover()

            # Se atingiu o alvo (True)
            if resultado == True:
                if projetil.alvo and projetil.alvo in self.inimigos:
                    # Aplicar dano
                    morreu = projetil.alvo.receber_dano(projetil.dano)
                    if morreu:
                        self.dinheiro += projetil.alvo.recompensa
                        self.inimigos.remove(projetil.alvo)
                # Remover projétil
                if projetil in self.projeteis:
                    self.projeteis.remove(projetil)
            # Se o alvo não existe mais (None)
            elif resultado == None:
                if projetil in self.projeteis:
                    self.projeteis.remove(projetil)

        # Verificar início de nova onda
        if len(self.inimigos) == 0 and self.inimigos_por_spawn == 0:
            self.tempo_proxima_onda += 1
            if self.tempo_proxima_onda > 120:
                self.iniciar_onda()
                self.tempo_proxima_onda = 0

    def desenhar(self):
        self.tela.fill(VERDE)

        # Desenhar caminho
        for i in range(len(self.caminho) - 1):
            pygame.draw.line(self.tela, MARROM, self.caminho[i], self.caminho[i + 1], 35)

        for ponto in self.caminho:
            pygame.draw.circle(self.tela, MARROM, ponto, 18)

        # Desenhar inimigos
        for inimigo in self.inimigos:
            inimigo.desenhar(self.tela)

        # Desenhar projéteis
        for projetil in self.projeteis:
            projetil.desenhar(self.tela)

        # Desenhar torres
        for torre in self.torres:
            torre.desenhar(self.tela, torre == self.torre_selecionada)

        # Pré-visualização de construção
        if self.tipo_torre_construir:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.pode_construir(mouse_x, mouse_y):
                cor = (0, 255, 0, 100)
            else:
                cor = (255, 0, 0, 100)

            s = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            pygame.draw.circle(s, cor, (mouse_x, mouse_y), 15)
            self.tela.blit(s, (0, 0))

        # Interface
        self.desenhar_interface()

    def desenhar_interface(self):
        # Painel inferior
        pygame.draw.rect(self.tela, CINZA, (0, ALTURA - 150, LARGURA, 150))
        pygame.draw.rect(self.tela, PRETO, (0, ALTURA - 150, LARGURA, 150), 3)

        fonte = pygame.font.Font(None, 36)
        fonte_pequena = pygame.font.Font(None, 24)

        # Informações do jogo
        texto_dinheiro = fonte.render(f"Dinheiro: ${self.dinheiro}", True, AMARELO)
        texto_vidas = fonte.render(f"Vidas: {self.vidas}", True, VERMELHO)
        texto_onda = fonte.render(f"Onda: {self.onda}", True, BRANCO)

        self.tela.blit(texto_dinheiro, (20, ALTURA - 130))
        self.tela.blit(texto_vidas, (20, ALTURA - 90))
        self.tela.blit(texto_onda, (20, ALTURA - 50))

        # Botões de torres
        x_inicial = 350
        espacamento = 150

        tipos_torre = [
            (TipoTorre.BASICA, "Básica", 100, AZUL),
            (TipoTorre.RAPIDA, "Rápida", 150, LARANJA),
            (TipoTorre.SNIPER, "Sniper", 200, ROXO),
        ]

        for i, (tipo, nome, custo, cor) in enumerate(tipos_torre):
            x = x_inicial + i * espacamento
            y = ALTURA - 100

            # Botão
            pygame.draw.rect(self.tela, cor, (x, y, 120, 80))
            pygame.draw.rect(self.tela, PRETO, (x, y, 120, 80), 3)

            if self.tipo_torre_construir == tipo:
                pygame.draw.rect(self.tela, AMARELO, (x, y, 120, 80), 5)

            # Texto
            texto_nome = fonte_pequena.render(nome, True, BRANCO)
            texto_custo = fonte_pequena.render(f"${custo}", True, AMARELO)

            self.tela.blit(texto_nome, (x + 60 - texto_nome.get_width() // 2, y + 20))
            self.tela.blit(texto_custo, (x + 60 - texto_custo.get_width() // 2, y + 50))

        # Info da torre selecionada
        if self.torre_selecionada:
            x = 1000
            y = ALTURA - 130

            texto = [
                f"Torre: {self.torre_selecionada.nome}",
                f"Nível: {self.torre_selecionada.nivel}",
                f"Dano: {self.torre_selecionada.dano}",
                f"Melhorar: ${int(self.torre_selecionada.custo * 0.7)}"
            ]

            for i, linha in enumerate(texto):
                surf = fonte_pequena.render(linha, True, BRANCO)
                self.tela.blit(surf, (x, y + i * 25))

    def executar(self):
        self.iniciar_onda()
        rodando = True

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = evento.pos

                    # Selecionar torre ao clicar com botão esquerdo
                    if evento.button == 1:
                        for torre in self.torres:
                            dist = math.sqrt((torre.x - mouse_x) ** 2 + (torre.y - mouse_y) ** 2)
                            if dist <= 20:
                                self.torre_selecionada = torre
                                self.tipo_torre_construir = None
                                break
                        else:
                            # Se clicou longe das torres, remove seleção
                            self.torre_selecionada = None

                    # Melhorar torre com botão direito
                    if evento.button == 3 and self.torre_selecionada:
                        custo_upgrade = int(self.torre_selecionada.custo * 0.7)
                        if self.dinheiro >= custo_upgrade:
                            self.dinheiro -= custo_upgrade
                            self.torre_selecionada.melhorar()

                    # Verificar clique nos botões de torre
                    if ALTURA - 150 < mouse_y < ALTURA:
                        x_inicial = 350
                        espacamento = 150
                        tipos = [TipoTorre.BASICA, TipoTorre.RAPIDA, TipoTorre.SNIPER]

                        for i, tipo in enumerate(tipos):
                            x = x_inicial + i * espacamento
                            if x < mouse_x < x + 120 and ALTURA - 100 < mouse_y < ALTURA - 20:
                                self.tipo_torre_construir = tipo
                                self.torre_selecionada = None
                                break
                    else:
                        # Construir torre
                        if self.tipo_torre_construir:
                            torre = Torre(mouse_x, mouse_y, self.tipo_torre_construir)
                            if self.dinheiro >= torre.custo and self.pode_construir(mouse_x, mouse_y):
                                self.dinheiro -= torre.custo
                                self.torres.append(torre)
                            self.tipo_torre_construir = None
                        else:
                            # Selecionar torre
                            self.torre_selecionada = None
                            for torre in self.torres:
                                dist = math.sqrt((torre.x - mouse_x) ** 2 + (torre.y - mouse_y) ** 2)
                                if dist < 20:
                                    self.torre_selecionada = torre
                                    break

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.tipo_torre_construir = None
                        self.torre_selecionada = None

                    if evento.key == pygame.K_u and self.torre_selecionada:
                        custo = int(self.torre_selecionada.custo * 0.7)
                        if self.dinheiro >= custo:
                            self.dinheiro -= custo
                            self.torre_selecionada.melhorar()

            if self.vidas <= 0:
                fonte = pygame.font.Font(None, 72)
                texto = fonte.render("GAME OVER", True, VERMELHO)
                self.tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2))
                pygame.display.flip()
                pygame.time.wait(3000)
                rodando = False
            else:
                self.atualizar()
                self.desenhar()
                pygame.display.flip()
                self.relogio.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
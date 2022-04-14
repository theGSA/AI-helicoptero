import pygame
from Arvores import ARVORE
from enum import Enum
from math import *


class ACAO(Enum):
    APAGAR_FOGO = 1
    POUSAR = 2
    POUSANDO = 5
    DECOLAR = 3
    VOANDO = 4
    REPOUSO = 0


class Agente(pygame.sprite.Sprite):
    def __init__(self, Ambiente):
        # variaves pygame
        pygame.sprite.Sprite.__init__(self)
        self.sprite_sheet = pygame.image.load("Texturas/helicoptero.png")
        self.screen = None
        self.Pos = [0, 0]
        self.InicialPos = (0, 0)
        self.VoarRect = pygame.Rect(0, 0, 96, 128)
        self.RepousoRect = pygame.Rect(288, 128, 96, 128)
        self.CurRect = self.RepousoRect
        self.sprite = pygame.Surface((96, 128), pygame.SRCALPHA).convert_alpha()
        self.StartTime = pygame.time.get_ticks()
        # varaiveis do agente
        self.Ambiente = Ambiente
        self.Status = ACAO.REPOUSO
        self.Action = ACAO.REPOUSO
        self.ArvoreEmChamas = None
        #self.Arvores = None

    def Update(self, screen):
        self.screen = screen
        self.Desenha()
        self.Eventos()
        self.VerificarArvores()
        self.MoverAtePosicao()

    def Eventos(self):
        if pygame.key.get_pressed()[pygame.K_a]:
            self.Pos[0] -= 1
        if pygame.key.get_pressed()[pygame.K_s]: 
            self.Pos[0] += 1
        if pygame.key.get_pressed()[pygame.K_d]: 
            self.Pos[0] += 1
        if pygame.key.get_pressed()[pygame.K_w]: 
            self.Pos[0] -= 1

    def Desenha(self):
        if self.Status == ACAO.POUSAR or self.Status == ACAO.REPOUSO or self.Status == ACAO.VOANDO or self.Status == ACAO.DECOLAR:
            if self.Status == ACAO.REPOUSO:
                if self.Action == ACAO.APAGAR_FOGO:
                    self.Status = ACAO.DECOLAR
            elif self.Status == ACAO.DECOLAR:
                if pygame.time.get_ticks() - self.StartTime >= 100:
                    self.StartTime = pygame.time.get_ticks()
                    self.CurRect.x -= 96
                    if self.CurRect.x < 0:
                        self.CurRect.x += 96
                        self.CurRect.y -= 128
                        self.Status = ACAO.VOANDO
            else:
                self.Voar()
        elif self.Status == ACAO.POUSANDO:
            self.Pousar()
        elif self.Status == ACAO.REPOUSO:
            self.CurRect = self.RepousoRect
        self.UpdateSprite()

    def UpdateSprite(self):
        self.sprite.fill(0)
        self.sprite.blit(self.sprite_sheet, (0, 0), self.CurRect)
        self.screen.blit(self.sprite, self.Pos)

    def Voar(self):
        self.CurRect.x += 96
        if self.CurRect.x >= 384:
            self.CurRect.x = 0

    def BuscaGulosa(self):
        arvores_em_chamas = []
        temp_arvores = self.Ambiente.Arvores.copy()
        while len(temp_arvores) > 0:
            arvore_em_menor_distancia = None
            i = 0
            while i < len(temp_arvores):
                if temp_arvores[i].Status == ARVORE.FOGO:
                    tamlista = len(arvores_em_chamas)
                    if tamlista == 0:
                        if not arvore_em_menor_distancia or temp_arvores[i].DistanciaParaAgente < arvore_em_menor_distancia.DistanciaParaAgente:
                            arvore_em_menor_distancia = temp_arvores[i]
                    elif not arvore_em_menor_distancia or self.Ambiente.ObterDistanciasEntreObjetos(arvores_em_chamas[-1], temp_arvores[i]) < self.Ambiente.ObterDistanciasEntreObjetos(arvores_em_chamas[-1], arvore_em_menor_distancia):
                        arvore_em_menor_distancia = temp_arvores[i]
                else:
                    temp_arvores.pop(i)
                    i -= 1
                i += 1
            if arvore_em_menor_distancia:
                arvores_em_chamas.append(arvore_em_menor_distancia)
                temp_arvores.remove(arvore_em_menor_distancia)
        return arvores_em_chamas

    def VerificarArvores(self):
        if self.Action != ACAO.APAGAR_FOGO:
            self.ArvoreEmChamas = self.BuscaGulosa()
            if self.ArvoreEmChamas:
                print("apagar fogo de [", end='')
                for j in self.ArvoreEmChamas:
                    print(" "+str(j.Ambiente.Arvores.index(j)), end="")
                print("]")
            if self.ArvoreEmChamas:
                if self.Status == ACAO.POUSAR:
                    self.Status = ACAO.VOANDO
                self.Action = ACAO.APAGAR_FOGO
        else:
            if self.ArvoreEmChamas[0].Status != ARVORE.FOGO:
                self.Action = ACAO.REPOUSO
                self.Status = ACAO.POUSAR
        
    def Pousar(self):
        self.Status = ACAO.POUSANDO
        if pygame.time.get_ticks() - self.StartTime >= 100:
            self.StartTime = pygame.time.get_ticks()
            if self.CurRect.y == 0:
                self.CurRect.y += 128
            self.CurRect.x += 96
            if self.CurRect.x >= 384:
                self.CurRect.x -= 96
                self.Status = ACAO.REPOUSO

    def MoverAtePosicao(self):
        if self.Action == ACAO.APAGAR_FOGO and self.Status == ACAO.VOANDO:
            if self.ArvoreEmChamas[0]:
                offsety = 20
                self.Pos[0] += ((self.ArvoreEmChamas[0].Pos[0] + self.ArvoreEmChamas[0].CurRect.w/2) - (self.Pos[0] + self.CurRect.w/2))/100.0
                self.Pos[1] += ((self.ArvoreEmChamas[0].Pos[1] + self.ArvoreEmChamas[0].CurRect.h/2) - (self.Pos[1] + self.CurRect.h/2) - offsety)/100.0
                
                if self.ArvoreEmChamas[0].DistanciaParaAgente <= 1:
                    self.ArvoreEmChamas[0].ApagarFogo()
                    self.ArvoreEmChamas.remove(self.ArvoreEmChamas[0])
                    if len(self.ArvoreEmChamas) == 0:
                        self.Status = ACAO.POUSAR
                        self.Action = ACAO.REPOUSO
        elif self.Status == ACAO.POUSAR:
            self.Pos[0] += int(self.InicialPos[0] - self.Pos[0])/100
            self.Pos[1] += int(self.InicialPos[1] - self.Pos[1])/100
            if abs(int(self.InicialPos[0] - self.Pos[0])) <= 1 and abs(self.InicialPos[1] - self.Pos[1]) <= 1:
                self.Status = ACAO.POUSANDO

import pygame
from Arvores import Arvore
from random import randint
from Agente import Agente
from math import *


class Ambiente(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load("Texturas/Ambiente.png")
        self.GramasRect = pygame.Rect(32, 0, 24, 20)
        self.SpriteGramas = pygame.Surface((24,20), pygame.SRCALPHA).convert_alpha()
        self.SpriteGramas.blit(self.image, (0, 0), self.GramasRect)
        self.pos = [0, 0]
        self.ChaoRect = pygame.Rect(0, 0, 32, 32)
        self.Arvores = []
        self.chao = None
        self.CriarChao()
        self.CriarArvores()
        self.gramas = None
        self.CriarGramas()
        self.Helicoptero = Agente(self)
        #self.Helicoptero.Arvores = self.Arvores

    def Update(self):
        self.Desenhar()

    def CriarArvores(self):
        arvore_pos = []
        while len(arvore_pos) <= 30:
            screen = self.screen.get_rect()
            temp = pygame.Rect(randint(0, screen.w - 50), randint(0, screen.h - 50), 0, 0)
            checker = True
            for i in arvore_pos:
                if abs(temp[0] - i[0]) <= 72 and abs(temp[1] - i[1]) <= 84 or (temp[0] <= 96 and temp[1] <= 128):
                    checker = False
            if checker:
                arvore_pos.append(temp)

        for i in range(len(arvore_pos)):
            self.Arvores.append(Arvore())
            self.Arvores[-1].SetPos(arvore_pos[i])
            self.Arvores[-1].SetScreen(self.screen)
            self.Arvores[-1].SetMabiente(self)
        
        #for arvore in self.Arvores:
            #print("index: "+str(self.Arvores.index(arvore))) 

    def Desenhar(self):
        self.DesenharChao()
        self.DesenharGramas()
        self.DesenharArvores()
        self.DesenharHelicoptero()
        self.CheckDistanciaDeArvoreParaAgente()

    def DesenharHelicoptero(self):
        self.Helicoptero.Update(self.screen)

    def CriarChao(self):
        screen = self.screen.get_rect()
        tempsprite = pygame.Surface((32, 32))
        tempsprite.fill(0)
        tempsprite.blit(self.image, (0, 0), self.ChaoRect)
        self.chao = pygame.Surface((screen.w, screen.h), pygame.SRCALPHA).convert_alpha()
        self.chao.fill(0)
        for i in range(0, screen.w, 32):
            for j in range(0, screen.h, 32):
                self.chao.blit(tempsprite, (i, j))

    def DesenharChao(self):
        self.screen.blit(self.chao, (0, 0))

    @staticmethod
    def ObterDistanciasEntreObjetos(obj1, obj2):
        hel_pos_x = obj1.Pos[0] + obj1.CurRect.w/2
        hel_pos_y = obj1.Pos[1] + obj1.CurRect.h/2
        arv_pos_x = obj2.Pos[0] + obj2.CurRect.w/2
        arv_pos_y = obj2.Pos[1] + obj2.CurRect.h/2 - 20
        return sqrt(pow(hel_pos_x - arv_pos_x, 2) + pow(hel_pos_y - arv_pos_y, 2))

    def CheckDistanciaDeArvoreParaAgente(self):
        for arvore in self.Arvores:
            arvore.DistanciaParaAgente = self.ObterDistanciasEntreObjetos(self.Helicoptero, arvore)

    def CriarGramas(self):
        self.gramas = []
        screen = self.screen.get_rect()
        while len(self.gramas) < 200:
            mtemp = (randint(0, screen.w - 20), randint(0, screen.h - 20))
            checker = True
            for pos in self.gramas:
                if abs(pos[0] - mtemp[0]) <= 28 and abs(pos[1] - mtemp[1]) <= 32 or (mtemp[0] <= 96 and mtemp[1] <= 128):
                    checker = False
            if checker:
                self.gramas.append(mtemp)

    def DesenharGramas(self):
        for grama in self.gramas:
            self.screen.blit(self.SpriteGramas, grama)

    def DesenharArvores(self):
        for arvore in self.Arvores:
            arvore.Atualizar()




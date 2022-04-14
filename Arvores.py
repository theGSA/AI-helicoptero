import pygame
from enum import Enum


class ARVORE(Enum):
    NORMAL = 0
    FOGO = 1


class Arvore(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_sheet = pygame.image.load("Texturas/Ambiente.png")
        self.Pos = pygame.Rect(0, 0, 0, 0)
        self.CurRect = pygame.Rect(56, 0, 72, 84)
        self.RectFogo = pygame.Rect(128, 0, 72, 84)
        self.sprite = pygame.Surface((72, 84), pygame.SRCALPHA).convert_alpha()
        self.Status = ARVORE.NORMAL
        self.sprite.blit(self.sprite_sheet, (0, 0), self.CurRect)
        self.screen = None
        self.DistanciaParaAgente = 0
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 16)

    def SetPos(self, pos):
        self.Pos = pos

    def SetMabiente(self, amb):
        self.Ambiente = amb
        self.index = amb.Arvores.index(self)

    def ClickAtMe(self):
        mypos = pygame.Rect(self.Pos[0], self.Pos[1], self.CurRect[2], self.CurRect[3])
        if pygame.Rect.collidepoint(mypos, pygame.mouse.get_pos()):
            pressed = pygame.mouse.get_pressed()
            if pressed[0]:
                self.AcenderFogo()
            if pressed[2]:
                self.ApagarFogo()

    def DesenharDistancia(self):
        if self.Status == ARVORE.FOGO:
            textsurface = self.myfont.render(str(int(self.DistanciaParaAgente)) + "m("+str(self.Ambiente.Arvores.index(self))+")", False, (0, 0, 0))
            self.screen.blit(textsurface, self.Pos)

    def SpriteUpdate(self):
        self.sprite.fill(0)
        self.sprite.blit(self.sprite_sheet, (0, 0), self.CurRect)

    def ApagarFogo(self):
        self.Status = ARVORE.NORMAL
        self.SpriteUpdate()

    def AcenderFogo(self):
        self.Status = ARVORE.FOGO
        self.sprite.fill(0)
        self.sprite.blit(self.sprite_sheet, (0, 0), self.RectFogo)

    def Desenhar(self):
        self.screen.blit(self.sprite, self.Pos)
    
    def SetScreen(self, screen):
        self.screen = screen
    
    def Atualizar(self):
        self.Desenhar()
        self.ClickAtMe()
        self.DesenharDistancia()

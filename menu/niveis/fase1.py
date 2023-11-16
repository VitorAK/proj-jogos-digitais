import pygame
import os
from pygame.locals import *
from random import randint
from sys import exit

pygame.init()

# files
file_principal = os.path.dirname(__file__)
file_image = os.path.join(file_principal, 'image')

# variáveis
largura = 980
altura = 560
pontos = 0
velocidade = 5
died = False

lixo_x = randint(980, 980)
lixo_y = randint(10, 550)

fonte = pygame.font.SysFont('ariel', 40, True, True)
fundo = pygame.image.load(os.path.join('image/bg1.png'))
fundo = pygame.transform.scale(fundo, (largura, altura))

vilao = pygame.image.load(os.path.join('image/boss1.png'))
vilao_rect = vilao.get_rect()
vilao_x = largura - 190
vilao_y = altura // 13

personagem1 = pygame.image.load(os.path.join('image/personagem1.png'))
personagem1_rect = personagem1.get_rect()
personagem2 = pygame.image.load(os.path.join('image/personagem2.png'))
personagem2_rect = personagem2.get_rect()
personagem1_x = 70
personagem1_y = 100
personagem2_x = 70
personagem2_y = 400

bala_agua = pygame.image.load(os.path.join('image/bala_agua.png'))
bala_planta = pygame.image.load(os.path.join('image/bala_planta.png'))

lixo = pygame.image.load(os.path.join('image/lixo.png'))
lixo = pygame.transform.scale(lixo, (70, 70))
lixo_rect = lixo.get_rect()

attack = False

# Lista para armazenar os fogos
projeteis = []

# display
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('personagemjoker')
relogio = pygame.time.Clock()

# Variável de controle do cooldown
cooldown_timer1 = 0
cooldown_duration1 = 500
cooldown_timer2 = 0
cooldown_duration2 = 500

class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        # Calcular vida
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

# barra de vida
health_bar = HealthBar(340, 30, 300, 20, 100)

# Variável de controle do jogo
jogando = True
while jogando:
    relogio.tick(60)
    mensagem = f'Score : {pontos}'
    texto = fonte.render(mensagem, True, (255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                jogando = False
                
                
            # Atirar bola de planta com a tecla 'Space'
            if event.key == pygame.K_RETURN and pygame.time.get_ticks() - cooldown_timer1 > cooldown_duration1:
                projeteis.append([personagem1_x, personagem1_y, bala_agua])
                cooldown_timer1 = pygame.time.get_ticks() 
                
            # Atirar bala de água com a tecla 'Return'
            if event.key == pygame.K_SPACE and pygame.time.get_ticks() - cooldown_timer2 > cooldown_duration2:
                projeteis.append([personagem2_x, personagem2_y, bala_planta])
                cooldown_timer2 = pygame.time.get_ticks()


    screen.blit(fundo, (0, 0))
    
    # movimentacao tela
    rel_x = largura % fundo.get_rect().width
    screen.blit(fundo, (rel_x - fundo.get_rect().width, 0))
    if rel_x < 1280:
        screen.blit(fundo, (rel_x, 0))
  
    largura -= 2

    screen.blit(texto, (30, 30))
    screen.blit(lixo, (lixo_x, lixo_y))
    screen.blit(personagem1, (personagem1_x, personagem1_y))
    screen.blit(personagem2, (personagem2_x, personagem2_y))
    screen.blit(vilao, (vilao_x, vilao_y))

    # Atualização dos mísseis
    for proj in projeteis:
        proj[0] += velocidade * 2 

   
    for proj in projeteis:
        screen.blit(proj[2], (proj[0], proj[1]))  # Use a terceira posição da lista para a imagem do projétil
        proj_rect = proj[2].get_rect(topleft=(proj[0], proj[1]))
        if proj_rect.colliderect(vilao_rect):
        
         if health_bar.hp == 100:
             health_bar.hp = 90
      
         elif health_bar.hp == 90:
             health_bar.hp = 80
         elif health_bar.hp == 90:
             health_bar.hp = 80  
         elif health_bar.hp == 80:
             health_bar.hp = 70 
         elif health_bar.hp == 70:
             health_bar.hp = 60    
         elif health_bar.hp == 60:
             health_bar.hp = 50 
         elif health_bar.hp == 50:
             health_bar.hp = 40
         elif health_bar.hp == 40:
             health_bar.hp = 30    
         elif health_bar.hp == 30:
             health_bar.hp = 20 
         elif health_bar.hp == 20:
             health_bar.hp = 10 
         elif health_bar.hp == 10:
             health_bar.hp = 0  
         elif health_bar.hp == 0:
             jogando= False                                 
         projeteis.remove(proj)    
         
        if proj_rect.colliderect(lixo_rect):
            projeteis.remove(proj)  # Remove a bala que atingiu o lixo
            pontos += 5
            lixo_x = randint(980, 980)
            lixo_y = randint(10, 550)

    comandos = pygame.key.get_pressed()
    if comandos[pygame.K_UP] and personagem1_y > 1:
        if personagem1_y > altura / 2:
            personagem1_y -= velocidade * 2
        else: 
            personagem1_y -= velocidade
    if comandos[pygame.K_DOWN] and personagem1_y < 480:
        if personagem1_y > altura / 2:
            personagem1_y += velocidade * 2
        else:        
            personagem1_y += velocidade
    if comandos[pygame.K_LEFT] and personagem1_x > 1:
        if personagem1_y > altura / 2:  
            personagem1_x -= velocidade * 2
        else:        
            personagem1_x -= velocidade
    if comandos[pygame.K_RIGHT] and personagem1_x < 1200:
        if personagem1_y > altura / 2:  
            personagem1_x += velocidade * 2
        else:        
            personagem1_x += velocidade
    
    #Aumenta velocidade do personagem dois da metade do mapa para baixo
    if comandos[pygame.K_w]and personagem2_y > 1:
            personagem2_y -= velocidade

    if comandos[pygame.K_s]and personagem2_y < 480:

            personagem2_y += velocidade

    if comandos[pygame.K_a] and personagem2_x > 1:

            personagem2_x -= velocidade

    if comandos[pygame.K_d]and personagem2_x < 1200:

            personagem2_x += velocidade
            
    lixo_x -= 4

    if lixo_x < -2:
        lixo_x = randint(980, 980)
        lixo_y = randint(10, 550)

    personagem1_rect.x = personagem1_x
    vilao_rect.x = vilao_x
    personagem1_rect.y = personagem1_y
    personagem2_rect.x = personagem2_x
    personagem2_rect.y = personagem2_y
    lixo_rect.x = lixo_x
    lixo_rect.y = lixo_y

    # Verifica colisão entre fogo e lixo
    for proj in projeteis:
        screen.blit(proj[2], (proj[0], proj[1]))  # Use a terceira posição da lista para a imagem do projétil
        proj_rect = proj[2].get_rect(topleft=(proj[0], proj[1]))
        if proj_rect.colliderect(lixo_rect):
            pontos += 3
            lixo_x = randint(980, 980)
            lixo_y = randint(10, 550)
    if personagem2_rect.colliderect(lixo_rect):
            pontos += 3
            lixo_x = randint(980, 980)
            lixo_y = randint(10, 550)
    # Verifica colisão entre personagem e lixo
    if personagem1_rect.colliderect(lixo_rect) :
        died = True
        while died:
            fonte2 = pygame.font.SysFont('ariel', 50, True, True)
            mensagem = f'Pressione R para jogar novamente'
            texto = fonte2.render(mensagem, True, (255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K_r:
                        died = False
                        # Reiniciar jogo
                        personagem_x = 100
                        personagem_y = 400
                        vilao_x = 800
                        vilao_y = 10
                        personagem2_x = 200
                        personagem2_y = 300
                        lixo_x = randint(980, 980)
                        lixo_y = randint(10, 550)
                        pontos = 0
                        health_bar.hp = 100

            screen.fill((0, 0, 0))
            screen.blit(texto, (250, 300))
            pygame.display.update()

    # barra de vida
    health_bar.draw(screen)
    pygame.display.flip()

pygame.quit()
exit()

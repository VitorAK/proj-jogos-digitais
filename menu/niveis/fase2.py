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

onda_x = randint(980, 980)
onda_y = randint(10, 550)

fonte = pygame.font.SysFont('ariel', 40, True, True)
fundo = pygame.image.load(os.path.join('image/bg2.png'))
fundo = pygame.transform.scale(fundo, (largura, altura))

vilao = pygame.image.load(os.path.join('image/boss2.png'))
vilao_rect = vilao.get_rect()
vilao_x = largura - 190
vilao_y = altura // 4

personagem1 = pygame.image.load(os.path.join('image/personagem1.png'))
personagem1_rect = personagem1.get_rect()
parede = pygame.image.load(os.path.join('image/parede.png'))
parede_rect = parede.get_rect()
parede2= pygame.image.load(os.path.join('image/parede.png'))
parede2_rect = parede2.get_rect()

personagem2 = pygame.image.load(os.path.join('image/personagem2.png'))
personagem2_rect = personagem2.get_rect()
personagem1_x = 70
personagem1_y = 100
personagem2_x = 70
personagem2_y = 400
parede_x = 310
parede_y = -80
parede2_x = 310
parede2_y = 440


personagem3_imagem = pygame.image.load(os.path.join('image/personagem2.png'))
num_personagens = 6  # Adjust the number of characters as needed
personagens = []
   
bala_agua = pygame.image.load(os.path.join('image/bala_agua.png'))
bala_planta = pygame.image.load(os.path.join('image/bala_planta.png'))

onda = pygame.image.load(os.path.join('image/onda.png'))
onda = pygame.transform.scale(onda, (70, 70))
onda_rect = onda.get_rect()

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
health_bar = HealthBar(250, 30, 300, 20, 100)

for _ in range(num_personagens):
    personagem3 = pygame.image.load(os.path.join('image/humano.png'))
    personagem3_rect = personagem3.get_rect()

    personagem3_x = randint(10, 100)
    personagem3_y = randint(10, 500)

    personagens.append({'x': personagem3_x, 'y': personagem3_y, 'image': personagem3, 'rect': personagem3_rect})


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
    
    screen.blit(texto, (30, 30))
    screen.blit(onda, (onda_x, onda_y))
    screen.blit(personagem1, (personagem1_x, personagem1_y))
    screen.blit(personagem2, (personagem2_x, personagem2_y))
    screen.blit(parede, (parede_x, parede_y))
    screen.blit(parede2, (parede2_x, parede2_y))    
    screen.blit(vilao, (vilao_x, vilao_y))

    for personagem_data in personagens:
        screen.blit(personagem_data['image'], (personagem_data['x'], personagem_data['y']))
        
    personagem3_rect.x = personagem3_x
    personagem3_rect.y = personagem3_y



 #Colisoes com o personagem3   
    for personagem_data in personagens:
    # Atualiza os retângulos dos personagens
        personagem_data['rect'].x = personagem_data['x']
        personagem_data['rect'].y = personagem_data['y']
   
    # Colisao do personagem1 com o 3
        if personagem1_rect.colliderect(personagem_data['rect']):
         
            if personagem1_y < personagem_data['y']:
                if personagem_data['y'] < 480:
                    personagem_data['y'] += velocidade  # Move para baixo
            else:
             if personagem_data['y'] > 1:                 
                 personagem_data['y'] -= velocidade  # Move para cima
    # Colisao do personagem 3 com a agua         
        if personagem_data['rect'].colliderect(onda_rect):
            pontos -= 1
            onda_x = randint(980, 980)
            onda_y = randint(10, 550) 


    # Atualização dos mísseis
    for proj in projeteis:
        proj[0] += velocidade * 2 

   
    for proj in projeteis:
        screen.blit(proj[2], (proj[0], proj[1]))
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
         
        if proj_rect.colliderect(onda_rect):
            projeteis.remove(proj)  # Remove a bala que atingiu o lixo
            onda_x = randint(980, 980)
            onda_y = randint(10, 550)

    comandos = pygame.key.get_pressed()
    if comandos[pygame.K_UP] and personagem1_y > 1:
        if personagem1_x > largura / 3:
            personagem1_y -= velocidade * 2
        else: 
            personagem1_y -= velocidade
    if comandos[pygame.K_DOWN] and personagem1_y < 480:
        if personagem1_x > largura / 3:
            personagem1_y += velocidade * 2
        else:        
            personagem1_y += velocidade
    if comandos[pygame.K_LEFT] and personagem1_x > 1:
        if personagem1_x > largura / 3:
            personagem1_x -= velocidade * 2
        else:        
            personagem1_x -= velocidade
    if comandos[pygame.K_RIGHT] and personagem1_x < 1200:
        if personagem1_x > largura / 3: 
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
            
    onda_x -= 5

    if onda_x < -2:
        onda_x = randint(980, 980)
        onda_y = randint(10, 550)

    personagem1_rect.x = personagem1_x
    vilao_rect.x = vilao_x
    vilao_rect.y = vilao_y
    parede_rect.x = parede_x
    parede2_rect.x = parede2_x
    parede_rect.y = parede_y
    parede2_rect.y = parede2_y
    personagem1_rect.y = personagem1_y
    personagem2_rect.x = personagem2_x
    personagem2_rect.y = personagem2_y
    personagem3_rect.x = personagem3_x
    personagem3_rect.y = personagem3_y
    onda_rect.x = onda_x
    onda_rect.y = onda_y
    
    if onda_rect.colliderect(parede_rect):
    # Trash collided with parede_rect, reset trash position
        onda_x = randint(980, 980)
        onda_y = randint(10, 550)

    if onda_rect.colliderect(parede2_rect):
        # Trash collided with parede2_rect, reset trash position
        onda_x = randint(980, 980)
        onda_y = randint(10, 550)

    # Verifica colisão entre fogo e onda
    for proj in projeteis:
        screen.blit(proj[2], (proj[0], proj[1]))  
        proj_rect = proj[2].get_rect(topleft=(proj[0], proj[1]))
        if proj_rect.colliderect(onda_rect):
            pontos += 1
            onda_x = randint(980, 980)
            onda_y = randint(10, 550)
    if personagem2_rect.colliderect(onda_rect):
            pontos += 1
            onda_x = randint(980, 980)
            onda_y = randint(10, 550)
    if parede_rect.colliderect(onda_rect):
           
            onda_x = randint(980, 980)
            onda_y = randint(10, 550)
    if parede2_rect.colliderect(onda_rect):
            
            onda_x = randint(980, 980)
            onda_y = randint(10, 550)        
                               
           
    # Verifica colisão entre personagem e onda
    if personagem1_rect.colliderect(onda_rect):
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
                        vilao_x = largura - 190
                        vilao_y = altura // 4
                        personagem2_x = 200
                        personagem2_y = 300
                        personagem3_x = 400
                        personagem3_y = 400
                        parede_x = 310
                        parede_y = -80
                        parede2_x = 310
                        parede2_y = 440                  
                        onda_x = randint(980, 980)
                        onda_y = randint(10, 550)
                        pontos = 0
                        health_bar.hp = 100
                        

            screen.fill((0, 0, 0))
            screen.blit(texto, (250, 300))
            pygame.display.update()

    # barra de vida
    health_bar.draw(screen)
    health_bar.bar=50
    pygame.display.flip()

pygame.quit()
exit()

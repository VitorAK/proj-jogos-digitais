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
moving_left = False  

fogo_x = randint(980, 980)
fogo_y = randint(10, 550)

fonte = pygame.font.SysFont('ariel', 40, True, True)
fundo = pygame.image.load(os.path.join('image/bg3.png'))
fundo = pygame.transform.scale(fundo, (largura, altura))

vilao = pygame.image.load(os.path.join('image/boss3.png'))
vilao_rect = vilao.get_rect()
vilao_x = largura - 190
vilao_y = altura // 13

personagem1 = pygame.image.load(os.path.join('image/personagem1.png'))
personagem1_flipped = pygame.transform.flip(personagem1, True, False)  # Imagem virada para trás
personagem1_rect = personagem1.get_rect()
personagem2 = pygame.image.load(os.path.join('image/personagem2.png'))
personagem2_flipped = pygame.transform.flip(personagem2, True, False)  # Imagem virada para trás
personagem2_rect = personagem2.get_rect()

personagem1_x = 70
personagem1_y = 100
personagem2_x = 70
personagem2_y = 400

bala_agua = pygame.image.load(os.path.join('image/bala_agua.png'))
bala_planta = pygame.image.load(os.path.join('image/bala_planta.png'))

fogo = pygame.image.load(os.path.join('image/fogo.png'))
fogo_rect = fogo.get_rect()

attack = False

# Lista para armazenar os fogos
fogos = []

# display
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('personagemjoker')
relogio = pygame.time.Clock()

# Variável de controle do cooldown
cooldown_timer1 = 0
cooldown_duration1 = 500
cooldown_timer2 = 0
cooldown_duration2 = 500

class Tronco(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_normal = pygame.image.load(os.path.join('image/tronco.png'))
        self.image_normal = pygame.transform.scale(self.image_normal, (60, 60))
        self.image_fire = pygame.image.load(os.path.join('image/tronco_pegando_fogo.png'))
        self.image_fire = pygame.transform.scale(self.image_fire, (60, 60))
        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.on_fire = False
        self.fire_timer = 0
        self.points = 0
        self.fire_duration = 3000  # 3 segundos
        self.max_fire_duration = 5000  # 5 segundos
        self.initial_image_normal = self.image_normal.copy()
        self.initial_image_fire = self.image_fire.copy()

    def update(self):
        if self.on_fire:
            current_time = pygame.time.get_ticks()
            fire_time_elapsed = current_time - self.fire_timer
            if fire_time_elapsed > self.fire_duration and fire_time_elapsed <= self.max_fire_duration:
                self.points -= 20
            elif fire_time_elapsed > self.max_fire_duration:
                self.points -= 30
                self.on_fire = False
                self.image = self.image_normal
            if fire_time_elapsed <= self.fire_duration:
                self.image = self.image_fire

    def ignite(self):
        self.on_fire = True
        self.fire_timer = pygame.time.get_ticks()
        self.image = self.image_fire

    def extinguish(self):
        self.on_fire = False
        self.image = self.image_normal
        self.points += 5
        
    def reset(self):
        self.image_normal = self.initial_image_normal
        self.image_fire = self.initial_image_fire
        self.image = self.image_normal
        self.on_fire = False
        self.fire_timer = 0
        self.points = 0

# Lista para armazenar os troncos
troncos = [Tronco(10, 80 + i * 80) for i in range(6)]

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

class Esquilo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('image/esquilo.png'))
        self.rect = self.image.get_rect()
        self.rect.x = randint(100, 800)  # Posição X aleatória
        self.rect.y = randint(100, 500)  # Posição Y aleatória
        self.spawn_time = pygame.time.get_ticks()  # Momento de spawn
        self.visible = True

    def update(self):
        current_time = pygame.time.get_ticks()
        # Verifica se passaram 5 segundos desde o spawn
        if current_time - self.spawn_time > 5000:  # 5000ms = 5 segundos
            self.visible = False
esquilo_spawn_timer = pygame.time.get_ticks()        
esquilos = [] 
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
                fogos.append([personagem1_x, personagem1_y, bala_agua, moving_left_personagem1])
                cooldown_timer1 = pygame.time.get_ticks()
                
            # Atirar bala de água com a tecla 'Return'
            if event.key == pygame.K_SPACE and pygame.time.get_ticks() - cooldown_timer2 > cooldown_duration2:
                fogos.append([personagem2_x, personagem2_y, bala_planta, moving_left_personagem2])
                cooldown_timer2 = pygame.time.get_ticks()


    screen.blit(fundo, (0, 0))
    
    # movimentacao tela
    rel_x = largura % fundo.get_rect().width
    screen.blit(fundo, (rel_x - fundo.get_rect().width, 0))
    if rel_x < 1280:
        screen.blit(fundo, (rel_x, 0))
  
    largura -= 2

    screen.blit(texto, (30, 30))
    screen.blit(fogo, (fogo_x, fogo_y))
    screen.blit(personagem1, (personagem1_x, personagem1_y))
    screen.blit(personagem2, (personagem2_x, personagem2_y))
    screen.blit(vilao, (vilao_x, vilao_y))

    # Criando esquilos com intervalos de tempo
    current_time = pygame.time.get_ticks()
    for esquilo in esquilos:
        if current_time - esquilo.spawn_time > 10000:  # Verifica se passaram 10 segundos desde o spawn
            esquilo.visible = True
            esquilo.spawn_time = current_time  # Atualiza o momento de spawnwn
    if current_time > esquilo_spawn_timer + 2000:
        esquilos.append(Esquilo())
        esquilo_spawn_timer = current_time
    # Atualizando os esquilos na tela
    for esquilo in esquilos:
        if esquilo.visible:
            screen.blit(esquilo.image, esquilo.rect)
            esquilo.update()

    # Verificando colisão com os esquilos
    for esquilo in esquilos:
        if personagem1_rect.colliderect(esquilo.rect) or personagem2_rect.colliderect(esquilo.rect):
            if esquilo.visible:
                pontos += 2  # Aumenta a pontuação
                esquilo.visible = False  # Esconde o esquilo

    # Removendo esquilos invisíveis da lista
    esquilos = [esquilo for esquilo in esquilos if esquilo.visible]

    for tronco in troncos:
        screen.blit(tronco.image, tronco.rect)
        tronco.update()

        if tronco.rect.colliderect(fogo_rect):
            tronco.ignite()
            fogo_x = randint(980, 980)
            fogo_y = randint(10, 550)

        # Lógica de colisão com a bala de água
        for proj in fogos:
            if tronco.rect.colliderect(proj[2].get_rect(topleft=(proj[0], proj[1]))) and tronco.on_fire:
                if proj[2] == bala_agua:
                    pontos+=1
                    tronco.extinguish()
                    fogos.remove(proj)

    # Atualização dos mísseis
    for proj in fogos:
        if proj[3]:  
         proj[0] += velocidade * -2
        else:
         proj[0] += velocidade * 2
         
   
    for proj in fogos:
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
         fogos.remove(proj)    
         
        if proj_rect.colliderect(fogo_rect):
            if proj[2] == bala_planta:
                fogos.remove(proj)  # Remove a bala de planta atingida
            else:  # Se não for bala de planta, é a bala de água
                fogos.remove(proj)  # Remove a bala de água atingida
                fogo_x = randint(980, 980)
                fogo_y = randint(10, 550)
    moving_left_personagem1 = False
    moving_left_personagem2 = False
    comandos = pygame.key.get_pressed()
    if comandos[pygame.K_UP] and personagem1_y > 1:
        personagem1_y -= velocidade 
        moving_left_personagem1 = moving_left_personagem1 
    if comandos[pygame.K_DOWN] and personagem1_y < 480: 
        personagem1_y += velocidade
    if comandos[pygame.K_LEFT] and personagem1_x > 1:
        personagem1_x -= velocidade
        moving_left_personagem1 = True
    elif event.type == pygame.KEYUP:
            
            if event.key == pygame.K_LEFT:
                   
             moving_left_personagem1 = True 
          
    if comandos[pygame.K_RIGHT] and personagem1_x < 900:
        personagem1_x += velocidade
        moving_left_personagem1 = False  
        
    if moving_left_personagem1:
        personagem1 = personagem1_flipped  
    else:
        personagem1 = pygame.image.load(os.path.join('image/personagem1.png'))  # Usa a imagem original
            
            
    if comandos[pygame.K_w] and personagem2_y > 1:
        personagem2_y -= velocidade
    if comandos[pygame.K_s] and personagem2_y < 480:
        personagem2_y += velocidade
    if comandos[pygame.K_a] and personagem2_x > 1:
        personagem2_x -= velocidade
        moving_left_personagem2 = True  # Define a flag para verdadeiro
    elif event.type == pygame.KEYUP:
            
            if event.key == pygame.K_a:
                   
             moving_left_personagem2= True 
              
    if comandos[pygame.K_d] and personagem2_x < 900:
        personagem2_x += velocidade
        moving_left_personagem2 = False  # Define a flag para falso
        
    if   moving_left_personagem2 :
        personagem2 = personagem2_flipped  # Usa a imagem virada para trás
    else:
        personagem2 = pygame.image.load(os.path.join('image/personagem2.png'))  # Usa a imagem original
        
    
    for tronco in troncos:
    # Colisão do personagem 1 com os troncos
        if personagem1_rect.colliderect(tronco.rect):
            if comandos[pygame.K_UP]:
                if personagem1_rect.top > tronco.rect.bottom:
                    personagem1_y -= velocidade
            if comandos[pygame.K_DOWN]:
                if personagem1_rect.bottom < tronco.rect.top:
                    personagem1_y += velocidade
            if comandos[pygame.K_LEFT]:
                if personagem1_rect.left > tronco.rect.right:
                    personagem1_x -= velocidade
            if comandos[pygame.K_RIGHT]:
                if personagem1_rect.right < tronco.rect.left:
                    personagem1_x += velocidade
    
    # Colisão do personagem 2 com os troncos
        if personagem2_rect.colliderect(tronco.rect):
            if comandos[pygame.K_w]:
                if personagem2_rect.top > tronco.rect.bottom:
                    personagem2_y -= velocidade
            if comandos[pygame.K_s]:
                if personagem2_rect.bottom < tronco.rect.top:
                    personagem2_y += velocidade
            if comandos[pygame.K_a]:
                if personagem2_rect.left > tronco.rect.right:
                    personagem2_x -= velocidade
            if comandos[pygame.K_d]:
                if personagem2_rect.right < tronco.rect.left:
                    personagem2_x += velocidade

    fogo_x -= 7

    if fogo_x < -2:
        fogo_x = randint(980, 980)
        fogo_y = randint(10, 550)

    personagem1_rect.x = personagem1_x
    vilao_rect.x = vilao_x
    personagem1_rect.y = personagem1_y
    personagem2_rect.x = personagem2_x
    personagem2_rect.y = personagem2_y
    fogo_rect.x = fogo_x
    fogo_rect.y = fogo_y

    # Verifica colisão entre personagem e fogo
    if personagem1_rect.colliderect(fogo_rect) or personagem2_rect.colliderect(fogo_rect) :
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
                        fogo_x = randint(980, 980)
                        fogo_y = randint(10, 550)
                        pontos = 0
                        health_bar.hp = 100
                    for tronco in troncos:
                        tronco.reset()


            screen.fill((0, 0, 0))
            screen.blit(texto, (250, 300))
            pygame.display.update()

    # barra de vida
    health_bar.draw(screen)
    pygame.display.flip()

pygame.quit()
exit()

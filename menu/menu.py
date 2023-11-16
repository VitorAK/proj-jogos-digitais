import pygame
import sys
from button import Button  # Importe a classe Button conforme necessário
from pygame.locals import *
pygame.init()

SCREEN = pygame.display.set_mode((1280, 760))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def nivel1():
 from niveis import fase1   
 fase1() 

def nivel2():
 from niveis import fase2  
 fase2() 

def nivel3():
 from niveis import fase3    
 fase3()  
  
def instruções():
    pygame.init()
    FPS = 30
    fpsClock = pygame.time.Clock()
    largura, altura = 980, 560
    screen = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Jogos Digitais")
    BLACK = (0, 0, 0)

    running = True
    while running:
        screen.fill(BLACK)

        # Adicione este trecho para mostrar o texto na tela
        font = pygame.font.Font(None, 30)
        texto_linha1 = "W, A, S, D 	Teclas de movimento do personagem 2 ."
        texto_linha2 = "UP, RIGHT, DOWN, LEFT 	Teclas de movimento do personagem 1."
        texto_linha3 = "ESPAÇO 	Atira bola de planta."
        texto_linha4 = "ENTER 	Atira bola de água."
  

        text1 = font.render(texto_linha1, True, (255, 255, 255))
        text_rect1 = text1.get_rect(center=(largura // 2, altura // 2 -200))

        text2 = font.render(texto_linha2, True, (255, 255, 255))
        text_rect2 = text2.get_rect(center=(largura // 2, altura // 2 -100))

        text3 = font.render(texto_linha3, True, (255, 255, 255))
        text_rect3 = text3.get_rect(center=(largura // 2, altura // 2 ))

        text4 = font.render(texto_linha4, True, (255, 255, 255))
        text_rect4 = text4.get_rect(center=(largura // 2, altura // 2 +100))



      


        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        screen.blit(text3, text_rect3)
        screen.blit(text4, text_rect4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        fpsClock.tick(FPS)



def diminuir_volume(som, volume):
    som.set_volume(volume)
def main_menu():
    
    SCREEN = pygame.display.set_mode((980, 560))  # Ajuste das proporções para 980x560
    som_menu = pygame.mixer.Sound("menusom.mp3")
    som_menu.play()
    diminuir_volume(som_menu, 0.1)
    
    
    in_menu = True
    while in_menu:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        MENU_TEXT = get_font(80).render("MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN.get_width() // 2, 40))

       
        NIVEL1_BUTTON = Button(image = None, pos=(SCREEN.get_width() // 2, 100),
                              text_input="NIVEL 1", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        NIVEL2_BUTTON = Button(image = None, pos=(SCREEN.get_width() // 2, 200),
                              text_input="NIVEL 2", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        NIVEL3_BUTTON = Button(image = None, pos=(SCREEN.get_width() // 2, 300),
                              text_input="NIVEL 3", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        INSTRUÇÕES_BUTTON = Button(image = None, pos=(SCREEN.get_width() // 2, 400),
                              text_input="COMO JOGAR", font=get_font(60), base_color="#d7fcd4", hovering_color="White") 
        QUIT_BUTTON = Button(image = None, pos=(SCREEN.get_width() // 2, 500),
                             text_input="QUIT", font=get_font(60), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [ NIVEL1_BUTTON, NIVEL2_BUTTON, NIVEL3_BUTTON,INSTRUÇÕES_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                som_menu.stop()
                if NIVEL1_BUTTON.checkForInput(MENU_MOUSE_POS):
                    nivel1()
                    
                    som_menu.stop()
                if NIVEL2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    nivel2()
                    
                    som_menu.stop()
                if NIVEL3_BUTTON.checkForInput(MENU_MOUSE_POS):
                    nivel3()
                    
                    som_menu.stop()
                if INSTRUÇÕES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    instruções()
                    
                    som_menu.stop()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.update()
    som_menu.stop()  
    
main_menu()


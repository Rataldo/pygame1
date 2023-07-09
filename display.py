import pygame 
from sys import exit # funcion exit termina el codigo de forma segura


pygame.init() # comienza todo
screen = pygame.display.set_mode((800,400)) #valores de la tupla son weidth and height
pygame.display.set_caption("Runner")
clock = pygame.time.Clock() # limitar FPS
test_font = pygame.font.Font("font/Pixeltype.ttf", 50) # al final es font type, font size

# surfaces van asociadas a display surface
# test_surface = pygame.Surface((100,200))
# test_surface.fill("Red")


sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

score_surface = test_font.render("My game", False, (64,64,64)) # text del score
score_rectangle = score_surface.get_rect(center = (400,50))

snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha() #convierte imagenes en algo que pygame puede procesar
snail_rectangle = snail_surface.get_rect(midbottom = (600,300))

player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rectangle = player_surface.get_rect(midbottom = (50,300)) # toma de referencia el punto topleft del rectangulo para colocar las coordenadas del display



# Todo va a ocurrir dentro de wl while loop. arriba solo definimos algunas variables

while True: #mantiene el juego abierto por siempre
    for event in pygame.event.get(): # para evento en eventos de pygame: (hay muchos eventos. todos en la documentacion)
        if event.type == pygame.QUIT: # si el tipo de evento es QUIT:
            pygame.quit() #ejecuta la funcion QUIT / finaliza todo
            exit() # ejecuta funcion exit y acaba con el codigo aca.
            
            
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rectangle.collidepoint(event.pos):
        #         print("collision")


    # en el screen blit el orden que lo coloco es el orden en que se generaran.
    screen.blit(sky_surface,(0,0)) #esto asocia el surface a la display surface.               
    screen.blit(ground_surface,(0,300))
    pygame.draw.rect(screen, "#c0e8ec", score_rectangle)
    pygame.draw.rect(screen, "#c0e8ec", score_rectangle,10)
    screen.blit(score_surface,score_rectangle)
    
    snail_rectangle.x -= 4 # variable para mover el surface
    if snail_rectangle.right <= 0: # if statement para regresar el surface a su origen
        snail_rectangle.left = 800    
    screen.blit(snail_surface,snail_rectangle) # colocamos el surface usando un rectangulo
    screen.blit(player_surface,player_rectangle)
    
    
    
    # if player_rectangle.colliderect(snail_rectangle): # por defecto solo un if en python es False
    #     print("collision")
    # mouse_pos = pygame.mouse.get_pos()
    # if player_rectangle.collidepoint((mouse_pos)):
    #     print(pygame.mouse.get_pressed())
    
    
    
    
    pygame.display.update() # updatea el display surface (la pantalla abierta arriba)
    clock.tick(60) #limite de 60 fps
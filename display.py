import pygame 
from sys import exit # funcion exit termina el codigo de forma segura


pygame.init() # comienza todo
screen = pygame.display.set_mode((800,400)) #valores de la tupla son weidth and height
pygame.display.set_caption("Runner")
clock = pygame.time.Clock() # limitar FPS

# surfaces van asociadas a display surface
# test_surface = pygame.Surface((100,200))
# test_surface.fill("Red")
sky_surface = pygame.image.load("graphics/Sky.png")
ground_surface = pygame.image.load("graphics/ground.png")



# Todo va a ocurrir dentro de wl while loop. arriba solo definimos algunas variables

while True: #mantiene el juego abierto por siempre
    for event in pygame.event.get(): # para evento en eventos de pygame: (hay muchos eventos. todos en la documentacion)
        if event.type == pygame.QUIT: # si el tipo de evento es QUIT:
            pygame.quit() #ejecuta la funcion QUIT / finaliza todo
            exit() # ejecuta funcion exit y acaba con el codigo aca.

    # en el screen blit el orden que lo coloco es el orden en que se generaran.
    
    screen.blit(sky_surface,(0,0)) #esto asocia el surface a la display surface.               
    screen.blit(ground_surface,(0,300))
    
    pygame.display.update() # updatea el display surface (la pantalla abierta arriba)
    clock.tick(60) #limite de 60 fps
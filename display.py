import pygame 
from sys import exit # funcion exit termina el codigo de forma segura

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time # necesario para resetear contador a 0
    score_surface = test_font.render(f"Score: {current_time}", False,(64,64,64))
    score_rectangle = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rectangle)
    

pygame.init() # comienza todo
screen = pygame.display.set_mode((800,400)) #valores de la tupla son weidth and height
pygame.display.set_caption("Runner")
clock = pygame.time.Clock() # limitar FPS
test_font = pygame.font.Font("font/Pixeltype.ttf", 50) # al final es font type, font size
game_active = True
start_time = 0 #variable para resetear el contador a 0

# surfaces van asociadas a display surface
# test_surface = pygame.Surface((100,200))
# test_surface.fill("Red")


sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# score_surface = test_font.render("My game", False, (64,64,64)) # text del score
# score_rectangle = score_surface.get_rect(center = (400,50))

snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha() #convierte imagenes en algo que pygame puede procesar
snail_rectangle = snail_surface.get_rect(midbottom = (600,300))

player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rectangle = player_surface.get_rect(midbottom = (50,300)) # toma de referencia el punto topleft del rectangulo para colocar las coordenadas del display
player_gravity = 0


# Todo va a ocurrir dentro de wl while loop. arriba solo definimos algunas variables

while True: #mantiene el juego abierto por siempre
    for event in pygame.event.get(): # para evento en eventos de pygame: (hay muchos eventos. todos en la documentacion)
        if event.type == pygame.QUIT: # si el tipo de evento es QUIT:
            pygame.quit() #ejecuta la funcion QUIT / finaliza todo
            exit() # ejecuta funcion exit y acaba con el codigo aca.
        
        if game_active:
                # aca colocamos que debemos apretar el boton k_space y abajo que es lo que hace.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300: #condicion para solo saltar si estamos en este punto.
                    player_gravity = -23
                
            if event.type == pygame.MOUSEBUTTONDOWN and player_rectangle.bottom >= 300:
                    if player_rectangle.collidepoint(event.pos):
                        player_gravity = -23
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rectangle.left = 800
                start_time = int(pygame.time.get_ticks() / 1000) #resetea contador a cero

    #codigo del juego activo. 
    if game_active:
        # en el screen blit el orden que lo coloco es el orden en que se generaran.
        screen.blit(sky_surface,(0,0)) #esto asocia el surface a la display surface.               
        screen.blit(ground_surface,(0,300))
        display_score()
        
        snail_rectangle.x -= 4 # variable para mover el surface
        if snail_rectangle.right <= 0: # if statement para regresar el surface a su origen
            snail_rectangle.left = 800    
        screen.blit(snail_surface,snail_rectangle) # colocamos el surface usando un rectangulo
        
        #player
        player_gravity += 1 #aumento exponencial del valor de gravedad
        player_rectangle.y += player_gravity # sumamos la gravedad a el eje y  del rectangulo del jugador
        if player_rectangle.bottom >= 300: 
            player_rectangle.bottom = 300
            
        screen.blit(player_surface,player_rectangle)
        
        #collision
        if snail_rectangle.colliderect(player_rectangle):
            game_active = False
    #que pasa luego del gameover, intro o menu
    else:
        screen.fill("Yellow")
    
    
    # keys = pygame.key.get_pressed()
    pygame.display.update() # updatea el display surface (la pantalla abierta arriba)
    clock.tick(60) #limite de 60 fps
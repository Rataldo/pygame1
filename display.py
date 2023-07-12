import pygame 
from sys import exit # funcion exit termina el codigo de forma segura
import random
from random import randint, choice


# classes

class Player(pygame.sprite.Sprite): # se agrega todo el codigo del jugador aca
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2] # lista con animaciones de caminar
        self.player_index = 0 # indice para ser usado debajo
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()
    
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        
        self.jump_sound = pygame.mixer.Sound("audio/audio_jump.mp3")
        self.jump_sound.set_volume(0.5)
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -22
            self.jump_sound.play()
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        
        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if  type == "fly":
            fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha() #convierte imagenes en algo que pygame puede procesar
            snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2] # lista con todos los frames
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900,1100), y_pos))
        
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()




# score function
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time # necesario para resetear contador a 0
    score_surface = test_font.render(f"Score: {current_time}", False,(64,64,64))
    score_rectangle = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rectangle)
    return current_time

# obstacle movement function
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            # if statement para tener fly o snail 
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)
            
            # borra obstaculos que esten fuera de la pantalla
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

# collissions function
def collisions (player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False # si jugador choca con obstaculo retorna False
    return True # si jugador no choca con nada return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False): # necesitamos player.sprite para acceder al sprite dentro de player group single
        obstacle_group.empty() # limpia la lista cuando hay colision
        return False
    else:
        return True

# animations de correr y saltar
def player_animation():
    global player_surface, player_index
    
    if player_rectangle.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]

# comienza todo
pygame.init() 
screen = pygame.display.set_mode((800,400)) #valores de la tupla son weidth and height
pygame.display.set_caption("Runner")
clock = pygame.time.Clock() # limitar FPS
test_font = pygame.font.Font("font/Pixeltype.ttf", 50) # al final es font type, font size
game_active = False # si esta en True empieza el juego, si esta en false primero ira al else statement y mostrara el game over screen
start_time = 0 #variable para resetear el contador a 0
score = 0
bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.play(loops= -1)
bg_music.set_volume(0.3)
# groups

# player
player = pygame.sprite.GroupSingle() # se asigna el jugador a un grupo
player.add( Player())

# obstacles
obstacle_group = pygame.sprite.Group()


# sky surface
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# score_surface = test_font.render("My game", False, (64,64,64)) # text del score
# score_rectangle = score_surface.get_rect(center = (400,50))

# obstacles

# snail
snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha() #convierte imagenes en algo que pygame puede procesar
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2] # lista con todos los frames
snail_frame_index = 0 # indice de frames (para cambiar entre frames)
snail_surface = snail_frames[snail_frame_index] # surface que hace que el indice de frames cambie

# fly
fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []

# player surface and gravity
player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_rectangle = player_walk_1.get_rect(midbottom = (50,300)) # toma de referencia el punto topleft del rectangulo para colocar las coordenadas del display
player_walk = [player_walk_1, player_walk_2] # lista con animaciones de caminar
player_index = 0 # indice para ser usado debajo
player_surface = player_walk[player_index] # usamos walking animation con el indice, el cual va a ir alternando

player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()
player_gravity = 0

# intro screen
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha() # imagen para mostrar en intro screen
player_stand = pygame.transform.rotozoom(player_stand,0,2) # transformar el tamaño del player a mostrar en intro screen
player_stand_rectangle = player_stand.get_rect(center = (400,200)) # ubicacion de la imagen a mostrar

# intro screen text
game_name_surface = test_font.render("Pixel Runner",False, (64,64,64))
game_name_rectangle = game_name_surface.get_rect(center = (400,50))

# intro screen continue text
continue_surface = test_font.render("Press SPACE to play", False, (64,64,64))
continue_rectangle = continue_surface.get_rect(center = (400,350))

# Timer
obstacle_timer = pygame.USEREVENT + 1 # se pone +1 para evitar conflicto con USEREVENTS de pygame
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)


fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


# Todo va a ocurrir dentro del while loop. arriba solo definimos algunas variables

while True: #mantiene el juego abierto por siempre
    for event in pygame.event.get(): # para evento en eventos de pygame: (hay muchos eventos. todos en la documentacion)
        if event.type == pygame.QUIT: # si el tipo de evento es QUIT:
            pygame.quit() #ejecuta la funcion QUIT / finaliza todo
            exit() # ejecuta funcion exit y acaba con el codigo aca.
        
        if game_active:
                # aca colocamos que debemos apretar el boton k_space y abajo que es lo que hace.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300: # condicion para solo saltar si estamos en este punto.
                    player_gravity = -23
                
            if event.type == pygame.MOUSEBUTTONDOWN and player_rectangle.bottom >= 300: # condicion para saltar con mouse
                    if player_rectangle.collidepoint(event.pos):
                        player_gravity = -23
            
            # evento de timer de obstaculos (coloca un enemigo desde la lista y le hace append)
            if event.type == obstacle_timer: # timer de spawneo de bichos (dentro de game_active)
                obstacle_group.add(Obstacle(choice(["fly", "snail", "snail"]))) # llamo clase de obstaculos
                # if randint(0,2):
                #     obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900,1100),300)))
                # else:
                #     obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900,1100),210)))                
            
            # event animacion de snail
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]    
                
            # event animacion de fly
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]
            
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # snail_rectangle.left = 800
                start_time = int(pygame.time.get_ticks() / 1000) #resetea contador a cero
                
                
    #codigo del juego activo. 
    if game_active:
        # en el screen blit el orden que lo coloco es el orden en que se generaran.
        
        screen.blit(sky_surface,(0,0)) #esto asocia el surface a la display surface.               
        screen.blit(ground_surface,(0,300))
        score = display_score()
        
        #player
        # player_gravity += 1 #aumento exponencial del valor de gravedad
        # player_rectangle.y += player_gravity # sumamos la gravedad a el eje y  del rectangulo del jugador
        # if player_rectangle.bottom >= 300: 
        #     player_rectangle.bottom = 300 
        # screen.blit(player_surface,player_rectangle)
        # player_animation() # llamamos funcion de animaciones del jugador
        
        # metodos de clases
        player.draw(screen) # se llama al jugador aca
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active = collision_sprite()
        
        # obstacle movement
        
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        
        #collision
        # game_active = collisions(player_rectangle, obstacle_rect_list) # corre funcion collisions con player rectanlge y obstacle rect
        
    #que pasa luego del gameover, intro o menu
    else:
        # game over loop
        screen.fill((94,129,162)) # fill del fondo del intro screen
        screen.blit(player_stand, player_stand_rectangle) # que se muestra en intro screen
        obstacle_rect_list.clear() # limpia la lista de obstaculos al terminar el juego.
        player_rectangle.midbottom = (80,300)
        player_gravity = 0
        
        
        score_message = test_font.render(f"Your score: {score}", False, (64,64,64))
        score_message_rect = score_message.get_rect(center = (400, 50))
        
        if score == 0:
            screen.blit(game_name_surface, game_name_rectangle) # game over text
            screen.blit(continue_surface, continue_rectangle)
        else:
            screen.blit(score_message, score_message_rect)
            screen.blit(continue_surface, continue_rectangle)
            
        

    
    pygame.display.update() # updatea el display surface (la pantalla abierta arriba)
    clock.tick(60) #limite de 60 fps
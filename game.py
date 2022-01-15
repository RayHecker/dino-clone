#boilerplate stuff for initializing window
import pygame
import os
import random
from pygame import font
from pygame.display import get_active

pygame.init()

screen_height = 600;
screen_width = 1100;

screen = pygame.display.set_mode((screen_width, screen_height))
programIcon = pygame.image.load(os.path.join("assets\\Other", "icon.png"))
pygame.display.set_icon(programIcon)
pygame.display.set_caption("Chrome Dino Clone")



#importing all the required assets (this includes- dino assets, cacti assets, dino-bird assets, background cloud and foreground track)
dino_running = [pygame.image.load(os.path.join("assets\\Dino", "dino_run_1.png")), 
                pygame.image.load(os.path.join("assets\\Dino", "dino_run_2.png"))]
dino_jumping = [pygame.image.load(os.path.join("assets\\Dino", "dino_jump.png"))]
dino_ducking = [pygame.image.load(os.path.join("assets\\Dino", "dino_duck_1.png")), 
                pygame.image.load(os.path.join("assets\\Dino", "dino_duck_2.png"))]
dino_dead = pygame.image.load(os.path.join("assets\\Dino", "dino_dead.png"))
screen.blit(dino_dead, (100, 100))

s_cactus = [pygame.image.load(os.path.join("assets\\Cactus", "s_cactus_1.png")),
            pygame.image.load(os.path.join("assets\\Cactus", "s_cactus_2.png")),
            pygame.image.load(os.path.join("assets\\Cactus", "s_cactus_3.png"))]
l_cactus = [pygame.image.load(os.path.join("assets\\Cactus", "l_cactus_1.png")),
            pygame.image.load(os.path.join("assets\\Cactus", "l_cactus_2.png")),
            pygame.image.load(os.path.join("assets\\Cactus", "l_cactus_3.png"))]

bird = [pygame.image.load(os.path.join("assets\\Bird", "bird_1.png")),
        pygame.image.load(os.path.join("assets\\Bird", "bird_2.png"))]

bg_cloud = pygame.image.load(os.path.join("assets\\Other", "Cloud.png"))
fg_track = pygame.image.load(os.path.join("assets\\Other", "Track.png"))



#defining the dino class- it has the various methods needed for the movement and other functionalities of the dinosaur
class Dinosaur:
    #defining position of dinosaur
    x_pos = 100
    y_pos = 310
    y_duck_pos = 340
    jump_vel_const = 8.5
        
    def __init__ (self):
        #defining class variables
        self.ducking = dino_ducking
        self.running = dino_running
        self.jumping = dino_jumping
        self.dead = dino_dead
        
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False 
        
        self.step_index = 0
        self.jump_velocity = self.jump_vel_const
        self.image = self.running[0]
        self.dino_collider = self.image.get_rect()
        self.dino_collider.x = self.x_pos
        self.dino_collider.y = self.y_pos
        
    def update(self, user_input):

        
        #resetting step index
        if self.step_index >= 10:
            self.step_index = 0
        
        #changing movement booleans according to the keybinds

        if (user_input[pygame.K_SPACE] or user_input[pygame.K_UP]) and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
            self.dino_duck = False
        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_jump = False
            self.dino_run = False
            self.dino_duck = True
                
        elif not(self.dino_duck or self.dino_jump):
            self.dino_jump = False
            self.dino_run = True
            self.dino_duck = False
            
        #interconnecting the movement booleans to the methods
        if self.dino_duck:
            self.duck()
        if self.dino_jump:
            self.jump()
        if self.dino_run:
            self.run()
    
    #duck function
    def duck(self):
        self.image = self.ducking[self.step_index // 5]
        self.dino_collider = self.image.get_rect()
        self.dino_collider.x = self.x_pos
        self.dino_collider.y = self.y_duck_pos
        self.step_index +=1
    
    #run function
    def run(self):
        self.image = self.running[self.step_index // 5]
        self.dino_collider = self.image.get_rect()
        self.dino_collider.x = self.x_pos
        self.dino_collider.y = self.y_pos
        self.step_index +=1
        
    #jump function
    def jump(self):
        self.image = self.jumping[0]
        if self.dino_jump:
            self.dino_collider.y -= self.jump_velocity * 4
            self.jump_velocity -= 0.8
        if self.jump_velocity <= - self.jump_vel_const:
            self.dino_jump = False
            self.jump_velocity = self.jump_vel_const
            
    def die(self):
        self.image = self.dead
        pygame.time.delay(500)
    
    #drawing the dino on the screen at its defined position
    def draw(self, screen):
        screen.blit(self.image, (self.dino_collider.x, self.dino_collider.y))
        

class Cloud:
    def __init__(self, x_domain, y_domain, vel_delta):
        self.x = screen_width + 250
        self.y_domain = y_domain
        self.x_domain = x_domain
        self.vel_delta = vel_delta
        self.y = random.randint(y_domain[0], y_domain[1])
        self.image = bg_cloud
        self.width  = self.image.get_width()
        
    def update(self):
        self.x -= (game_time_speed+(self.vel_delta * game_time_speed/100))
        if self.x < -self.width:
            self.x = screen_width + random.randint(self.x_domain[0], self.x_domain[1])
            self.y = random.randint(self.y_domain[0], self.y_domain[1])
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
              
        
class Background:
    def __init__(self, x_pos_bg_const, y_pos_bg_const):
        self.x_pos_bg = x_pos_bg_const
        self.y_pos_bg = y_pos_bg_const
        self.image = fg_track
        self.width = fg_track.get_width()
    
    def draw(self, screen):
        screen.blit(self.image, (self.x_pos_bg, self.y_pos_bg))
        screen.blit(self.image, (self.x_pos_bg + self.width, self.y_pos_bg))
        if self.x_pos_bg <= -self.width:
            screen.blit(self.image, (self.x_pos_bg + self.width, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= game_time_speed

class Obstacles:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_width
        
    def update(self):
        self.rect.x -= game_time_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
        
    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)
        

class SmallCactus(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325
        
class LargeCactus(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300
        
class Bird(Obstacles):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
    
    def draw(self, screen):
        if self.type == 10:
            self.type = 0
        screen.blit(self.image[self.type // 5], self.rect)
        self.type += 1
    

class UI:
    def __init__(self):
        pass
        
    def score(self):
        global points, game_time_speed, score_font
        points+=1
        if points%25 == 0:
            game_time_speed += 0.5
        
        text = score_font.render(str(int(points/4)), True, (75, 75, 75))
        text_rect = text.get_rect()
        text_rect.center = (1000, 40)
        screen.blit(text, text_rect)
        
#game function
def game():
    #defining the while loop variable to true; defining the clock for game and player object    
    global game_time_speed, points, obstacles
    obstacles = []
    is_running = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    ui = UI()
    cloud_1 = Cloud([50, 250],[50, 60], -35)
    cloud_2 = Cloud([150, 300],[100, 200], -25)
    background = Background(0, 380)
    game_time_speed = 15;
    points = 0;
    death_count = 0;
    global score_font
    score_font = pygame.font.Font(os.path.join('assets\\Fonts', 'Arcade_Font.ttf'), 20)
    
    
    #game while loop
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        
        screen.fill((255, 255, 255))
        user_input = pygame.key.get_pressed()

        player.draw(screen)
        player.update(user_input)
        
        cloud_1.draw(screen)
        cloud_1.update()
        cloud_2.draw(screen)
        cloud_2.update()
        
        background.draw(screen)
        
        ui.score()
        
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(s_cactus))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(l_cactus))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(bird))
        
        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            if player.dino_collider.colliderect(obstacle.rect):
                screen.blit(dino_dead, (0, 380))
                pygame.time.delay(1000)
                death_count+=1
                menu(death_count)
                     
        clock.tick(30)
        pygame.display.update()
        
#calling the game function
def menu(death_count):
    global points
    run = True
    while run:
        screen.fill((255, 255, 255))
        font = pygame.font.Font(os.path.join('assets\\Fonts', 'Arcade_Font.ttf'), 30)
        
        if death_count == 0:
            text = font.render("Press any Key to Start", True, (50, 50, 50))
        elif death_count >0:
            text = font.render("Press any Key to Play Again", True, (50, 50, 50))
            score = font.render("Score: " + str(int(points/4)), True, (100, 100, 100))
            
            score_rect = score.get_rect()
            score_rect.center = (screen_width//2, screen_height//2 + 50)
            screen.blit(score, score_rect)
            
        text_rect = text.get_rect()
        text_rect.center = (screen_width//2, screen_height//2)
        screen.blit(text, text_rect)
        screen.blit(dino_running[0], (screen_width//2 - 20, screen_height//2 - 140))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                game()
                
                
                
menu(death_count=0)
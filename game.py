import random
import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60


#game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

#define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 30


#def fonts
font = pygame.font.SysFont('Times New Roman', 26)

#define colours
red = (255, 0, 0)
green = (0, 255, 0)

#load images
#background image TEST

background_img = pygame.image.load('img/Background/background.png').convert_alpha()
#panel image
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()

#function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
    screen.blit(background_img, (0, 0))

#function for drawing panel TEST
def draw_panel():
    #draw oaber rectangle
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    #show knight stats text
    draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
    for count, i in enumerate(bandit_list):
        #show knight stats
        draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 10) + count * 60)

#fighter class
class Fighter():
    def __init__(self, x, y, name, max_hp, strenght, potions):
       self.name = name
       self.max_hp = max_hp 
       self.hp = max_hp
       self.strenght = strenght
       self.start_potions = potions
       self.alive = True
       self.animation_list = []
       self.frame_index = 0
       self.action = 0#0:idle, 1:attack, 2:dead
       self.update_time = pygame.time.get_ticks()
       #load idle images
       temp_list = []
       for i in range(8):
           img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
           img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
           temp_list.append(img) 
       self.animation_list.append(temp_list)
       #load attack images
       temp_list = []
       for i in range(8):
           img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
           img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
           temp_list.append(img) 
       self.animation_list.append(temp_list)
       self.image = self.animation_list[self.action][self.frame_index]
       self.rect = self.image.get_rect()
       self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        #handle animation
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index +=1
        #if the animation has run out reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.idle()

    def idle(self):
        #set variable to attack animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks() 

    def attack(self, target):
        #deal dmg to enemy
        rand = random.randint(-5, 5)
        damage = self.strenght + rand
        target.hp -= damage 
        #set variables to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()        

    def draw(self):
        screen.blit(self.image, self.rect)

class HealtBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        #update with new health
        self.hp = hp
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


knight = Fighter(200, 260, 'Knight', 30, 10, 3)
bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)
bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_healt_bar = HealtBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
bandit1_healt_bar = HealtBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_healt_bar = HealtBar(550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp)



run = True
while run:

    clock.tick(fps)

    #draw background
    draw_bg()

    #draw panel
    draw_panel()
    knight_healt_bar.draw(knight.hp)
    bandit1_healt_bar.draw(bandit1.hp)
    bandit2_healt_bar.draw(bandit2.hp)

    #draw fighters
    knight.update()
    knight.draw()
    for bandit in bandit_list:
        bandit.update()
        bandit.draw()

    #player action
    if knight.alive == True:
        if current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                #look for player action
                #attack
                knight.attack(bandit1)
                current_fighter += 1
                action_cooldown



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
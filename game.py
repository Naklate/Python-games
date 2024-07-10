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

#load images
#background image TEST

background_img = pygame.image.load('img/Background/background.png').convert_alpha()
#panel image
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()

#function for drawing background
def draw_bg():
    screen.blit(background_img, (0, 0))

#function for drawing panel TEST
def draw_panel():
    screen.blit(panel_img, (0, screen_height - bottom_panel))

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
       self.update_time = pygame.time.get_ticks()
       for i in range(8):
           img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
           img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
           self.animation_list.append(img)
       self.image = self.animation_list[self.frame_index]
       self.rect = self.image.get_rect()
       self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        #handle animation
        #update image
        self.image = self.animation_list[self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index +=1
        #if the animation has run out reset back to the start
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
            
             

    def draw(self):
        screen.blit(self.image, self.rect)

knight = Fighter(200, 260, 'Knight', 300, 10, 3)
bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)
bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)




run = True
while run:

    clock.tick(fps)

    #draw background
    draw_bg()

    #draw panel
    draw_panel()

    #draw fighters
    knight.update()
    knight.draw()
    for bandit in bandit_list:
        bandit.update()
        bandit.draw()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
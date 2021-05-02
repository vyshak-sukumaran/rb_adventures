import pygame
import random
import sys
import pygame.font

pygame.init()
pygame.mixer.init()

#Load sounds
jmp = pygame.mixer.Sound("music/jump.wav")
hit = pygame.mixer.Sound("music/collide.wav")
score = pygame.mixer.Sound("music/highscore.wav")
click = pygame.mixer.Sound("music/button.wav")

pygame.mixer.music.load("music/gmusic.wav")



clock = pygame.time.Clock()
start_timer = pygame.time.get_ticks()

black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
green = [0, 255, 0]
fps = 50
width, height = 1280, 720
ball_x = 640
ball_y = 360
ball_radius = 50
floor_x = 0
floor_y = (height - 100)
top_x = 0
top_y = 0
w = 50
h = 50


all_sprites = pygame.sprite.Group()
redball_group = pygame.sprite.Group()
obstacle = pygame.sprite.Group()
obstacleii = pygame.sprite.Group()


screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Red Ball Adventures")


#events
def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()
            if event.key == pygame.K_r :
                redball.game_active = True
                pygame.mouse.set_visible(False)

            if event.key == pygame.K_SPACE and redball.game_active == True:
                redball.jmp()
                pygame.mixer.Sound.play(jmp)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(screen,mouse_x,mouse_y)



def check_play_button(screen,mouse_x,mouse_y):
    button_clicked=button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not redball.game_active:
        pygame.mixer.Sound.play(click)
        pygame.mouse.set_visible(False)
        redball.game_active = True


        sb.draw()
        sb.prep_high_score()
        block.score = 0
        obstacle.empty()
        obstacleii.empty()
        multi_blocks()
        other_blocks()





def startscreen_text():
    font = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 100)
    text = font.render("RedBall Adventures", True, red)
    text_rect = text.get_rect()
    screen_rect = screen.get_rect()
    text_rect.centerx = screen_rect.centerx
    text_rect.y = 100
    screen.blit(text, text_rect)
    

#red ball
class RedBall(pygame.sprite.Sprite):

    def __init__(self,screen,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.x = x
        self.y = y
        self.image =pygame.Surface((ball_radius,ball_radius))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.jump_height = 0
        self.gravity = 0.5
        pygame.draw.ellipse(self.image, red, self.rect)
        self.rect.centerx = self.screen_rect.centerx
        self.game_active = False
        
        


    def update(self):
        
        self.jump_height += self.gravity
        self.rect.centery += self.jump_height
        self.check_edges()

    def jmp(self):
        self.jump_height = 0
        self.jump_height = -10

    def check_edges(self):
        
        if self.rect.centery >= floor.floor_rect.top - 25:
            self.rect.centery = floor.floor_rect.top - 25

        if self.rect.centery <= top.top_rect.bottom + 25:
            self.rect.centery = top.top_rect.bottom + 25




#floor
class Floor:
    def __init__(self,screen,x,y):
        self.screen = screen
        self.floor_x = x
        self.floor_y = y
        self.floor_rect = pygame.Rect((0,0,width,100))
        self.screen_rect = screen.get_rect()
        self.floor_rect.bottom = self.screen_rect.bottom
    
        
    def draw(self):
        pygame.draw.rect(screen, red, self.floor_rect ) #(x,y,width of rect,height of rect)
        

class Top:
    def __init__(self,screen,x,y):
        self.screen = screen
        self.top_x = x
        self.top_y = y
        self.top_rect = pygame.Rect((0,0,width,100))
        self.screen_rect = screen.get_rect()
        self.top_rect.top = self.screen_rect.top

    def draw(self):
        pygame.draw.rect(screen, red, self.top_rect)


class Block(pygame.sprite.Sprite):
    def __init__(self,screen,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.Surface((w,h))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width, width + 200)
        self.rect.y = random.randrange(100, height - 150)
        self.block_speedx = random.randrange(2,8)
        self.block_move = False
        self.score = 0



    def update(self):

        self.rect.x -= self.block_speedx
        block_overlap = pygame.sprite.spritecollide(self, obstacle, False)
        block_overlap.remove(self)
        if self.rect.right < self.screen_rect.left :
            self.rect.x = random.randrange(width, width + 100)
            self.rect.y = random.randrange(100, height - 150)
            self.block_speedx = random.randrange(2,8)

       
class Blockii(pygame.sprite.Sprite):
    def __init__(self,screen,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.Surface((1500,400))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width, width + 100)
        self.rect.centery = self.screen_rect.centery
        self.block_speedx = 3
        self.block_move = False



    def update(self):
        self.rect.x -= self.block_speedx


class Blockiii(pygame.sprite.Sprite):
    def __init__(self,screen,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.Surface((1500,150))
        self.rect = self.image.get_rect()
        self.rect.x = blockii.rect.right +150
        self.rect.bottom = self.screen_rect.bottom
        self.block_speedx = 3
        self.block_move = False



    def update(self):
        
        self.rect.x -= self.block_speedx

class Blockiv(pygame.sprite.Sprite):
    def __init__(self,screen,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.Surface((1500,150))
        self.rect = self.image.get_rect()
        self.rect.x = blockii.rect.right +150
        self.rect.top = self.screen_rect.top
        self.block_speedx = 3
        self.block_move = False



    def update(self):
        
        self.rect.x -= self.block_speedx

class Blockv(pygame.sprite.Sprite):
    def __init__(self,screen,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.Surface((1500,250))
        self.rect = self.image.get_rect()
        self.rect.x = blockiii.rect.right
        self.rect.bottom = self.screen_rect.bottom
        self.block_speedx = 3
        self.block_move = False



    def update(self):
        
        self.rect.x -= self.block_speedx

class Blockvi(pygame.sprite.Sprite):
    def __init__(self,screen,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.Surface((1500,250))
        self.rect = self.image.get_rect()
        self.rect.x = blockiii.rect.right
        self.rect.top = self.screen_rect.top
        self.block_speedx = 3
        self.block_move = False



    def update(self):
        
        self.rect.x -= self.block_speedx

class Blockvii(pygame.sprite.Sprite):
    def __init__(self,screen,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.Surface((1500,150))
        self.rect = self.image.get_rect()
        self.rect.x = blockvi.rect.right
        self.rect.top = self.screen_rect.top
        self.block_speedx = 3
        self.block_move = False



    def update(self):
        
        self.rect.x -= self.block_speedx  

class Blockviii(pygame.sprite.Sprite):
    def __init__(self,screen,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.Surface((1500,150))
        self.rect = self.image.get_rect()
        self.rect.x = blockvi.rect.right
        self.rect.bottom = self.screen_rect.bottom
        self.block_speedx = 3
        self.block_move = False



    def update(self):
        
        self.rect.x -= self.block_speedx   

class Blockix(pygame.sprite.Sprite):
    def __init__(self,screen,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.Surface((100,400))
        self.rect = self.image.get_rect()
        self.rect.x = blockviii.rect.right + 100
        self.rect.bottom = self.screen_rect.bottom
        self.block_speedx = 3
        self.block_move = False



    def update(self):
        
        self.rect.x -= self.block_speedx 

class Blockx(pygame.sprite.Sprite):
    def __init__(self,screen,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.Surface((100,400))
        self.rect = self.image.get_rect()
        self.rect.x = blockix.rect.right + 200
        self.rect.top = self.screen_rect.top
        self.block_speedx = 3
        self.block_move = False



    def update(self):
        
        self.rect.x -= self.block_speedx 


class Blockxi(pygame.sprite.Sprite):
    def __init__(self,screen,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.Surface((100,400))
        self.rect = self.image.get_rect()
        self.rect.x = blockx.rect.right + 200
        self.rect.bottom = self.screen_rect.bottom
        self.block_speedx = 3
        self.block_move = False



    def update(self):
        
        self.rect.x -= self.block_speedx 
   
class Blockxii(pygame.sprite.Sprite):
    def __init__(self,screen,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.Surface((100,400))
        self.rect = self.image.get_rect()
        self.rect.x = blockxi.rect.right + 200
        self.rect.top = self.screen_rect.top
        self.block_speedx = 3
        self.block_move = False


    def update(self):
        
        self.rect.x -= self.block_speedx

class Blockxiii(pygame.sprite.Sprite):
    def __init__(self,screen,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.Surface((100,400))
        self.rect = self.image.get_rect()
        self.rect.x = blockxii.rect.right + 200
        self.rect.bottom = self.screen_rect.bottom
        self.block_speedx = 3
        self.block_move = False


    def update(self):
        
        self.rect.x -= self.block_speedx


class Button():
    def __init__(self,screen,msg):
        self.screen=screen
        self.screen_rect=screen.get_rect()
        self.width,self.height=200,50
        self.button_color = red
        self.text_color = white
        self.font=pygame.font.Font("fonts/ARCADECLASSIC.TTF",48)
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=self.screen_rect.center
        self.prep_msg(msg)

    def prep_msg(self,msg):
        self.msg_image=self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect=self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

class Scoreboard:
    def __init__(self,screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.high_score = 0

    def draw(self):
        self.font = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 40)
        self.text = self.font.render("Score  "+str(block.score), 1, white)
        screen.blit(self.text, (1050,40))

    def prep_high_score(self):
        self.high_score_image = self.font.render("High Score  "+str(self.high_score), True, white)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.x = 40
        self.high_score_rect.y = 40
        self.screen.blit(self.high_score_image, self.high_score_rect)

    
button = Button(screen,"play")       
sb = Scoreboard(screen)

block = Block(screen, w, h)
blockii = Blockii(screen,w,h)
blockiii = Blockiii(screen,w,h)   
blockiv = Blockiv(screen,w,h)
blockv = Blockv(screen,w,h) 
blockvi = Blockvi(screen,w,h)
blockvii = Blockvii(screen,w,h) 
blockviii = Blockviii(screen,w,h) 
blockix = Blockix(screen,w,h)
blockx = Blockx(screen,w,h)
blockxi = Blockxi(screen,w,h)
blockxii = Blockxii(screen,w,h)
blockxiii = Blockxiii(screen,w,h)


#All sprite works done here
redball = RedBall(screen, ball_x, ball_y)


redball_group.add(redball)

def single_block():
    block = Block(screen, w, h)
    obstacle.add(block)

def multi_blocks():
    block = Block(screen, w, h)
    max_block = 10
    for i in range(max_block):
        single_block()


def other_blocks():
    if len(obstacle) == 0:
        obstacleii.add(blockii)
        obstacleii.add(blockiii)
        obstacleii.add(blockiv)
        obstacleii.add(blockv)
        obstacleii.add(blockvi)
        obstacleii.add(blockvii)
        obstacleii.add(blockviii)
        obstacleii.add(blockix)
        obstacleii.add(blockx)
        obstacleii.add(blockxi)
        obstacleii.add(blockxii)
        obstacleii.add(blockxiii)

#obstacle stuff
def obstacle_maintanance():
    for block in obstacle.copy():
        if block.rect.right <=0:
            obstacle.remove(block)
            
        other_blocks()

    check_collision()
    

#check collision / All collision stuff are done here
def check_collision():
    collision = pygame.sprite.groupcollide(redball_group, obstacle, False, True)
    collisionii = pygame.sprite.groupcollide(redball_group, obstacleii, False, True)
    if collision or collisionii  :
        
        check_high_score(block, sb)
        pygame.mixer.Sound.play(hit)

        obstacle.empty()
        obstacleii.empty()
        multi_blocks()
        other_blocks()
        redball.game_active = False
        pygame.mouse.set_visible(True)


#Show text        
def level_one():
    font = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 40)
    text = font.render("Level completed" , True, green)
    text_rect = text.get_rect()
    screen_rect = screen.get_rect()
    text_rect.center = screen_rect.center
    screen.blit(text,text_rect)


#timer stuff    
def timer():
    seconds = (pygame.time.get_ticks() - start_timer)/1000
    if seconds%2 != 0:
        block.score += 1

def start_screen():
    screen.fill(white)
    button.prep_msg("play")
    button.draw_button()
    startscreen_text()

def check_high_score(block,sb):
    if block.score>sb.high_score:
        sb.high_score=block.score
        sb.prep_high_score()


floor = Floor(screen, floor_x, floor_y)
top = Top(screen, top_x, top_y)


run = True
while run:
    events() 
    if not redball.game_active:
        pygame.mixer.music.play(-1)
        start_screen()
       
        all_sprites.empty()
        

    if redball.game_active:
        screen.fill(white)
        timer()

        obstacle_maintanance()

        #update
        redball.update()
        all_sprites.update()
        obstacle.update()
        obstacleii.update()
        

        #draw
        floor.draw()
        top.draw()
        redball_group.draw(screen)
        all_sprites.draw(screen)
        obstacle.draw(screen)
        obstacleii.draw(screen)
        sb.draw()
        sb.prep_high_score()
        
        
    clock.tick(fps)
    pygame.display.flip()
#pygame.mixer.quit()
import pygame, time
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

WIDTH, HEIGHT = 4096 / 2, 2304 / 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))

colors = {'white': (255, 255, 255), 'black': (0, 0, 0), 'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255)}

class Ball(pygame.sprite.Sprite):
    def __init__(self, img, sizex, sizey):
        super(Ball, self).__init__()
        self.surf = img
        self.surf.set_colorkey((colors['white']), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (100, 100))
        self.size = (sizex, sizey)
        self.yspeed = 0
        self.xspeed = 0
        self.offset = (0, 0)
        self.rect = self.surf.get_rect()
        self.thrown = False
    
    def follow(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect = pygame.Rect((mouse_pos[0] - self.offset[0], mouse_pos[1] - self.offset[1]), self.size)
    
    def top_check(self):
        if self.rect[1] < 0:
            return True
    
    def bottom_check(self):
        if self.rect[1] > HEIGHT - self.size[1]:
            return True
    
    def horizontal_check(self):
        if self.rect[0] > WIDTH - self.size[0] or self.rect[0] < 0:
            return True

    def fall(self, fall_ticks, grabbed):

        if grabbed:
            if self.speed <= 0:
                self.thrown = True
        
        if self.thrown and self.speed > 0:
            fall_ticks = 0

        if self.bottom_check():
            self.yspeed = 0
            if self.xspeed > 0:
              self.xspeed -= 0.5
            elif self.xspeed < 0:
               self.xspeed += 0.5
            self.rect = pygame.Rect((self.rect[0], HEIGHT + 1 - self.size[1]), self.size)
        else:
           self.yspeed += (9.8 * (fall_ticks/ 50)) ** 2
        self.rect.move_ip(self.xspeed, self.yspeed)
        if self.horizontal_check():
            self.xspeed = 0
        
        if self.top_check():
            self.yspeed = 0
        #print(self.xspeed, self.yspeed)

    def set_offset(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.offset = (mouse_x - self.rect[0], mouse_y - self.rect[1])


ball_img = pygame.image.load('bouncy_ball.jpeg')
ball = Ball(ball_img, 100, 100)
print('before loop')

clock = pygame.time.Clock()
running = True
mouse_up = True
grabbed = False
fall_ticks = 0

while running:
    events = pygame.event.get()
    release_coords = pygame.mouse.get_rel()

    for event in events:
        if event.type == QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and ball.rect.collidepoint(pygame.mouse.get_pos()):
            grabbed = True
            ball.set_offset()
        
        if grabbed and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            grabbed = False
            ball.xspeed = release_coords[0] / 4
            ball.yspeed = release_coords[1] / 4

    if ball.bottom_check() or grabbed:
        fall_ticks = 0
    else:
        fall_ticks += 1

    if grabbed:
        ball.follow()
    else:
        ball.fall(fall_ticks, grabbed)

    screen.fill(colors['white'])
    screen.blit(ball.surf, ball.rect)
    pygame.display.flip()
    clock.tick(50)
    event_types = {event.type for event in events}
import pygame
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

WIDTH, HEIGHT = 1000, 1000

screen = pygame.display.set_mode((WIDTH, HEIGHT))

colors = {'white': (255, 255, 255), 'black': (0, 0, 0), 'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255)}

class Ball(pygame.sprite.Sprite):
    def __init__(self, img, sizex, sizey):
        super(Ball, self).__init__()
        self.surf = img
        self.surf.set_colorkey((colors['white']), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (100, 100))
        self.size = (sizex, sizey)
        self.speed = 0
        self.offset = (0, 0)
        self.rect = self.surf.get_rect()
    
    def follow(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect = pygame.Rect((mouse_pos[0] - self.offset[0], mouse_pos[1] - self.offset[1]), self.size)
    
    def fall(self):
        if self.rect[1] > HEIGHT - self.size[1]:
            self.speed = 0
            self.rect = pygame.Rect((self.rect[0], HEIGHT + 1 - self.size[1]), self.size)
        else:
           self.speed += 1
        self.rect.move_ip(0, self.speed)
        print(self.speed)
    
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

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and ball.rect.collidepoint(pygame.mouse.get_pos()):
            grabbed = True
            ball.set_offset()
        
        if grabbed and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            grabbed = False

    if grabbed:
        ball.follow()
        ball.speed = 0
    else:
        ball.fall()

    screen.fill(colors['white'])
    screen.blit(ball.surf, ball.rect)
    pygame.display.flip()
    clock.tick(50)
    event_types = {event.type for event in events}
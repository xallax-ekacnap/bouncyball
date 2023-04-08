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

WIDTH, HEIGHT = 1500, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

gravity = 9.8

font = pygame.font.Font('freesansbold.ttf', 32)

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
    
    def follow(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect = pygame.Rect((mouse_pos[0] - self.offset[0], mouse_pos[1] - self.offset[1]), self.size)
    
    def top_check(self):
        if self.rect[1] < 0:
            return True
    
    def bottom_check(self):
        if self.rect[1] > HEIGHT - self.size[1]:
            return True
    
    def side_check(self):
        if self.rect[0] > WIDTH - self.size[0] or self.rect[0] < 0:
            return True

    def fall(self, fall_ticks):
        try:
            increment = (9.8 / gravity) / 4 * -1
        except ZeroDivisionError:
            increment = 0
        if self.bottom_check():
            self.yspeed *= increment * -1 if increment > 0.25 else -0.25
            fall_ticks = 0
            if self.xspeed > 0:
              self.xspeed -= 1
            elif self.xspeed < 0:
               self.xspeed += 1
            self.rect = pygame.Rect((self.rect[0], HEIGHT + 1 - self.size[1]), self.size)
        else:
           self.yspeed += (gravity * (fall_ticks/ 50)) ** 2
        self.rect.move_ip(self.xspeed, self.yspeed)
        
        if self.top_check():
            fall_ticks = 0
            self.yspeed *= -0.25
            
        
        if self.side_check():
            self.xspeed *= -1
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
        
        pressed_keys = pygame.key.get_pressed()

        if event.type == KEYDOWN:
            if pressed_keys[K_UP]:
                gravity += 0.5
            if pressed_keys[K_DOWN]:
                gravity -= 0.5
            if gravity <= 0:
                gravity = 0

    text = font.render(f'Gravity: {round(gravity, 2)} m/s^2', True, (0, 0, 0))
    textrect = text.get_rect()

    if ball.bottom_check() or grabbed:
        fall_ticks = 0
    else:
        fall_ticks += 1

    if grabbed:
        ball.follow()
    else:
        ball.fall(fall_ticks)

    screen.fill(colors['white'])
    screen.blit(ball.surf, ball.rect)
    screen.blit(text, textrect)
    pygame.display.flip()
    clock.tick(50)
    event_types = {event.type for event in events}
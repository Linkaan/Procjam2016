import os
import sys
import pygame
from GameConfig import *
from graphics.textures import *
from level.level import Level
from level.pathfinding.findpath import find_path
from graphics.sprite.basicsprite import BasicSprite
from graphics.sprite.animatedsprite import AnimatedSprite
from entity.mob.unit.squad import Squad

class Game(object):

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 30.0
        self.keys = pygame.key.get_pressed()
        self.camera_x = 0
        self.camera_y = 0

    def load(self):
        # load game here
        load_textures()
        self.level = Level(self, WIDTH, HEIGHT)
        #path = find_path(self.level, (3, 3), (12, 12))
        #print(len(path))
        #self.testsprite1 = AnimatedSprite(self.level.sprite_group, "../res/soldier_spritesheet.png", 0, 0, 10)
        #self.testsprite2 = AnimatedSprite(self.level.sprite_group, "../res/enemy_spritesheet.png", 32, 0, 5)
        #self.testsprite3 = BasicSprite(self.level.sprite_group, "../res/bazooka.png", 64, 0)
        #self.testunit1 = Unit(self.level, 96, 64)
        #self.testunit2 = Unit(self.level, 96, 32*4)
        #self.squad1 = Squad(self.level, 64*2, 64*2, 3)
        self.level.add_entity(Squad(self.level, 64*2, 64*2, 3))
        self.running = True

    def event_loop(self):
        self.mouse_up = False
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_up = True

    def show_fps(self):
        caption = "{} - FPS: {:.2f}".format(CAPTION, self.clock.get_fps())
        pygame.display.set_caption(caption)

    def tick(self):
        # update game here
        if self.keys[pygame.K_RIGHT]:
            self.camera_x += SCROLL_SPEED
        if self.keys[pygame.K_LEFT]:
            self.camera_x -= SCROLL_SPEED
        if self.keys[pygame.K_UP]:
            self.camera_y -= SCROLL_SPEED
        if self.keys[pygame.K_DOWN]:
            self.camera_y += SCROLL_SPEED

        if self.camera_x < 0:
            self.camera_x = 0
        if self.camera_x > ((self.level.width << 5) - SCREEN_SIZE[0]):
            self.camera_x = ((self.level.width << 5) - SCREEN_SIZE[0])
        if self.camera_y < 0:
            self.camera_y = 0
        if self.camera_y > ((self.level.height << 5) - SCREEN_SIZE[1]):
            self.camera_y = ((self.level.height << 5) - SCREEN_SIZE[1])

        self.level.tick()
        #self.testsprite1.tick()
        #self.testsprite2.tick()
        #self.testunit1.tick()
        #self.testunit2.tick()
        #self.squad1.tick()

    def render(self):
        # render game here
        self.screen.fill(self.BLACK)
        x_offset = self.camera_x
        y_offset = self.camera_y
        self.level.render(self.screen, x_offset, y_offset)
        #self.testsprite2.render(x_offset, y_offset)
        #self.testsprite3.render(x_offset, y_offset)
        #self.testsprite1.render(x_offset, y_offset)
        #self.testunit1.render(x_offset, y_offset)
        #self.testunit2.render(x_offset, y_offset)
        pygame.display.flip()

    def game_loop(self):
        while self.running:
            self.event_loop()
            self.tick()
            self.render()
            self.clock.tick(self.fps)
            self.show_fps()

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.display.set_caption(CAPTION)
    pygame.display.set_mode(SCREEN_SIZE, True)
    game = Game()
    game.load()
    game.game_loop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

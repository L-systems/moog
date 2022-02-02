import sys
from typing import Tuple
import pygame, os
from pygame.locals import *
import constants as c

padding: int = 10
my_surface: pygame.Surface = pygame.Surface((c.W_WIDTH - (padding * c.SCALE), 150))
my_surface.fill('red')

def init() -> Tuple[pygame.Surface, pygame.Surface, pygame.time.Clock]:
  x: int = 100 # window pos
  y: int = 300
  os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
  pygame.mixer.pre_init(44100, -16, 2, 512)
  pygame.init()
  pygame.display.set_caption('MIDI emulator')
  renderer = pygame.display.set_mode((c.WIDTH, c.HEIGHT), 0, 32)
  window = pygame.Surface((c.W_WIDTH, c.W_HEIGHT))
  clock = pygame.time.Clock()
  return (renderer, window, clock)

def game_loop(condition: bool, renderer: pygame.Surface, window: pygame.Surface, clock: pygame.time.Clock, fn) -> None:
  while condition:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN: 
        if event.key == K_ESCAPE: 
          pygame.quit()
          sys.exit()

    window.fill((18, 18, 48))
    fn()
    renderer.blit(pygame.transform.scale(window, (c.WIDTH, c.HEIGHT)), (0, 0))
    pygame.display.update()

def render_all() -> None: 
  window.blit(my_surface, (padding, c.W_HEIGHT / 2 - 75))

if __name__ == '__main__':
  is_running: bool = True
  renderer, window, clock = init()
  game_loop(is_running, renderer, window, clock, render_all)
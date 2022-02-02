import sys
from typing import Tuple
import pygame, os
from pygame.locals import *
import constants as c


def init() -> Tuple[pygame.Surface, pygame.Surface, pygame.time.Clock]: 
  x: int = 100 # window pos
  y: int = 300 
  os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
  pygame.init()
  pygame.display.set_caption('MIDI emulator')
  screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT), 0, 32)
  display = pygame.Surface((400, 225))
  clock = pygame.time.Clock()
  return (screen, display, clock)

def game_loop(condition: bool, screen: pygame.Surface, display: pygame.Surface, clock) -> None: 
  while condition: 
    for event in pygame.event.get():
      if event.type == QUIT: 
        pygame.quit()
        sys.exit()
    
    screen.fill((0, 0, 0))
    screen.blit(pygame.transform.scale(display, (c.WIDTH, c.HEIGHT)), (0, 0))
    pygame.display.update()
    clock.tick(60)
  
if __name__ == '__main__': 
  screen, display, clock = init()
  game_loop(True, screen, display, clock)
import sys
from typing import Tuple
import pygame, os
from pygame.locals import *
import constants as c

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

def load_sfx(name: str) -> pygame.mixer.Sound:
  return pygame.mixer.Sound(f'assets/sfx/{name}.ogg')

def handle_keypress(event) -> None: 
  if event.key == K_a:
    c3.play()
  elif event.key == K_s:
    d3.play()
  elif event.key == K_d:
    e3.play()
  elif event.key == K_f:
    f3.play()
  elif event.key == K_g:
    g3.play()
  elif event.key == K_h:
    a3.play()
  elif event.key == K_j:
    b3.play()
  elif event.key == K_k:
    c4.play()
  elif event.key == K_l:
    d4.play()
  elif event.key == K_SEMICOLON:
    e4.play()
  elif event.key == K_QUOTE:
    f4.play()
  elif event.key == K_RETURN:
    g4.play()

def game_loop(condition: bool, renderer: pygame.Surface, window: pygame.Surface, clock: pygame.time.Clock) -> None:
  last_updated_tick: int = pygame.time.get_ticks()
  midi_frame_idx: int = 0

  for x in range(c.MIDI_FRAMES_STEPS):
    image = pygame.image.load(f'./assets/midi/frame_{x + 1}.jpg').convert()
    image_frame = pygame.transform.scale(image, (round(image.get_width() / c.SCALE), round(image.get_height() / c.SCALE)))
    c.MIDI_FRAMES.append(image_frame)

  padding: int = 10
  my_surface_width: int  = c.W_WIDTH - (padding * c.SCALE)
  my_surface_height: int = 150
  my_surface: pygame.Surface = pygame.Surface((my_surface_width, my_surface_height))
  my_surface.fill((240, 230, 80))

  while condition:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == KEYDOWN: 
        if event.key == K_ESCAPE: 
          pygame.quit()
          sys.exit() 
        handle_keypress(event)
      elif event.type == KEYUP:
        pygame.mixer.fadeout(2000)

    window.fill((38, 110, 122))
    # window.blit(my_surface, (padding, c.W_HEIGHT / 2 - 75))
    
    current_midi_frame: pygame.Surface = c.MIDI_FRAMES[midi_frame_idx]
    window.blit(current_midi_frame, (c.W_WIDTH / 2 - current_midi_frame.get_width() / 2, 0))

    current_tick: int = pygame.time.get_ticks()
    if current_tick - last_updated_tick >= c.ANIMATION_COOLDOWN:
      midi_frame_idx = (midi_frame_idx + 1) % c.MIDI_FRAMES_STEPS
      last_updated_tick = current_tick

    renderer.blit(pygame.transform.scale(window, (c.WIDTH, c.HEIGHT)), (0, 0))
    pygame.display.update()
    clock.tick(60)

if __name__ == '__main__':
  is_running: bool = True
  renderer, window, clock = init()
  c3, d3, e3, f3, g3, a3, b3, c4, d4, e4, f4, g4 = list(map(load_sfx, ['c3', 'd3', 'e3', 'f3', 'g3', 'a3', 'b3', 'c4', 'd4', 'e4', 'f4', 'g4']))
  game_loop(is_running, renderer, window, clock)
import sys
from typing import List, Tuple
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

def handle_keypress(event, key_particles: List) -> List: 
  music_map[event.key][0].play()

  key_particles.append([music_map[event.key][1], 3]) # [(x, y): location, initial_radius]
  if key_particles: 
    return key_particles
  else:
    return []

def game_loop(condition: bool, renderer: pygame.Surface, window: pygame.Surface, clock: pygame.time.Clock) -> None:
  last_updated_tick: int = pygame.time.get_ticks()
  midi_frame_idx: int = 0

  padding: int = 10
  my_surface_width: int  = c.W_WIDTH - (padding * c.SCALE)
  my_surface_height: int = 150
  my_surface: pygame.Surface = pygame.Surface((my_surface_width, my_surface_height))
  my_surface.fill((240, 230, 80))

  ring_particles = []

  while condition:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == KEYDOWN: 
        if event.key == K_ESCAPE: 
          pygame.quit()
          sys.exit() 
        if event.key in music_map.keys():
          ring_particles = handle_keypress(event, ring_particles)
      elif event.type == KEYUP:
        pygame.mixer.fadeout(2000)

    window.fill((38, 110, 122))
    # window.blit(my_surface, (padding, c.W_HEIGHT / 2 - 75))
    
    current_midi_frame: pygame.Surface = c.MIDI_FRAMES[midi_frame_idx]

    window.blit(current_midi_frame, (midi_frame_x_pos, 0))

    if ring_particles: 
      for i, ring in sorted(enumerate(ring_particles), reverse=True): # [(x, y): location, initial_radius]
        ring[1] += 10
        if ring[1] > 160: 
          ring_particles.pop(i)
        else: 
          pygame.draw.circle(window, (240, 20, 40), ring[0], ring[1], 1)
          # pygame.draw.circle(window, (240, 20, 40), ring[0], ring[1] * ring[1], 3)

    # Higher pitched notes
    pygame.draw.circle(window, 'white', (midi_frame_x_pos + 48 + 7         , 100), 3)
    pygame.draw.circle(window, 'white', (midi_frame_x_pos + 49 + 7 + 13    , 100), 3)

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
  midi_frame_x_pos: int = c.W_WIDTH / 2 - c.MIDI_FRAMES[0].get_width() / 2
  music_map = { # keycode: [sound_profile, (x, y): particle coordinates]
    K_a: [c3, (midi_frame_x_pos + 49, 100 + 20)], 
    K_s: [d3, (midi_frame_x_pos + 49 + 13, 100 + 20)], 
    K_d: [e3, (midi_frame_x_pos + 49 + 13 * 2, 100 + 20)], 
    K_f: [f3, (midi_frame_x_pos + 49 + 13 * 3, 100 + 20)], 
    K_g: [g3, (midi_frame_x_pos + 49 + 13 * 4, 100 + 20)], 
    K_h: [a3, (midi_frame_x_pos + 49 + 13 * 5, 100 + 20)],
    K_j: [b3, (midi_frame_x_pos + 49 + 13 * 6, 100 + 20)], 
    K_k: [c4, (midi_frame_x_pos + 49 + 13 * 7, 100 + 20)], 
    K_l: [d4, (midi_frame_x_pos + 49 + 13 * 8, 100 + 20)], 
    K_SEMICOLON: [e4, (midi_frame_x_pos + 49 + 13 * 9, 100 + 20)], 
    K_QUOTE: [f4, (midi_frame_x_pos + 49 + 13 * 10, 100 + 20)], 
    K_RETURN: [g4, (midi_frame_x_pos + 49 + 13 * 11, 100 + 20)] 
  }

  game_loop(is_running, renderer, window, clock)
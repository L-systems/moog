import pygame

WIDTH: int = 800
HEIGHT: int = 700
SCALE: int = 2
W_WIDTH: int = WIDTH / SCALE
W_HEIGHT: int = HEIGHT / SCALE

ANIMATION_COOLDOWN = 32 

MIDI_FRAMES = []
MIDI_FRAMES_STEPS = 30
for x in range(MIDI_FRAMES_STEPS):
  image = pygame.image.load(f'./assets/midi/frame_{x + 1}.jpg')
  image_frame = pygame.transform.scale(image, (round(image.get_width() / SCALE), round(image.get_height() / SCALE)))
  MIDI_FRAMES.append(image_frame)
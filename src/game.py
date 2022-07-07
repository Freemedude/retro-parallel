#!/usr/bin/env python

import pygame as pg
import os
import json
from src.player import *
from src.atlas import Atlas

# See if we can load more than standard BMP
if not pg.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

SCREENRECT = pg.Rect(0, 0, 640, 480)

def load_image(file):
    file = os.path.join(os.curdir, "data", "images", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert_alpha()


def main(winstyle=0):
    #  Initialize pygame
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    if pg.mixer and not pg.mixer.get_init():
        print("Warning, no sound")
        pg.mixer = None

    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    pg.display.set_caption("Retro Parallel")

    bgdtile = load_image("test.png")
    # Load texture atlas
    atlas = Atlas("texture-atlas.json", "texture-atlas.png")

    clock = pg.time.Clock()
    background = pg.Surface(SCREENRECT.size, pg.SRCALPHA)

    pg.Surface.fill(background, (255, 0, 0))
    background.blit(bgdtile, (5, 5))
    pg.display.flip()
    icon = pg.transform.scale(bgdtile, (32, 32))
    pg.display.set_icon(icon)
    color = (255, 0, 0)
    running = True


    all = pg.sprite.RenderUpdates()
   
    Player.containers = all
    player = Player(atlas)

    frame_rate = 30
    delta_time = 0
    while running:

        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                    return
        
        screen.blit(background, (0, 0))
        
        red = 255 if color[0] <= 0 else color[0] - 1
        blue = 0 if color[2] >= 255 else color[2] + 1

        player.update(delta_time)
        all.draw(screen)
        color = (red, 0, blue) 
        pg.Surface.fill(background, color)
#        background.blit(bgdtile, (5, 5))
        pg.display.update()
        
        delta_time = clock.tick(frame_rate) / 1000

    pg.time.wait(1000)

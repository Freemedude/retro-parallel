#!/usr/bin/env python

import pygame as pg
import os
import sys
from src.player import *
from src.assets import Atlas, pack_raw_files, live_pack_check_monitored_files, update_monitored_raw_files


# See if we can load more than standard BMP
if not pg.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

SCREENRECT = pg.Rect(0, 0, 640, 480)

atlas : Atlas

def set_icon(atlas):
    icon = atlas.get_image("icon.aseprite")
    pg.display.set_icon(icon.image)


def main(winstyle=0):
    if len(sys.argv) > 1:
        # Pack on startup
        if sys.argv[1] == "pack":
            pack_raw_files()
        
        # Keep packing when changes are detected, this is pretty fkin neat.
        if sys.argv[1] == "live-pack":
            pack_raw_files()
            update_monitored_raw_files()

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

    # Load texture atlas
    global atlas
    atlas = Atlas("texture-atlas.json", "texture-atlas.png")

    clock = pg.time.Clock()
    background = pg.Surface(SCREENRECT.size, pg.SRCALPHA)

    pg.Surface.fill(background, (255, 0, 0))
    pg.display.flip()

    set_icon(atlas)
    atlas.add_listener(set_icon)
    
    color = (255, 0, 0)
    running = True


    all = pg.sprite.RenderUpdates()
   
    Player.containers = all
    player = Player(atlas)

    frame_rate = 30
    delta_time = 0
    while running:
        live_pack_check_monitored_files(atlas)
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

    pg.saved_time.wait(1000)

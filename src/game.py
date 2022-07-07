#!/usr/bin/env python

import pygame as pg
import sys
from src.player import *
from src.assets import Atlas, pack_raw_files, live_pack_check_monitored_files, update_monitored_raw_file_timestamps


SCREENRECT = pg.Rect(0, 0, 1280, 720)

atlas : Atlas

def set_icon(atlas):
    icon = atlas.get_image("icon.aseprite")
    pg.display.set_icon(icon.image)


def main(winstyle=0):
    
    # See if we can load more than standard BMP
    if not pg.image.get_extended():
        raise SystemExit("Sorry, extended image module required")
    

    live_pack = False
    # Check command line arguments
    if len(sys.argv) > 1:

        # Pack on startup
        if sys.argv[1] == "pack":
            pack_raw_files()
        
        # Keep packing when changes are detected, this is pretty fkin neat.
        if sys.argv[1] == "live-pack":
            pack_raw_files()
            update_monitored_raw_file_timestamps()
            live_pack = True


    #  Initialize pygame
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    if pg.mixer and not pg.mixer.get_init():
        print("Warning, no sound")
        pg.mixer = None


    # Set the display mode
    winstyle = pg.RESIZABLE
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    pg.display.set_caption("Retro Parallel")

    # Load texture atlas
    global atlas
    atlas = Atlas("texture_atlas.json", "texture_atlas.png")

    set_icon(atlas)
    atlas.add_listener(set_icon)

    clock = pg.time.Clock()
    background = pg.Surface(SCREENRECT.size, pg.SRCALPHA)

    pg.display.flip()


    
    color = (255, 0, 0)
    running = True


    all = pg.sprite.RenderUpdates()
   
    Player.containers = all
    player = Player(atlas)

    frame_rate = 30
    delta_time = 0
    
    color_fade_direction = 1
    color_fade = 0
    color_speed = 0.01 # Color changes by 0.01 per second
    color_range = 200
    color_min = 20
    
    while running:
        # Handle live packing
        if live_pack: 
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
        
        color_fade += color_fade_direction * color_speed

        # Inver color fade direction if we have gone out of bounds!
        if color_fade < 0 or color_fade > 1:
            color_fade_direction = -color_fade_direction
        red = color_min + color_range * color_fade
        blue = color_min + color_range * (1 - color_fade)

        player.update(delta_time)
        all.draw(screen)
        color = (red, 0, blue) 
        pg.Surface.fill(background, color)
#        background.blit(bgdtile, (5, 5))
        pg.display.update()
        
        delta_time = clock.tick(frame_rate) / 1000

    pg.saved_time.wait(1000)

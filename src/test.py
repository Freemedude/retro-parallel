#!/usr/bin/env python

from turtle import back
import pygame as pg
import os


main_dir = os.curdir

# See if we can load more than standard BMP
if not pg.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

def load_image(file):
   
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, "data", "images", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert_alpha()


SCREENRECT = pg.Rect(0, 0, 640, 480)

def init_elements():
    """
    Initialize the various elements we got. Must be done after initializing the screen.
    """
    pass

def main(winstyle=0):
    init_elements()

    #  Initialize pygame
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    if pg.mixer and not pg.mixer.get_init():
        print("Warning, no sound")
        pg.mixer = None

    fullscreen = False
    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    pg.display.set_caption("Pygame The Thing")

    bgdtile = load_image("test.png")

    clock = pg.time.Clock()
    background = pg.Surface(SCREENRECT.size, pg.SRCALPHA)
    pg.Surface.fill(background, (255, 0, 0))
    background.blit(bgdtile, (5, 5))
    pg.display.flip()

    color = (255, 0, 0)
    running = True
    while running:
        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                return
        
        screen.blit(background, (0, 0))
        
        red = 255 if color[0] <= 0 else color[0] - 1
        blue = 0 if color[2] >= 255 else color[2] + 1

        color = (red, 0, blue) 
        pg.Surface.fill(background, color)
        background.blit(bgdtile, (5, 5))
        pg.display.update()
        
        # cap the framerate at 40fps. Also called 40HZ or 40 times per second.
        clock.tick(60)

    pg.time.wait(1000)


# call the "main" function if running this script
if __name__ == "__main__":
    main()
    pg.quit()
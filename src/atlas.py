#!/usr/bin/env python

import os
import pygame as pg
import json

class Texture():
    rect : pg.Rect
    seconds : int
    image : pg.Surface

    def __init__(self, rect, seconds, image):
        self.rect = rect
        self.seconds = seconds
        self.image = image


class Atlas():

    entries : list[Texture]

    def __init__(self, data_path: str, atlas_path: str):
        self.entries = {}

        # Load the files
        data = open(os.path.join(os.curdir, "data", "animations", "out", data_path))
        
        atlas_full_path = os.path.join(os.curdir, "data", "animations", "out", atlas_path)
        self.image = pg.image.load(atlas_full_path)
        
        # Convert from JSON to python dict.
        content = json.load(data)

        # Fetch each frame
        frames = content['frames']

        # Go over all frames
        for frame in frames:

            this = frames[frame]
            
            # Extract data
            x = this['frame']['x']
            y = this['frame']['y']
            w = this['frame']['w']
            h = this['frame']['h']
            seconds = this['duration'] / 1000.0
            rect = pg.Rect(x, y, w, h)
            image = pg.Surface((w, h), pg.SRCALPHA).convert_alpha()
            
            image.blit(self.image, (0, 0), rect)

            self.entries[frame] = Texture(rect, seconds, image)


    def get_animation(self, name): 
        results = []
        # We need to look through the atlas for everyhing that starts with name
        for key in self.entries.keys():
            if key.startswith(name):
                results.append(self.entries[key])

        # Todo: Sort them
        return results


    def get_image(atlas, name):
        return atlas.entries[name]

   
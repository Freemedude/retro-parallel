#!/usr/bin/env python

import os
import pygame as pg
import json
from pathlib import Path

monitored_raw_files = []

def load_image(file):
    file = os.path.join(os.curdir, "data", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert_alpha()


# Packing requires aseprite on the path!
def pack_raw_files():
    in_dir = os.path.join("data", "raw")
    out_dir = os.path.join("data", "packed")
    os.system(f"aseprite -b {in_dir}{os.sep}*.aseprite --sheet-pack --ignore-empty --split-layers --sheet {out_dir}{os.sep}texture-atlas.png --data {out_dir}{os.sep}texture-atlas.json")


def update_monitored_raw_files():
    global monitored_raw_files
    monitored_raw_files = [(str(file), os.path.getmtime(file)) for file in Path(os.path.join("data", "raw")).rglob("*.aseprite")]


def live_pack_check_monitored_files(atlas):
      global monitored_raw_files
      if any(os.path.getmtime(file) != saved_time for (file, saved_time) in monitored_raw_files):
        print("Some file has changed, updating packed!")
        pack_raw_files()
        update_monitored_raw_files()
        atlas.update_atlas()
        
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
        self.data_path = data_path
        self.atlas_path = atlas_path
        self.initialize_atlas()
        self.listeners = []


    def initialize_atlas(self):
        
        self.entries = {}

        # Load the files
        data = open(os.path.join("data", "packed", self.data_path))
        
        atlas_full_path = os.path.join("data", "packed", self.atlas_path)
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

    def update_atlas(self):
        self.initialize_atlas()

        for listener in self.listeners:
            listener(self)

    def add_listener(self, func):
        self.listeners.append(func)


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

   
#!/usr/bin/env python

"""
This file contains stuff related to asset management

"""

from email.mime import base
import os
import pygame as pg
import json
from pathlib import Path

"""
This is a list of all the files that are monitored for changed when live-pack is on.
"""
monitored_raw_files = []

base_dir = os.path.join("data", "images")

def load_image_alpha(file):
    """
    Loads a file from disk and exports it as a Pygame.Surface
    """
    file = os.path.join(base_dir, file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert_alpha()


def pack_raw_files():
    """
    Uses Aseprite to take all the Aseprite project files and combine them into a texture atlas (see 
    data/packed/texture-atlas). A texture atlas is a collection of many individual images and a 
    data file (in JSON) describing where in the image the invidiual images are located. This is 
    done to make it easier for a computer to work with them. This might not matter at all in 
    Pygame, since they all have to be exported as Surfaces anyway. BUT NOW WE GOT EM.

    This function runs a small commandline command to take all the files ending in ".aseprite" in 
    the data/raw directory and combine them into a texture atlas. Using this function requires 
    Aseprite to be installed and added to the path!
    """

    input_files = os.path.join(base_dir, "raw", "*.aseprite")

    options = "--sheet-pack --ignore-empty --split-layers"

    out_dir = os.path.join(base_dir, "packed")
    out_name = "texture_atlas"
    json_out = os.path.join(out_dir, out_name + ".json")
    png_out = os.path.join(out_dir, out_name + ".png")

    os.system(f"aseprite -b {input_files} {options} --sheet {png_out} --data {json_out}")


def update_monitored_raw_file_timestamps():
    """
    Update the timestamps on all the monitored files
    """
    global monitored_raw_files
    monitored_raw_files = [(str(file), os.path.getmtime(file)) for file in Path(os.path.join(base_dir, "raw")).rglob("*.aseprite")]


def live_pack_check_monitored_files(atlas):
    """
    Checks if any the files in monitored_raw_files have been updated since last we packed.
    If any have changed, update the atlas.
    """
    global monitored_raw_files
    if any(os.path.getmtime(file) != saved_time for (file, saved_time) in monitored_raw_files):
        print("Some file has changed, updating packed!")
        pack_raw_files()
        update_monitored_raw_file_timestamps()
        atlas.update_atlas()
        
class Texture():
    """
    Represents a texture. Essentially just a Pygame.Surface with a little extra info.
    """
    name : str
    seconds : int
    image : pg.Surface

    def __init__(self, name, seconds, image):
        self.name = name
        self.seconds = seconds
        self.image = image


    def __str__(self):
        return self.name
       
    def __lt__(self, other):
        return self.name < other.name
    


class Atlas():

    """
    A list of all the textures
    """
    entries : list[Texture]

    def __init__(self, data_path: str, atlas_path: str):
        self.data_path = data_path
        self.atlas_path = atlas_path
        self.initialize_atlas()

        self.listeners = []


    def initialize_atlas(self):
        
        self.entries = {}

        # Load the files
        data = open(os.path.join(base_dir, "packed", self.data_path))
        
        atlas_full_path = os.path.join(base_dir, "packed", self.atlas_path)
        self.image = pg.image.load(atlas_full_path)
        
        # Convert from JSON to python dict.
        content = json.load(data)

        # Fetch each frame
        frames = content['frames']

        # Go over all frames
        for name in frames:

            this = frames[name]
            
            # Extract data
            x = this['frame']['x']
            y = this['frame']['y']
            w = this['frame']['w']
            h = this['frame']['h']
            seconds = this['duration'] / 1000.0
            rect = pg.Rect(x, y, w, h)
            image = pg.Surface((w, h), pg.SRCALPHA).convert_alpha()
            
            image.blit(self.image, (0, 0), rect)

            self.entries[name] = Texture(name, seconds, image)


    def update_atlas(self):
        self.initialize_atlas()

        for listener in self.listeners:
            listener(self)


    def add_listener(self, func):
        self.listeners.append(func)


    def get_animation(self, name): 
        def anim_comp(a):
            start = a.name.find(" ")
            end = a.name.find(".")
            number_str = a.name[start:end]
            number = int(number_str)
            return number


        results = []
        # We need to look through the atlas for everyhing that starts with name
        for key in self.entries.keys():
            if key.startswith(name):
                results.append(self.entries[key])

        results.sort(key=anim_comp)

        return results


    def get_image(atlas, name):
        return atlas.entries[name]

   
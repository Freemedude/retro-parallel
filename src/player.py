#!/usr/bin/env python

import pygame as pg
from enum import Enum
from src.assets import Texture

class Player(pg.sprite.Sprite):

    class Animations(Enum):
        RUNNING = 1

    current_animation : Animations
    animations : dict[Animations, list[Texture]] = {}

    def __init__(self, atlas):
        # Add this to atlas
        pg.sprite.Sprite.__init__(self, self.containers)
        
        self.fetch_player_assets(atlas)
        atlas.add_listener(self.fetch_player_assets)

        self.start_animation(self.Animations.RUNNING)
        

    def fetch_player_assets(self, atlas):        
        self.animations[self.Animations.RUNNING] = atlas.get_animation("anim_player_run")

    def start_animation(self, animation):
        self.current_animation = animation
        self.animation_index = 0
        frame = self.animations[self.current_animation][self.animation_index]
        self.animation_timer = frame.seconds
        self.image = frame.image
        self.image = pg.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()


    def update_animation(self, delta_time):
        self.animation_timer -= delta_time
        anim = self.animations[self.current_animation]

        if self.animation_timer < 0:
            self.animation_index = (self.animation_index + 1) % len(anim)
            frame = anim[self.animation_index]
            self.image = frame.image
            self.animation_timer = frame.seconds
            self.rect = self.image.get_rect()


    def update(self, delta_time):
        self.update_animation(delta_time)
        
        self.rect.move_ip(5 * delta_time, 0)
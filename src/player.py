#!/usr/bin/env python

import pygame as pg

class Player(pg.sprite.Sprite):

    def __init__(self, atlas):
        pg.sprite.Sprite.__init__(self, self.containers)

        self.running_anim = atlas.get_animation("run_animation_color")

        self.start_animation(self.running_anim)


    def start_animation(self, animation):
        self.current_animation = animation
        self.animation_index = 0
        frame = self.current_animation[self.animation_index]
        self.animation_timer = frame.seconds
        self.image = frame.image
        self.rect = self.image.get_rect()


    def update_animation(self, delta_time):
        self.animation_timer -= delta_time

        if self.animation_timer < 0:
            self.animation_index = (self.animation_index + 1) % len(self.current_animation)
            frame = self.current_animation[self.animation_index]
            self.image = frame.image
            self.animation_timer = frame.seconds
            self.rect = self.image.get_rect()


    def update(self, delta_time):
        self.update_animation(delta_time)
        
        self.rect.move_ip(5 * delta_time, 0)
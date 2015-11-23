#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" An old scool fight game """
import kivy
kivy.require('1.9.0')

from kivy.config import Config
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', '10')
Config.set('graphics', 'left', '10')

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '800')

from kivy.core.window import Window
# Instead of Config.set: What is the best way?
# Window.fullscreen = True
# Window.maximize()
# Window.size = (1280, 800)

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.animation import Animation
import random
import os

import change_character  # (self, keycode)
import load_character  # (self)
import change_background  # (self, keycode)
import change_level  # (self, level)


class Game(FloatLayout):
    """ Add all character and background """
    pass


class ImagePlayer(Image):
    """ Display Player """

    def __init__(self, **kwargs):
        super(ImagePlayer, self).__init__(**kwargs)


class ImageDog(Image):
    """ Display Dog """
    pass


class ImageMonster(Image):
    """ Display Monster """
    pass


class ImagePlayerHealth(Image):
    """ Health of Player """
    pass


class ImageMonsterHealth(Image):
    """ Health of the monster """
    pass


class ImageMonster2Health(Image):
    """ Health of monster2 """
    pass


class FightGame(App):
    """ Kivy app """
    path = os.getcwd()
    level = 1
    path_player = "/Samurai"
    path_monster = "/Ranger"
    path_monster2 = "/Ranger"
    monster1 = "monster1"
    monster2 = "monster2"
    path_dog = "/German_Shepherd"
    default_y_character = 110  # See change_background.py base 110
    finish = False
    img = ImagePlayer(source=path +
                      '/Samurai/5x/idle_left.gif',
                      y=default_y_character, x=Window.size[0]/2,
                      size_hint=(0.1, 0.1))
    img_dog = ImagePlayer(source=path +
                          '/German_Shepherd/x3/idle_right.gif',
                          y=default_y_character + 12, x=400,
                          size_hint=(0.07, 0.07))
    gif_anim_delay = 0.05
    img_monster = ImageMonster(source=path + path_monster +
                               '/5x/idle_right.gif',
                               y=default_y_character, x=Window.size[0],
                               size_hint=(0.1, 0.1))
    img_monster2 = ImageMonster(source=path + path_monster2 +
                                '/5x/idle_right.gif',
                                y=default_y_character, x=30,
                                size_hint=(0.1, 0.1))
    monster_healt = NumericProperty(3)
    monster2_healt = NumericProperty(3)
    player_healt = NumericProperty(3)
    player_img_healt = ImagePlayerHealth(source=path + "/Heart_health_bar/" +
                                         "3" + ".png",
                                         y=350,
                                         x=-430,
                                         size_hint=(1, 1))
    monster1_img_healt = ImageMonsterHealth(source=path + path_monster + "/" +
                                            "3" + ".png",
                                            y=350,
                                            x=90,
                                            size_hint=(1, 1))
    monster2_img_healt = ImageMonster2Health(source=path + path_monster2 +
                                             "/" + "3" + ".png",
                                             y=350,
                                             x=450,
                                             size_hint=(1, 1))
    monster_damage = 1
    monster2_damage = 1
    monster_rapidity = 5
    monster2_rapidity = 6
    space_down = "False"  # False or True
    jump = "no"  # no or yes
    jump_monster = "no"  # no or yes
    shield = "Down"  # Down or Up
    # Background Image
    img_back = Image(source=path +
                     '/background/country-platform-preview.png',
                     allow_stretch=True)

    def __init__(self, **kwargs):
        super(FightGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down,
                            on_key_up=self._on_keyboard_up)

    def heart(self, img_of_monster):
        """ Check if the player touch the monster """
        if "jump" not in img_of_monster.source:
            if self.img.source == (self.path + self.path_player +
                                   '/5x/attack_right.gif'):
                if self.img.x >= img_of_monster.x - 60 and\
                        self.img.x <= img_of_monster.x:
                    self.check_monster_healt(img_of_monster)
            elif self.img.source == (self.path + self.path_player +
                                     '/5x/attack_left.gif'):
                if self.img.x <= img_of_monster.x + 40 and\
                        self.img.x >= img_of_monster.x:
                    self.check_monster_healt(img_of_monster)
        else:
            pass

    def monster_dead(self, img_of_monster, path_of_monster):
        """ Display dead picture if monster is dead: monster_healt <= 0 """
        img_of_monster.source = (self.path + path_of_monster +
                                 '/5x/x_1.png')

    def check_monster_healt(self, img_of_monster):
        """ Check if monster is dead """
        self.animate_character(img_of_monster, self.img, 0.6)
        if self.img_monster2 == img_of_monster:
            self.check_monster_healt_2(self.monster2_healt,
                                       self.monster2,
                                       img_of_monster,
                                       self.path_monster2)
        elif self.img_monster == img_of_monster:
            self.check_monster_healt_2(self.monster_healt,
                                       self.monster1,
                                       img_of_monster,
                                       self.path_monster)
        else:
            pass

    def check_monster_healt_2(self, monster_healt_of,
                              monster, img_of_monster,
                              path_of_monster_of):
        """ Remove healt to monster of kill him: change image """
        if "2" in monster:
            if monster_healt_of > 0:
                self.monster2_healt -= 1
                self.health_update()
            else:
                self.monster_dead(img_of_monster, path_of_monster_of)
        else:
            if monster_healt_of > 0:
                self.monster_healt -= 1
                self.health_update()
            else:
                self.monster_dead(img_of_monster, path_of_monster_of)

    def animate_character(self, img_of_attacked, img_of_attacker, duration):
        """ Anim when character is touched """
        if "right" in img_of_attacker.source:
            anim = Animation(x=img_of_attacked.x + 80,
                             t='out_quint',
                             duration=duration)
        else:
            anim = Animation(x=img_of_attacked.x - 80,
                             t='out_quint',
                             duration=duration)
        anim.start(img_of_attacked)

    def monster_move(self, monster_healt_to, img_to_monster, path_to_monster,
                     rapidity):
        """ Move if monster is not dead """
        if monster_healt_to > 0:
            if self.jump_monster == "no":
                self.monster_move_ok(monster_healt_to, img_to_monster,
                                     path_to_monster, rapidity)
            else:
                pass
        else:
            self.monster_dead(img_to_monster, path_to_monster)

    def monster_move_ok(self, monster_healt_to, img_of_monster,
                        path_of_monster, rapidity):
        """ Move the monster """
        if img_of_monster.x < self.img.x:
            if img_of_monster.x >= self.img.x - 20:
                if monster_healt_to > 0:
                    img_of_monster.source = (self.path + path_of_monster +
                                             "/5x/attack_right.gif")
            else:
                img_of_monster.source = (self.path + path_of_monster +
                                         "/5x/run_right.gif")
                img_of_monster.x += rapidity
        elif img_of_monster.x > self.img.x:
            if img_of_monster.x <= self.img.x + 25:
                if monster_healt_to > 0:
                    img_of_monster.source = (self.path + path_of_monster +
                                             "/5x/attack_left.gif")
            else:
                img_of_monster.source = (self.path + path_of_monster +
                                         "/5x/run_left.gif")
                img_of_monster.x -= rapidity

    def monster_attack(self, img_of_monster, path_of_monster, damage):
        """ Check if monster touch you """
        if self.shield == "Up" and\
                ("right" in self.img.source and
                 "left" in img_of_monster.source or
                 "left" in self.img.source and
                 "right" in img_of_monster.source):
            # print " Attack blocked"
            pass
        else:
            self.monster_got_you(img_of_monster, path_of_monster, damage)

    def monster_got_you(self, img_of_monster, path_of_monster, damage):
        """ Check if monster touch you or kill you! """
        if img_of_monster.source ==\
            (self.path + path_of_monster +
             "/5x/attack_left.gif")\
            or img_of_monster.source == (self.path + path_of_monster +
                                         "/5x/attack_right.gif"):
            got_you = random.randint(0, 1)
            if got_you == 0 and self.img.y == self.default_y_character:
                # print "touched"
                self.animate_character(self.img,
                                       img_of_monster, 0.3)
                self.player_healt -= damage
                self.health_update()
                if self.player_healt <= 0:
                    self.img.source = (self.path + self.path_player +
                                       "/5x/x_1.png")

    def character_down(self, img_of_character, path_to_character,
                       jump_character, character):
        """ Get the player down back! """
        if img_of_character.y == self.default_y_character\
                and jump_character == "no"\
                and "jump" in img_of_character.source:
            if "right" in img_of_character.source:
                img_of_character.source = (self.path + path_to_character +
                                           "/5x/idle_right.gif")
            else:
                img_of_character.source = (self.path + path_to_character +
                                           "/5x/idle_left.gif")
        if img_of_character.y >= self.default_y_character + 50:
            if "monster" in character:
                self.jump_monster = "no"
            else:
                self.jump = "no"
            if "right" in img_of_character.source:
                anim = Animation(x=img_of_character.x + 100,
                                 y=self.default_y_character,
                                 t='out_expo',
                                 duration=0.5)
            else:
                anim = Animation(x=img_of_character.x - 100,
                                 y=self.default_y_character,
                                 t='out_expo',
                                 duration=0.5)
            anim.start(img_of_character)

    def health_update(self):
        """ Update pictuer of healt """
        print self.player_healt
        self.player_img_healt.source = (self.path +
                                        "/Heart_health_bar/" +
                                        str(self.player_healt) +
                                        ".png")
        self.monster1_img_healt.source = (self.path +
                                          self.path_monster + "/" +
                                          str(self.monster_healt) +
                                          ".png")
        self.monster2_img_healt.source = (self.path +
                                          self.path_monster2 + "/" +
                                          str(self.monster2_healt) +
                                          ".png")
        print self.player_img_healt.source
        print self.monster1_img_healt.source

    def dog_move(self):
        """ The Dog follow the player """
        # Dog away
        if self.img_dog.x < self.img.x - 60:
            self.img_dog.x += 10
            self.img_dog.source = (self.path + self.path_dog +
                                   "/x3/run_right.gif")
        elif self.img_dog.x > self.img.x + 60:
            self.img_dog.x -= 10
            self.img_dog.source = (self.path + self.path_dog +
                                   "/x3/run_left.gif")
        # If Dog turned in the bad direction
        elif "run" not in self.img.source:
            if "left" in self.img.source:
                if self.img_dog.x < self.img.x + 50:
                    self.img_dog.source = (self.path + self.path_dog +
                                           "/x3/run_right.gif")
                    self.img_dog.x += 5
                else:
                    self.img_dog.source = (self.path + self.path_dog +
                                           "/x3/idle_left.gif")
            else:
                if self.img_dog.x > self.img.x - 30:
                    self.img_dog.source = (self.path + self.path_dog +
                                           "/x3/run_left.gif")
                    self.img_dog.x -= 5
                else:
                    self.img_dog.source = (self.path + self.path_dog +
                                           "/x3/idle_right.gif")
        # Dog Waiting if player waiting
        elif self.img_dog.x == self.img.x - 60:
            self.img_dog.source = (self.path + self.path_dog +
                                   "/x3/idle_right.gif")
        elif self.img_dog.x == self.img.x + 60:
            self.img_dog.source = (self.path + self.path_dog +
                                   "/x3/idle_left.gif")

        else:
            pass

    def change_player(self, player, delay):
        """ Change the player """
        self.path_player = player
        self.gif_anim_delay = delay

    def _keyboard_closed(self):
        """ Call _on_keyboard_down """
        print'My keyboard have been closed!'
        self._keyboard.unbind(on_key_down=self._on_keyboard_down,
                              on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def build(self):
        """ Return the game """
        # Load all the images during loading
        load_character.load_character(self, self.path_player, "player")
        load_character.load_character(self, self.path_monster, "1")
        load_character.load_character(self, self.path_monster2, "2")

        Clock.schedule_interval(lambda dt:
                                self.monster_move(self.monster_healt,
                                                  self.img_monster,
                                                  self.path_monster,
                                                  self.monster_rapidity),
                                0.04)
        Clock.schedule_interval(lambda dt:
                                self.monster_move(self.monster2_healt,
                                                  self.img_monster2,
                                                  self.path_monster2,
                                                  self.monster2_rapidity),
                                0.04)
        Clock.schedule_interval(lambda dt: self.dog_move(), 0.04)
        Clock.schedule_interval(lambda dt:
                                self.monster_attack(self.img_monster,
                                                    self.path_monster,
                                                    self.monster_damage), 1)
        Clock.schedule_interval(lambda dt:
                                self.monster_attack(self.img_monster2,
                                                    self.path_monster2,
                                                    self.monster2_damage), 1)
        Clock.schedule_interval(lambda dt:
                                self.monster_jump(self.img_monster,
                                                  self.img_monster2), 0.04)
        Clock.schedule_interval(lambda dt:
                                self.character_down(self.img,
                                                    self.path_player,
                                                    self.jump, "player"), 0.04)
        Clock.schedule_interval(lambda dt:
                                self.character_down(self.img_monster,
                                                    self.path_monster,
                                                    self.jump_monster,
                                                    "monster"), 0.04)
        Clock.schedule_interval(lambda dt:
                                self.character_down(self.img_monster2,
                                                    self.path_monster2,
                                                    self.jump_monster,
                                                    "monster"), 0.04)
        Clock.schedule_interval(lambda dt: self.win(), 0.04)
        game = Game()
        game.add_widget(self.img_back)
        game.add_widget(self.player_img_healt)
        game.add_widget(self.img_dog)
        game.add_widget(self.img_monster)
        game.add_widget(self.monster1_img_healt)
        game.add_widget(self.monster2_img_healt)
        game.add_widget(self.img_monster2)
        game.add_widget(self.img)
        return game

    def _on_keyboard_up(self, keyboard, keycode):
        """ Events on keyboard up """
        self.shield = "Down"
        self.space_down = "False"
        if "jump" not in self.img.source:
            if self.img.x is not int:
                # self.img.x can't be 112 or 434.3 but 110 and 430
                self.img.x = ((self.img.x // 10)*10)
            if 'attack' in self.img.source:
                pass
            else:
                if 'left' in self.img.source:
                    self.img.source = (self.path + self.path_player +
                                       '/5x/idle_left.gif')
                elif 'right' in self.img.source:
                    self.img.source = (self.path + self.path_player +
                                       '/5x/idle_right.gif')
                self.img.anim_loop = 0
                self.img.anim_delay = 0.5

    def load_new_player(self):
        """ Change the Player: used by change_character() """
        if "right" in self.img.source:
            self.img.source = (self.path + self.path_player +
                               '/5x/idle_right.gif')
        else:
            self.img.source = (self.path + self.path_player +
                               '/5x/idle_left.gif')

    def monster_jump(self, img_of_monster1, img_of_monster2):
        """ Monster jump the player if player already fighting """
        # Check if a monster is fighting
        # if "attack" in img_of_monster1.source or\
        # "attack" in img_of_monster2.source:
        if "yes" in self.jump_monster:
            pass

        elif "right" in img_of_monster1.source and\
                "right" in img_of_monster2.source:
            if img_of_monster1.x - img_of_monster2.x <= 50 and\
                    img_of_monster1.x - img_of_monster2.x >= -1 or\
                    img_of_monster2.x - img_of_monster1.x <= 50 and\
                    img_of_monster2.x - img_of_monster1.x >= -1:
                self.jump_monster = "yes"
                if "attack" in img_of_monster1.source:
                    self.jump_character_and_monster(img_of_monster2,
                                                    self.path_monster2)
                elif "attack" in img_of_monster2.source:
                    self.jump_character_and_monster(img_of_monster1,
                                                    self.path_monster)
                else:
                    self.jump_ahah(img_of_monster1, img_of_monster2, 3)

        elif "left" in img_of_monster1.source and\
                "left" in img_of_monster2.source:
            if img_of_monster2.x - img_of_monster1.x <= 50 and\
                    img_of_monster2.x - img_of_monster1.x >= -1 or\
                    img_of_monster1.x - img_of_monster2.x <= 50 and\
                    img_of_monster1.x - img_of_monster2.x >= -1:
                self.jump_monster = "yes"
                if "attack" in img_of_monster1.source:
                    self.jump_character_and_monster(img_of_monster2,
                                                    self.path_monster2)
                elif "attack" in img_of_monster2.source:
                    self.jump_character_and_monster(img_of_monster1,
                                                    self.path_monster)
                else:
                    self.jump_ahah(img_of_monster1, img_of_monster2, 3)

        elif "idle" or "attack" or "block" in self.img.source:
            # if one monster is dead, second monster jump more (more agressive)
            if self.monster_healt <= 0 or self.monster2_healt <= 0:
                number_proba = 80
            else:
                number_proba = 150
            self.jump_ahah(img_of_monster1, img_of_monster2, number_proba)

    def jump_ahah(self, img_of_monster1, img_of_monster2, number_probability):
        """ Monster Jump sometimes! """
        number_jump = random.randint(0, number_probability)
        # print img_of_monster1.source
        # print number_jump
        # if monster not dead (png) monster jump
        if number_jump == 0 and "png" not in img_of_monster1.source:
            self.jump_monster = "yes"
            self.jump_character_and_monster(img_of_monster1,
                                            self.path_monster)
        elif number_jump == 1 and "png" not in img_of_monster2.source:
            self.jump_monster = "yes"
            self.jump_character_and_monster(img_of_monster2,
                                            self.path_monster2)
        else:
            self.jump_monster = "no"

    def jump_character(self):
        """ Check if character is alone and can jump """
        if (self.img_monster.x > self.img.x - 60
                and "right" in self.img_monster.source)\
            or (self.img_monster2.x > self.img.x - 60
                and "right" in self.img_monster2.source)\
            or (self.img_monster.x < self.img.x + 60
                and "left" in self.img_monster.source)\
            or (self.img_monster2.x < self.img.x + 60
                and "left" in self.img_monster2.source):
            pass
        else:
            if self.img.y == self.default_y_character:
                self.jump = "yes"
                self.jump_character_and_monster(self.img, self.path_player)

    def jump_character_and_monster(self, img_of_character, path_of_character):
        """ Make the character jump """
        if 'right' in img_of_character.source:
            anim = Animation(x=img_of_character.x + 100,
                             y=self.default_y_character + 50,
                             t='in_quad',
                             duration=0.5)
            img_of_character.source = (self.path +
                                       path_of_character +
                                       '/5x/jump_right.gif')
            anim.start(img_of_character)
        else:
            anim = Animation(x=img_of_character.x - 100,
                             y=self.default_y_character + 50,
                             t='in_quad',
                             duration=0.5)
            img_of_character.source = (self.path +
                                       path_of_character +
                                       '/5x/jump_left.gif')
            anim.start(img_of_character)

    def restart_game(self):
        """ Restart the game: r key or change_background """
        print self.monster1_img_healt.source
        self.finish = False
        self.jump_monster = "no"
        change_level.change_healt(self, self.level)
        self.player_healt = 3
        x_monster = random.randint(Window.size[0] - 80, Window.size[0])
        x_monster2 = random.randint(-100, 30)
        self.img.source = (self.path + self.path_player +
                           '/5x/idle_right.gif')
        self.img_monster.source = (self.path + self.path_monster +
                                   '/5x/idle_right.gif')
        self.img_monster2.source = (self.path + self.path_monster2 +
                                    '/5x/idle_left.gif')
        self.img.x = Window.size[0]/2
        self.img_monster.x = x_monster
        self.img_monster2.x = x_monster2
        self.img.y = self.default_y_character
        self.img_monster.y = self.default_y_character
        self.img_monster2.y = self.default_y_character
        self.img_dog.y = self.default_y_character + 12
        self.health_update()

    def win(self):
        """ Win the level """
        if self.monster_healt <= 0 and self.monster2_healt <= 0:
            self.finish = True
            if self.finish is True:
                self.health_update()
                self.img.source = (self.path + self.path_player +
                                   "/5x/run_right.gif")
                if self.img.x < Window.size[0] + 60:
                    self.img.x += 10
                else:
                    if self.level == 5:
                        pass
                    else:
                        self.level = self.level + 1
                        change_level.change_level(self, self.level)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        """ Move the Image: Player(Widget) """
        # print('The key', keycode, 'have been pressed')
        # print' - text is %r' % text
        # print' - modifiers are %r' % modifiers
        if keycode[1] == 'escape':
            keyboard.release()
        elif keycode[1] == 'r':
            self.restart_game()
        if self.finish is True:
            pass
        else:
            self.keyboard_action(keyboard, keycode, text, modifiers)

    def keyboard_action(self, keyboard, keycode, text, modifiers):
        """ Call by __on_keyboard_down """
        # Change player
        if (keycode[1] == '&' or
                keycode[1] == '\xc3\xa9' or
                keycode[1] == '"' or
                keycode[1] == "'" or
                keycode[1] == "("):
            if 'shift' in modifiers:
                change_background.change_background(self, keycode)
            else:
                # See file change_character.py
                change_character.change_character(self, keycode)
        else:
            if self.player_healt <= 0:
                pass
            else:
                # Player can't leave the screen!, work but not good
                if self.img.x < -40:
                    self.img.x = -40
                elif self.img.x > Window.size[0] - 80:
                    self.img.x = Window.size[0] - 80
                elif keycode[1] == 'left':
                    if self.img.source == (self.path + self.path_player +
                                           '/5x/crouch_left.gif'):
                        self.img.x -= 5
                    else:
                        self.img.source = (self.path + self.path_player +
                                           '/5x/run_left.gif')
                        self.img.anim_delay = 0.25
                        self.img.x -= 10
                elif keycode[1] == 'right':
                    if self.img.source == (self.path + self.path_player +
                                           '/5x/crouch_right.gif'):
                        self.img.x += 5
                    else:
                        self.img.source = (self.path + self.path_player +
                                           '/5x/run_right.gif')
                        self.img.anim_delay = 0.25
                        self.img.x += 10
                elif keycode[1] == 'down':
                    self.shield = "Up"
                    if 'right' in self.img.source:
                        self.img.source = (self.path + self.path_player +
                                           '/5x/block_right.gif')
                    else:
                        self.img.source = (self.path + self.path_player +
                                           '/5x/block_left.gif')
                    self.img.anim_delay = 0.25
                    self.img.anim_loop = 0
                elif keycode[1] == 'up':
                    if self.jump == "yes":
                        pass
                    else:
                        self.jump_character()
                elif keycode[1] == 'spacebar':
                    if self.space_down == "False":
                        self.space_down = "True"
                        if self.img.source == (self.path +
                                               self.path_player +
                                               '/5x/idle_right.gif'):
                            self.img.source = (self.path +
                                               self.path_player +
                                               '/5x/attack_right.gif')
                            self.img.anim_delay = self.gif_anim_delay
                            self.img.anim_loop = 1
                            self.heart(self.img_monster)
                            self.heart(self.img_monster2)

                        elif self.img.source == (self.path +
                                                 self.path_player +
                                                 '/5x/attack_right.gif'):
                            self.img.source = (self.path +
                                               self.path_player +
                                               '')
                            self.img.source = (self.path +
                                               self.path_player +
                                               '/5x/attack_right.gif')
                            self.img.anim_loop = 1
                            self.heart(self.img_monster)
                            self.heart(self.img_monster2)

                        elif self.img.source == (self.path +
                                                 self.path_player +
                                                 '/5x/attack_left.gif'):
                            self.img.source = (self.path +
                                               '')
                            self.img.source = (self.path +
                                               self.path_player +
                                               '/5x/attack_left.gif')
                            self.img.anim_loop = 1
                            self.heart(self.img_monster)
                            self.heart(self.img_monster2)
                        else:
                            if self.img.source == (self.path +
                                                   self.path_player +
                                                   '/5x/idle_left.gif'):
                                self.img.source = (self.path +
                                                   self.path_player +
                                                   '/5x/attack_left.gif')
                                self.img.anim_delay = self.gif_anim_delay
                                self.img.anim_loop = 1
                                self.heart(self.img_monster)
                                self.heart(self.img_monster2)
        return True


if __name__ == '__main__':
    FightGame().run()

# -*- coding: utf-8 -*-
""" This file is a part of fightgame made by Maltouzes """


def change_level(self, level):
    """ Change the background """
    if level == 2:
        self.img_back.source = (self.path +
                                # '/background/fight-backgrounds-07.gif')
                                '/background/fantasy_001_1920x1080.png')
        # self.default_y_character = 130
        self.default_y_character = 60
    elif level == 3:
        self.img_back.source = (self.path +
                                # '/background/fight-backgrounds-01.gif')
                                '/background/fantasy_002_1920x1080.png')
        # self.default_y_character = 60
        self.default_y_character = 40
    elif level == 4:
        self.img_back.source = (self.path +
                                # '/background/fight-backgrounds-04.gif')
                                '/background/village_004_1920x1080.png')
        # self.default_y_character = 105
        self.default_y_character = 80
    elif level == 5:
        self.img_back.source = (self.path +
                                # '/background/fight-backgrounds-15.gif')
                                '/background/forest_001_1920x1080.png')
        # self.default_y_character = 135
        self.default_y_character = 60
    self.restart_game()


def change_healt(self, level):
    import load_character
    if level == 1:
        self.monster_healt = 3
        self.monster2_healt = 3
        self.monster_rapidity = 5
        self.monster2_rapidity = 6
        self.path_monster = "/Ranger"
        self.path_monster2 = "/Ranger"
    elif level == 2:
        self.monster_healt = 4
        self.monster2_healt = 4
        self.monster_rapidity = 6
        self.monster2_rapidity = 6
        self.path_monster = "/Pirate"
        self.path_monster2 = "/Ranger"
    elif level == 3:
        self.monster_healt = 4
        self.monster2_healt = 5
        self.monster_rapidity = 6
        self.monster2_rapidity = 7
        self.path_monster = "/Pirate"
        self.path_monster2 = "/Shieldmaiden"
    elif level == 4:
        self.monster_healt = 5
        self.monster2_healt = 5
        self.monster_rapidity = 7
        self.monster2_rapidity = 7
        self.path_monster = "/Shieldmaiden"
        self.path_monster2 = "/Ninja"
    elif level == 5:
        self.monster_healt = 6
        self.monster2_healt = 7
        self.monster_rapidity = 8
        self.monster2_rapidity = 8
        self.path_monster = "/Ninja"
        self.path_monster2 = "/Samurai"
    load_character.load_character(self, self.path_monster, "1")
    load_character.load_character(self, self.path_monster2, "2")

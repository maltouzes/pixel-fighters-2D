""" This file is a part of pixel-fighters-2D made by Maltouzes """


def change_background(self, keycode):
    """ Change the background """
    if keycode[1] == '&':
        self.img_back.source = (self.path +
                                '/background/fight-backgrounds-16.gif')
        self.default_y_character = 110
    elif keycode[1] == '\xc3\xa9':
        self.img_back.source = (self.path +
                                '/background/fight-backgrounds-07.gif')
        self.default_y_character = 130
    elif keycode[1] == '"':
        self.img_back.source = (self.path +
                                '/background/fight-backgrounds-01.gif')
        self.default_y_character = 40
    elif keycode[1] == "'":
        self.img_back.source = (self.path +
                                '/background/fight-backgrounds-04.gif')
        self.default_y_character = 105
    elif keycode[1] == '(':
        self.img_back.source = (self.path +
                                '/background/fight-backgrounds-15.gif')
        self.default_y_character = 135
    self.restart_game()

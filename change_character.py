""" This file is a part of pixel-fighters-2D made by Maltouzes """


def change_character(self, keycode):
    """ Change the character player """
    if keycode[1] == '&':
        self.change_player('/Samurai', 0.05)
    elif keycode[1] == '\xc3\xa9':
        self.change_player('/Pirate', 0.1)
    elif keycode[1] == '"':
        self.change_player('/Ranger', 0.2)
    elif keycode[1] == "'":
        self.change_player('/Shieldmaiden', 0.1)
    elif keycode[1] == '(':
        self.change_player('/Ninja', 0.1)
    self.load_new_player()

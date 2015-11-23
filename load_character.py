""" This file is a part of fightgame made by Maltouzes """


def load_character(self, character, character_source):
    import os
    print character
    """ Load all img when the game start """
    for file in os.listdir(self.path + character + '/5x/'):
        if file.endswith(".gif"):
            if "player" in character_source:
                self.img.source = (self.path + self.path_player + "/5x/" +
                                   file)
            elif "1" in character_source:
                self.img_monster.source = (self.path + self.path_monster
                                           + "/5x/" + file)
            elif "2" in character_source:
                self.img_monster2.source = (self.path + self.path_monster2
                                            + "/5x/" + file)

        # print self.img.source

from .hardcore_obj import HardcoreObj
from .section import Section


class SectionHardcore(Section, HardcoreObj):
    def __init__(self, pieces, turn_time):
        Section.__init__(self, pieces)
        HardcoreObj.__init__(self, turn_time)

    def add_piece(self, piece_to_add):
        if self.grabbed:
            piece_to_add.stop_turning()
            piece_to_add.auto_turn(self.pieces[0].get_num_of_image())
        else:
            num = piece_to_add.get_num_of_image()
            self.auto_turn(num)
        self.prepare_turn()
        return Section.add_piece(self, piece_to_add)

    def add_section(self, section):
        section.auto_turn(self.pieces[0].get_num_of_image())
        Section.add_section(self, section)

    def click(self, mouse_pos):
        Section.click(self, mouse_pos)
        HardcoreObj.click(self)

    def unclick(self):
        Section.unclick(self)
        HardcoreObj.unclick(self)

    def update(self, dt):
        HardcoreObj.update(self, dt)

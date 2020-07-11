from .hardcore_obj import HardcoreObj
from .section import Section


class SectionHardcore(Section, HardcoreObj):
    def __init__(self, pieces, flip_time):
        Section.__init__(self, pieces)
        HardcoreObj.__init__(self, flip_time)

    def add_piece(self, piece_to_add):
        self.stop_moving()
        piece_to_add.stop_moving()
        if self.grabbed:
            piece_to_add.stop_turning()
            piece_to_add.auto_turn(self.pieces[0].get_num_of_image())
        else:
            num = piece_to_add.get_num_of_image()
            self.auto_turn(num)
        self.prepare_to_flip()
        return Section.add_piece(self, piece_to_add)

    def add_section(self, section):
        self.stop_moving()
        section.stop_moving()
        section.auto_turn(self.pieces[0].get_num_of_image())
        Section.add_section(self, section)

    def relax(self):
        """
        Stop trying to move all the time.
        Used when the puzzle is finished.
        """
        self.relaxed = True
        self.stop_moving()
        self.move_task = None

    def click(self, mouse_pos):
        Section.click(self, mouse_pos)
        HardcoreObj.click(self)

    def unclick(self):
        Section.unclick(self)
        HardcoreObj.unclick(self)

    def update(self, dt):
        HardcoreObj.update(self, dt)

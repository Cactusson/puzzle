import pickle
import pygame as pg

from .. import prepare, tools
from ..components.gui import GUI
from ..components.puzzle import Puzzle
from ..components.timer import Timer


def time_to_text(time):
    minutes = str(time // 60)
    if len(minutes) == 1:
        minutes = '0' + minutes
    seconds = str(time % 60)
    if len(seconds) == 1:
        seconds = '0' + seconds
    return '{}:{}'.format(minutes, seconds)


class Game(tools._State):
    def __init__(self):
        tools._State.__init__(self)

    def start(self, pic_num, pic):
        self.pic_num = pic_num

        if not self.hardcore:
            try:
                results_file = open('results', 'rb')
                self.results = pickle.load(results_file)
            except:
                # results coded this way:
                # for each pic [0, 0, 0] (for EASY, NORMAL, HARD)
                # hardcore mode doesn't use results
                self.results = [[0, 0, 0] for _ in
                                range(prepare.PICS_AMOUNT)]

            self.current_result = \
                self.results[self.pic_num][self.difficulty]
            best_time = time_to_text(self.current_result)
        else:
            best_time = None

        self.puzzle = Puzzle(self.puzzle_finished, pic,
                             prepare.DIFFICULTY_SIZE[self.difficulty])
        self.timer = Timer((816, 0))
        self.timer.start()
        self.gui = GUI(best_time, self.difficulty, self.hardcore)

    def puzzle_finished(self):
        self.timer.stop()
        if not self.hardcore:
            result_time = self.timer.current_time
            if result_time < self.current_result or self.current_result == 0:
                self.results[self.pic_num][self.difficulty] = \
                    result_time
                results_file = open('results', 'wb')
                pickle.dump(self.results, results_file)

    def startup(self, persistant):
        self.persist = persistant
        pic_num = self.persist['pic_num']
        del self.persist['pic_num']
        pic = self.persist['pic']
        del self.persist['pic']
        self.difficulty = self.persist['difficulty']
        del self.persist['difficulty']
        self.hardcore = self.persist['hardcore']
        del self.persist['hardcore']
        self.start(pic_num, pic)

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.puzzle.click(event.pos)
        elif event.type == pg.MOUSEBUTTONUP:
            self.puzzle.unclick()

    def draw(self, surface):
        surface.fill(pg.Color('lightgray'))
        self.puzzle.draw(surface)
        self.timer.draw(surface)
        self.gui.draw(surface)

    def update(self, surface, dt):
        self.timer.update(dt)
        mouse_pos = pg.mouse.get_pos()
        self.puzzle.update(mouse_pos)
        self.draw(surface)

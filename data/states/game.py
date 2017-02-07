import pickle
import pygame as pg

from .. import prepare, tools
from ..components.gui import GUI
from ..components.puzzle import Puzzle
from ..components.puzzle_hardcore import PuzzleHardcore
from ..components.timer import Timer


class Game(tools._State):
    def __init__(self):
        tools._State.__init__(self)

    def start(self, pic, pic_num=None, pic2=None):
        if not self.hardcore:
            self.pic_num = pic_num
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
            best_time = tools.time_to_text(self.current_result)
            self.puzzle = Puzzle(self.puzzle_finished, pic,
                                 prepare.DIFFICULTY_SIZE[self.difficulty])
        else:
            best_time = None
            self.puzzle = PuzzleHardcore(
                self.puzzle_finished, pic, pic2,
                prepare.TURN_TIME[self.difficulty],
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
        if self.previous == 'LOAD':
            pic_num = self.persist['pic_num']
            del self.persist['pic_num']
            pic = self.persist['pic']
            del self.persist['pic']
            self.difficulty = self.persist['difficulty']
            del self.persist['difficulty']
            self.hardcore = self.persist['hardcore']
            del self.persist['hardcore']
            if self.hardcore:
                pic2 = self.persist['pic2']
                del self.persist['pic2']
                self.start(pic, pic2=pic2)
            else:
                self.start(pic, pic_num=pic_num)
            prepare.make_transition(self, 'GAME', True)

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            elif event.key == pg.K_q:
                self.persist['screen'] = pg.display.get_surface().copy()
                self.next = 'PAUSE'
                self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.puzzle.click(event.pos)
        elif event.type == pg.MOUSEBUTTONUP:
            self.puzzle.unclick()

    def draw(self, surface):
        surface.fill(prepare.BG_GAME_COLOR)
        self.puzzle.draw(surface)
        self.timer.draw(surface)
        self.gui.draw(surface)

    def update(self, surface, dt):
        self.timer.update(dt)
        mouse_pos = pg.mouse.get_pos()
        self.puzzle.update(mouse_pos, dt)
        self.draw(surface)

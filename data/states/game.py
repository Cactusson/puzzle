import pickle
import pygame as pg
import random

from .. import prepare, tools
from ..components.darkness import Darkness
from ..components.gui import GUI
from ..components.puzzle import Puzzle
from ..components.puzzle_hardcore import PuzzleHardcore
from ..components.timer import Timer


class Game(tools._State):
    def __init__(self):
        tools._State.__init__(self)

    def start(self):
        self.pic_num = random.randint(0, prepare.PICS_AMOUNT - 1)
        self.pic = prepare.GFX['pictures']['pic0{}'.format(self.pic_num)]
        if self.hardcore:
            pic_num2 = random.choice([num for num in range(prepare.PICS_AMOUNT)
                                      if num != self.pic_num])
            self.pic2 = prepare.GFX['pictures']['pic0{}'.format(pic_num2)]
        else:
            self.pic2 = None
        self.create_round()

    def create_round(self):
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
            best_time = tools.time_to_text(self.current_result)
            self.puzzle = Puzzle(self.puzzle_finished, self.pic,
                                 prepare.DIFFICULTY_SIZE[self.difficulty])
        else:
            best_time = None
            self.puzzle = PuzzleHardcore(
                self.puzzle_finished, self.pic, self.pic2,
                prepare.TURN_TIME[self.difficulty],
                prepare.DIFFICULTY_SIZE[self.difficulty])

        self.timer = Timer((816, 0))
        self.timer.start()
        self.gui = GUI(best_time, self.difficulty, self.hardcore,
                       self.finish_game)
        if self.hardcore:
            self.dark_cover = Darkness()
        else:
            self.dark_cover = None

    def puzzle_finished(self):
        self.timer.stop()
        if not self.hardcore:
            result_time = self.timer.current_time
            if result_time < self.current_result or self.current_result == 0:
                self.results[self.pic_num][self.difficulty] = \
                    result_time
                results_file = open('results', 'wb')
                pickle.dump(self.results, results_file)
        self.gui.show_finish_button()

    def finish_game(self):
        self.next = 'MENU'
        self.done = True

    def startup(self, persistant):
        self.persist = persistant
        if self.previous == 'CHOOSE':
            self.difficulty = self.persist['difficulty']
            del self.persist['difficulty']
            self.hardcore = self.persist['hardcore']
            del self.persist['hardcore']
            self.start()
            prepare.make_transition(self, 'GAME', True)
        elif self.previous == 'PAUSE':
            if 'restart' in self.persist:
                if self.persist['restart'] == 'INIT':
                    self.create_round()
                    image = pg.Surface(prepare.SCREEN_RECT.size).convert()
                    self.draw(image)
                    self.persist['restart_screen'] = image
                    self.next = 'PAUSE'
                    self.done = True
                elif self.persist['restart'] == 'DONE':
                    del self.persist['restart']

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.persist['screen'] = pg.display.get_surface().copy()
                self.next = 'PAUSE'
                self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.puzzle.click(event.pos)
            self.gui.click()
        elif event.type == pg.MOUSEBUTTONUP:
            self.puzzle.unclick()

    def draw(self, surface):
        surface.fill(prepare.BG_GAME_COLOR)
        self.puzzle.draw(surface)
        self.timer.draw(surface)
        self.gui.draw(surface)
        if self.dark_cover:
            self.dark_cover.draw(surface)

    def update(self, surface, dt):
        self.timer.update(dt)
        mouse_pos = pg.mouse.get_pos()
        self.puzzle.update(mouse_pos, dt)
        self.gui.update(mouse_pos, dt)
        if self.dark_cover:
            self.dark_cover.update(mouse_pos, dt)
        self.draw(surface)

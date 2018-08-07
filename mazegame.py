from maze import Maze
from mouse import Mouse
from mazedisplay import MazeDisplay
from pygtools import TextBox
import pygame
import os
from sys import exit

class MazeGame:

    def start(self, (width, height)=(640, 480), fullscreen=False):
        pygame.init()
        if fullscreen:
            os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
            self.window = pygame.display.set_mode((0,0), pygame.NOFRAME)
        else:
            self.window = pygame.display.set_mode((width, height))
        while True:
            pygame.key.set_repeat(0)
            pygame.event.clear()
            self.display_welcome()
            maze_instance = Maze((55, 55))
            maze_display = MazeDisplay(maze_instance, self.window)
            maze_display.run()

    def display_welcome(self):
        self.loading = True
        start_text = pygame.font.Font(None, 18).render(
                "Begin!", False, (0, 0, 0))
        maze_demo = Maze((9, 9))
        mouse_demo = Mouse(maze_demo)
        mouse_image = pygame.transform.scale(
            pygame.image.load("mouse.png"), (20, 20))
        board_demo = pygame.Surface((180, 180))
        pygame.draw.rect(board_demo, (150, 150, 150),
                pygame.Rect(20, 20, 140, 140))
        for x in range(1, 8):
                for y in range(1, 8):
                    maze_demo.change_cell((x, y))

        while self.loading:
            #demo maze blitting, updating
            self.window.blit(pygame.transform.scale(board_demo,
                    self.window.get_size()), (0, 0))
            board_demo.fill((0, 0, 0))
            pygame.draw.rect(board_demo, (150, 150, 150),
                    pygame.Rect(20, 20, 140, 140))
            board_demo.blit(
                    pygame.transform.rotate(mouse_image,
                        90 * mouse_demo.facing),
                        (20 * mouse_demo.pos[0], 20 * mouse_demo.pos[1]))
            mouse_demo.demo_move()
            #start button
            pygame.draw.rect(board_demo, (0, 200, 0),
                    pygame.Rect(70, 80, 40, 20))
            self.start_mask = pygame.mask.from_threshold(
                    board_demo, (0, 200, 0), (10, 10, 10, 255)).scale((
                            self.window.get_width(),
                            self.window.get_height()))
            pygame.draw.rect(board_demo, (0, 0, 0),
                    pygame.Rect(70, 80, 40, 20), 1)
            board_demo.blit(start_text, (
                    90 - start_text.get_width() / 2,
                    90 - start_text.get_height() / 2))
            #events and flip
            self.check_events()
            pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit(0)
                elif event.key == pygame.K_RETURN:
                    self.loading = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.start_mask.get_at(event.pos):
                    self.loading = False

game = MazeGame()
game.start(fullscreen=True)
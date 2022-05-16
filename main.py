import pygame
import time
import random
from pygame.locals import *
import threading
import speech_recognition
import speech_recognition as sr
import playsound
from playsound import playsound

SIZE = 40
screen = pygame.display.set_mode((1000, 600))
screen.fill((39, 217, 155))
pygame.display.flip()

# class Threader:
    # def __init__(self, screen):
    #     self.game = Game()
    #     self.screen = screen
    #     self.snake = Snake(screen)
    #     self.apple = Apple(screen)
    #
    # def thread_deez(self):
    #     x = threading.Thread(target=self.game.run(), args=)

class Apple:
    def __init__(self, main_screen):
        self.main_screen = main_screen
        self.apple = pygame.image.load("venv/resources/apple.png").convert()
        self.apple = pygame.transform.scale(self.apple, (40, 40))
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw_apple(self):
        # self.main_screen.fill((39, 217, 155))
        self.main_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

    def move_apple(self):
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 14) * SIZE

class Snake:

    def __init__(self, main_screen, length):
        self.main_screen = main_screen
        self.length = length
        self.block = pygame.image.load("venv/resources/block.png").convert()
        self.block = pygame.transform.scale(self.block, (40, 40))
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = ""

    def draw_snake(self):
        self.main_screen.fill((39, 217, 155))
        for i in range(self.length):
            self.main_screen.blit(self.block, (self.x[i], self.y[i]))

        pygame.display.flip()

    def grow_snake(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def crawl(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]


        if self.direction == "left":
            self.x[0] -= SIZE

        if self.direction == "right":
            self.x[0] += SIZE

        if self.direction == "up":
            self.y[0] -= SIZE

        if self.direction == "down":
            self.y[0] += SIZE

        self.draw_snake()

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"



class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = screen
        # self.play_bgmusic()

        self.apple = Apple(screen)
        self.apple.draw_apple()

        self.snake = Snake(screen, 1)
        self.snake.draw_snake()

    # def voice(self):
    #     r = sr.Recognizer()
    #
    #     print("What do you want?")
    #
    #     with sr.Microphone() as source:
    #         audio = r.listen(source)
    #         voice_data = ''
    #
    #         try:
    #             voice_data = r.recognize_google(audio)
    #             print(voice_data)
    #
    #         except sr.UnknownValueError:
    #             print("Sorry I didn't get that")
    #
    #         except sr.RequestError:
    #             print("Sorry I'm a dumb bitch")
    #
    #     return voice_data



    def collision(self, x1, y1, x2, y2):
        if x1 == x2 and x1 < x2 + SIZE:
            if y1 == y2 and y1 < y2 + SIZE:
                return True

        return False

    def over_boundary(self, x1, y1):
        if x1 < 0 or x1 > 1000:
            return True
        if y1 < 0 or y1 > 600:
            return True
        return False

    def play_bgmusic(self):
        # pygame.mixer.music.load(filename='pop.mp3')
        # pygame.mixer.music.play()
        pass
        # playsound('pop.mp3')

    def play(self):
        self.snake.crawl()
        self.apple.draw_apple()
        self.display_score()
        pygame.display.flip()

        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound = pygame.mixer.Sound('venv/resources/eating_sound.mp3')
            pygame.mixer.Sound.play(sound)
            self.snake.grow_snake()
            self.apple.move_apple()

        for i in range(1, self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]) or self.over_boundary(self.snake.x[0], self.snake.y[0]):
                sound = pygame.mixer.Sound('venv/resources/game_over.mp3')
                pygame.mixer.Sound.play(sound)
                raise "game over"


    def game_over(self):
        self.screen.fill((255, 255, 255))
        font = pygame.font.SysFont('calibre', 25)

        message = font.render(f'Game Over! Your final score is {self.snake.length-1}', True, (0, 0, 0))
        self.screen.blit(message, (200, 300))

        replay = font.render(f'To replay press Enter. To exit press Escape', True, (0, 0, 0))
        self.screen.blit(replay, (200, 350))

        pygame.mixer.music.pause()
        pygame.display.flip()

    def display_score(self):
        font = pygame.font.SysFont('calibre', 25)
        score = font.render(f'Score: {self.snake.length-1}', True, (255, 255, 255))
        self.screen.blit(score, (800, 10))

    def reset(self):
        self.snake = Snake(screen, 1)
        self.apple = Apple(screen)

    def run(self):
        running = True
        pause = False

        while running:

            for event in pygame.event.get():

                if event.type == KEYDOWN:

                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()

                    if not pause:

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            # self.voice()
            try:
                if not pause:
                    self.play()


            except Exception as e:
                self.game_over()
                pause = True
                self.reset()

            time.sleep(0.1)

if __name__ == "__main__":
    game = Game()
    game.run()



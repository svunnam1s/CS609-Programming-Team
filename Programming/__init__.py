import time

import pygame
import sys
# TODO bring in game components
from game.constants import Constants
from game.player import Player
from game.ball import Ball
from game.bricks import Bricks
from game.sortutil import getSortedHighScores
import csv





class Game:
    def __init__(self, playerName):
        pygame.init()
        self.pName = playerName
        self.game_over = False
        self.screen = pygame.display.set_mode((Constants._swidth, Constants._sheight))
        self.clock = pygame.time.Clock()
        self.bg_color = pygame.Color("white")
        self.font = pygame.font.Font('assets/kenney_future.ttf', 16)
        self.csvUpdate = False

        self.player = Player()

        self.ball = Ball()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player, self.ball)
        self.bricks = Bricks(self.all_sprites)

    def reset(self):
        self.game_over = False
        self.player = Player()
        self.ball = Ball()

        self.all_sprites.empty()
        self.all_sprites.add(self.player, self.ball)
        self.bricks = Bricks(self.all_sprites)


    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
        if keys[pygame.K_LEFT]:
            self.player.move_left()

        if self.game_over and keys[pygame.K_RETURN]:
            self.reset()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        if self.ball.is_off_screen():
            self.player.lose_life()
            if self.player.lives <= 0:
                self.game_over = True
            self.ball.reset()
        self.ball.check_collide_paddle(self.player)
        self.bricks.check_collision(self.ball)
        self.all_sprites.update()
        pygame.display.update()
        self.clock.tick(120)

    def draw(self):
        self.screen.fill(self.bg_color)
        highscores = getHScores()
        if self.game_over:
            self.all_sprites.empty()
            updatehighscores = _top10HighScores(highscores, self.bricks.score, self.pName)

            if not self.csvUpdate:
                writeToFile(updatehighscores)
                self.csvUpdate = True

            highscores = getSortedHighScores(updatehighscores)
            text = self.font.render("Game Over!", 1, pygame.Color("black"))
            self.screen.blit(text, (Constants._swidth / 2 - 75, Constants._sheight / 2 - 230))
            text = self.font.render("{0}  score is - {1}".format(self.pName, self.bricks.score), 1, pygame.Color("black"))
            self.screen.blit(text, (Constants._swidth / 2 - 120, Constants._sheight / 2 - 190))

            text = self.font.render("Press enter to replay the game", 1, pygame.Color("black"))
            self.screen.blit(text, (Constants._swidth / 2 - 200, (Constants._sheight / 2) - 150))

            text = self.font.render("Top 10 High Scores", 1, pygame.Color("black"))
            self.screen.blit(text, (Constants._swidth / 2 - 110, Constants._sheight / 2 - 110))
            text = self.font.render("----------------------------", 1, pygame.Color("black"))
            self.screen.blit(text, (Constants._swidth / 2 - 180, Constants._sheight / 2 - 90))

            text4 = self.font.render("|    Name    |    Score    |", 1, pygame.Color("black"))
            self.screen.blit(text4, (Constants._swidth / 2 - 80, Constants._sheight / 2 - 60))


            index = 1
            for highscore in highscores:
                _score = "|    " + highscore.strip('\n').replace("-", "    |    ") + "    |"
                _test = self.font.render(_score, 1, pygame.Color("black"))
                self.screen.blit(_test, (Constants._swidth / 2 - 80, Constants._sheight / 2 - (60 - index * 20)))
                index += 1

            self.screen.blit(text, (Constants._swidth / 2 - 180, Constants._sheight / 2 + 162))


            text = self.font.render("Press escape to quit the game", 1, pygame.Color("black"))
            self.screen.blit(text, (Constants._swidth / 2 - 160, Constants._sheight / 2 + 220))

        else:
            self.all_sprites.draw(self.screen)
            text = self.font.render("Lives {0}".format(self.player.lives), 1, pygame.Color("black"))
            self.screen.blit(text, (250, 580))

            text = self.font.render("PName - {0}".format(self.pName), 1, pygame.Color("black"))
            self.screen.blit(text, (15, 580))

            text = self.font.render("Score {0}".format(self.bricks.score), 1, pygame.Color("black"))
            self.screen.blit(text, (450, 580))

            text = self.font.render("High Score {0}".format(getHScore(highscores)), 1, pygame.Color("black"))
            self.screen.blit(text, (650, 580))

        self.all_sprites.draw(self.screen)


def _top10HighScores(highscores, currentUserScore, playerName):
    top10highscores = []

    for highscore in highscores :
        highscore = highscore.strip()
        score = highscore[:highscore.find(',')]
        player = highscore[highscore.find(',') + 1:]

        if playerName == player:
            if currentUserScore > int(score):
                _playerscore = str(currentUserScore) + "," + playerName
                top10highscores.append(_playerscore)
            else:
                top10highscores.append(highscore)
        else:
            top10highscores.append(highscore)

    return top10highscores


def getHScores():
    lines = []
    with open('scores.csv') as f:
        lines = f.readlines()

    return lines

def writeToFile(rows):
    with open('scores.csv', 'w') as f:
        for row in rows:
            f.write(row)
            f.write('\n')


def getHScore(players):
    high_score = 0
    for player in players:
        score = player[:player.find(',')]
        if int(score) > high_score:
            high_score = int(score)
    return high_score

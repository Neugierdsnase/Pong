import math
from random import uniform

import pyxel

BALL_SIZE = 2
BALL_SPEED = 2
BRICK_SIZE = 8
SCREEN_WIDTH = 255
SCREEN_HEIGHT = 120

class Vec2:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Vec2Norm:
  def __init__(self, x, y):
    self.m = math.sqrt(x * x + y * y)
    self.x = x / self.m * BALL_SPEED
    self.y = y / self.m * BALL_SPEED

class HitBox:
  def __init__(self, x1, y1, x2, y2):
    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2

class Brick:
  def __init__(self, x, y):
    self.pos = Vec2(x, y)
    self.vel = Vec2(0, 0)
    self.hitBox = HitBox(
      self.pos.x - BRICK_SIZE / 4, 
      self.pos.y - BRICK_SIZE, 
      self.pos.x + BRICK_SIZE / 4, 
      self.pos.y + BRICK_SIZE
    )

  def update(self):
    self.pos.x += self.vel.x
    self.pos.y += self.vel.y
    self.hitBox = HitBox(
      self.pos.x - BRICK_SIZE / 4, 
      self.pos.y - BRICK_SIZE, 
      self.pos.x + BRICK_SIZE / 4, 
      self.pos.y + BRICK_SIZE
    )

    if self.pos.y - BRICK_SIZE < 0:
      self.pos.y = BRICK_SIZE
      self.vel.y = 0

    if self.pos.y + BRICK_SIZE > SCREEN_HEIGHT:
      self.pos.y = SCREEN_HEIGHT - BRICK_SIZE
      self.vel.y = 0

    if pyxel.btnp(pyxel.KEY_W):
      self.vel.y = -2

    if pyxel.btnp(pyxel.KEY_S):
      self.vel.y = 2

class Ball:
  def __init__(self, px, py, vx, vy):
    self.pos = Vec2(px, py)
    self.vel = Vec2Norm(vx, vy)

  def update(self):
    self.pos.x += self.vel.x
    self.pos.y += self.vel.y

    if self.pos.y >= SCREEN_HEIGHT - BALL_SIZE:
      self.vel.y = -self.vel.y

    if self.pos.y <= BALL_SIZE:
      self.vel.y = -self.vel.y

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bricks = [
          Brick(10, BRICK_SIZE), 
          Brick(SCREEN_WIDTH - 10, BRICK_SIZE)
        ]
        self.ball = Ball(20, 20, 2, 2)
        self.score = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
          pyxel.quit()
        self.ball.update()
        for brick in self.bricks:
          brick.update()
          if (brick.hitBox.x1 < self.ball.pos.x < brick.hitBox.x2
          and brick.hitBox.y1 < self.ball.pos.y < brick.hitBox.y2):
            self.ball.vel.x = -self.ball.vel.x
            self.ball.vel.y = self.ball.vel.y + uniform(-1.1, 1.1)
            self.score += 1
        if self.ball.pos.x >= SCREEN_WIDTH - BALL_SIZE:
          pyxel.quit()
        if self.ball.pos.x <= BALL_SIZE:
          pyxel.quit()

    def draw(self):
        pyxel.cls(5)
        for brick in self.bricks:
          pyxel.rect(
            brick.hitBox.x1,
            brick.hitBox.y1,
            brick.hitBox.x2,
            brick.hitBox.y2,
            6
          )
        pyxel.circ(
          self.ball.pos.x,
          self.ball.pos.y,
          BALL_SIZE,
          7
        )
        pyxel.text(
          SCREEN_WIDTH / 2, 
          SCREEN_HEIGHT / 12,
          str(self.score), 
          6
        )

App()
import variables
from constants import *
from player import Player

JUMP_DURATION = 24


class Enemy:
    def __init__(self, image, window, time):
        self.image = image
        self.window = window
        self.jumpCount = JUMP_DURATION * 2
        self.x = 0
        self.y = 0
        self.cubeNumber = 0
        self.rowNumber = 0
        self.destroy = False
        self.time = time
        self.jumpDirection = FALLING

    def draw(self):
        pass

    def detect_collision(self, player: Player) -> bool:
        if player.jumpDirection == RIGHT_SPIN or player.jumpDirection == LEFT_SPIN or player.jumpDirection == FALLING:
            return False

        if abs(self.x - player.x) <= CUBE_SIZE // 4 and abs(self.y - player.y) <= CUBE_SIZE // 4:
            return True

        return False

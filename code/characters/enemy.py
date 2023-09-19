from constants import *
from characters.player import Player

JUMP_DURATION = 24


class Enemy:
    def __init__(self, image, time):
        self.image = image
        self.jumpCount = JUMP_DURATION * 2
        self.x = 0
        self.y = 0
        self.cubeNumber = 0
        self.rowNumber = 0
        self.destroy = False
        self.time = time
        self.jumpDirection = FALLING
        self.version = 0
    
    def __deepcopy__(self, memo):
        new_instance = self.__class__(self.image, self.time)
        
        new_instance.jumpCount = self.jumpCount
        new_instance.x = self.x
        new_instance.y = self.y
        new_instance.cubeNumber = self.cubeNumber
        new_instance.rowNumber = self.rowNumber
        new_instance.destroy = self.destroy
        new_instance.time = self.time
        new_instance.jumpDirection = self.jumpDirection
        new_instance.version = self.version

        return new_instance

    def move(self):
        pass

    def draw(self):
        pass

    def detect_collision(self, player: Player) -> bool:
        if player.jumpDirection == RIGHT_SPIN or player.jumpDirection == LEFT_SPIN or player.jumpDirection == FALLING:
            return False

        if abs(self.x - player.x) <= CUBE_SIZE // 4 and abs(self.y - player.y) <= CUBE_SIZE // 4:
            return True

        return False

from typing import Optional, List

import pygame

from constants import START, STANDING, GAME_WINDOW_WIDTH
from cube import Cube
from level import Level
from player import Player
from red_ball import RedBall

jump_direction_player = STANDING
state = START
score = 0

cubes: Optional[List[Cube]] = []
player: Optional[Player] = None
level: Optional[Level] = None
round_completed: Optional[bool] = None
level_completed: Optional[bool] = None
red_balls: Optional[List[RedBall]] = []
game_time = 0

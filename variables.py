from typing import Optional, List

import pygame

from constants import START, STANDING, GAME_WINDOW_WIDTH
from cube import Cube
from enemy import Enemy
from level import Level
from player import Player

jump_direction_player = STANDING
state = START
score = 0

cubes: Optional[List[Cube]] = []
something = 5
player: Optional[Player] = None
level: Optional[Level] = None
round_completed: Optional[bool] = None
level_completed: Optional[bool] = None
enemies: Optional[List[Enemy]] = []
game_time = 0

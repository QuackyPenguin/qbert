from typing import Optional, List

from constants import START, STANDING
from cube import Cube
from disc import Disc
from enemy import Enemy
from level import Level
from player import Player

jump_direction_player = STANDING
state = START
score = 0
speed = 35
freeze = False
freeze_timer = 0
rainbow_color = 0
celebrate = False

helpx, helpy = 0, 0

cubes: Optional[List[Cube]] = []
player: Optional[Player] = None
level: Optional[Level] = None
round_completed: Optional[bool] = None
level_completed: Optional[bool] = None
enemies: Optional[List[Enemy]] = []
discs: Optional[List[Disc]] = []
game_time = 0

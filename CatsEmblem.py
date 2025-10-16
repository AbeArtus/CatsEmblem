import random
from sys import path as syspath
syspath.insert(0, '/Games/CatsEmblem')
import thumbyGrayscale as thumby

# --- TILE DATA ---
forestTile = (bytearray([255, 255, 255, 255, 127, 255, 255, 255]), bytearray([0, 0, 96, 124, 255, 124, 96, 0]))
mountainTile = (bytearray([255, 255, 255, 255, 255, 252, 227, 31]), bytearray([192, 240, 252, 255, 255, 255, 252, 224]))
grassTile = (bytearray([255, 255, 255, 255, 255, 255, 255, 255]), bytearray([0, 64, 0, 64, 4, 0, 4, 0]))
houseTile = (bytearray([255, 255, 255, 255, 255, 255, 255, 255]), bytearray([8, 252, 142, 239, 239, 142, 252, 8]))
water = (bytearray([0, 4, 2, 4, 64, 32, 64, 0, 0, 0, 4, 66, 36, 64, 0, 0]), bytearray([0, 4, 2, 4, 64, 32, 64, 0, 0, 0, 4, 66, 36, 64, 0, 0]))
coastX = (bytearray([0, 64, 160, 0, 7, 136, 86, 239, 0, 4, 10, 0, 64, 161, 86, 239]), bytearray([0, 64, 160, 0, 7, 136, 16, 0, 0, 4, 10, 0, 64, 161, 16, 0]))
coastY = (bytearray([160, 208, 136, 16, 164, 194, 196, 160, 160, 196, 130, 68, 160, 208, 208, 160]), bytearray([32, 16, 8, 16, 36, 2, 4, 32, 32, 4, 2, 68, 32, 16, 16, 32]))
bridge = (bytearray([126, 126, 126, 126, 126, 126, 126, 126]), bytearray([193, 193, 193, 193, 193, 193, 193, 193]))
cliffT = (bytearray([254, 254, 254, 254, 254, 254, 254, 254]), bytearray([1, 1, 1, 1, 1, 1, 1, 1]))
cliffR = (bytearray([255, 255, 255, 255, 255, 255, 255, 0]), bytearray([0, 0, 0, 0, 0, 0, 0, 255]))
cliffBTLBR = (bytearray([126, 253, 251, 247, 239, 223, 191, 127]), bytearray([255, 254, 252, 248, 240, 224, 192, 128])) # bottom to left then top to right
cliffTTLBR = (bytearray([127, 191, 223, 239, 247, 251, 253, 254]), bytearray([128, 64, 32, 16, 72, 36, 66, 1])) # top to left then bottom to right
cliffStraight = (bytearray([126, 126, 126, 126, 126, 126, 126, 126]), bytearray([255, 255, 255, 255, 255, 255, 255, 255]))
coastCornerBR = (bytearray([160, 208, 160, 0, 164, 217, 194, 247, 136, 200, 128, 4, 130, 192, 194, 247]), bytearray([32, 16, 32, 0, 36, 25, 0, 0, 8, 8, 0, 4, 2, 0, 0, 0]))
stairs = (bytearray([255, 255, 255, 255, 255, 255, 255, 255]), bytearray([85, 85, 85, 85, 85, 85, 85, 85]))
shop = (bytearray([255, 255, 255, 255, 255, 255, 255, 255]), bytearray([254, 2, 5, 229, 229, 5, 2, 254]))
wallTop = (bytearray([127, 127, 127, 127, 127, 127, 127, 1]), bytearray([128, 254, 254, 254, 254, 254, 254, 254]))
wallSide = (bytearray([17, 17, 68, 68, 17, 17, 68, 68]), bytearray([85, 17, 85, 68, 85, 17, 85, 68]))
waterCliff = (bytearray([0, 1, 3, 7, 15, 31, 63, 127]), bytearray([1, 2, 4, 8, 16, 32, 64, 128]))

# --- TILE TYPES ---
TILE_GRASS = 0
TILE_FOREST = 1
TILE_MOUNTAIN = 2
TILE_HOUSE = 3
EMPTY = 4
TILE_WATER = 5
TILE_COAST_X = 6
TILE_COAST_XFLIP = 7
TILE_COASTY = 8
TILE_COASTY_YFLIP = 9
TILE_BRIDGE = 10
TILE_CLIFFBTLBR = 11
TILE_CLIFF_B_TLBR_XFLIP = 12
TILE_CLIFF_B_TLBR_YFLIP = 13
TILE_CLIFF_B_TLBR_XYFLIP = 14
TILE_CLIFF_TTLBR = 15
TILE_CLIFF_TTLBR_XFLIP = 16
TILE_CLIFF_STRAIGHT = 17
TILE_STAIRS = 18
TILE_SHOP = 19
WALL_TOP = 20
WALL_SIDE = 21
TILE_CLIFF_TOP = 22
TILE_CLIFF_TOP_YFLIP = 23
TILE_CLIFF_RIGHT = 24
TILE_CLIFF_RIGHT_XFLIP = 25
TILE_COAST_CORNER_BR = 26
TILE_COAST_CORNER_BR_XFLIP = 27
TILE_COAST_CORNER_BR_YFLIP = 28
TILE_COAST_CORNER_BR_XYFLIP = 29
TILE_WATER_CLIFF = 30
TILE_WATER_CLIFF_YFLIP = 31
TILE_WATER_CLIFF_XFLIP = 32
TILE_WATER_CLIFF_XYFLIP = 33

## Dictionary for if cat can walk on tile type
canWalkOn = {
    TILE_GRASS: True,
    TILE_FOREST: True,
    TILE_MOUNTAIN: False,
    TILE_HOUSE: True,
    EMPTY: True,
    TILE_WATER: False,
    TILE_COAST_X: False,
    TILE_COAST_XFLIP: False,
    TILE_COASTY: False,
    TILE_COASTY_YFLIP: False,
    TILE_BRIDGE: True,
    TILE_CLIFFBTLBR: False,
    TILE_CLIFF_B_TLBR_XFLIP: False,
    TILE_CLIFF_B_TLBR_YFLIP: False,
    TILE_CLIFF_B_TLBR_XYFLIP: False,
    TILE_CLIFF_TTLBR: False,
    TILE_CLIFF_TTLBR_XFLIP: False,
    TILE_CLIFF_STRAIGHT: False,
    TILE_STAIRS: True,
    TILE_SHOP: True,
    WALL_TOP: False,
    WALL_SIDE: False,
    TILE_CLIFF_TOP: True,
    TILE_CLIFF_TOP_YFLIP: True,
    TILE_CLIFF_RIGHT: True,
    TILE_CLIFF_RIGHT_XFLIP: True,
    TILE_COAST_CORNER_BR: False,
    TILE_COAST_CORNER_BR_XFLIP: False,
    TILE_COAST_CORNER_BR_YFLIP: False,
    TILE_COAST_CORNER_BR_XYFLIP: False,
}

# --- CONSTANTS ---
SCREEN_TILES_X = 9
SCREEN_TILES_Y = 5
MOVE_DELAY = 8

# --- LEVEL DATA ---
map1 = [
    [TILE_COASTY, TILE_COASTY, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER],
    [EMPTY, EMPTY, TILE_COAST_CORNER_BR_XFLIP, TILE_COASTY, TILE_COASTY, TILE_COASTY, TILE_COASTY, TILE_WATER, TILE_WATER, TILE_WATER],
    [EMPTY, TILE_HOUSE, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_COAST_CORNER_BR_XFLIP, TILE_COASTY, TILE_COASTY],
    [TILE_FOREST, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_FOREST, TILE_MOUNTAIN],
    [TILE_MOUNTAIN, TILE_GRASS, TILE_FOREST, TILE_GRASS, EMPTY, TILE_GRASS, TILE_FOREST, EMPTY, TILE_MOUNTAIN, TILE_MOUNTAIN],
    [WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, EMPTY, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP],
    [WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_SIDE, EMPTY, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_SIDE],
    [TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_GRASS, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, TILE_FOREST, TILE_MOUNTAIN, TILE_MOUNTAIN],
    [TILE_MOUNTAIN, TILE_FOREST, TILE_GRASS, TILE_GRASS, EMPTY, TILE_GRASS, TILE_GRASS, EMPTY, TILE_FOREST, TILE_MOUNTAIN],
    [TILE_MOUNTAIN, EMPTY, TILE_GRASS, EMPTY, EMPTY, TILE_FOREST, EMPTY, EMPTY, TILE_FOREST, TILE_MOUNTAIN],
    [TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_FOREST, EMPTY, TILE_GRASS, TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, TILE_MOUNTAIN],
    [TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_GRASS, EMPTY, EMPTY, TILE_GRASS, TILE_FOREST, EMPTY, EMPTY, TILE_MOUNTAIN],
    [TILE_MOUNTAIN, TILE_FOREST, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, EMPTY, TILE_FOREST],
    [TILE_MOUNTAIN, TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, EMPTY, TILE_FOREST, TILE_GRASS, EMPTY, TILE_FOREST],
    [TILE_FOREST, TILE_FOREST, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, TILE_FOREST, TILE_FOREST]
]

map2 = [
    [TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_COASTY, TILE_COASTY, TILE_COASTY, TILE_COASTY, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER],
    [TILE_WATER_CLIFF_YFLIP, TILE_CLIFF_TOP, TILE_CLIFF_TOP, TILE_CLIFF_TOP, TILE_CLIFF_TOP, TILE_HOUSE, TILE_SHOP, TILE_CLIFF_TOP, TILE_WATER_CLIFF_XYFLIP, TILE_WATER, TILE_WATER, TILE_COAST_X, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_GRASS, TILE_GRASS, TILE_COAST_CORNER_BR_XFLIP, TILE_WATER, TILE_WATER, TILE_WATER],
    [TILE_GRASS, TILE_FOREST, TILE_MOUNTAIN, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_FOREST, WALL_TOP, TILE_WATER, TILE_COAST_X, TILE_MOUNTAIN, TILE_GRASS, TILE_GRASS, TILE_FOREST, TILE_FOREST, TILE_COAST_CORNER_BR_XFLIP, TILE_WATER, TILE_WATER],
    [WALL_TOP, WALL_TOP, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_TOP, WALL_TOP, WALL_TOP, WALL_SIDE, TILE_WATER, TILE_COAST_X, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_FOREST, TILE_FOREST, TILE_WATER],
    [WALL_SIDE, WALL_SIDE, WALL_SIDE, TILE_STAIRS, TILE_STAIRS, TILE_STAIRS, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_SIDE, TILE_WATER, TILE_COAST_X, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, EMPTY, EMPTY, TILE_COAST_XFLIP],
    [WALL_SIDE, WALL_SIDE, WALL_SIDE, TILE_STAIRS, TILE_STAIRS, TILE_STAIRS, WALL_SIDE, WALL_SIDE, WALL_SIDE, TILE_WATER, TILE_WATER, TILE_COAST_CORNER_BR, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_COAST_XFLIP],
    [TILE_COAST_X, TILE_GRASS, TILE_FOREST, TILE_GRASS, EMPTY, EMPTY, TILE_FOREST, EMPTY, EMPTY, TILE_COAST_XFLIP, TILE_COAST_X, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_COAST_XFLIP],
    [TILE_COAST_X, TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_BRIDGE, TILE_BRIDGE, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_COAST_XFLIP],
    [TILE_COAST_X, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, TILE_COAST_XFLIP, TILE_COAST_X, EMPTY, WALL_TOP, WALL_TOP, EMPTY, EMPTY, WALL_TOP, WALL_TOP, WALL_TOP, TILE_COAST_XFLIP],
    [TILE_COAST_X, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, TILE_FOREST, TILE_FOREST, TILE_COAST_CORNER_BR_XFLIP, TILE_WATER, TILE_COAST_X, WALL_SIDE, WALL_SIDE, EMPTY, EMPTY, WALL_SIDE, WALL_SIDE, WALL_SIDE, TILE_COAST_XFLIP],
    [TILE_WATER, TILE_COAST_CORNER_BR_YFLIP, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_COAST_XFLIP, TILE_COAST_X, EMPTY, TILE_FOREST, EMPTY, EMPTY, TILE_FOREST, EMPTY, EMPTY, TILE_COAST_XFLIP],
    [TILE_WATER, TILE_COAST_X, TILE_MOUNTAIN, TILE_GRASS, TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, TILE_COAST_XFLIP, TILE_WATER, TILE_COAST_CORNER_BR_YFLIP, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_MOUNTAIN, TILE_COAST_XFLIP],
    [TILE_WATER, TILE_WATER, TILE_COAST_CORNER_BR_YFLIP, TILE_MOUNTAIN, TILE_GRASS, TILE_FOREST, EMPTY, EMPTY, TILE_GRASS, TILE_MOUNTAIN, TILE_COAST_XFLIP, TILE_WATER, TILE_COAST_X, EMPTY, EMPTY, EMPTY, EMPTY, TILE_MOUNTAIN, TILE_COAST_CORNER_BR_XYFLIP, TILE_WATER],
    [TILE_WATER, TILE_WATER, TILE_WATER, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_WATER, TILE_WATER, TILE_COAST_X, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_COAST_XFLIP, TILE_WATER],
    [TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_WATER, TILE_WATER]
]

# --- CLASSES ---
class Stats:
    def __init__(
            self,
            attack: int,
            defense: int,
            max_hp: int,
            speed: int,
            luck: int,
            range: int
        ):
        self.attack = attack
        self.defense = defense
        self.max_hp = max_hp
        self.speed = speed
        self.luck = luck
        self.range = range

## growth rates for leveling up 1-100 for each stat
class GrowthRates:
    def __init__(
            self,
            attack: int=50,
            defense: int=50,
            max_hp: int=50,
            speed: int=50,
            luck: int=50,
            range: int=50
        ):
        self.attack = attack
        self.defense = defense
        self.max_hp = max_hp
        self.speed = speed
        self.luck = luck
        self.range = range

class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Position) and self.x == other.x and self.y == other.y

class Cat:
    _id_counter = 0  # Class variable for unique IDs
    def __init__(
            self,
            sprite: thumby.Sprite,
            position: Position,
            name: str,
            selected: bool=False,
            exhausted: bool=False,
            stats: Stats=Stats(attack=5, defense=5, max_hp=10, speed=5, luck=5, range=3),
            growthRates: GrowthRates=GrowthRates(),
            enemy: bool=False,
            exp: int=0,
            level: int=1,
            next_level_exp: int=10,
            aiType: str='stand' or 'searchAndDestroy'
        ):
        self.id = f"cat_{Cat._id_counter}"  # Generate a sequential ID
        Cat._id_counter += 1
        self.sprite: thumby.Sprite = sprite
        self.position: Position = position
        self.selected: bool = selected
        self.exhausted: bool = exhausted
        self.name: str = name
        self.stats: Stats = stats
        self.growthRates: GrowthRates = growthRates if growthRates else GrowthRates() 
        self.enemy: bool = enemy
        self.hp: bool = self.stats.max_hp  # Initialize HP to max_hp
        self.exp: int = exp + 10**(level - 1)
        self.moved = False
        self.level: int = level
        self.next_level_exp: int = next_level_exp
        self.aiType: str = aiType  # 'stand' or 'searchAndDestroy'

    def set_position(self, position: Position):
        self.position = position
    
    def set_exhausted(self, exhausted):
        self.exhausted = exhausted
    
    def set_selected(self, selected):
        self.selected = selected
    
    def set_enemy(self, enemy):
        self.enemy = enemy

    def set_sprite_position(self, position):
        self.sprite.x = position.x
        self.sprite.y = position.y
    
    def set_hp(self, new_hp):
        self.hp = min(new_hp, self.stats.max_hp)

    def advance_animation(self):
        curFrame = self.sprite.getFrame()
        nextFrame = (curFrame + 1) % self.sprite.frameCount
        self.sprite.setFrame(nextFrame)

    def add_exp(self, amount):
        self.exp += amount
        if self.exp >= self.next_level_exp:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.next_level_exp += int(self.next_level_exp * 1.5)

        RN = random.randint(1, 100)
        CF = random.randint(1, 100)
        for stat in ['attack', 'defense', 'max_hp', 'speed', 'luck', 'range']:
            RN = (RN + CF) % 100
            CF = (CF + RN) % 100
            if RN <= getattr(self.growthRates, stat):
                setattr(self.stats, stat, getattr(self.stats, stat) + 1)
                if CF < (getattr(self.growthRates, stat) + self.stats.luck):
                    setattr(self.stats, stat, getattr(self.stats, stat) + 1)
             
class LevelUpLog:
    def __init__(
            self,
            catName: str,
            catSprite: thumby.Sprite,
            newLevel: int,
            stats: Stats,
        ):
        self.catName = catName
        self.catSprite = catSprite
        self.newLevel = newLevel
        self.stats = stats

class AttackLog:
    def __init__(
            self,
            attacker_name: str,
            attacker_hp: int,
            attacker_enemy: bool,
            attacker_sprite: thumby.Sprite,
            defender_name: str,
            defender_hp: int,
            defender_enemy: bool,
            defender_sprite: thumby.Sprite,
            damage: int,
            old_hp: int,
            new_hp: int,
            text: str,
        ):
        self.attacker_name = attacker_name
        self.attacker_hp = attacker_hp
        self.attacker_enemy = attacker_enemy
        self.attacker_sprite = attacker_sprite
        self.defender_name = defender_name
        self.defender_hp = defender_hp
        self.defender_enemy = defender_enemy
        self.defender_sprite = defender_sprite
        self.damage = damage
        self.old_hp = old_hp
        self.new_hp = new_hp
        self.text = text

class Level:
    def __init__(
            self,
            map,
            enemies,
            number,
            seizePosition=Position(1, 1),
            startingPositions=[]
        ):
        self.map = map
        self.enemies = enemies
        self.viewport = Position()
        self.selectorPosition = Position()
        self.number = number
        self.seizePosition = seizePosition
        self.startingPositions = startingPositions

class GameState:
    def __init__(
            self,
            level,
            party: list[Cat],
            state='title',
        ):
        self.level: Level = level
        for i, p in enumerate(party):
            p.set_position(level.startingPositions[i])
        self.party = party
        self.current_turn: str = 'player'
        self.combat_log = []
        self.state = state

    def load_level(self, level: Level):
        for i, p in enumerate(self.party):
            p.set_position(level.startingPositions[i])
            p.set_exhausted(False)
            p.set_selected(False)
            p.moved = False
            p.set_hp(p.stats.max_hp)
        self.level = level
        self.selectorPosition = Position(self.party[0].position.x, self.party[0].position.y)
        needsUpdate = True

# --- GAME STATE ---
frame = 0
selectedCatId = None
activeEnemy = None
readyForBattle = False
needsUpdate = False
lastPos = Position()
option = 0
current_hp_display = -1

# --- SPRITES ---
selector_sprite = thumby.Sprite(8, 8, (bytearray([255, 255, 255, 255, 255, 255, 255, 255, 24, 126, 126, 255, 255, 126, 126, 24, 28, 126, 127, 255, 255, 254, 126, 56]), bytearray([199, 129, 1, 0, 0, 128, 129, 227, 0, 0, 0, 0, 0, 0, 0, 0, 227, 129, 128, 0, 0, 1, 129, 199])), 32, 16, key=1)
def cat_sprite(): return thumby.Sprite(8, 8, (bytearray([0, 207, 15, 15, 192, 5, 241, 244, 6, 201, 15, 15, 192, 5, 241, 244, 7, 201, 14, 15, 192, 5, 241, 244, 1, 206, 15, 15, 192, 5, 241, 244])), 32, 16, key=1)
def enemy_sprite(): return thumby.Sprite(8, 8, (bytearray([3, 143, 2, 4, 129, 1, 228, 242, 3, 143, 2, 4, 145, 17, 196, 242, 7, 139, 2, 4, 129, 1, 228, 242]), bytearray([252, 112, 253, 251, 118, 246, 27, 13, 252, 112, 253, 251, 102, 230, 59, 13, 248, 116, 253, 251, 118, 246, 27, 13])), 32, 16, key=1)

# --- UNITS ---
catSprite = cat_sprite()
cat = Cat(catSprite, Position(2, 4), 'cat', False, False, Stats(attack=5, defense=3, max_hp=10, speed=8, luck=4, range=4), None, False)
tacSprite = cat_sprite()
tac = Cat(tacSprite, Position(2, 5), 'tac', False, False, Stats(attack=4, defense=4, max_hp=8, speed=8, luck=4, range=6), None, False)

def get_stats_for_level(level: int):
    return Stats(
        attack=3 + level,
        defense=2 + level,
        max_hp=7 + level,
        speed=2 + level,
        luck=1 + level,
        range=3
    )

def generate_enemy(level: int, position: Position, ai = 'searchAndDestroy', name = 'enemy'):
    enemySprite = enemy_sprite()
    return Cat(
        enemySprite,
        position,
        name,
        False,
        False,
        get_stats_for_level(level),
        None,
        True,
        level,
        aiType=ai
    )


# --- LEVELS ---
level1 = Level(
    map1, 
    [
        generate_enemy(1, Position(4, 4), name='bork'),
        generate_enemy(1, Position(6, 4), name='bark'),
        generate_enemy(1, Position(1, 2), ai='stand', name='sean')
    ], 
    1, 
    Position(1, 2),
    [Position(5,14), Position(4,14)]
)
level2 = Level(
    map2, 
    [
        generate_enemy(2, Position(10, 7), name ='jr'),
        generate_enemy(1, Position(4, 6), name='mini'),
        generate_enemy(2, Position(5, 1), 'stand', name='xl')
    ],
    2,
    Position(5, 1), 
    [Position(16, 13), Position(17, 13)]
)

## --- INITIALIZE GAME STATE ---
gameState = GameState(level1, [cat, tac])

# --- FUNCTIONS ---
def get_selected_cat():
    for c in gameState.party:
        if c.id == selectedCatId:
            return c
    return None

def find_valid_positions(cat: Cat, gameState: GameState):
    def is_walkable(position):
        # Check if the position is within bounds
        if not (0 <= position.x < len(gameState.level.map[0]) and 0 <= position.y < len(gameState.level.map)):
            return False
        # Check if the tile is walkable
        tile = gameState.level.map[position.y][position.x]
        if tile not in canWalkOn or not canWalkOn[tile]:
            return False
        return True

    def is_occupied(position):
        # Check if the position is occupied by a party member or enemy
        if cat.enemy:
            # Enemies cannot pass through party members
            return any(p.position == position for p in gameState.party)
        else:
            # Party members cannot pass through enemies
            return any(e.position == position for e in gameState.level.enemies)

    # DFS implementation
    def dfs(current_pos, remaining_range, visited: list):
        # Base case: Out of range or already visited
        if remaining_range < 0 or current_pos in visited:
            return

        # Check if the current position is walkable and not occupied
        if not is_walkable(current_pos) or is_occupied(current_pos):
            return

        # Mark the current position as visited
        visited.append(current_pos)

        # Explore neighbors (up, down, left, right)
        neighbors = [
            Position(current_pos.x + 1, current_pos.y),
            Position(current_pos.x - 1, current_pos.y),
            Position(current_pos.x, current_pos.y + 1),
            Position(current_pos.x, current_pos.y - 1),
        ]
        for neighbor in neighbors:
            dfs(neighbor, remaining_range - 1, visited)

    # Initialize DFS
    visited: list[Position] = []
    dfs(cat.position, cat.stats.range + 1, visited)

    # Return the list of valid positions
    return visited

def can_attack():
    cat = get_selected_cat()
    if not cat:
        return False
    if cat.exhausted:
        return False
    for enemy in gameState.level.enemies:
        dx = abs(enemy.position.x - cat.position.x)
        dy = abs(enemy.position.y - cat.position.y)
        if dx + dy <= 1:
            return True
    return False

def battle(attacker: Cat, defender: Cat):
    global gameState

    attackerExp = 0
    defenderExp = 0
    
    # Record all attacks in the log
    attackerExp =+ record_attack(attacker, defender)
    if defender.hp <= 0:
        attacker.add_exp(defender.stats.max_hp)
        return
    
    defenderExp += record_attack(defender, attacker)
    if attacker.hp <= 0:
        defender.add_exp(attacker.stats.max_hp)
        return

    if attacker.stats.speed * int(1.5 > defender.stats.speed):
        attackerExp += record_attack(attacker, defender)
    if defender.hp <= 0:
        attacker.add_exp(defender.stats.max_hp)
        return

    if defender.stats.speed * int(1.5 > attacker.stats.speed):
         attackerExp += record_attack(defender, attacker)
    if attacker.hp <= 0:
        defender.add_exp(attacker.stats.max_hp)
        return

    defender.add_exp(defenderExp)
    attacker.add_exp(attackerExp)
    
def record_attack(attacker: Cat, defender: Cat):
    global gameState

    damage = calculate_damage(attacker, defender)
    old_hp = defender.hp
    new_hp = old_hp - damage

    log = AttackLog(
        attacker_name=attacker.name,
        attacker_hp=attacker.hp,
        attacker_enemy=attacker.enemy,
        attacker_sprite=attacker.sprite,    
        defender_name=defender.name,
        defender_hp=defender.hp,
        defender_enemy=defender.enemy,
        defender_sprite=defender.sprite,
        damage=damage,
        old_hp=old_hp,
        new_hp=new_hp,
        text=f"{attacker.name} attacks {defender.name} for {damage} damage!"
    )

    gameState.combat_log.append(log)
    
    defender.set_hp(new_hp)
    
    if defender.hp <= 0:
        if defender in gameState.level.enemies:
            gameState.level.enemies.remove(defender)
        if defender in gameState.party:
            gameState.party.remove(defender)
    
    if attacker.hp <= 0:
        if attacker in gameState.level.enemies:
            gameState.level.enemies.remove(attacker)
        if attacker in gameState.party:
            gameState.party.remove(attacker)

    return damage

def calculate_damage(attacker, defender):
    import random
    
    # Base damage calculation
    base_damage = attacker.stats.attack - defender.stats.defense
    if base_damage < 1:
        base_damage = 1  # Minimum 1 damage
    
    # Critical hit calculation
    crit_chance = (attacker.stats.luck + attacker.stats.speed) / 20.0  # 0-1 range
    if random.random() < crit_chance:
        base_damage = int(base_damage * 1.25)  # 25% crit bonus
    
    return base_damage

def update_selector_position(x, y, level):
    new_x = max(0, min(len(level[0]) - 1, x))
    new_y = max(0, min(len(level) - 1, y))

    selCat = get_selected_cat()
    if selCat:
        if abs(new_x - selCat.position.x) + abs(new_y - selCat.position.y) > selCat.stats.range:
            return

    gameState.level.selectorPosition.x = new_x
    gameState.level.selectorPosition.y = new_y

    # Center the viewport around the selector
    center_x = SCREEN_TILES_X // 2  # Center x position (4 for 9 tiles wide)
    center_y = SCREEN_TILES_Y // 2  # Center y position (2 for 5 tiles high)

    # Calculate the new viewport position to center the selector
    viewport_x = max(0, min(len(level[0]) - SCREEN_TILES_X, new_x - center_x))
    viewport_y = max(0, min(len(level) - SCREEN_TILES_Y, new_y - center_y))

    gameState.level.viewport.x = viewport_x
    gameState.level.viewport.y = viewport_y

def handle_movement():
    global needsUpdate, gameState
    
    # Handle immediate button presses
    x = gameState.level.selectorPosition.x
    y = gameState.level.selectorPosition.y
    isCatSelected = selectedCatId is not None

    directions = {
        "L": (-1, 0),
        "R": (1, 0),
        "U": (0, -1),
        "D": (0, 1)
    }

    for button, (dx, dy) in directions.items():
        if getattr(thumby, f"button{button}").justPressed():
            new_x, new_y = x + dx, y + dy
            if 0 <= new_y < len(gameState.level.map) and 0 <= new_x < len(gameState.level.map[0]):
                isWalkable = gameState.level.map[new_y][new_x] in canWalkOn and canWalkOn[gameState.level.map[new_y][new_x]]
            else:
                isWalkable = False
            for unit in gameState.level.enemies:
                if isCatSelected and unit.id == selectedCatId:
                    continue
                elif unit.position.x == new_x and unit.position.y == new_y:
                    isWalkable = False
                    break
            canUpdate = isWalkable or selectedCatId is None
            update_selector_position(x + (dx if canUpdate else 0), y + (dy if canUpdate else 0), gameState.level.map)
            needsUpdate = True
            return True
    
    for button, (dx, dy) in directions.items():
        if getattr(thumby, f"button{button}").pressed():
            new_x, new_y = x + dx, y + dy
            if 0 <= new_y < len(gameState.level.map) and 0 <= new_x < len(gameState.level.map[0]):
                isWalkable = gameState.level.map[new_y][new_x] in canWalkOn and canWalkOn[gameState.level.map[new_y][new_x]]
            else:
                isWalkable = False
            # Check if the tile is occupied by another unit
            for unit in gameState.level.enemies + gameState.party:
                if isCatSelected and unit.id == selectedCatId:
                    continue
                elif unit.position.x == new_x and unit.position.y == new_y:
                    isWalkable = False
                    break
            canUpdate = isWalkable or selectedCatId is None
            update_selector_position(x + (dx if canUpdate else 0), y + (dy if canUpdate else 0), gameState.level.map)
            needsUpdate = True
            return True
    return False

def render_map(level):
    global gameState
    thumby.display.fill(thumby.display.WHITE)

    # TODO adjust viewport to keep selector in view can be more that 1 tile away !!!
    
    # Render tiles
    for y in range(SCREEN_TILES_Y):
        for x in range(SCREEN_TILES_X):
            map_x = gameState.level.viewport.x + x
            map_y = gameState.level.viewport.y + y
            if 0 <= map_x < len(level[0]) and 0 <= map_y < len(level):
                tile_type = level[map_y][map_x]
                if tile_type == TILE_GRASS:
                    yEven = (map_y & 1) == 0
                    sprite = thumby.Sprite(8, 8, grassTile, x * 8, y * 8, -1, yEven)
                elif tile_type == TILE_FOREST:
                    xEven = (map_x & 1) == 0
                    yEven = (map_y & 1) == 0
                    shouldFlip = (xEven and not yEven) or (not xEven and yEven)
                    sprite = thumby.Sprite(8, 8, forestTile, x * 8, y * 8, -1, shouldFlip)
                elif tile_type == TILE_MOUNTAIN:
                    sprite = thumby.Sprite(8, 8, mountainTile, x * 8, y * 8)
                elif tile_type == TILE_HOUSE:
                    sprite = thumby.Sprite(8, 8, houseTile, x * 8, y * 8)
                elif tile_type == TILE_WATER:
                    sprite = thumby.Sprite(8, 8, water, x * 8, y * 8)
                elif tile_type == TILE_COAST_X:
                    sprite = thumby.Sprite(8, 8, coastX, x * 8, y * 8)
                elif tile_type == TILE_COAST_XFLIP:
                    sprite = thumby.Sprite(8, 8, coastX, x * 8, y * 8, -1, True)
                elif tile_type == TILE_COASTY:
                    sprite = thumby.Sprite(8, 8, coastY, x * 8, y * 8)
                elif tile_type == TILE_COASTY_YFLIP:
                    sprite = thumby.Sprite(8, 8, coastY, x * 8, y * 8, -1, False, True)
                elif tile_type == TILE_BRIDGE:
                    sprite = thumby.Sprite(8, 8, bridge, x * 8, y * 8)
                elif tile_type == TILE_CLIFFBTLBR:
                    sprite = thumby.Sprite(8, 8, cliffBTLBR, x * 8, y * 8)
                elif tile_type == TILE_CLIFF_B_TLBR_XFLIP:
                    sprite = thumby.Sprite(8, 8, cliffBTLBR, x * 8, y * 8, -1, True)
                elif tile_type == TILE_CLIFF_B_TLBR_YFLIP:
                    sprite = thumby.Sprite(8, 8, cliffBTLBR, x * 8, y * 8, -1, False, True)
                elif tile_type == TILE_CLIFF_B_TLBR_XYFLIP:
                    sprite = thumby.Sprite(8, 8, cliffBTLBR, x * 8, y * 8, -1, True, True)
                elif tile_type == TILE_CLIFF_TTLBR:
                    sprite = thumby.Sprite(8, 8, cliffTTLBR, x * 8, y * 8)
                elif tile_type == TILE_CLIFF_TTLBR_XFLIP:
                    sprite = thumby.Sprite(8, 8, cliffTTLBR, x * 8, y * 8, -1, True)
                elif tile_type == TILE_CLIFF_STRAIGHT:
                    sprite = thumby.Sprite(8, 8, cliffStraight, x * 8, y * 8)
                elif tile_type == TILE_STAIRS:
                    sprite = thumby.Sprite(8, 8, stairs, x * 8, y * 8)
                elif tile_type == TILE_SHOP:
                    sprite = thumby.Sprite(8, 8, shop, x * 8, y * 8)
                elif tile_type == WALL_TOP:
                    sprite = thumby.Sprite(8, 8, wallTop, x * 8, y * 8)
                elif tile_type == WALL_SIDE:
                    sprite = thumby.Sprite(8, 8, wallSide, x * 8, y * 8)
                elif tile_type == TILE_CLIFF_TOP:
                    sprite = thumby.Sprite(8, 8, cliffT, x * 8, y * 8)
                elif tile_type == TILE_CLIFF_TOP_YFLIP:
                    sprite = thumby.Sprite(8, 8, cliffT, x * 8, y * 8, -1, False, True)
                elif tile_type == TILE_CLIFF_RIGHT:
                    sprite = thumby.Sprite(8, 8, cliffR, x * 8, y * 8)
                elif tile_type == TILE_CLIFF_RIGHT_XFLIP:
                    sprite = thumby.Sprite(8, 8, cliffR, x * 8, y * 8, -1, True)
                elif tile_type == TILE_COAST_CORNER_BR:
                    sprite = thumby.Sprite(8, 8, coastCornerBR, x * 8, y * 8)
                elif tile_type == TILE_COAST_CORNER_BR_XFLIP:
                    sprite = thumby.Sprite(8, 8, coastCornerBR, x * 8, y * 8, -1, True)
                elif tile_type == TILE_COAST_CORNER_BR_YFLIP:
                    sprite = thumby.Sprite(8, 8, coastCornerBR, x * 8, y * 8, -1, False, True)
                elif tile_type == TILE_COAST_CORNER_BR_XYFLIP:
                    sprite = thumby.Sprite(8, 8, coastCornerBR, x * 8, y * 8, -1, True, True)
                elif tile_type == TILE_WATER_CLIFF:
                    sprite = thumby.Sprite(8, 8, waterCliff, x * 8, y * 8)
                elif tile_type == TILE_WATER_CLIFF_YFLIP:
                    sprite = thumby.Sprite(8, 8, waterCliff, x * 8, y * 8, -1, False, True)
                elif tile_type == TILE_WATER_CLIFF_XFLIP:
                    sprite = thumby.Sprite(8, 8, waterCliff, x * 8, y * 8, -1, True)
                elif tile_type == TILE_WATER_CLIFF_XYFLIP:
                    sprite = thumby.Sprite(8, 8, waterCliff, x * 8, y * 8, -1, True, True)
                else:
                    continue
                sprite.setFrame((frame // 10) % sprite.frameCount)
                thumby.display.drawSprite(sprite)

    for unit in gameState.party + gameState.level.enemies:
        if (gameState.level.viewport.x <= unit.position.x < gameState.level.viewport.x + SCREEN_TILES_X and 
            gameState.level.viewport.y <= unit.position.y < gameState.level.viewport.y + SCREEN_TILES_Y):
            unit_screen_x = (unit.position.x - gameState.level.viewport.x) * 8
            unit_screen_y = (unit.position.y - gameState.level.viewport.y) * 8
            unit.set_sprite_position(Position(unit_screen_x, unit_screen_y))
            thumby.display.drawSprite(unit.sprite)

    # Render selector
    selector_sprite.x = (gameState.level.selectorPosition.x - gameState.level.viewport.x) * 8
    selector_sprite.y = (gameState.level.selectorPosition.y - gameState.level.viewport.y) * 8
    thumby.display.drawSprite(selector_sprite)

def animate_cats():
    global needsUpdate, gameState
    for c in gameState.party + gameState.level.enemies:
        c.advance_animation()
    ## now re-render all the cats
    selector_sprite.setFrame((selector_sprite.getFrame() + 1) % selector_sprite.frameCount)
    needsUpdate = True

def get_attack_tile(cat: Cat):
    global gameState

    enemy_range = (cat.stats.range + 1) if cat.aiType == "searchAndDestroy" else 1
    domain = find_valid_positions(cat, gameState)
    closest_tile = None
    target = None

    for p in gameState.party:
        dx = abs(p.position.x - cat.position.x)
        dy = abs(p.position.y - cat.position.y)
        keyTiles = [
                Position(p.position.x + 1, p.position.y),
                Position(p.position.x - 1, p.position.y),
                Position(p.position.x, p.position.y + 1),
                Position(p.position.x, p.position.y - + 1),
            ]
        if dx + dy <= enemy_range and [t for t in keyTiles if t in domain]:
            target = p
            ## filter keyTiles to only those in domain
            filtered = [t for t in keyTiles if t in domain]
            for t in filtered:
                if closest_tile is None:
                    closest_tile = t
                else:
                    current_dx = abs(t.x - cat.position.x)
                    current_dy = abs(t.y - cat.position.y)
                    closest_dx = abs(closest_tile.x - cat.position.x)
                    closest_dy = abs(closest_tile.y - cat.position.y)
                    if current_dx + current_dy < closest_dx + closest_dy:
                        closest_tile = t
                        target = p
    return closest_tile, target


# --- MAIN LOOP ---
thumby.display.setFPS(8)
while True:
    frame += 1

    partyFullyExhausted = True
    for p in gameState.party:
        if not p.exhausted:
            partyFullyExhausted = False
    if partyFullyExhausted:
        gameState.state = 'enemy-turn'
    if len(gameState.party) == 0:
        gameState.state = 'game-over'
    if (frame % 5 == 0): animate_cats()

    if needsUpdate:
        render_map(gameState.level.map)
        needsUpdate = False

    if len(gameState.combat_log) > 0:
        thumby.display.fill(thumby.display.WHITE)
        if (current_hp_display == - 1):
            current_hp_display = gameState.combat_log[0].defender_hp
        log = gameState.combat_log[0]
        attackerHealth = log.attacker_hp
        defenderHealth = current_hp_display

        # Display based on who is attacking
        if log.attacker_enemy:
            # Enemy is attacking (right side)
            thumby.display.drawText(log.attacker_name, 40, 24, thumby.display.BLACK)
            thumby.display.drawText(f"HP:{attackerHealth}", 40, 32, thumby.display.BLACK)
            thumby.display.drawText(log.defender_name, 2, 24, thumby.display.DARKGRAY)
            thumby.display.drawText(f"HP:{defenderHealth}", 2, 32, thumby.display.DARKGRAY)
            # render the cats
            log.attacker_sprite.x = 52
            log.attacker_sprite.y = 8
            thumby.display.drawSprite(log.attacker_sprite)
            log.defender_sprite.x = 12
            log.defender_sprite.y = 8
            thumby.display.drawSprite(log.defender_sprite)
        else:
            # Party is attacking (right side)
            thumby.display.drawText(log.attacker_name, 2, 24, thumby.display.BLACK)
            thumby.display.drawText(f"HP:{attackerHealth}", 2, 32, thumby.display.BLACK)
            thumby.display.drawText(log.defender_name, 40, 24, thumby.display.DARKGRAY)
            thumby.display.drawText(f"HP:{defenderHealth}", 40, 32, thumby.display.DARKGRAY)
            # render the cats
            log.attacker_sprite.x = 12
            log.attacker_sprite.y = 8
            thumby.display.drawSprite(log.attacker_sprite)
            log.defender_sprite.x = 52
            log.defender_sprite.y = 8
            thumby.display.drawSprite(log.defender_sprite)

        if current_hp_display <= gameState.combat_log[0].new_hp or current_hp_display <= 0:
            gameState.combat_log.pop(0)
            if len(gameState.combat_log) > 0:
                current_hp_display = gameState.combat_log[0].old_hp
        # Animate HP counting down
        elif (frame % 7 == 1): 
            current_hp_display = current_hp_display - 1
        if len(gameState.combat_log) == 0:
            needsUpdate = True
            current_hp_display = -1

    elif gameState.state == 'title':
        thumby.display.fill(thumby.display.WHITE)
        thumby.display.drawText("Cats Emblem", 3, 24, thumby.display.BLACK)
        title_cat = thumby.Sprite(8, 8, (bytearray([0, 207, 15, 15, 192, 5, 241, 244]), bytearray([0, 0, 0, 0, 0, 0, 0, 0])), 32, 8, key=1)
        thumby.display.drawSprite(title_cat)
        if thumby.buttonA.justPressed():
            gameState.state = 'map'
            needsUpdate = True

    elif gameState.state == 'map':
        # Handle movement
        handle_movement()
        
        # Handle selection
        if thumby.buttonA.justPressed():
            cat_here = None
            for c in gameState.party:
                if c.position == gameState.level.selectorPosition:
                    cat_here = c
                    break
            if cat_here:
                selectedCatId = cat_here.id
                if cat_here.exhausted:
                    gameState.state = 'unitSelect'  # View stats for exhausted cats
                else:
                    cat_here.set_selected(True)
                    lastPos = Position(gameState.level.selectorPosition.x, gameState.level.selectorPosition.y)
                    gameState.state = 'unitSelect'
                needsUpdate = True
            elif selectedCatId != None:
                cat = get_selected_cat()
                if cat:
                    cat.set_position(Position(gameState.level.selectorPosition.x, gameState.level.selectorPosition.y))
                    cat.moved = True
                    gameState.state = 'unitSelect'
                    needsUpdate = True
            else:
                # Check if an enemy is selected
                gameState.state = 'unitSelect'
                needsUpdate = True
                for enemy in gameState.level.enemies:
                    if enemy.position == gameState.level.selectorPosition:
                        selectedCatId = enemy.id
                        gameState.state = 'view-stats'

        if needsUpdate:
            render_map(gameState.level.map)
            needsUpdate = False

    elif gameState.state == 'unitSelect':
        actions = [
            {"label": "Seize", "action": lambda: seize_action(), "condition": lambda: get_selected_cat() and get_selected_cat().position == gameState.level.seizePosition},
            {"label": "Move", "action": lambda: move_action(), "condition": lambda: get_selected_cat() and not get_selected_cat().moved},
            {"label": "Wait", "action": lambda: wait_action(), "condition": lambda: selectedCatId is not None and not get_selected_cat().exhausted and not get_selected_cat().enemy},
            {"label": "Fight", "action": lambda: fight_action(), "condition": lambda: can_attack()},
            {"label": "Stats", "action": lambda: stats_action(), "condition": lambda: selectedCatId is not None},
            {"label": "End Turn", "action": lambda: end_turn_action(), "condition": lambda: True},  # Always available
        ]

        # Filter actions based on their conditions
        visible_actions = [action for action in actions if action["condition"]()]
        thumby.display.fill(thumby.display.WHITE)

        # Render the list of actions
        curY = 0
        for i, action in enumerate(visible_actions):
            selected = thumby.display.LIGHTGRAY if i == option and frame & 1 else thumby.display.BLACK
            thumby.display.drawText(action["label"], 2, curY, selected if i == option else thumby.display.DARKGRAY)
            curY += 8

        # Handle input for navigating the list
        if thumby.buttonU.justPressed() and option > 0:
            option -= 1
        if thumby.buttonD.justPressed() and option < len(visible_actions) - 1:
            option += 1

        # Handle input for selecting an action
        if thumby.buttonA.justPressed():
            visible_actions[option]["action"]() 
            option = 0  # Reset option after action

        # Handle input for canceling
        if thumby.buttonB.justPressed():
            cat = get_selected_cat()
            if cat:
                cat.set_selected(False)
                if cat.moved and not cat.exhausted:
                    cat.moved = False
                    cat.set_position(lastPos)
                    gameState.level.selectorPosition = Position(lastPos.x, lastPos.y)
            selectedCatId = None
            lastPos = Position()
            gameState.state = 'map'
            option = 0
            needsUpdate = True

        # Define the action functions
        def move_action():
            global gameState, needsUpdate
            gameState.state = 'map'
            needsUpdate = True

        def stats_action():
            global gameState, needsUpdate
            gameState.state = 'view-stats'
            needsUpdate = True

        def wait_action():
            cat = get_selected_cat()
            if cat:
                cat.set_exhausted(True)
            global selectedCatId, gameState, needsUpdate
            selectedCatId = None
            gameState.state = 'map'
            needsUpdate = True

        def fight_action():
            global gameState, needsUpdate, option
            gameState.state = 'enemy-select'
            needsUpdate = True
            option = 0

        def end_turn_action():
            global selectedCatId, gameState, needsUpdate
            selectedCatId = None
            gameState.state = 'enemy-turn'
            needsUpdate = True

        def seize_action():
            global selectedCatId, gameState, needsUpdate
            selectedCatId = None
            gameState.state = 'map'
            needsUpdate = True
            # move to the next level
            currentLevelNumber = gameState.level.number
            if currentLevelNumber == 1:
                gameState.load_level(level2)
            else: 
                gameState.state = 'end'
    
    elif gameState.state == 'enemy-select':
        # Get enemies in range of the selected cat
        selected_cat = get_selected_cat()
        enemies_in_range = []

        if selected_cat:
            for enemy in gameState.level.enemies:
                dx = abs(enemy.position.x - selected_cat.position.x)
                dy = abs(enemy.position.y - selected_cat.position.y)
                if dx + dy <= 1:
                    enemies_in_range.append(enemy)
                    # If selector is on the selected cat, move to first enemy found
                    if gameState.level.selectorPosition == selected_cat.position:
                        gameState.level.selectorPosition.x = enemy.position.x
                        gameState.level.selectorPosition.y = enemy.position.y

        # If no enemies in range, return to unit select
        if len(enemies_in_range) == 0:
            gameState.state = 'unitSelect'
            option = 0
        else:
            # Navigate between enemies in range
            if thumby.buttonU.justPressed() or thumby.buttonL.justPressed():
                option = (option - 1) % len(enemies_in_range)
                # Move cursor to the selected enemy's position
                gameState.level.selectorPosition.x = enemies_in_range[option].position.x
                gameState.level.selectorPosition.y = enemies_in_range[option].position.y
                needsUpdate = True
            elif thumby.buttonD.justPressed() or thumby.buttonR.justPressed():
                option = (option + 1) % len(enemies_in_range)
                # Move cursor to the selected enemy's position
                gameState.level.selectorPosition.x = enemies_in_range[option].position.x
                gameState.level.selectorPosition.y = enemies_in_range[option].position.y
                needsUpdate = True

            # Update viewport to follow cursor
            if gameState.level.selectorPosition.x - gameState.level.viewport.x < 1 and gameState.level.viewport.x > 0:
                gameState.level.viewport.x -= 1
            elif gameState.level.selectorPosition.x - gameState.level.viewport.x > SCREEN_TILES_X - 2 and gameState.level.viewport.x < len(gameState.level.map)[0] - SCREEN_TILES_X:
                gameState.level.viewport.x += 1
            if gameState.level.selectorPosition.y - gameState.level.viewport.y < 1 and gameState.level.viewport.y > 0:
                gameState.level.viewport.y -= 1
            elif gameState.level.selectorPosition.y - gameState.level.viewport.y > SCREEN_TILES_Y - 2 and gameState.level.viewport.y < len(gameState.level.map) - SCREEN_TILES_Y:
                gameState.level.viewport.y += 1

            # Handle selection
            if thumby.buttonA.justPressed():
                # Get the selected enemy and perform combat
                selected_cat = get_selected_cat()
                selected_enemy = enemies_in_range[option]
                
                # Perform all attacks and record them
                battle(selected_cat, selected_enemy)
                selected_cat.set_exhausted(True)
                selectedCatId = None
                gameState.state = 'map'
            elif thumby.buttonB.justPressed():
                gameState.state = 'unitSelect'
                option = 0

            # Render the map with enemy selection overlay
            if needsUpdate:
                render_map(gameState.level.map)
                needsUpdate = False
    
    elif gameState.state == 'enemy-turn':
        # loop through the enemies and move/attack
        if frame % 10 == 1:  # Slow down enemy actions
            if activeEnemy:
                print(f"Active enemy: {activeEnemy.name} at position {activeEnemy.position}.")

                # Step 1: Find a target in range
                closest_tile, target = get_attack_tile(activeEnemy)

                if target is None:
                    print(f"No target in range for enemy {activeEnemy.name}.")
                    readyForBattle = False
                    activeEnemy.set_exhausted(True)  # No target in range, skip this enemy's turn\
                    activeEnemy = None

                # Attack the target if in range
                if target and readyForBattle:
                    battle(activeEnemy, target)
                    activeEnemy.set_exhausted(True)
                    activeEnemy = None
                    needsUpdate = True
                    readyForBattle = False
                
                # Move towards the target if not in range
                elif target and not readyForBattle:
                    if closest_tile:
                        activeEnemy.set_position(closest_tile)
                        update_selector_position(closest_tile.x, closest_tile.y, gameState.level.map)
                        needsUpdate = True
                        readyForBattle = True

            else:
                # Step 4: Select the next active enemy
                for e in gameState.level.enemies:
                    if not e.exhausted:
                        ## Check if the enemy has any valid moves
                        mcRib = get_attack_tile(e)
                        if mcRib != (None, None):
                            activeEnemy = e
                            update_selector_position(activeEnemy.position.x, activeEnemy.position.y, gameState.level.map)
                            needsUpdate = True
                            break
                        else:
                            print(f"Enemy {e.name} has no valid moves, marking as exhausted.")
                            readyForBattle = False
                            activeEnemy = None
                            e.set_exhausted(True)

                # Check if all enemies are exhausted again
                if all(e.exhausted for e in gameState.level.enemies):
                    # All enemies exhausted, reset party and return to map
                    for p in gameState.party:
                        p.set_exhausted(False)
                        p.moved = False
                    for e in gameState.level.enemies:
                        e.set_exhausted(False)
                    gameState.state = 'map'
                    if (gameState.party[0]):
                        update_selector_position(gameState.party[0].position.x, gameState.party[0].position.y, gameState.level.map)
                    needsUpdate = True

            if needsUpdate:
                render_map(gameState.level.map)
                needsUpdate = False

    elif gameState.state == 'end':
        thumby.display.fill(thumby.display.WHITE)
        thumby.display.drawText("You Win!", 20, 24, thumby.display.BLACK)
        if thumby.buttonA.justPressed():
            # Reset the game
            gameState = GameState(level1, [cat, tac])
            selectedCatId = None
            needsUpdate = True
            gameState.state = 'title'
    
    elif gameState.state == 'view-stats':
        unit = None
        unit = get_selected_cat()
        if not unit:
            for e in gameState.level.enemies:
                if e.id == selectedCatId:
                    unit = e
                    break
        if unit:
            thumby.display.fill(thumby.display.WHITE)
            thumby.display.drawText(f"{unit.name}", 2, 0, thumby.display.BLACK)
            thumby.display.drawText(f"LV:{unit.level}", 32, 0, thumby.display.BLACK)
            thumby.display.drawText(f"HP:{unit.hp}/{cat.stats.max_hp}", 2, 8, thumby.display.BLACK)
            thumby.display.drawText(f"AT:{unit.stats.attack}", 2, 16, thumby.display.BLACK)
            thumby.display.drawText(f"DE:{unit.stats.defense}", 32, 16, thumby.display.BLACK)
            thumby.display.drawText(f"SP:{unit.stats.speed}", 2, 24, thumby.display.BLACK)
            thumby.display.drawText(f"LK:{unit.stats.luck}", 32, 24, thumby.display.BLACK)
            thumby.display.drawText(f"RG:{unit.stats.range}", 2, 32, thumby.display.BLACK)
            thumby.display.drawText(f"NL:{unit.next_level_exp - unit.exp}", 32, 32, thumby.display.BLACK)
            if thumby.buttonB.justPressed() or thumby.buttonA.justPressed():
                gameState.state = 'unitSelect' if not unit.exhausted and not unit.enemy else 'map'
                if unit.enemy:
                    selectedCatId = None
                needsUpdate = True

    elif gameState.state == 'gameOver':
        thumby.display.fill(thumby.display.WHITE)
        thumby.display.drawText("Game Over", 15, 24, thumby.display.BLACK)
        if thumby.buttonA.justPressed():
            gameState = GameState(level1, [cat, tac])
            selectedCatId = None
            needsUpdate = True
            gameState.state = 'title'

    thumby.display.update()

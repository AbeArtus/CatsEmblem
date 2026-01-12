from sys import path as syspath
syspath.insert(0, '/Games/CatsEmblem')

from Shared import Cat, Dialog, House, Position, Shop, ShopItem, Stats, itemDict
import thumbyGrayscale as thumby

def cat_sprite(): return thumby.Sprite(8, 8, (bytearray([0, 207, 15, 15, 192, 5, 241, 244, 6, 201, 15, 15, 192, 5, 241, 244, 7, 201, 14, 15, 192, 5, 241, 244, 1, 206, 15, 15, 192, 5, 241, 244])), 32, 16, key=1)
def enemy_sprite(): return thumby.Sprite(8, 8, (bytearray([3, 143, 2, 4, 129, 1, 228, 242, 3, 143, 2, 4, 145, 17, 196, 242, 7, 139, 2, 4, 129, 1, 228, 242]), bytearray([252, 112, 253, 251, 118, 246, 27, 13, 252, 112, 253, 251, 102, 230, 59, 13, 248, 116, 253, 251, 118, 246, 27, 13])), 32, 16, key=1)

_add_to_party = None
_update_bank = None

def set_game_state_callbacks(add_to_party, update_bank):
    global _add_to_party, _update_bank
    _add_to_party = add_to_party
    _update_bank = update_bank

# Use the callbacks in your code
def add_party_member(cat):
    if _add_to_party:
        _add_to_party(cat)

def modify_bank(amount):
    if _update_bank:
        _update_bank(amount)

# --- UNITS ---
cat = Cat(
    cat_sprite(),
    Position(2, 4),
    'cat',
    False,
    False,
    Stats(attack=5, defense=3, max_hp=10, speed=8, luck=4, range=4),
    None,
    False,
    items=[itemDict['Stick'], itemDict['Tuna']],
    classType='warrior'
)

tac = Cat(
    cat_sprite(),
    Position(5, 13),
    'tac',
    False,
    False,
    Stats(attack=4, defense=4, max_hp=8, speed=8, luck=4, range=6),
    None,
    False,
    items=[itemDict['Slngsht']]
)

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

tiles = {
    TILE_GRASS: {"sprite": (bytearray([255, 255, 255, 255, 255, 255, 255, 255]), bytearray([0, 64, 0, 64, 4, 0, 4, 0])), "XFLIP": False, "YFLIP": False},
    TILE_FOREST: {"sprite": (bytearray([255, 255, 255, 255, 127, 255, 255, 255]), bytearray([0, 0, 96, 124, 255, 124, 96, 0])), "XFLIP": False, "YFLIP": False},
    TILE_MOUNTAIN: {"sprite": (bytearray([255, 255, 255, 255, 255, 252, 227, 31]), bytearray([192, 240, 252, 255, 255, 255, 252, 224])), "XFLIP": False, "YFLIP": False},
    TILE_HOUSE: {"sprite": (bytearray([255, 255, 255, 255, 255, 255, 255, 255]), bytearray([8, 252, 142, 239, 239, 142, 252, 8])), "XFLIP": False, "YFLIP": False},
    TILE_WATER: {"sprite": (bytearray([0, 4, 2, 4, 64, 32, 64, 0, 0, 0, 4, 66, 36, 64, 0, 0]), bytearray([0, 4, 2, 4, 64, 32, 64, 0, 0, 0, 4, 66, 36, 64, 0, 0])), "XFLIP": False, "YFLIP": False},
    TILE_COAST_X: {"sprite": (bytearray([0, 64, 160, 0, 7, 136, 86, 239, 0, 4, 10, 0, 64, 161, 86, 239]), bytearray([0, 64, 160, 0, 7, 136, 16, 0, 0, 4, 10, 0, 64, 161, 16, 0])), "XFLIP": False, "YFLIP": False},
    TILE_COASTY: {"sprite": (bytearray([160, 208, 136, 16, 164, 194, 196, 160, 160, 196, 130, 68, 160, 208, 208, 160]), bytearray([32, 16, 8, 16, 36, 2, 4, 32, 32, 4, 2, 68, 32, 16, 16, 32])), "XFLIP": False, "YFLIP": False},
    TILE_BRIDGE: {"sprite": (bytearray([126, 126, 126, 126, 126, 126, 126, 126]), bytearray([193, 193, 193, 193, 193, 193, 193, 193])), "XFLIP": False, "YFLIP": False},
    TILE_CLIFF_TOP: {"sprite": (bytearray([254, 254, 254, 254, 254, 254, 254, 254]), bytearray([1, 1, 1, 1, 1, 1, 1, 1])), "XFLIP": False, "YFLIP": False},
    TILE_CLIFF_RIGHT: {"sprite": (bytearray([255, 255, 255, 255, 255, 255, 255, 0]), bytearray([0, 0, 0, 0, 0, 0, 0, 255])), "XFLIP": False, "YFLIP": False},
    TILE_CLIFFBTLBR: {"sprite": (bytearray([126, 253, 251, 247, 239, 223, 191, 127]), bytearray([255, 254, 252, 248, 240, 224, 192, 128])), "XFLIP": False, "YFLIP": False},
    TILE_CLIFF_TTLBR: {"sprite": (bytearray([127, 191, 223, 239, 247, 251, 253, 254]), bytearray([128, 64, 32, 16, 72, 36, 66, 1])), "XFLIP": False, "YFLIP": False},
    TILE_CLIFF_STRAIGHT: {"sprite": (bytearray([126, 126, 126, 126, 126, 126, 126, 126]), bytearray([255, 255, 255, 255, 255, 255, 255, 255])), "XFLIP": False, "YFLIP": False},
    TILE_COAST_CORNER_BR: {"sprite": (bytearray([160, 208, 160, 0, 164, 217, 194, 247, 136, 200, 128, 4, 130, 192, 194, 247]), bytearray([32, 16, 32, 0, 36, 25, 0, 0, 8, 8, 0, 4, 2, 0, 0, 0])),"XFLIP": False, "YFLIP": False },
    TILE_STAIRS: {"sprite": (bytearray([255, 255, 255, 255, 255, 255, 255, 255]), bytearray([85, 85, 85, 85, 85, 85, 85, 85])), "XFLIP": False, "YFLIP": False},
    TILE_SHOP: {"sprite": (bytearray([255, 255, 255, 255, 255, 255, 255, 255]), bytearray([254, 2, 5, 229, 229, 5, 2, 254])), "XFLIP": False, "YFLIP": False},
    WALL_TOP: {"sprite": (bytearray([127, 127, 127, 127, 127, 127, 127, 1]), bytearray([128, 254, 254, 254, 254, 254, 254, 254])), "XFLIP": False, "YFLIP": False},
    WALL_SIDE: {"sprite": (bytearray([17, 17, 68, 68, 17, 17, 68, 68]), bytearray([85, 17, 85, 68, 85, 17, 85, 68])), "XFLIP": False, "YFLIP": False},
    TILE_WATER_CLIFF: {"sprite": (bytearray([0, 1, 3, 7, 15, 31, 63, 127]), bytearray([1, 2, 4, 8, 16, 32, 64, 128])), "XFLIP": False, "YFLIP": False},
}
tiles.update({
    TILE_COAST_XFLIP: dict(tiles[TILE_COAST_X], XFLIP=True),
    TILE_COASTY_YFLIP: dict(tiles[TILE_COASTY], YFLIP=True),
    TILE_CLIFF_B_TLBR_XFLIP: dict(tiles[TILE_CLIFFBTLBR], XFLIP=True),
    TILE_CLIFF_B_TLBR_YFLIP: dict(tiles[TILE_CLIFFBTLBR], YFLIP=True),
    TILE_CLIFF_B_TLBR_XYFLIP: dict(tiles[TILE_CLIFFBTLBR], XFLIP=True, YFLIP=True),
    TILE_CLIFF_TTLBR_XFLIP: dict(tiles[TILE_CLIFF_TTLBR], XFLIP=True),
    TILE_COAST_CORNER_BR_XFLIP: dict(tiles[TILE_COAST_CORNER_BR], XFLIP=True),
    TILE_COAST_CORNER_BR_YFLIP: dict(tiles[TILE_COAST_CORNER_BR], YFLIP=True),
    TILE_COAST_CORNER_BR_XYFLIP: dict(tiles[TILE_COAST_CORNER_BR], XFLIP=True, YFLIP=True),
    TILE_WATER_CLIFF_YFLIP: dict(tiles[TILE_WATER_CLIFF], YFLIP=True),
    TILE_WATER_CLIFF_XFLIP: dict(tiles[TILE_WATER_CLIFF], XFLIP=True),
    TILE_WATER_CLIFF_XYFLIP: dict(tiles[TILE_WATER_CLIFF], XFLIP=True, YFLIP=True),
})

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

tileEncumberence = {
    TILE_FOREST: 2,
}

map1 = [
    [TILE_COASTY, TILE_COASTY, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER],
    [TILE_GRASS, TILE_GRASS, TILE_COAST_CORNER_BR_XFLIP, TILE_COASTY, TILE_COASTY, TILE_COASTY, TILE_COASTY, TILE_WATER, TILE_WATER, TILE_WATER],
    [TILE_GRASS, TILE_HOUSE, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_COAST_CORNER_BR_XFLIP, TILE_COASTY, TILE_COASTY],
    [TILE_FOREST, EMPTY, EMPTY, EMPTY, TILE_GRASS, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, TILE_FOREST],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_FOREST, TILE_MOUNTAIN],
    [TILE_MOUNTAIN, TILE_GRASS, TILE_FOREST, TILE_GRASS, EMPTY, TILE_GRASS, TILE_FOREST, EMPTY, TILE_MOUNTAIN, TILE_MOUNTAIN],
    [WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, EMPTY, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP],
    [WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_SIDE, EMPTY, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_SIDE],
    [TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_GRASS, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, TILE_FOREST, TILE_MOUNTAIN, TILE_MOUNTAIN],
    [TILE_MOUNTAIN, TILE_FOREST, TILE_GRASS, TILE_GRASS, EMPTY, TILE_GRASS, TILE_GRASS, EMPTY, TILE_FOREST, TILE_MOUNTAIN],
    [TILE_MOUNTAIN, EMPTY, TILE_GRASS, EMPTY, EMPTY, TILE_FOREST, TILE_FOREST, TILE_FOREST, TILE_FOREST, TILE_MOUNTAIN],
    [TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_FOREST, EMPTY, EMPTY, TILE_GRASS, TILE_HOUSE, TILE_SHOP, TILE_HOUSE, TILE_MOUNTAIN],
    [TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_GRASS, EMPTY, EMPTY, TILE_FOREST, TILE_GRASS, EMPTY, EMPTY, TILE_MOUNTAIN],
    [TILE_MOUNTAIN, TILE_FOREST, TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST],
    [TILE_MOUNTAIN, TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, TILE_GRASS, EMPTY, EMPTY, TILE_GRASS, TILE_FOREST],
    [TILE_FOREST, TILE_FOREST, TILE_GRASS, TILE_GRASS, TILE_FOREST, TILE_FOREST, TILE_GRASS, TILE_GRASS, TILE_FOREST, TILE_FOREST]
]

map2 = [
    [TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_COASTY, TILE_COASTY, TILE_COASTY, TILE_COASTY, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER],
    [TILE_WATER_CLIFF_YFLIP, TILE_FOREST, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, TILE_WATER_CLIFF_XYFLIP, TILE_WATER, TILE_COAST_X, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_GRASS, TILE_GRASS, TILE_COAST_CORNER_BR_XFLIP, TILE_WATER, TILE_WATER, TILE_WATER],
    [TILE_MOUNTAIN, TILE_FOREST, TILE_FOREST, TILE_GRASS, TILE_HOUSE, EMPTY, TILE_GRASS, TILE_GRASS, TILE_FOREST, TILE_GRASS, TILE_WATER, TILE_COAST_X, TILE_MOUNTAIN, TILE_GRASS, TILE_GRASS, TILE_FOREST, TILE_FOREST, TILE_COAST_CORNER_BR_XFLIP, TILE_WATER, TILE_WATER],
    [TILE_MOUNTAIN, TILE_FOREST, TILE_GRASS, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_WATER, TILE_COAST_X, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_FOREST, TILE_FOREST, TILE_WATER],
    [TILE_CLIFFBTLBR, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_CLIFF_B_TLBR_XFLIP, TILE_WATER, TILE_COAST_X, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, EMPTY, EMPTY, TILE_COAST_XFLIP],
    [TILE_CLIFF_B_TLBR_XYFLIP, WALL_SIDE, WALL_SIDE, TILE_STAIRS, TILE_STAIRS, TILE_STAIRS, TILE_STAIRS, WALL_SIDE, WALL_SIDE, TILE_CLIFF_B_TLBR_YFLIP, TILE_COAST_XFLIP, TILE_COAST_CORNER_BR, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_COAST_XFLIP],
    [TILE_MOUNTAIN, TILE_GRASS, TILE_FOREST, TILE_GRASS, EMPTY, EMPTY, TILE_GRASS, TILE_FOREST, TILE_MOUNTAIN, TILE_COAST_CORNER_BR_XYFLIP, TILE_COAST_X, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_MOUNTAIN, TILE_COAST_XFLIP],
    [TILE_COAST_CORNER_BR_YFLIP, TILE_GRASS, TILE_GRASS, TILE_FOREST, TILE_FOREST, EMPTY, EMPTY, TILE_GRASS, TILE_COAST_CORNER_BR_XYFLIP, TILE_WATER, TILE_COAST_X, WALL_TOP, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_COAST_XFLIP],
    [TILE_COAST_X, TILE_GRASS, EMPTY, TILE_FOREST, TILE_FOREST, TILE_FOREST, EMPTY, TILE_GRASS, TILE_COAST_CORNER_BR_XFLIP, TILE_WATER, TILE_COAST_X, WALL_SIDE, WALL_TOP, WALL_TOP, EMPTY, EMPTY, WALL_TOP, WALL_TOP, WALL_TOP, TILE_COAST_XFLIP],
    [TILE_COAST_X, EMPTY, EMPTY, EMPTY, TILE_FOREST, TILE_FOREST, TILE_GRASS, TILE_FOREST, TILE_FOREST, TILE_COAST_CORNER_BR_XFLIP, TILE_WATER, TILE_COAST_CORNER_BR_YFLIP, WALL_SIDE, WALL_SIDE, EMPTY, EMPTY, WALL_SIDE, WALL_SIDE, WALL_SIDE, TILE_COAST_XFLIP],
    [TILE_WATER, TILE_COAST_CORNER_BR_YFLIP, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_COAST_XFLIP, TILE_COAST_X, TILE_FOREST, TILE_GRASS, EMPTY, EMPTY, TILE_HOUSE, TILE_HOUSE, TILE_MOUNTAIN, TILE_COAST_XFLIP],
    [TILE_WATER, TILE_COAST_X, TILE_MOUNTAIN, TILE_GRASS, TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, TILE_BRIDGE, TILE_BRIDGE, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_MOUNTAIN, TILE_COAST_XFLIP],
    [TILE_WATER, TILE_WATER, TILE_COAST_CORNER_BR_YFLIP, TILE_MOUNTAIN, TILE_GRASS, TILE_FOREST, EMPTY, EMPTY, TILE_GRASS, TILE_MOUNTAIN, TILE_COAST_XFLIP, TILE_COAST_X, TILE_GRASS, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_MOUNTAIN, TILE_COAST_CORNER_BR_XYFLIP, TILE_WATER],
    [TILE_WATER, TILE_WATER, TILE_WATER, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_WATER, TILE_WATER, TILE_COAST_CORNER_BR_YFLIP, TILE_GRASS, EMPTY, TILE_GRASS, TILE_GRASS, TILE_MOUNTAIN, TILE_COAST_XFLIP, TILE_WATER],
    [TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_WATER, TILE_WATER]
]

def get_stats_for_level(level: int):
    return Stats(
        attack=3 + level,
        defense=2 + level,
        max_hp=7 + level,
        speed=2 + level,
        luck=1 + level,
        range=3
    )

def generate_enemy(level: int, position: Position, ai='searchAndDestroy', name='enemy', weapon="Stick", classType='pupil'):
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
        aiType=ai,
        items=[itemDict[weapon]],
        classType=classType
    )

class Level:
    def __init__(
            self,
            map: list[list[int]],
            enemies: list[Cat],
            number: int=1,
            seizePosition=Position(1, 1),
            startingPositions=[],
            shops: list[Shop]=[],
            houses: list[House]=[]
        ):
        self.map = map
        self.enemies = enemies
        self.viewport = Position()
        self.selectorPosition = Position()
        self.number = number
        self.seizePosition = seizePosition
        self.startingPositions = startingPositions
        self.shops = shops
        self.houses: list[House] = houses

# --- LEVELS ---
level1 = Level(
    map1, 
    [
        generate_enemy(1, Position(4, 4), name='bork'),
        generate_enemy(1, Position(6, 4), name='bark'),
        generate_enemy(1, Position(1, 2), ai='stand', name='sean', classType='warrior')
    ], 
    1, 
    Position(1, 2),
    [Position(6,14), Position(8,14)],
    houses = [
        House(
            Position(6, 11),
            [Dialog(
                lines=["save the","village,","take 50g"],
                left_cats=[cat],
                right_cats=[tac],
                currentlyTalking='cat',
                lambda_after=lambda: modify_bank(50)
            )],
            [Dialog(
                lines=["Thats all","we got"],
                left_cats=[],
                right_cats=[cat],
                currentlyTalking='cat'
            )]
        ),
        House(
            Position(8, 11),
            [Dialog(
                lines=["join me","tac"],
                left_cats=[cat],
                right_cats=[tac],
                currentlyTalking='cat',
                lambda_after=lambda: (tac.set_position(Position(8, 12)), add_party_member(tac))
            ), Dialog(
                lines=["I feel","ready for","anything"],
                left_cats=[cat],
                right_cats=[tac],
                currentlyTalking='tac'
            )],
        )
    ],
    shops = [
        Shop(
            Position(7, 11),
            inventory=[
                ShopItem(itemDict['Tuna'], 8),
                ShopItem(itemDict['Stick'], 10),
                ShopItem(itemDict['Slngsht'], 20)
            ]
        )
    ]
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
    [Position(16, 3), Position(15, 3)]
)

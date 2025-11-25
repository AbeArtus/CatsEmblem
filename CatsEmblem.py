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
cliffBTLBR = (bytearray([126, 253, 251, 247, 239, 223, 191, 127]), bytearray([255, 254, 252, 248, 240, 224, 192, 128]))
cliffTTLBR = (bytearray([127, 191, 223, 239, 247, 251, 253, 254]), bytearray([128, 64, 32, 16, 72, 36, 66, 1]))
cliffStraight = (bytearray([126, 126, 126, 126, 126, 126, 126, 126]), bytearray([255, 255, 255, 255, 255, 255, 255, 255]))
coastCornerBR = (bytearray([160, 208, 160, 0, 164, 217, 194, 247, 136, 200, 128, 4, 130, 192, 194, 247]), bytearray([32, 16, 32, 0, 36, 25, 0, 0, 8, 8, 0, 4, 2, 0, 0, 0]))
stairs = (bytearray([255, 255, 255, 255, 255, 255, 255, 255]), bytearray([85, 85, 85, 85, 85, 85, 85, 85]))
shop_tile = (bytearray([255, 255, 255, 255, 255, 255, 255, 255]), bytearray([254, 2, 5, 229, 229, 5, 2, 254]))
wallTop = (bytearray([127, 127, 127, 127, 127, 127, 127, 1]), bytearray([128, 254, 254, 254, 254, 254, 254, 254]))
wallSide = (bytearray([17, 17, 68, 68, 17, 17, 68, 68]), bytearray([85, 17, 85, 68, 85, 17, 85, 68]))
waterCliff = (bytearray([0, 1, 3, 7, 15, 31, 63, 127]), bytearray([1, 2, 4, 8, 16, 32, 64, 128]))

catsCave = bytearray([1,0,192,224,225,199,7,7,7,7,199,225,224,192,0,1,
           0,0,0,1,1,240,248,248,248,248,240,1,1,0,0,0])

bitmap0 = bytearray([120,254,254,255,255,255,255,254,254,120,
           0,1,1,3,3,3,3,1,1,0])
bitmap0SHD = bytearray([204,0,1,1,0,0,1,1,0,204,
           0,0,2,2,0,0,2,2,0,0])

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
    [TILE_MOUNTAIN, TILE_FOREST, TILE_GRASS, EMPTY, EMPTY, EMPTY, TILE_HOUSE, TILE_GRASS, TILE_HOUSE, TILE_FOREST],
    [TILE_MOUNTAIN, TILE_GRASS, TILE_GRASS, TILE_SHOP, EMPTY, EMPTY, TILE_FOREST, TILE_GRASS, EMPTY, TILE_FOREST],
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

class Item:
    def __init__(self, name: str, item_type: str, effect=None, attack=0, accuracy=0, range=1, crit=0):
        self.name = name
        self.type = item_type
        self.effect = effect
        self.attack = attack
        self.accuracy = accuracy
        self.range = range
        self.crit = crit

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
            aiType: str='stand' or 'searchAndDestroy',
            items: list[Item]=[]
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
        self.items: list[Item] = items[:4]  # Limit inventory to 4 items

    def use_item(self, item_index):
        if item_index < 0 or item_index >= len(self.items):
            return 

        item = self.items[item_index]
        if item.type == 'consumable' and item.effect and 'heal' in item.effect:
            self.hp = min(self.stats.max_hp, self.hp + item.effect['heal'])
            self.items.pop(item_index)

    def set_position(self, position: Position):
        self.position = position

    def set_moved(self, moved):
        self.moved = moved
    
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

    def get_weapon(self):
        for item in self.items:
            if item.type == 'weapon':
                return item
        return Item(name="Fists", item_type="weapon", attack=0, accuracy=90, range=1, crit=0)

    def open_item_menu(self):
        global gameState, needsUpdate
        gameState.state = 'item-menu'
        needsUpdate = True

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

class Dialog:
    def __init__(
            self,
            lines: list[str]=[],
            left_cats: list[Cat]=[],
            right_cats: list[Cat]=[],
            currentlyTalking: str='',
            lambda_after=None
        ):
        self.lines = lines
        self.currentlyTalking = currentlyTalking
        self.left_cats = left_cats
        self.right_cats = right_cats
        self.lambda_after = lambda_after

class House:
    def __init__(
            self,
            position: Position,
            dialogs: list[Dialog]=[],
            postVisitDialog: list[Dialog]=[]
        ):
        self.position = position
        self.dialogs = dialogs
        self.postVisitDialog = postVisitDialog
        self.visited = False
    
    def visit(self):
        self.visited = True

    def has_more_dialogs(self):
        if self.visited:
            return len(self.postVisitDialog) > 0
        else:
            return len(self.dialogs) > 0

class ShopItem:
    def __init__(self, item: Item, price: int):
        self.item: Item = item
        self.price: int = price

class Shop:
    def __init__(
            self,
            position: Position,
            inventory: list[ShopItem]=[],
        ):
        self.position = position
        self.inventory = inventory

class Level:
    def __init__(
            self,
            map,
            enemies: list[Cat],
            number,
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

class GameState:
    def __init__(
            self,
            level: Level,
            party: list[Cat],
            state='title',
        ):
        self.bank = 0
        self.party = party
        self.current_turn: str = 'player'
        self.load_level(level)
        self.combat_log = []
        self.dialog: list[Dialog] = []
        self.state = state

    def load_level(self, level: Level):
        for i, p in enumerate(self.party):
            p.set_position(level.startingPositions[i])
            p.set_exhausted(False)
            p.set_selected(False)
            p.moved = False
            p.set_hp(p.stats.max_hp)
        self.level = level
        self.update_selector_position(level.startingPositions[0].x, level.startingPositions[0].y)
         
        needsUpdate = True

    def add_dialog(self, dialog: 'Dialog'):
        self.dialog.append(dialog)

    def pop_dialog(self):
        if self.dialog:
            self.dialog.pop(0)

    def get_selected_cat(self):
        for c in self.party:
            if c.id == selectedCatId:
                return c
        return None
    
    def update_selector_position(self, x, y):
        new_x = max(0, min(len(self.level.map[0]) - 1, x))
        new_y = max(0, min(len(self.level.map) - 1, y))
        selCat = self.get_selected_cat()
        if selCat:
            if abs(new_x - selCat.position.x) + abs(new_y - selCat.position.y) > selCat.stats.range:
                return

        self.level.selectorPosition.x = new_x
        self.level.selectorPosition.y = new_y

        center_x = SCREEN_TILES_X // 2
        center_y = SCREEN_TILES_Y // 2

        viewport_x = max(0, min(len(self.level.map[0]) - SCREEN_TILES_X, new_x - center_x))
        viewport_y = max(0, min(len(self.level.map) - SCREEN_TILES_Y, new_y - center_y))

        self.level.viewport.x = viewport_x
        self.level.viewport.y = viewport_y

    def cat_is_on_shop(self):
        lateBirthdayCelebration = self.get_selected_cat()
        if not lateBirthdayCelebration:
            return None
        for shop in self.level.shops:
            if lateBirthdayCelebration.position == shop.position:
                return shop
        return None

    def cat_is_on_house(self):
        neo = self.get_selected_cat()
        if not neo:
            return None
        for house in self.level.houses:
            if neo.position == house.position:
                return house
        return None

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
selector_sprite = thumby.Sprite(10, 10, (bitmap0, bitmap0SHD) , 32, 16, key=1)
def cat_sprite(): return thumby.Sprite(8, 8, (bytearray([0, 207, 15, 15, 192, 5, 241, 244, 6, 201, 15, 15, 192, 5, 241, 244, 7, 201, 14, 15, 192, 5, 241, 244, 1, 206, 15, 15, 192, 5, 241, 244])), 32, 16, key=1)
def enemy_sprite(): return thumby.Sprite(8, 8, (bytearray([3, 143, 2, 4, 129, 1, 228, 242, 3, 143, 2, 4, 145, 17, 196, 242, 7, 139, 2, 4, 129, 1, 228, 242]), bytearray([252, 112, 253, 251, 118, 246, 27, 13, 252, 112, 253, 251, 102, 230, 59, 13, 248, 116, 253, 251, 118, 246, 27, 13])), 32, 16, key=1)

## --- ITEMS ---
tuna = Item(name="Tuna", item_type="consumable", effect={"heal": 10})

## --- WEAPONS ---
stick = Item(name="Stick", item_type="weapon", attack=1, accuracy=90, range=1, crit=0)
slingshot = Item(name="Slingshot", item_type="weapon", attack=2, accuracy=75, range=2, crit=5)
baseballBat = Item(name="Baseball Bat", item_type="weapon", attack=5, accuracy=70, range=1, crit=15)
dagger = Item(name="Dagger", item_type="weapon", attack=3, accuracy=80, range=1, crit=10)
sword = Item(name="Sword", item_type="weapon", attack=4, accuracy=85, range=1, crit=5)

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
    items=[stick, tuna]
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
    items=[slingshot]
)

def get_stats_for_level(level: int):
    return Stats(
        attack=3 + level,
        defense=2 + level,
        max_hp=7 + level,
        speed=2 + level,
        luck=1 + level,
        range=3
    )

def generate_enemy(level: int, position: Position, ai='searchAndDestroy', name='enemy', weapon=stick):
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
        items=[weapon]
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
    [Position(5,14), Position(4,14)],
    houses = [
        House(
            Position(8, 13),
            [Dialog(
                lines=[
                    "save our home",
                    "Here is 500g"
                ],
                left_cats=[cat],
                right_cats=[],
                currentlyTalking='cat',
                lambda_after=lambda: setattr(gameState, 'bank', gameState.bank + 500)
            )],
            [Dialog(
                lines=[
                    "Thats all",
                    "we got"
                ],
                left_cats=[],
                right_cats=[cat],
                currentlyTalking='cat'
            )]
        ),
        House(
            Position(6, 13),
            [Dialog(
                lines=[
                    "join me tac",
                ],
                left_cats=[cat],
                right_cats=[tac],
                currentlyTalking='cat',
                lambda_after=lambda: gameState.party.append(tac)
            ), Dialog(
                lines=[
                    "I feel",
                    "ready for"
                    "anything"
                ],
                left_cats=[cat],
                right_cats=[tac],
                currentlyTalking='tac'
            )],
        )
    ],
    shops = [
        Shop(
            Position(3, 14),
            inventory=[
                ShopItem(tuna, 80),
                ShopItem(stick, 100),
                ShopItem(slingshot, 200)
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
    [Position(16, 13), Position(17, 13)]
)

## --- INITIALIZE GAME STATE ---
gameState = GameState(level1, [cat])

def find_valid_positions(cat: Cat, gameState: GameState):
    def is_walkable(position):
        if not (0 <= position.x < len(gameState.level.map[0]) and 0 <= position.y < len(gameState.level.map)):
            return False
        tile = gameState.level.map[position.y][position.x]
        if tile not in canWalkOn or not canWalkOn[tile]:
            return False
        return True

    def is_occupied(position):
        if cat.enemy:
            return any(p.position == position for p in gameState.party)
        else:
            return any(e.position == position for e in gameState.level.enemies)

    def dfs(current_pos, remaining_range, visited: list):
        if remaining_range < 0 or current_pos in visited:
            return

        if not is_walkable(current_pos) or is_occupied(current_pos):
            return

        visited.append(current_pos)

        neighbors = [
            Position(current_pos.x + 1, current_pos.y),
            Position(current_pos.x - 1, current_pos.y),
            Position(current_pos.x, current_pos.y + 1),
            Position(current_pos.x, current_pos.y - 1),
        ]
        for neighbor in neighbors:
            dfs(neighbor, remaining_range - 1, visited)

    visited: list[Position] = []
    dfs(cat.position, cat.stats.range + 1, visited)

    return visited

def can_attack():
    cat = gameState.get_selected_cat()
    if not cat:
        return False
    if cat.exhausted:
        return False
    for enemy in gameState.level.enemies:
        dx = abs(enemy.position.x - cat.position.x)
        dy = abs(enemy.position.y - cat.position.y)
        if dx + dy <= cat.get_weapon().range and dx + dy >= cat.get_weapon().range:
            return True
    return False

def battle(attacker: Cat, defender: Cat):
    global gameState

    attackerExp = 0
    defenderExp = 0

    attackerExp =+ record_attack(attacker, defender)
    if defender.hp <= 0:
        attacker.add_exp(defender.stats.max_hp)
        return

    enemy_range = defender.get_weapon().range
    dx = abs(attacker.position.x - defender.position.x)
    dy = abs(attacker.position.y - defender.position.y)
    if dx + dy <= enemy_range and dx + dy >= enemy_range:
        defenderExp += record_attack(defender, attacker)
        if attacker.hp <= 0:
            defender.add_exp(attacker.stats.max_hp)
            return

    if attacker.stats.speed * int(1.5) > defender.stats.speed:
        attackerExp += record_attack(attacker, defender)
    if defender.hp <= 0:
        attacker.add_exp(defender.stats.max_hp)
        return

    if dx + dy <= enemy_range and dx + dy >= enemy_range:
        if defender.stats.speed * int(1.5) > attacker.stats.speed:
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

    base_damage = attacker.stats.attack - defender.stats.defense
    if base_damage < 1:
        base_damage = 1

    crit_chance = (attacker.stats.luck + attacker.stats.speed) / 20.0
    if random.random() < crit_chance:
        base_damage = int(base_damage * 1.25)
    
    return base_damage

def handle_movement():
    global needsUpdate, gameState

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
            gameState.update_selector_position(x + (dx if canUpdate else 0), y + (dy if canUpdate else 0))
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
            gameState.update_selector_position(x + (dx if canUpdate else 0), y + (dy if canUpdate else 0))
            needsUpdate = True
            return True
    return False

def render_map(level):
    global gameState
    thumby.display.fill(thumby.display.WHITE)


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
                      sprite = thumby.Sprite(8, 8, shop_tile, x * 8, y * 8)
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
    selector_sprite.x = (gameState.level.selectorPosition.x - gameState.level.viewport.x) * 8 - 1
    selector_sprite.y = (gameState.level.selectorPosition.y - gameState.level.viewport.y) * 8 - 1
    thumby.display.drawSprite(selector_sprite)

def animate_cats():
    global needsUpdate, gameState
    for c in gameState.party + gameState.level.enemies:
        c.advance_animation()
    selector_sprite.setFrame((selector_sprite.getFrame() + 1) % (selector_sprite.frameCount + 1))
    needsUpdate = True

def get_attack_tile(cat: Cat):
    global gameState

    enemy_range = (cat.stats.range + cat.get_weapon().range) if cat.aiType == "searchAndDestroy" else 1
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

    if needsUpdate:
        render_map(gameState.level.map)
        needsUpdate = False

    if len(gameState.dialog) > 0:
        thumby.display.fill(thumby.display.WHITE)
        thumby.display.drawLine(0, 14, 72, 14, thumby.display.BLACK)
        dialog = gameState.dialog[0]
        yOffset = 1
        xOffset = 4
        for cat in dialog.left_cats:
            clone = cat_sprite()
            clone.x = xOffset
            clone.y = yOffset
            thumby.display.drawSprite(clone)
            if cat.name == dialog.currentlyTalking:
                thumby.display.drawLine(xOffset + 3, yOffset +12, xOffset + 5, yOffset + 10, thumby.display.BLACK)
                thumby.display.drawLine(xOffset + 5, yOffset + 10, xOffset + 7, yOffset + 12, thumby.display.BLACK)
                thumby.display.drawLine(xOffset + 3, yOffset + 13, xOffset + 8,  yOffset + 13, thumby.display.WHITE)
            xOffset += 10
        xOffset = 62
        for cat in dialog.right_cats:
            clone = cat_sprite()
            clone.x = xOffset
            clone.y = yOffset
            thumby.display.drawSprite(clone)
            if cat.name == dialog.currentlyTalking:
                thumby.display.drawLine(xOffset + 3, yOffset +12, xOffset + 5, yOffset + 10, thumby.display.BLACK)
                thumby.display.drawLine(xOffset + 5, yOffset + 10, xOffset + 7, yOffset + 12, thumby.display.BLACK)
                thumby.display.drawLine(xOffset + 3, yOffset + 13, xOffset + 8,  yOffset + 13, thumby.display.WHITE)
            xOffset -= 10
        yOffset = 16

        for line in dialog.lines:
            thumby.display.drawText(line, 1, yOffset, thumby.display.BLACK)
            yOffset += 8
        if thumby.buttonA.justPressed():
            if dialog.lambda_after:
                dialog.lambda_after()
            gameState.pop_dialog()
            needsUpdate = True

    elif len(gameState.combat_log) > 0:
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
            gameState.add_dialog(Dialog(
                lines=[
                    "Must conquer",
                    ", undeniable",
                    "is my fate",
                ],
                currentlyTalking="cat",
                left_cats=[cat],
                right_cats=[tac]
            ))

            needsUpdate = True

    elif gameState.state == 'map':
        handle_movement()
        if (frame % 5 == 0): animate_cats()

        if thumby.buttonA.justPressed():
            cat_here = None
            for c in gameState.party:
                if c.position == gameState.level.selectorPosition:
                    cat_here = c
                    break
            if cat_here:
                selectedCatId = cat_here.id
                if cat_here.exhausted:
                    gameState.state = 'unitSelect'
                else:
                    cat_here.set_selected(True)
                    lastPos = Position(gameState.level.selectorPosition.x, gameState.level.selectorPosition.y)
                    gameState.state = 'unitSelect'
                needsUpdate = True
            elif selectedCatId != None:
                cat = gameState.get_selected_cat()
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
        if thumby.buttonB.justPressed() and selectedCatId is not None:
            cat = gameState.get_selected_cat()
            gameState.update_selector_position(lastPos.x, lastPos.y)
            selectedCatId = None
            lastPos = Position()
            needsUpdate = True

        if needsUpdate:
            render_map(gameState.level.map)
            needsUpdate = False

    elif gameState.state == 'unitSelect':
        def check_house_condition():
            global gameState
            house = gameState.cat_is_on_house()
            if not house:
                return False
            if not house.visited:
                return True
            if house.has_more_dialogs():
                return True
            return False

        actions = [
            {"label": "Seize", "action": lambda: seize_action(), "condition": lambda: gameState.get_selected_cat() and gameState.get_selected_cat().position == gameState.level.seizePosition},
            {"label": "Fight", "action": lambda: fight_action(), "condition": lambda: can_attack()},
            {"label": "Move", "action": lambda: move_action(), "condition": lambda: gameState.get_selected_cat() and not gameState.get_selected_cat().moved and not gameState.get_selected_cat().exhausted},
            {"label": "Wait", "action": lambda: wait_action(), "condition": lambda: selectedCatId is not None and not gameState.get_selected_cat().exhausted and not gameState.get_selected_cat().enemy},
            {"label": "Items", "action": lambda: gameState.get_selected_cat().open_item_menu(), "condition": lambda: selectedCatId is not None},
            {"label": "Stats", "action": lambda: stats_action(), "condition": lambda: selectedCatId is not None},
            {"label": "Shop", "action": lambda: setattr(gameState, 'state', 'shop'), "condition": lambda: gameState.cat_is_on_shop() is not None},
            {"label": "Visit", "action": lambda: setattr(gameState, 'state', 'house-visit'), "condition": lambda: check_house_condition()},
            {"label": "End Turn", "action": lambda: end_turn_action(), "condition": lambda: True},
        ]

        # Filter actions based on their conditions
        actions = [action for action in actions if action["condition"]()]
        ## make another array of size 5 since we can only show 5 options at a time
        offset = option - 4 if option >= 4 else 0
        visible_actions = actions[0+offset:5+offset]
        thumby.display.fill(thumby.display.WHITE)

        # Render the list of actions
        curY = 0
        for i, action in enumerate(visible_actions):
            selected = thumby.display.LIGHTGRAY if i + offset == option else thumby.display.BLACK
            thumby.display.drawText(action["label"], 2, curY, selected if i + offset == option and frame & 1 else thumby.display.DARKGRAY)
            curY += 8

        # Handle input for navigating the list
        if thumby.buttonU.justPressed() and option > 0:
            option -= 1
        if thumby.buttonD.justPressed() and option < len(actions)-1:
            option += 1

        # Handle input for selecting an action
        if thumby.buttonA.justPressed():
            visible_actions[option]["action"]()
            option = 0  # Reset option after action

        # Handle input for canceling
        if thumby.buttonB.justPressed():
            cat = gameState.get_selected_cat()
            if cat:
                cat.set_selected(False)
                if cat.moved and not cat.exhausted:
                    cat.moved = False
                    cat.set_position(lastPos)
                    gameState.update_selector_position(lastPos.x, lastPos.y)
            selectedCatId = None
            lastPos = Position()
            gameState.state = 'map'
            option = 0
            needsUpdate = True

        def move_action():
            global gameState, needsUpdate
            gameState.state = 'map'
            needsUpdate = True

        def stats_action():
            global gameState, needsUpdate
            gameState.state = 'view-stats'
            needsUpdate = True

        def wait_action():
            global selectedCatId, gameState, needsUpdate
            cat = gameState.get_selected_cat()
            if cat:
                cat.set_exhausted(True)
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

    elif gameState.state == 'item-menu':
        cat = gameState.get_selected_cat()
        if not cat:
            gameState.state = 'map'

        thumby.display.fill(thumby.display.WHITE)
        curY = 0
        for i, item in enumerate(cat.items):
            selected = thumby.display.LIGHTGRAY if i == option and frame & 1 else thumby.display.BLACK
            thumby.display.drawText(item.name, 2, curY, selected if i == option else thumby.display.DARKGRAY)
            curY += 8

        if thumby.buttonU.justPressed() and option > 0:
            option -= 1
        if thumby.buttonD.justPressed() and option < len(cat.items) - 1:
            option += 1

        if thumby.buttonA.justPressed():
            selected_item = cat.items[option]
            if selected_item.type == 'weapon':
                cat.items.pop(option)
                cat.items.insert(0, selected_item)
            elif selected_item.type == 'consumable' and selected_item.effect and 'heal' in selected_item.effect:
                cat.use_item(option)
            gameState.state = 'map'
            needsUpdate = True

        if thumby.buttonB.justPressed():
            gameState.state = 'unitSelect'
            needsUpdate = True
    
    elif gameState.state == 'enemy-select':
        selected_cat = gameState.get_selected_cat()
        enemies_in_range = []

        if selected_cat:
            for enemy in gameState.level.enemies:
                dx = abs(enemy.position.x - selected_cat.position.x)
                dy = abs(enemy.position.y - selected_cat.position.y)
                if dx + dy <= selected_cat.get_weapon().range:
                    enemies_in_range.append(enemy)
                    if gameState.level.selectorPosition == selected_cat.position:
                        gameState.level.selectorPosition.x = enemy.position.x
                        gameState.level.selectorPosition.y = enemy.position.y

        if len(enemies_in_range) == 0:
            gameState.state = 'unitSelect'
            option = 0
        else:
            if thumby.buttonU.justPressed() or thumby.buttonL.justPressed():
                option = (option - 1) % len(enemies_in_range)
                gameState.level.selectorPosition.x = enemies_in_range[option].position.x
                gameState.level.selectorPosition.y = enemies_in_range[option].position.y
                needsUpdate = True
            elif thumby.buttonD.justPressed() or thumby.buttonR.justPressed():
                option = (option + 1) % len(enemies_in_range)
                gameState.level.selectorPosition.x = enemies_in_range[option].position.x
                gameState.level.selectorPosition.y = enemies_in_range[option].position.y
                needsUpdate = True

            if gameState.level.selectorPosition.x - gameState.level.viewport.x < 1 and gameState.level.viewport.x > 0:
                gameState.level.viewport.x -= 1
            elif gameState.level.selectorPosition.x - gameState.level.viewport.x > SCREEN_TILES_X - 2 and gameState.level.viewport.x < len(gameState.level.map)[0] - SCREEN_TILES_X:
                gameState.level.viewport.x += 1
            if gameState.level.selectorPosition.y - gameState.level.viewport.y < 1 and gameState.level.viewport.y > 0:
                gameState.level.viewport.y -= 1
            elif gameState.level.selectorPosition.y - gameState.level.viewport.y > SCREEN_TILES_Y - 2 and gameState.level.viewport.y < len(gameState.level.map) - SCREEN_TILES_Y:
                gameState.level.viewport.y += 1

            if thumby.buttonA.justPressed():
                selected_cat = gameState.get_selected_cat()
                selected_enemy = enemies_in_range[option]
                
                battle(selected_cat, selected_enemy)
                selected_cat.set_exhausted(True)
                selectedCatId = None
                gameState.state = 'map'
            elif thumby.buttonB.justPressed():
                gameState.state = 'unitSelect'
                option = 0
            if needsUpdate:
                render_map(gameState.level.map)
                needsUpdate = False
    
    elif gameState.state == 'enemy-turn':
        if frame % 10 == 1:
            if activeEnemy:

                closest_tile, target = get_attack_tile(activeEnemy)
                if target is None:
                    print(f"No target in range for enemy {activeEnemy.name}.")
                    readyForBattle = False
                    activeEnemy.set_exhausted(True)
                    activeEnemy = None

                if target and readyForBattle:
                    battle(activeEnemy, target)
                    activeEnemy.set_exhausted(True)
                    activeEnemy = None
                    needsUpdate = True
                    readyForBattle = False

                elif target and not readyForBattle:
                    if closest_tile:
                        activeEnemy.set_position(closest_tile)
                        gameState.update_selector_position(closest_tile.x, closest_tile.y)
                        needsUpdate = True
                        readyForBattle = True

            else:
                for e in gameState.level.enemies:
                    if not e.exhausted:
                        mcRib = get_attack_tile(e)
                        if mcRib != (None, None):
                            activeEnemy = e
                            gameState.update_selector_position(activeEnemy.position.x, activeEnemy.position.y)
                            needsUpdate = True
                            break
                        else:
                            readyForBattle = False
                            activeEnemy = None
                            e.set_exhausted(True)

                if all(e.exhausted for e in gameState.level.enemies):
                    for p in gameState.party:
                        p.set_exhausted(False)
                        p.moved = False
                    for e in gameState.level.enemies:
                        e.set_exhausted(False)
                    gameState.state = 'map'
                    if (gameState.party[0]):
                        gameState.update_selector_position(gameState.party[0].position.x, gameState.party[0].position.y)
                    needsUpdate = True

            if needsUpdate:
                render_map(gameState.level.map)
                needsUpdate = False

    elif gameState.state == 'shop':
        # get the shop thats the same position as the selected cat
        shop = gameState.cat_is_on_shop()
        cat = gameState.get_selected_cat()
        if len(cat.items) > 4:
            gameState.add_dialog(Dialog(
                lines=[
                    "I have",
                    "too many",
                    "items...",
                ],
                currentlyTalking=cat.name,
                left_cats=[cat],
                right_cats=[]
            ))
            gameState.state = 'unitSelect'
        xOffset = 0
        if shop:
            thumby.display.fill(thumby.display.WHITE)
            for i, shopItem in enumerate(shop.inventory):
                selected = thumby.display.LIGHTGRAY if i == option and frame & 1 else thumby.display.BLACK
                thumby.display.drawText(f"{shopItem.item.name}{shopItem.price}", 2, xOffset, selected if i == option else thumby.display.DARKGRAY)
                xOffset += 8

            thumby.display.drawText(f"Gold: ${gameState.bank}", 2, 32, thumby.display.BLACK)
            if thumby.buttonU.justPressed() and option > 0:
                option -= 1
            if thumby.buttonD.justPressed() and option < len(shop.inventory) - 1:
                option += 1
            if thumby.buttonA.justPressed():
                selected_item = shop.inventory[option]
                if gameState.bank >= selected_item.price:
                    gameState.bank -= selected_item.price
                    cat.items.append(selected_item)
                    shop.inventory.pop(option)
                    gameState.add_dialog(Dialog(
                        lines=[
                            f"Bought {selected_item.name}!",
                        ],
                        currentlyTalking=cat.name,
                        left_cats=[cat],
                        right_cats=[]
                    ))
                else:
                    gameState.add_dialog(Dialog(
                        lines=[
                            "we're too",
                            "broke bud",
                            "...",
                        ],
                        currentlyTalking=cat.name,
                        left_cats=[cat],
                        right_cats=[]
                    ))
            if thumby.buttonB.justPressed():
                cat.set_exhausted(True)
                gameState.state = 'unitSelect'
                option = 0
                needsUpdate = True

    elif gameState.state == 'house-visit':
        house = gameState.cat_is_on_house()
        selCat = gameState.get_selected_cat()
        if not house.visited:
            house.visit()
            for dialog in house.dialogs:
                gameState.add_dialog(dialog)
                selCat.set_moved(True)
                selCat.set_exhausted(True)
        else:
            for dialog in house.postVisitDialog:
                gameState.add_dialog(dialog)
                selCat.set_moved(True)
                selCat.set_exhausted(True)
                
        gameState.state = 'unitSelect'

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
        unit = gameState.get_selected_cat()
        if not unit:
            for e in gameState.level.enemies:
                if e.id == selectedCatId:
                    unit = e
                    break
        if unit:
            thumby.display.fill(thumby.display.WHITE)
            thumby.display.drawText(f"{unit.name}", 2, 0, thumby.display.BLACK)
            thumby.display.drawText(f"LV:{unit.level}", 32, 0, thumby.display.BLACK)
            thumby.display.drawText(f"HP:{unit.hp}/{unit.stats.max_hp}", 2, 8, thumby.display.BLACK)
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

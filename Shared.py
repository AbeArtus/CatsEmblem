import gc

def checkClearMem(message: str = ''):
    gc.collect()
    print("Free memory (Shared.py):", gc.mem_free(), message)

import random
from sys import path as syspath
syspath.insert(0, '/Games/CatsEmblem')
import thumbyGrayscale as thumby
import thumbySaves as thumbySaveData
thumbySaveData.saveData.setName("CatsEmblem")

classEnum = {
    'pupil': 0,
    'warrior': 1,
    'sniper': 2,
    'wizard': 3
}

weaponAdvantages = {
    'sword': 'mace',
    'spear': 'sword',
    'mace': 'spear',
    'longbow': 'bow',
    'bow': 'repeater',
    'repeater': 'longbow',
    'lightning': 'water',
    'water': 'earth',
    'earth': 'lightning'
}

classAdvantages = {
    'warrior': ['wizard', 'pupil'],
    'sniper': ['warrior', 'pupil'],
    'wizard': ['sniper', 'pupil'],
}

class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def copy(self):
        return Position(self.x,self.y)

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
            attack: int=40,
            defense: int=40,
            max_hp: int=60,
            speed: int=60,
            luck: int=30,
            range: int=20
        ):
        self.attack = attack
        self.defense = defense
        self.max_hp = max_hp
        self.speed = speed
        self.luck = luck
        self.range = range

class Item:
    def __init__(self, name: str, item_type: str, effect=None, attack=0, accuracy=0, range=1, crit=0, allowedClasses=['pupil'], weaponType: str=None):
        self.name = name
        self.type = item_type
        self.effect = effect
        self.attack = attack
        self.accuracy = accuracy
        self.range = range
        self.crit = crit
        self.allowedClasses = allowedClasses
        self.weaponType: str = weaponType

    def can_use(self, classType: str):
        return classType in self.allowedClasses

    def can_counter(self, other_weapon_type: str):
        if self.weaponType in weaponAdvantages:
            return weaponAdvantages[self.weaponType] == other_weapon_type
        return False

class WeaponExp:
    def __init__(
            self,
            sword: int=0,
            repeater: int=0,
            longbow: int=-1,
            bow: int=-1,
            lightning: int=-1,
            water: int=-1,
            earth: int=-1,
            mace: int=-1,
            spear: int=-1
        ):
        self.sword = sword
        self.repeater = repeater
        self.longbow = longbow
        self.bow = bow
        self.lightning = lightning
        self.water = water
        self.earth = earth
        self.mace = mace
        self.spear = spear

    def get_weapon_exp(self, weapon_type: str) -> int:
        if hasattr(self, weapon_type):
            return getattr(self, weapon_type)
        return -1

    def get_weapon_attack_bonus(self, weapon_type: str) -> int:
        exp = self.get_weapon_exp(weapon_type)
        if exp == -1:
            return 1
        elif exp < 10:
            return 1
        elif exp < 25:
            return 1.05
        elif exp < 35:
            return 1.10
        elif exp < 50:
            return 1.15
        else:
            return 1.20
        
    def increase_exp(self, weapon_type: str, amount: int = 1):
        if hasattr(self, weapon_type):
            current_exp = getattr(self, weapon_type)
            if current_exp >= 0:
                setattr(self, weapon_type, current_exp + amount)
                
    def add_weapons(self, weapon_types: list[str]):
        for weapon_type in weapon_types:
            if hasattr(self, weapon_type):
                if getattr(self, weapon_type) == -1:
                    setattr(self, weapon_type, 0)

def growthRate(name: str):
    if name == 'mew': return GrowthRates(attack=45, defense=45, max_hp=60, speed=60, luck=30, range=25)
    if name == 'tac': return GrowthRates(attack=40, defense=40, max_hp=60, speed=60, luck=40, range=20)
    if name == 'cat': return GrowthRates(attack=45, defense=45, max_hp=50, speed=60, luck=40, range=20)
    if name == 'bub': return GrowthRates(attack=45, defense=45, max_hp=60, speed=45, luck=60, range=40)
    if name == 'bao': return GrowthRates(attack=40, defense=60, max_hp=50, speed=60, luck=45, range=40)
    return GrowthRates(attack=40, defense=40, max_hp=60, speed=60, luck=30, range=20)

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
            enemy: bool=False,
            level: int=1,
            exp: int=0,
            next_level_exp: int=10,
            aiType: str='stand' or 'searchAndDestroy',
            items: list[Item]=[],
            classType: str='pupil' or 'warrior' or 'sniper' or 'wizard',
            weaponExp: WeaponExp=None
        ):
        self.id = f"cat_{Cat._id_counter}"  # Generate a sequential ID
        Cat._id_counter += 1
        self.sprite: thumby.Sprite = sprite
        self.position: Position = position
        self.selected: bool = selected
        self.exhausted: bool = exhausted
        self.name: str = name
        self.stats: Stats = stats
        self.growthRates: GrowthRates = growthRate(name) 
        self.enemy: bool = enemy
        self.hp: int = self.stats.max_hp  # Initialize HP to max_hp
        self.exp: int = exp
        self.moved = False
        self.level: int = level
        self.next_level_exp: int = next_level_exp
        self.aiType: str = aiType  # 'stand' or 'searchAndDestroy'
        self.items: list[Item] = items[:4]  # Limit inventory to 4 items
        self.max_items = 4
        self.classType: str = classType
        self.weaponExp: WeaponExp = weaponExp if weaponExp else WeaponExp()

    def save_state(self):
        thumbySaveData.saveData.setItem(f"{self.name}_stats", [
            self.stats.attack,
            self.stats.defense,
            self.stats.max_hp,
            self.stats.speed,
            self.stats.luck,
            self.stats.range,
            self.level,
            self.exp,
            self.next_level_exp,
            self.position.x,
            self.position.y,
            classEnum[self.classType] if self.classType in classEnum else 0,
            self.weaponExp.sword,
            self.weaponExp.repeater,
            self.weaponExp.longbow,
            self.weaponExp.bow,
            self.weaponExp.lightning,
            self.weaponExp.water,
            self.weaponExp.earth,
            self.weaponExp.mace,
            self.weaponExp.spear,
        ])
        thumbySaveData.saveData.setItem(f"{self.name}_items", [item.name for item in self.items])

    def getClassSprite(self, position: Position=Position(0,0)):
        if self.enemy:
            if self.classType == 'wizard':
                pigHood = (bytearray([255, 231, 208, 140, 141, 141, 204, 224]), bytearray([0, 0, 16, 0, 0, 0, 0, 0]))
                return thumby.Sprite(8, 8, pigHood , position.x, position.y, key=1)
            if self.classType == 'sniper':
                pigArrowQuill =(bytearray([255, 135, 123, 255, 255, 255, 255, 255]), bytearray([32, 0, 32, 0, 0, 0, 0, 0]))
                return thumby.Sprite(8, 8, pigArrowQuill , position.x, position.y, key=1)
            if self.classType == 'warrior':
                pigArmor = (bytearray([207, 175, 143, 159, 159, 159, 255, 255]), bytearray([0, 32, 0, 0, 0, 0, 0, 0]))
                return thumby.Sprite(8, 8, pigArmor , position.x, position.y, key=1)
        else:
            if self.classType == 'wizard':   
                catMageHood = (bytearray([255, 255, 231, 193, 194, 206, 206, 238]), bytearray([0, 0, 24, 62, 63, 49, 49, 17]))
                return thumby.Sprite(8, 8, catMageHood , position.x, position.y, key=1)
            if self.classType == 'sniper':
                catArrowQuill = (bytearray([255, 135, 123, 255, 255, 255, 255, 255]), bytearray([32, 120, 164, 0, 0, 0, 0, 0]))
                return thumby.Sprite(8, 8, catArrowQuill , position.x, position.y, key=1)
            if self.classType == 'warrior':
                catArmor = (bytearray([255, 207, 143, 159, 191, 159, 255, 255]), bytearray([0, 48, 112, 112, 96, 96, 0, 0]))
                return thumby.Sprite(8, 8, catArmor , position.x, position.y, key=1)
            else:
                return None

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

    def add_exp(self, amount, addDialog):
        self.exp += amount
        if self.exp >= self.next_level_exp:
            self.level_up(addDialog)

    def get_weapon(self):
        for item in self.items:
            if item.type == 'weapon' and item.can_use(self.classType):
                return item
        return Item(name="Fists", item_type="weapon", attack=0, accuracy=90, range=1, crit=0, allowedClasses=['pupil', 'warrior', 'sniper', 'wizard'])

    def level_up(self, addDialog: callable):
        self.level += 1
        self.next_level_exp += 20

        RN = random.randint(1, 100)
        CF = random.randint(1, 100)

        if not self.enemy:
            addDialog([f"{self.name} level up",f"to {self.level}"], self)
        for stat in ['attack', 'defense', 'max_hp', 'speed', 'luck', 'range']:
            RN = (RN + CF) % 100
            CF = (CF + RN) % 100
            added = 0
            if RN <= getattr(self.growthRates, stat):
                setattr(self.stats, stat, getattr(self.stats, stat) + 1)
                added += 1
                if CF < (getattr(self.growthRates, stat)):
                    setattr(self.stats, stat, getattr(self.stats, stat) + 1)
                    added += 1
            if added > 0 and not self.enemy:
                currentValue = getattr(self.stats, stat)
                addDialog([f"{stat} up",f"from {currentValue - added}", f"to {currentValue}!"], self)
    
    def can_move(self):
        return not self.exhausted and not self.moved

    def promote(self, new_class: str):
        self.classType = new_class
        self.classSprite = self.getClassSprite(self.classType, self.enemy, self.position)
        self.exp = 0
        self.next_level_exp = 12
        if new_class == 'warrior':
            self.stats.attack += 2
            self.stats.defense += 2
            self.stats.max_hp += 3
            self.weaponExp.add_weapons(['spear', 'mace'])
        elif new_class == 'sniper':
            self.stats.attack += 2
            self.stats.speed += 2
            self.stats.luck += 1
            self.weaponExp.add_weapons(['longbow', 'bow'])
        elif new_class == 'wizard':
            self.stats.attack += 2
            self.stats.max_hp += 2
            self.stats.luck += 1
            self.weaponExp.add_weapons(['lightning', 'water', 'earth'])

class Dialog:
    def __init__(
            self,
            lines: list[str]=[],
            left_cats: list[Cat]=[],
            right_cats: list[Cat]=[],
            currentlyTalking: str='',
            decision: bool=True,
            lambda_after=None
        ):
        self.lines = lines
        self.currentlyTalking = currentlyTalking
        self.left_cats = left_cats
        self.right_cats = right_cats
        self.lambda_after = lambda_after
        self.decision = decision

class House:
    def __init__(
            self,
            position: Position,
            preVistedDialogs: list[Dialog]=[],
            dialogs: list[Dialog]=[],
            postVisitDialog: list[Dialog]=[],
            visitCondition: callable=None
        ):
        self.position = position
        self.dialogs = dialogs
        self.preVistedDialogs = preVistedDialogs
        self.postVisitDialog = postVisitDialog
        defaultVisitCondition = lambda: True
        self.visitCondition = visitCondition if visitCondition else defaultVisitCondition
        self.multipleVisits = False
        self.visited = False
    
    def visit(self):
        if self.multipleVisits:
            self.visited = False
            return
        self.visited = True

    def can_visit(self):
        if self.visitCondition:
            return self.visitCondition()
        return True

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

def cat_sprite(): return thumby.Sprite(8, 8, (bytearray([0, 207, 15, 15, 192, 5, 241, 244, 6, 201, 15, 15, 192, 5, 241, 244, 7, 201, 14, 15, 192, 5, 241, 244, 1, 206, 15, 15, 192, 5, 241, 244])), 32, 16, key=1)
def enemy_sprite(): return thumby.Sprite(8, 8, (bytearray([3, 143, 2, 4, 129, 1, 228, 242, 3, 143, 2, 4, 145, 17, 196, 242, 7, 139, 2, 4, 129, 1, 228, 242]), bytearray([252, 112, 253, 251, 118, 246, 27, 13, 252, 112, 253, 251, 102, 230, 59, 13, 248, 116, 253, 251, 118, 246, 27, 13])), 32, 16, key=1)

## --- ITEMS ---
tuna = Item(name="Tuna", item_type="consumable", effect={"heal": 10})

## --- WEAPONS ---
stick = Item(name="Stick", item_type="weapon", attack=2, accuracy=80, range=1, crit=0, allowedClasses=['pupil', 'warrior', 'sniper', 'wizard'], weaponType='sword')
slingshot = Item(name="Slngsht", item_type="weapon", attack=1, accuracy=75, range=2, crit=1, allowedClasses=['pupil', 'sniper', 'warrior', 'wizard'], weaponType='repeater')

lightningTome = Item(name="LghtngTm", item_type="weapon", attack=4, accuracy=80, range=2, crit=5, allowedClasses=['wizard'], weaponType='lightning')
waterTome = Item(name="WaterTm", item_type="weapon", attack=3, accuracy=85, range=2, crit=3, allowedClasses=['wizard'], weaponType='water')
earthTome = Item(name="EarthTm", item_type="weapon", attack=5, accuracy=70, range=1, crit=2, allowedClasses=['wizard'], weaponType='earth')

longBow = Item(name="LongBow", item_type="weapon", attack=3, accuracy=80, range=3, crit=5, allowedClasses=['sniper'], weaponType='longbow')
bow = Item(name="Bow", item_type="weapon", attack=4, accuracy=85, range=2, crit=3, allowedClasses=['sniper'], weaponType='bow')
repeater = Item(name="Repeater", item_type="weapon", attack=5, accuracy=75, range=2, crit=4, allowedClasses=['sniper'], weaponType='repeater')

sword = Item(name="Sword", item_type="weapon", attack=5, accuracy=85, range=1, crit=5, allowedClasses=['warrior', 'pupil'], weaponType='sword')
spear = Item(name="Spear", item_type="weapon", attack=4, accuracy=60, range=2, crit=3, allowedClasses=['warrior'], weaponType='spear')
mace = Item(name="Mace", item_type="weapon", attack=6, accuracy=75, range=1, crit=2, allowedClasses=['warrior'], weaponType='mace')

mysticPotion = Item(name="MystPot", item_type="promote", effect={"promote": "wizard"})
mysticMeal = Item(name="MstMeal", item_type="promote", effect={"promote": "warrior"})
mysticQuill = Item(name="MstQll", item_type="promote", effect={"promote": "sniper"})

itemDict = {
    "Tuna": tuna,
    "Stick": stick,
    "Slngsht": slingshot,
    "LghtngTm": lightningTome,
    "WaterTm": waterTome,
    "EarthTm": earthTome,
    "LongBow": longBow,
    "Bow": bow,
    "Repeater": repeater,
    "Sword": sword,
    "Spear": spear,
    "Mace": mace,
    "MystPot": mysticPotion,
    "MstMeal": mysticMeal,
    "MstQll": mysticQuill
}

class Conversation:
	def __init__(
			self,
			dialogs: list[Dialog],
			nameOne: str='',
			nameTwo: str='',
			condition: callable=lambda: True
		):
		self.dialogs = dialogs
		self.nameOne = nameOne
		self.nameTwo = nameTwo
		self.condition = condition

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
)

tac = Cat(
	cat_sprite(),
	Position(5, 13),
	'tac',
	False,
	False,
	Stats(attack=4, defense=4, max_hp=8, speed=8, luck=4, range=5),
	None,
	False,
	items=[itemDict['Slngsht']]
)

mew = Cat(
	sprite=cat_sprite(),
	level=3,
	name='mew',
	position=Position(3,1),
	stats=Stats(attack=4, defense=4, max_hp=8, speed=8, luck=4, range=5),
	enemy=True,
	items=[itemDict['Stick']],
	weaponExp=WeaponExp(repeater=10, sword=20)
)

bub = Cat(
	level=6,
	sprite=cat_sprite(),
	name='bub',
	position=Position(8,1),
	stats=Stats(attack=4, defense=4, max_hp=8, speed=8, luck=4, range=5),
	enemy=False,
	classType='sniper',
	items=[itemDict['Slngsht']],
	weaponExp=WeaponExp(bow=10, longbow=50, repeater=35, sword=10)
)

bao = Cat(
	sprite=cat_sprite(),
	name='bao',
	position=Position(8,14),
	stats=Stats(attack=8, defense=5, max_hp=10, speed=10, luck=8, range=6),
	level=5,
	enemy=False,
	aiType='stand',
	classType='wizard',
	items=[itemDict['LghtngTm'], itemDict['Tuna']],
	weaponExp=WeaponExp(lightning=60, water=20, earth=35, sword=10, repeater=15)
)

npc = Cat(
	sprite=cat_sprite(),
	name='npc',
	position=Position(0,0),
	stats=Stats(attack=0, defense=0, max_hp=1, speed=0, luck=0, range=0),
	enemy=False,
	items=[]
)

checkClearMem("After defining units")

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

tileEvation = {
	TILE_FOREST: 20,
	TILE_GRASS: 5,
	TILE_HOUSE: 10,
	TILE_SHOP: 10,
}

checkClearMem("After defining tile properties")

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
	[TILE_FOREST, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, EMPTY, TILE_GRASS, TILE_FOREST, TILE_GRASS, EMPTY, TILE_GRASS, TILE_FOREST],
	[TILE_GRASS, EMPTY, TILE_HOUSE, EMPTY, TILE_HOUSE, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, EMPTY, EMPTY, EMPTY, TILE_GRASS],
	[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS],
	[EMPTY, TILE_FOREST, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_FOREST, EMPTY, EMPTY, TILE_GRASS, EMPTY, EMPTY],
	[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, TILE_FOREST, TILE_FOREST, TILE_FOREST, EMPTY, EMPTY, EMPTY, EMPTY],
	[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_FOREST, TILE_FOREST, TILE_MOUNTAIN, TILE_FOREST, TILE_GRASS, EMPTY, TILE_FOREST, WALL_TOP],
	[EMPTY, EMPTY, EMPTY, TILE_FOREST, EMPTY, TILE_GRASS, TILE_FOREST, TILE_MOUNTAIN, TILE_FOREST, TILE_GRASS, EMPTY, EMPTY, TILE_GRASS, WALL_SIDE],
	[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, TILE_FOREST, TILE_FOREST, TILE_FOREST, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
	[WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, TILE_FOREST, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS],
	[WALL_SIDE, EMPTY, EMPTY, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_FOREST, TILE_FOREST, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
	[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, TILE_MOUNTAIN, TILE_FOREST, EMPTY, TILE_FOREST, TILE_GRASS, EMPTY, EMPTY, EMPTY],
	[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_MOUNTAIN, EMPTY, EMPTY, TILE_GRASS, EMPTY, EMPTY, EMPTY, TILE_GRASS],
	[EMPTY, TILE_HOUSE, EMPTY, EMPTY, TILE_FOREST, EMPTY, TILE_MOUNTAIN, EMPTY, EMPTY, EMPTY, TILE_FOREST, EMPTY, EMPTY, WALL_TOP],
	[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_HOUSE, WALL_SIDE],
	[TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, EMPTY, EMPTY]
]

map3 = [
	[EMPTY, TILE_FOREST, EMPTY, EMPTY, TILE_GRASS, EMPTY, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, EMPTY, TILE_FOREST, WALL_TOP, TILE_BRIDGE, WALL_TOP, TILE_FOREST],
	[TILE_FOREST, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_COAST_CORNER_BR_XYFLIP, TILE_COASTY_YFLIP, TILE_COASTY_YFLIP, TILE_COAST_CORNER_BR_YFLIP, WALL_SIDE, TILE_HOUSE, WALL_SIDE, EMPTY],
	[TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, TILE_COAST_CORNER_BR_XFLIP, TILE_WATER, TILE_WATER, TILE_COAST_X, TILE_FOREST, TILE_GRASS, EMPTY, EMPTY],
	[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_COAST_CORNER_BR_XFLIP, TILE_WATER, TILE_COAST_X, TILE_GRASS, EMPTY, EMPTY, EMPTY],
	[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_FOREST, TILE_GRASS, TILE_COAST_CORNER_BR_XFLIP, TILE_COAST_CORNER_BR, EMPTY, EMPTY, EMPTY, EMPTY],
	[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST],
	[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_FOREST, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, EMPTY, TILE_GRASS, TILE_GRASS, EMPTY],
	[WALL_TOP, TILE_STAIRS, TILE_STAIRS, TILE_STAIRS, TILE_STAIRS, TILE_STAIRS, WALL_TOP, TILE_CLIFF_STRAIGHT, TILE_CLIFFBTLBR, TILE_GRASS, TILE_GRASS, TILE_GRASS, EMPTY, TILE_CLIFF_B_TLBR_XFLIP, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT],
	[WALL_SIDE, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, WALL_SIDE, TILE_FOREST, TILE_CLIFF_B_TLBR_XYFLIP, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_B_TLBR_YFLIP, TILE_FOREST, EMPTY, TILE_GRASS, TILE_HOUSE, TILE_GRASS, TILE_GRASS],
	[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST],
	[EMPTY, TILE_FOREST, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
	[TILE_CLIFF_STRAIGHT, TILE_CLIFFBTLBR, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_CLIFF_B_TLBR_XFLIP, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, WALL_TOP, TILE_STAIRS, TILE_STAIRS, TILE_STAIRS, TILE_STAIRS, WALL_TOP, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT],
	[TILE_GRASS, TILE_CLIFF_B_TLBR_XYFLIP, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_B_TLBR_YFLIP, TILE_GRASS, TILE_GRASS, WALL_SIDE, EMPTY, EMPTY, EMPTY, EMPTY, WALL_SIDE, TILE_FOREST, TILE_GRASS, TILE_GRASS, TILE_GRASS, EMPTY],
	[EMPTY, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, EMPTY, TILE_FOREST, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, EMPTY, EMPTY],
	[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
]

map4 = [
    [TILE_HOUSE, TILE_HOUSE, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS],
    [EMPTY, EMPTY, TILE_FOREST, TILE_GRASS, TILE_FOREST, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, TILE_GRASS, TILE_FOREST, TILE_FOREST, EMPTY, EMPTY, TILE_GRASS, EMPTY, EMPTY],
    [EMPTY, TILE_FOREST, TILE_GRASS, TILE_FOREST, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, TILE_FOREST, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_COAST_CORNER_BR_XYFLIP],
    [EMPTY, TILE_FOREST, EMPTY, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, TILE_COAST_XFLIP],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_COAST_CORNER_BR_XYFLIP, TILE_WATER],
    [EMPTY, EMPTY, TILE_FOREST, TILE_GRASS, EMPTY, EMPTY, TILE_FOREST, TILE_COAST_XFLIP, TILE_WATER],
    [EMPTY, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_MOUNTAIN, EMPTY, TILE_MOUNTAIN, TILE_COAST_XFLIP, TILE_WATER],
    [EMPTY, TILE_GRASS, EMPTY, TILE_SHOP, TILE_MOUNTAIN, EMPTY, EMPTY, TILE_COAST_XFLIP, TILE_WATER],
    [EMPTY, EMPTY, EMPTY, EMPTY, TILE_MOUNTAIN, TILE_GRASS, EMPTY, TILE_COAST_CORNER_BR_XFLIP, TILE_WATER],
    [EMPTY, TILE_GRASS, EMPTY, EMPTY, TILE_MOUNTAIN, TILE_FOREST, EMPTY, EMPTY, TILE_COAST_CORNER_BR_XFLIP],
    [EMPTY, EMPTY, TILE_GRASS, EMPTY, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY],
    [TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_HOUSE, EMPTY],
    [EMPTY, TILE_GRASS, EMPTY, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS]
]

map5 = [
	[TILE_WATER, TILE_WATER, TILE_WATER, TILE_COAST_X, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_HOUSE, TILE_GRASS, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_FOREST, EMPTY, EMPTY, EMPTY],
	[TILE_WATER, TILE_WATER, TILE_WATER, TILE_COAST_X, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, EMPTY, EMPTY, TILE_MOUNTAIN, TILE_FOREST, EMPTY, EMPTY, EMPTY],
	[TILE_WATER, TILE_WATER, TILE_WATER, TILE_COAST_X, EMPTY, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_MOUNTAIN, EMPTY, TILE_FOREST, EMPTY, EMPTY],
	[TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_COAST_CORNER_BR_YFLIP, TILE_GRASS, TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, TILE_MOUNTAIN, TILE_FOREST, EMPTY, EMPTY, EMPTY, EMPTY],
	[TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_COAST_X, EMPTY, TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, TILE_MOUNTAIN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
	[TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_COAST_CORNER_BR, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS],
	[TILE_WATER, TILE_WATER, TILE_BRIDGE, TILE_BRIDGE, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, EMPTY],
	[TILE_WATER, TILE_WATER, TILE_WATER, TILE_COAST_X, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP],
	[TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_COAST_CORNER_BR_YFLIP, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_SIDE],
	[TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_COAST_X, EMPTY, TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, TILE_FOREST, TILE_GRASS, TILE_FOREST, TILE_FOREST, TILE_HOUSE, TILE_GRASS],
	[TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_COAST_X, EMPTY, EMPTY, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, EMPTY, EMPTY, TILE_FOREST],
	[TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_COAST_X, TILE_MOUNTAIN, TILE_MOUNTAIN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
	[TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_COAST_X, EMPTY, TILE_FOREST, TILE_MOUNTAIN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
	[TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_COAST_CORNER_BR_YFLIP, EMPTY, TILE_GRASS, TILE_MOUNTAIN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
	[TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_COAST_X, EMPTY, TILE_GRASS, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_MOUNTAIN, EMPTY, TILE_GRASS, EMPTY, EMPTY, EMPTY],
	[TILE_WATER, TILE_BRIDGE, TILE_BRIDGE, TILE_BRIDGE, TILE_BRIDGE, TILE_BRIDGE, EMPTY, TILE_FOREST, EMPTY, TILE_FOREST, TILE_FOREST, TILE_HOUSE, TILE_FOREST, TILE_FOREST, TILE_GRASS, EMPTY],
	[TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_COAST_X, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY],
	[TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_WATER, TILE_COAST_X, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
]

map6 = [
	[WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP],
	[WALL_TOP, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_TOP, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_TOP, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_SIDE, WALL_TOP],
	[WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP],
	[WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP],
	[WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP],
	[WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP, WALL_TOP, EMPTY, WALL_TOP, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_TOP, WALL_TOP, WALL_TOP, EMPTY, WALL_TOP, WALL_TOP, WALL_TOP],
	[WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP, WALL_SIDE, EMPTY, WALL_SIDE, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_TOP, WALL_SIDE, WALL_SIDE, EMPTY, WALL_SIDE, WALL_SIDE, WALL_TOP],
	[WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP],
	[WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP],
	[WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP],
	[WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP, WALL_TOP, EMPTY, WALL_TOP, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP],
	[WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP, WALL_SIDE, EMPTY, WALL_SIDE, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP],
	[WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_SIDE, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP],
	[WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP],
	[WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP],
	[WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP, WALL_TOP]
]

map7 = [
    [TILE_GRASS, TILE_FOREST, TILE_FOREST, EMPTY, TILE_GRASS, EMPTY, EMPTY, TILE_FOREST, TILE_GRASS, TILE_MOUNTAIN, TILE_GRASS, EMPTY, TILE_GRASS, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_FOREST, EMPTY, TILE_GRASS, EMPTY, EMPTY],
    [EMPTY, TILE_HOUSE, EMPTY, TILE_SHOP, TILE_SHOP, TILE_FOREST, TILE_GRASS, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_GRASS, EMPTY, EMPTY, TILE_GRASS, TILE_FOREST, TILE_GRASS, TILE_HOUSE, TILE_GRASS, TILE_MOUNTAIN, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_MOUNTAIN, TILE_FOREST],
    [TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, EMPTY, TILE_MOUNTAIN, EMPTY, EMPTY, EMPTY, TILE_FOREST, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, TILE_GRASS, EMPTY],
    [TILE_MOUNTAIN, TILE_MOUNTAIN, EMPTY, EMPTY, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS],
    [EMPTY, TILE_MOUNTAIN, EMPTY, TILE_FOREST, TILE_FOREST, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_MOUNTAIN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, TILE_FOREST, EMPTY, TILE_FOREST, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, TILE_GRASS, EMPTY, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [TILE_FOREST, EMPTY, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_FOREST, EMPTY, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_MOUNTAIN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, EMPTY, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_MOUNTAIN, EMPTY, EMPTY, EMPTY, TILE_FOREST, TILE_GRASS, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_MOUNTAIN, EMPTY, EMPTY, EMPTY, EMPTY, TILE_MOUNTAIN, TILE_GRASS, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_FOREST, EMPTY, EMPTY, TILE_GRASS, TILE_MOUNTAIN, EMPTY, EMPTY, EMPTY],
    [TILE_FOREST, TILE_GRASS, EMPTY, TILE_GRASS, EMPTY, EMPTY, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_MOUNTAIN, EMPTY, EMPTY, EMPTY, EMPTY],
    [TILE_GRASS, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_FOREST, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, EMPTY, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [TILE_GRASS, TILE_MOUNTAIN, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS],
    [EMPTY, TILE_FOREST, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_HOUSE, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_MOUNTAIN, TILE_MOUNTAIN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_MOUNTAIN],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_GRASS, EMPTY, TILE_FOREST, EMPTY, EMPTY, EMPTY, TILE_FOREST, EMPTY, EMPTY, TILE_GRASS, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_GRASS],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_GRASS, EMPTY, TILE_MOUNTAIN]
]

map8 = [
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

map9 = [
	[TILE_MOUNTAIN, TILE_MOUNTAIN, TILE_GRASS, TILE_GRASS, TILE_MOUNTAIN, TILE_GRASS, TILE_CLIFF_B_TLBR_XYFLIP, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFFBTLBR, EMPTY, EMPTY, WALL_TOP, WALL_TOP, TILE_STAIRS, TILE_STAIRS, TILE_STAIRS, WALL_TOP, WALL_TOP],
	[TILE_GRASS, TILE_HOUSE, TILE_HOUSE, TILE_GRASS, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, EMPTY, TILE_FOREST, TILE_CLIFF_B_TLBR_XYFLIP, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, WALL_SIDE, WALL_SIDE, TILE_STAIRS, TILE_STAIRS, TILE_STAIRS, WALL_SIDE, WALL_SIDE],
	[TILE_MOUNTAIN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS],
	[TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS],
	[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
	[WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, WALL_TOP, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
	[WALL_SIDE, TILE_STAIRS, TILE_STAIRS, TILE_STAIRS, TILE_STAIRS, WALL_SIDE, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFFBTLBR, EMPTY, EMPTY, TILE_CLIFF_B_TLBR_XFLIP, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFFBTLBR, EMPTY, EMPTY, TILE_CLIFF_B_TLBR_XFLIP],
	[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, TILE_CLIFF_B_TLBR_XYFLIP, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_B_TLBR_YFLIP, TILE_FOREST, TILE_GRASS, TILE_GRASS, TILE_FOREST, TILE_CLIFF_B_TLBR_XYFLIP, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_B_TLBR_YFLIP],
	[TILE_MOUNTAIN, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, EMPTY, TILE_FOREST, EMPTY, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, TILE_GRASS, EMPTY],
	[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
	[TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
	[TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
	[TILE_GRASS, TILE_GRASS, TILE_CLIFF_B_TLBR_XFLIP, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFFBTLBR, EMPTY, EMPTY, TILE_CLIFF_B_TLBR_XFLIP, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_STAIRS, TILE_STAIRS, TILE_STAIRS, TILE_STAIRS, TILE_CLIFF_STRAIGHT],
	[TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_B_TLBR_YFLIP, TILE_FOREST, TILE_FOREST, TILE_GRASS, TILE_CLIFF_B_TLBR_XYFLIP, TILE_CLIFF_STRAIGHT, TILE_CLIFF_STRAIGHT, TILE_CLIFF_B_TLBR_YFLIP, TILE_GRASS, TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
	[TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_GRASS, TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
	[TILE_GRASS, TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, TILE_FOREST],
	[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, EMPTY],
	[TILE_GRASS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TILE_FOREST, EMPTY, EMPTY]
]
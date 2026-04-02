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
            level: int=1,
            exp: int=0,
            next_level_exp: int=10,
            aiType: str='stand' or 'searchAndDestroy',
            items: list[Item]=[],
            classType: str='pupil',
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
        self.growthRates: GrowthRates = growthRates if growthRates else GrowthRates() 
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
            self.weaponExp.spear
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
        self.next_level_exp += int(self.next_level_exp * 1.5)

        RN = random.randint(1, 100)
        CF = random.randint(1, 100)

        if not self.enemy:
            addDialog([f"{self.name} level","up to", f"{self.level}"], self)
        for stat in ['attack', 'defense', 'max_hp', 'speed', 'luck', 'range']:
            RN = (RN + CF) % 100
            CF = (CF + RN) % 100
            added = 0
            if RN <= getattr(self.growthRates, stat):
                setattr(self.stats, stat, getattr(self.stats, stat) + 1)
                added += 1
                if CF < (getattr(self.growthRates, stat) + self.stats.luck):
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
        self.visited = False
    
    def visit(self):
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

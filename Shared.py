import gc

def checkClearMem(message: str = ''):
    gc.collect()
    print("Free memory (Shared.py):", gc.mem_free(), message)

from sys import path as syspath
syspath.insert(0, '/Games/CatsEmblem')
import thumbyGrayscale as thumby

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

_class_overlay_data = None

def get_class_overlay_data():
    global _class_overlay_data
    if _class_overlay_data is None:
        _class_overlay_data = {
            (True, 'wizard'): (bytearray([255, 231, 208, 140, 141, 141, 204, 224]), bytearray([0, 0, 16, 0, 0, 0, 0, 0])),
            (True, 'sniper'): (bytearray([255, 135, 123, 255, 255, 255, 255, 255]), bytearray([32, 0, 32, 0, 0, 0, 0, 0])),
            (True, 'warrior'): (bytearray([207, 175, 143, 159, 159, 159, 255, 255]), bytearray([0, 32, 0, 0, 0, 0, 0, 0])),
            (False, 'wizard'): (bytearray([255, 255, 231, 193, 194, 206, 206, 238]), bytearray([0, 0, 24, 62, 63, 49, 49, 17])),
            (False, 'sniper'): (bytearray([255, 135, 123, 255, 255, 255, 255, 255]), bytearray([32, 120, 164, 0, 0, 0, 0, 0])),
            (False, 'warrior'): (bytearray([255, 207, 143, 159, 191, 159, 255, 255]), bytearray([0, 48, 112, 112, 96, 96, 0, 0])),
        }
    return _class_overlay_data

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
            attack: int = 3,
            defense: int = 2,
            max_hp: int = 8,
            speed: int = 3,
            luck: int = 2,
            range: int = 3
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
    def __init__(self, name: str, item_type: str, effect=None, attack=0, accuracy=0, range=1, crit=0, allowedClasses: list[str] | None = None, weaponType: str=None):
        self.name = name
        self.type = item_type
        self.effect = effect
        self.attack = attack
        self.accuracy = accuracy
        self.range = range
        self.crit = crit
        self.allowedClasses = allowedClasses if allowedClasses else ['pupil']
        self.weaponType: str = weaponType

    def can_use(self, classType: str):
        return classType in self.allowedClasses

    def can_counter(self, other_weapon_type: str):
        if self.weaponType in weaponAdvantages:
            return weaponAdvantages[self.weaponType] == other_weapon_type
        return False

    def get_range(self):
        if self.range == 12:
            return [1,2]
        return [self.range]

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
            return 0
        elif exp < 10:
            return 0
        elif exp < 50:
            return 0.05
        elif exp < 100:
            return 0.10
        elif exp < 200:
            return 0.15
        else:
            return 0.20
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

class Option:
    def __init__(self, label: str, action: callable, condition: callable = lambda: True):
        self.label: str = label
        self.action: callable = action
        self.condition: callable = condition

class Menu:
    def __init__(self, options: list[list[Option]], title: list[function[str]] | None = None, option_index: int = 0, menu_index: int = 0, leave_action: function | None = None):
        self.options = options
        self.title = title if title else [lambda: ""]
        self.option_index = option_index
        self.menu_index = menu_index
        self.leave_action = leave_action

    def get_options(self):
        return [opt for opt in self.options[self.menu_index] if opt.condition()]

    def get_visible_options(self, max_visible: int = 4):
        valid_options = self.get_options()
        offset = max(0, self.option_index - max_visible + 1)
        return valid_options[offset:offset + max_visible], offset

    def handle_input(self):
        visibile_options = self.get_options()
        if thumby.buttonU.justPressed() and self.option_index > 0:
            self.option_index -= 1
        elif thumby.buttonD.justPressed() and self.option_index < len(visibile_options) - 1:
            self.option_index += 1

        elif thumby.buttonL.justPressed() and self.menu_index > 0:
            self.menu_index -= 1
            self.option_index = 0

        elif thumby.buttonR.justPressed() and self.menu_index < len(self.options) - 1:
            self.menu_index += 1
            self.option_index = 0

        elif thumby.buttonA.justPressed():
            valid_options = self.get_options()
            if valid_options:
                valid_options[self.option_index].action()
        
        elif thumby.buttonB.justPressed():
            if self.leave_action:
                self.leave_action()

    def render(self):
        thumby.display.fill(thumby.display.BLACK)

        if self.title and self.menu_index < len(self.title):
            thumby.display.drawText(self.title[self.menu_index](), 2, 0, thumby.display.LIGHTGRAY)

        visible_options, offset = self.get_visible_options()
        for i, option in enumerate(visible_options):
            selected = thumby.display.WHITE if i + offset == self.option_index else thumby.display.DARKGRAY
            if i + offset == self.option_index:
                thumby.display.drawRectangle(0, 8 + i * 8, 1, 7, thumby.display.WHITE)
            thumby.display.drawText(option.label, 2, 8 + i * 8, selected)


class Cat:
    _id_counter = 0  # Class variable for unique IDs
    def __init__(
            self,
            sprite,
            position: Position,
            name: str,
            selected: bool=False,
            exhausted: bool=False,
            stats: Stats = None,
            enemy: bool=False,
            level: int=1,
            exp: int=0,
            next_level_exp: int=20,
            aiType: str='stand' or 'searchAndDestroy',
            items: list[Item] | None = None,
            classType: str='pupil' or 'warrior' or 'sniper' or 'wizard',
            weaponExp: WeaponExp=None,
            growthRates: GrowthRates = None
        ):
        self.id = f"cat_{Cat._id_counter}"  # Generate a sequential ID
        Cat._id_counter += 1
        self._sprite = None
        self._sprite_factory = None
        if callable(sprite):
            self._sprite_factory = sprite
        else:
            self._sprite = sprite
        self.position: Position = position
        self.selected: bool = selected
        self.exhausted: bool = exhausted
        self.name: str = name
        self.stats: Stats = stats if stats is not None else Stats()
        self.growthRates: GrowthRates = growthRates if growthRates is not None else GrowthRates()
        self.enemy: bool = enemy
        self.hp: int = self.stats.max_hp  # Initialize HP to max_hp
        self.exp: int = exp
        self.moved = False
        self.level: int = level
        self.next_level_exp: int = next_level_exp
        self.aiType: str = aiType  # 'stand' or 'searchAndDestroy'
        self.items: list[Item] = (items if items else [])[:4]  # Limit inventory to 4 items
        self.max_items = 4
        self.classType: str = classType
        self.weaponExp: WeaponExp = weaponExp if weaponExp else WeaponExp()
        self._class_sprite = None
        self._class_sprite_key = None

    @property
    def sprite(self):
        if self._sprite is None and self._sprite_factory is not None:
            self._sprite = self._sprite_factory()
        return self._sprite

    @sprite.setter
    def sprite(self, value):
        self._sprite = value
        self._sprite_factory = None

    def save_state(self):
        import thumbySaves as thumbySaveData
        thumbySaveData.saveData.setName("CatsEmblem")
        thumbySaveData.saveData.delItem(f"{self.name}_stats")
        thumbySaveData.saveData.delItem(f"{self.name}_items")
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
        thumbySaveData.saveData.save()

    def getClassSprite(self, position: Position=Position(0,0)):
        sprite_key = (self.enemy, self.classType)
        sprite_data = get_class_overlay_data().get(sprite_key)
        if sprite_data is None:
            return None

        if self._class_sprite is None or self._class_sprite_key != sprite_key:
            self._class_sprite = thumby.Sprite(8, 8, sprite_data, position.x, position.y, key=1)
            self._class_sprite_key = sprite_key
        else:
            self._class_sprite.x = position.x
            self._class_sprite.y = position.y
        return self._class_sprite

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

    def add_exp(self, amount, addDialog: callable | None = None):
        levels_gained = ((self.exp % 20) + amount) // 20
        self.exp += amount

        for _ in range(levels_gained):
            print(f"{self.name} leveled up to {self.level + 1}!")
            self.level_up(addDialog)

        return self

    def get_weapon(self):
        for item in self.items:
            if item.type == 'weapon' and item.can_use(self.classType):
                return item
        return None

    def level_up(self, addDialog: callable | None = None):
        import random
        self.level += 1
        self.next_level_exp += 20

        RN = random.randint(1, 100)
        CF = random.randint(1, 100)

        if not self.enemy and addDialog:
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
            if added > 0 and not self.enemy and addDialog:
                currentValue = getattr(self.stats, stat)
                addDialog([f"{stat} up",f"from {currentValue - added}", f"to {currentValue}!"], self)
    
    def can_move(self):
        return not self.exhausted and not self.moved

    def promote(self, new_class: str):
        self.classType = new_class
        self.classSprite = self.getClassSprite(self.position)
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
            lines: list[str] | None = None,
            left_cats: list[Cat] | None = None,
            right_cats: list[Cat] | None = None,
            currentlyTalking: str='',
            decision: bool=True,
            lambda_after=None
        ):
        self.lines = lines if lines else []
        self.currentlyTalking = currentlyTalking
        self.left_cats = left_cats if left_cats else []
        self.right_cats = right_cats if right_cats else []
        self.lambda_after = lambda_after
        self.decision = decision

class House:
    def __init__(
            self,
            position: Position,
            preVistedDialogs: list[Dialog] | None = None,
            dialogs: list[Dialog] | None = None,
            postVisitDialog: list[Dialog] | None = None,
            visitCondition: callable=None,
            multipleVisits: bool=False
        ):
        self.position = position
        self.dialogs = dialogs if dialogs else []
        self.preVistedDialogs = preVistedDialogs if preVistedDialogs else []
        self.postVisitDialog = postVisitDialog if postVisitDialog else []
        defaultVisitCondition = lambda: True
        self.visitCondition = visitCondition if visitCondition else defaultVisitCondition
        self.multipleVisits = multipleVisits
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

# --- CLASSES ---
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
            attacker_max_hp: int,
            attacker_enemy: bool,
            attacker_sprite: thumby.Sprite,
            defender_name: str,
            defender_hp: int,
            defender_max_hp: int,
            defender_enemy: bool,
            defender_sprite: thumby.Sprite,
            damage: int,
            old_hp: int,
            new_hp: int,
            miss: bool,
            dodge: bool,
            text: str,
            static_render_time: int = 0
        ):
        self.attacker_name = attacker_name
        self.attacker_hp = attacker_hp
        self.attacker_max_hp = attacker_max_hp
        self.attacker_enemy = attacker_enemy
        self.attacker_sprite = attacker_sprite
        self.defender_name = defender_name
        self.defender_hp = defender_hp
        self.defender_max_hp = defender_max_hp
        self.defender_enemy = defender_enemy
        self.defender_sprite = defender_sprite
        self.damage = damage
        self.old_hp = old_hp
        self.new_hp = new_hp
        self.miss = miss
        self.dodge = dodge
        self.text = text
        self.static_render_time = static_render_time

def cat_sprite(): return thumby.Sprite(8, 8, (bytearray([0, 207, 15, 15, 192, 5, 241, 244, 6, 201, 15, 15, 192, 5, 241, 244, 7, 201, 14, 15, 192, 5, 241, 244, 1, 206, 15, 15, 192, 5, 241, 244])), 32, 16, key=1)
def enemy_sprite(): return thumby.Sprite(8, 8, (bytearray([3, 143, 2, 4, 129, 1, 228, 242, 3, 143, 2, 4, 145, 17, 196, 242, 7, 139, 2, 4, 129, 1, 228, 242]), bytearray([252, 112, 253, 251, 118, 246, 27, 13, 252, 112, 253, 251, 102, 230, 59, 13, 248, 116, 253, 251, 118, 246, 27, 13])), 32, 16, key=1)

_item_cache = {}

def _build_item(item_name: str):
    if item_name == "Tuna":
        return Item(name="Tuna", item_type="consumable", effect={"heal": 10})
    if item_name == "Stick":
        return Item(name="Stick", item_type="weapon", attack=2, accuracy=80, range=1, crit=0, allowedClasses=['pupil', 'warrior', 'sniper', 'wizard'], weaponType='sword')
    if item_name == "Slngsht":
        return Item(name="Slngsht", item_type="weapon", attack=1, accuracy=75, range=2, crit=1, allowedClasses=['pupil', 'sniper', 'warrior', 'wizard'], weaponType='repeater')
    if item_name == "LghtngTm":
        return Item(name="LghtngTm", item_type="weapon", attack=4, accuracy=80, range=12, crit=5, allowedClasses=['wizard'], weaponType='lightning')
    if item_name == "WaterTm":
        return Item(name="WaterTm", item_type="weapon", attack=3, accuracy=85, range=12, crit=3, allowedClasses=['wizard'], weaponType='water')
    if item_name == "EarthTm":
        return Item(name="EarthTm", item_type="weapon", attack=5, accuracy=70, range=12, crit=2, allowedClasses=['wizard'], weaponType='earth')
    if item_name == "LongBow":
        return Item(name="LongBow", item_type="weapon", attack=3, accuracy=80, range=3, crit=5, allowedClasses=['sniper'], weaponType='longbow')
    if item_name == "Bow":
        return Item(name="Bow", item_type="weapon", attack=5, accuracy=85, range=2, crit=3, allowedClasses=['sniper'], weaponType='bow')
    if item_name == "Repeater":
        return Item(name="Repeater", item_type="weapon", attack=3, accuracy=75, range=12, crit=4, allowedClasses=['sniper'], weaponType='repeater')
    if item_name == "Sword":
        return Item(name="Sword", item_type="weapon", attack=5, accuracy=85, range=1, crit=5, allowedClasses=['warrior', 'pupil'], weaponType='sword')
    if item_name == "Spear":
        return Item(name="Spear", item_type="weapon", attack=4, accuracy=60, range=2, crit=3, allowedClasses=['warrior'], weaponType='spear')
    if item_name == "Mace":
        return Item(name="Mace", item_type="weapon", attack=6, accuracy=75, range=12, crit=2, allowedClasses=['warrior'], weaponType='mace')
    if item_name == "MystPot":
        return Item(name="MystPot", item_type="promote", effect={"promote": "wizard"})
    if item_name == "MstMeal":
        return Item(name="MstMeal", item_type="promote", effect={"promote": "warrior"})
    if item_name == "MstQll":
        return Item(name="MstQll", item_type="promote", effect={"promote": "sniper"})
    raise KeyError(item_name)

class LazyItemDict:
    def __contains__(self, key):
        return key in {
            "Tuna", "Stick", "Slngsht", "LghtngTm", "WaterTm", "EarthTm",
            "LongBow", "Bow", "Repeater", "Sword", "Spear", "Mace",
            "MystPot", "MstMeal", "MstQll"
        }

    def __getitem__(self, key):
        if key not in self:
            raise KeyError(key)
        if key not in _item_cache:
            _item_cache[key] = _build_item(key)
        return _item_cache[key]

    def get(self, key, default=None):
        if key in self:
            return self[key]
        return default

itemDict = LazyItemDict()

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

# --- UNITS (lazy) ---
_unit_cache = {}

def _build_cat_unit():
    return Cat(
        sprite=cat_sprite,
        position=Position(2, 4),
        name='cat',
        stats=Stats(attack=4, speed=5, luck=4),
        growthRates=GrowthRates(attack=45, defense=45, luck=50, range=15),
        items=[itemDict['Stick'], itemDict['Tuna']],
    )

def _build_tac_unit():
    return Cat(
        sprite=cat_sprite,
        position=Position(5, 13),
        name='tac',
        stats=Stats(defense=3, speed=4, luck=3),
        growthRates=GrowthRates(defense=50, speed=70, luck=25, range=25),
        items=[itemDict['Slngsht']]
    )

def _build_mew_unit():
    return Cat(
        sprite=cat_sprite,
        name='mew',
        position=Position(3,1),
        stats=Stats(attack=5, max_hp=10, speed=4),
        items=[itemDict['Stick']],
        weaponExp=WeaponExp(repeater=10, sword=20),
        growthRates=GrowthRates(attack=50, speed=65, range=15)
    ).add_exp(40, None)

def _build_bub_unit():
    return Cat(
        sprite=cat_sprite,
        name='bub',
        position=Position(8,1),
        stats=Stats(attack=4, speed=4, luck=4),
        enemy=False,
        classType='sniper',
        items=[itemDict['Repeater'], itemDict['Tuna']],
        growthRates=GrowthRates(attack=60, defense=30, max_hp=55, speed=45, luck=40, range=30),
        weaponExp=WeaponExp(bow=10, longbow=50, repeater=35, sword=10)
    ).add_exp(100, None)

def _build_bao_unit():
    return Cat(
        sprite=cat_sprite,
        name='bao',
        position=Position(8,14),
        stats=Stats(attack=5, defense=3, luck=4, range=6),
        level=5,
        enemy=False,
        aiType='stand',
        classType='wizard',
        items=[itemDict['EarthTm'], itemDict['Tuna']],
        growthRates=GrowthRates(attack=45, defense=45, max_hp=65, speed=50, luck=50),
        weaponExp=WeaponExp(lightning=60, water=20, earth=35, sword=10, repeater=15)
    ).add_exp(80, None)

def _build_npc_unit():
    return Cat(
        sprite=cat_sprite,
        name='npc',
        position=Position(0,0),
        stats=Stats(attack=0, defense=0, max_hp=1, speed=0, luck=0, range=0),
        enemy=False,
        items=[]
    )

def _get_or_create_unit(unit_name: str, factory):
    if unit_name not in _unit_cache:
        _unit_cache[unit_name] = factory()
    return _unit_cache[unit_name]

def get_cat():
    return _get_or_create_unit('cat', _build_cat_unit)

def get_tac():
    return _get_or_create_unit('tac', _build_tac_unit)

def get_mew():
    return _get_or_create_unit('mew', _build_mew_unit)

def get_bub():
    return _get_or_create_unit('bub', _build_bub_unit)

def get_bao():
    return _get_or_create_unit('bao', _build_bao_unit)

def get_npc():
    return _get_or_create_unit('npc', _build_npc_unit)

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
TILE_SEIZE = 34

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
    TILE_SEIZE: {"sprite": (bytearray([255, 127, 127, 127, 127, 127, 127, 255]), bytearray([252, 134, 131, 129, 129, 131, 134, 252])), "XFLIP": False, "YFLIP": False},
}

_tile_flip_overrides = {
    TILE_COAST_XFLIP: (TILE_COAST_X, True, False),
    TILE_COASTY_YFLIP: (TILE_COASTY, False, True),
    TILE_CLIFF_B_TLBR_XFLIP: (TILE_CLIFFBTLBR, True, False),
    TILE_CLIFF_B_TLBR_YFLIP: (TILE_CLIFFBTLBR, False, True),
    TILE_CLIFF_B_TLBR_XYFLIP: (TILE_CLIFFBTLBR, True, True),
    TILE_CLIFF_TTLBR_XFLIP: (TILE_CLIFF_TTLBR, True, False),
    TILE_CLIFF_RIGHT_XFLIP: (TILE_CLIFF_RIGHT, True, False),
    TILE_COAST_CORNER_BR_XFLIP: (TILE_COAST_CORNER_BR, True, False),
    TILE_COAST_CORNER_BR_YFLIP: (TILE_COAST_CORNER_BR, False, True),
    TILE_COAST_CORNER_BR_XYFLIP: (TILE_COAST_CORNER_BR, True, True),
    TILE_WATER_CLIFF_YFLIP: (TILE_WATER_CLIFF, False, True),
    TILE_WATER_CLIFF_XFLIP: (TILE_WATER_CLIFF, True, False),
    TILE_WATER_CLIFF_XYFLIP: (TILE_WATER_CLIFF, True, True),
}

def get_tile_data(tile_type: int):
    tileData = tiles.get(tile_type, None)
    if tileData:
        return tileData["sprite"], tileData["XFLIP"], tileData["YFLIP"]

    override = _tile_flip_overrides.get(tile_type, None)
    if override:
        base_type, x_flip, y_flip = override
        baseData = tiles.get(base_type, None)
        if baseData:
            return baseData["sprite"], x_flip, y_flip

    return None, False, False

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
    TILE_SEIZE: True,
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

_map_cache = {}

def get_map(map_number: int):
    if map_number in _map_cache:
        return _map_cache[map_number]

    import MapData
    maps = {
        1: MapData.map1,
        2: MapData.map2,
        3: MapData.map3,
        4: MapData.map4,
        5: MapData.map5,
        6: MapData.map6,
        7: MapData.map7,
        8: MapData.map8,
        9: MapData.map9,
    }
    if map_number not in maps:
        raise ValueError(f"Map {map_number} does not exist")

    map_data = maps[map_number]
    _map_cache.clear()
    _map_cache[map_number] = map_data
    gc.collect()
    return map_data
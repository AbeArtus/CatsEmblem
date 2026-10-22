from sys import path as syspath
import gc

syspath.insert(0, '/Games/CatsEmblem')

def checkClearMem(message: str):
	gc.collect()
	print(message, gc.mem_free(), "bytes free")

from MapData import tileEncumberence, canWalkOn

classEnum = {
    'pupil': 0,
    'warrior': 1,
    'sniper': 2,
    'wizard': 3
}

from Items import Item, itemDict

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
    __slots__ = ('x', 'y')

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
        return Position(self.x, self.y)

class Stats:
    __slots__ = ('attack', 'defense', 'max_hp', 'speed', 'luck', 'range')

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
    __slots__ = ('attack', 'defense', 'max_hp', 'speed', 'luck', 'range')

    def __init__(
            self,
            attack: int = 40,
            defense: int = 40,
            max_hp: int = 50,
            speed: int = 50,
            luck: int = 25,
            range: int = 10
        ):
        self.attack = attack
        self.defense = defense
        self.max_hp = max_hp
        self.speed = speed
        self.luck = luck
        self.range = range

class WeaponExp:
    __slots__ = ('sword', 'repeater', 'longbow', 'bow', 'lightning', 'water', 'earth', 'mace', 'spear')

    def __init__(
            self,
            sword: int = 0,
            repeater: int = 0,
            longbow: int = -1,
            bow: int = -1,
            lightning: int = -1,
            water: int = -1,
            earth: int = -1,
            mace: int = -1,
            spear: int = -1
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
    def add_weapons(self, weapon_types):
        for weapon_type in weapon_types:
            if hasattr(self, weapon_type):
                if getattr(self, weapon_type) == -1:
                    setattr(self, weapon_type, 0)

class Option:
    __slots__ = ('label', 'action', 'condition')

    def __init__(self, label, action, condition=lambda: True):
        self.label = label
        self.action = action
        self.condition = condition

class Menu:
    __slots__ = ('options', 'title', 'option_index', 'menu_index', 'leave_action')

    def __init__(self, options, title=None, option_index=0, menu_index=0, leave_action=None):
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

_growth = None

def _default_growth():
    global _growth
    if _growth is None:
        _growth = GrowthRates()
    return _growth

class Cat:
    _id_counter = 0
    __slots__ = (
        'id', 'position', 'selected', 'exhausted',
        'name', 'stats', 'growthRates', 'enemy', 'hp', 'exp', 'moved', 'level',
        'next_level_exp', 'aiType', 'aiPath', 'items', 'max_items', 'classType',
        'weaponExp', 'deathDialog', 'summon', 'summoner'
    )

    def __init__(
        self,
        position,
        name,
        selected=False,
        exhausted=False,
        stats=None,
        enemy=False,
        level=1,
        exp=0,
        next_level_exp=20,
        aiType='stand',
        aiPath=None,
        items=None,
        classType='pupil',
        weaponExp=None,
        growthRates=None,
        deathDialog=None,
        summon=None,
        summoner=None
    ):
        self.summon = summon
        self.summoner = summoner
        self.id = f"cat_{Cat._id_counter}"
        Cat._id_counter += 1
        self.position = position
        self.selected = selected
        self.exhausted = exhausted
        self.name = name
        self.stats = stats if stats is not None else Stats()
        self.growthRates = growthRates if growthRates is not None else _default_growth()
        self.enemy = enemy
        self.hp = self.stats.max_hp
        self.exp = exp
        self.moved = False
        self.level = level
        self.next_level_exp = next_level_exp
        self.aiType = aiType
        self.aiPath = aiPath if aiPath else []
        self.items: list[Item] = (items if items else [])[:4]
        self.max_items = 4
        self.classType = classType
        self.weaponExp = weaponExp if weaponExp else WeaponExp()
        self.deathDialog = deathDialog

    @property
    def sprite(self):
        if self.summon == 'skeleton':
            return skeleton_sprite()
        if self.summon == 'orb':
            return orb_sprite()
        return enemy_sprite() if self.enemy else cat_sprite()

    def save_state(self, saveData):
        saveData.delItem(f"{self.name}_stats")
        saveData.delItem(f"{self.name}_items")
        saveData.delItem(f"{self.name}_durabilities")

        saveData.setItem(f"{self.name}_stats", [
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
        saveData.setItem(f"{self.name}_items", [item.name for item in self.items])
        saveData.setItem(f"{self.name}_durabilities", [item.durability for item in self.items if item.type == 'weapon'])

    def equip_item(self, item_index: int):
        temp = self.items[0]
        self.items[0] = self.items[item_index]
        self.items[item_index] = temp

    def restore_state(self):
        self.set_exhausted(False)
        self.set_moved(False)
        self.set_hp(self.stats.max_hp)
        self.set_selected(False)

    def getClassSprite(self, x=0, y=0):
        if self.summon:
            return None
        sprite_key = (self.enemy, self.classType)
        sprite_data = get_class_overlay_data().get(sprite_key)
        if sprite_data is None:
            return None

        sprite = _class_sprite_cache.get(sprite_key)
        if sprite is None:
            from thumbyGrayscale import Sprite
            sprite = Sprite(8, 8, sprite_data, x, y, key=1)
            _class_sprite_cache[sprite_key] = sprite
        else:
            sprite.x = x
            sprite.y = y
        return sprite

    def use_item(self, item_index):
        if item_index < 0 or item_index >= len(self.items):
            return

        item = self.items[item_index]
        if item.type == 'consumable' and item.effect and 'heal' in item.effect:
            self.hp = min(self.stats.max_hp, self.hp + item.effect['heal'])
            self.items.pop(item_index)
        if item.type == 'consumable' and item.effect and 'luck' in item.effect:
            self.stats.luck += item.effect['luck']
            self.items.pop(item_index)
        if item.type == 'consumable' and item.effect and 'defense' in item.effect:
            self.stats.defense += item.effect['defense']
            self.items.pop(item_index)
        if item.type == 'consumable' and item.effect and 'attack' in item.effect:
            self.stats.attack += item.effect['attack']
            self.items.pop(item_index)
        if item.type == 'consumable' and item.effect and 'speed' in item.effect:
            self.stats.speed += item.effect['speed']
            self.items.pop(item_index)
        if item.type == 'consumable' and item.effect and 'level' in item.effect:
            self.add_exp(item.effect['level'] * 20)

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

    def set_sprite_position(self, x, y):
        self.sprite.x = x
        self.sprite.y = y

    def set_hp(self, new_hp):
        self.hp = min(new_hp, self.stats.max_hp)

    def advance_animation(self):
        curFrame = self.sprite.getFrame()
        nextFrame = (curFrame + 1) % self.sprite.frameCount
        self.sprite.setFrame(nextFrame)

    def add_exp(self, amount, addDialog=None):
        if amount <= 0 or self.summon:
            return
        levels_gained = ((self.exp % 20) + amount) // 20
        self.exp += amount

        if addDialog and not self.enemy:
            addDialog([f"{self.name} gained", f"{amount} exp!"], self)

        for _ in range(levels_gained):
            self.level_up(addDialog)

        return self

    def get_weapon(self):
        for item in self.items:
            if item.type == 'weapon' and item.can_use(self.classType):
                return None if item.is_tome() else item
        return None

    def level_up(self, addDialog=None):
        import random
        self.level += 1
        self.next_level_exp += 20

        RN = random.randint(1, 100)
        CF = random.randint(30, 70)
        luck = getattr(self.stats, 'luck', 0)

        if not self.enemy and addDialog:
            addDialog([f"{self.name} level up", f"to {self.level}"], self)
        for stat in ['attack', 'defense', 'max_hp', 'speed', 'luck', 'range']:
            RN = (RN + CF) % 100
            added = 0
            if RN <= getattr(self.growthRates, stat):
                setattr(self.stats, stat, getattr(self.stats, stat) + 1)
                added += 1
                if RN < luck and stat != 'range':
                    setattr(self.stats, stat, getattr(self.stats, stat) + 1)
                    added += 1
            if added > 0 and stat == 'max_hp':
                self.hp += added
            if added > 0 and not self.enemy and addDialog:
                currentValue = getattr(self.stats, stat)
                addDialog([f"{stat} up",f"from {currentValue - added}", f"to {currentValue}!"], self)
    
    def can_move(self):
        return not self.exhausted and not self.moved

    def promote(self, new_class: str):
        self.classType = new_class
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
    __slots__ = ('lines', 'currentlyTalking', 'left_cats', 'right_cats', 'lambda_after', 'decision', 'overlay', 'timeout', 'printIndex', 'charCount')

    def __init__(
        self,
        lines=None,
        left_cats=None,
        right_cats=None,
        currentlyTalking='',
        decision=True,
        lambda_after=None,
        overlay=False,
        timeout=None,
        instaText=False
    ):
        self.lines = lines if lines else []
        self.currentlyTalking = currentlyTalking
        self.left_cats = left_cats if left_cats else []
        self.right_cats = right_cats if right_cats else []
        self.lambda_after = lambda_after
        self.decision = decision
        self.overlay = overlay
        self.timeout = timeout
        lines_str = ''.join(self.lines)
        self.printIndex = 0 if timeout is None and not instaText else len(lines_str)
        self.charCount = len(lines_str)

class House:
    __slots__ = ('position', 'dialogs', 'preVisitedDialogs', 'postVisitDialog', 'visitCondition', 'multipleVisits', 'visited', 'destroyed', 'indestructible')

    def __init__(
        self,
        position,
        preVisitedDialogs=None,
        dialogs=None,
        postVisitDialog=None,
        visitCondition=None,
        multipleVisits=False,
        destroyed=False,
        indestructible=False
    ):
        self.position = position
        self.dialogs = dialogs if dialogs else []
        self.preVisitedDialogs = preVisitedDialogs if preVisitedDialogs else []
        self.postVisitDialog = postVisitDialog if postVisitDialog else []
        def defaultVisitCondition(): return True
        self.visitCondition = visitCondition if visitCondition else defaultVisitCondition
        self.multipleVisits = multipleVisits
        self.visited = False
        self.destroyed = destroyed
        self.indestructible = indestructible

    def visit(self):
        if self.multipleVisits:
            self.visited = False
            return
        if self.visitCondition(): self.visited = True

    def can_visit(self):
        if self.destroyed:
            return False
        if self.preVisitedDialogs and not self.visited and not self.visitCondition():
            return True
        if not self.visited and self.visitCondition():
            return True
        if self.visited and self.postVisitDialog:
            return True
        return self.destroyed

    def get_dialogs(self):
        if self.destroyed:
            print("House is destroyed, no dialogs available.")
            return []
        if self.preVisitedDialogs and not self.visited and not self.visitCondition():
            return self.preVisitedDialogs() if callable(self.preVisitedDialogs) else self.preVisitedDialogs
        if not self.visited and self.visitCondition():
            return self.dialogs() if callable(self.dialogs) else self.dialogs
        if self.visited and self.postVisitDialog:
            return self.postVisitDialog() if callable(self.postVisitDialog) else self.postVisitDialog
        return []

    def destroy(self):
        self.destroyed = True
        self.dialogs = []
        self.preVisitedDialogs = []
        self.postVisitDialog = []
        self.visitCondition = lambda: False

class ShopItem:
    __slots__ = ('item', 'price')

    def __init__(self, item, price):
        self.item: Item = item
        self.price: int = price

class Shop:
    __slots__ = ('position', 'inventory')

    def __init__(
        self,
        position: Position,
        inventory: list[ShopItem] = [],
    ):
        self.position = position
        self.inventory = inventory

class AttackLog:
    __slots__ = (
        'attacker_name', 'attacker_hp', 'attacker_max_hp', 'attacker_enemy', 'attacker_sprite',
        'defender_name', 'defender_hp', 'defender_max_hp', 'defender_enemy', 'defender_sprite',
        'damage', 'old_hp', 'new_hp', 'miss', 'dodge', 'text', 'static_render_time'
    )

    def __init__(
        self,
        attacker_name: str,
        attacker_hp: int,
        attacker_max_hp: int,
        attacker_enemy: bool,
        attacker_sprite,
        defender_name,
        defender_hp: int,
        defender_max_hp: int,
        defender_enemy: bool,
        defender_sprite,
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

class Button:
    __slots__ = ('position', 'pressed', 'pressAction', 'canPress', 'unPressAction', 'canUnpress')

    def __init__(self, position, pressed=None, pressAction=None, unPressAction=None, canUnpress=None, canPress=None):
        self.position = position
        self.pressed = False if pressed is None else pressed
        self.pressAction = pressAction
        self.canPress = canPress if canPress is not None else True
        self.unPressAction = unPressAction
        self.canUnpress = canUnpress if canUnpress is not None else True

    def press(self):
        if self.pressed:
            if not self.unPressAction:
                return
            self.unPressAction()
            self.pressed = False
        else:
            if not self.canPress:
                return
            self.pressed = True
            if self.pressAction:
                self.pressAction()

    def can_press(self):
        if self.pressed:
            return self.canUnpress
        else:
            return self.canPress

class Blockade:
    __slots__ = ('positions', 'cleared')

    def __init__(self, positions, cleared=None):
        self.positions = positions
        self.cleared = cleared if cleared is not None else False

    def clear(self):
        self.cleared = True

    def unclear(self):
        self.cleared = False

class OverlayObject:
    __slots__ = ('position', 'objectName', 'boundPositions')

    def __init__(self, position, objectName, boundPositions):
        self.position = position
        self.objectName = objectName
        self.boundPositions = boundPositions

class Conversation:
    __slots__ = ('dialogs', 'nameOne', 'nameTwo', 'condition')

    def __init__(
        self,
        dialogs,
        nameOne='',
        nameTwo='',
        condition=lambda: True
    ):
        self.dialogs = dialogs
        self.nameOne = nameOne
        self.nameTwo = nameTwo
        self.condition = condition

    get_dialogs = lambda self: self.dialogs() if callable(self.dialogs) else self.dialogs

class Level:
    __slots__ = (
        'map', 'enemies', 'viewport', 'selectorPosition', 'number', 'seizePosition',
        'startingPositions', 'shops', 'houses', 'conversations', 'buttons', 'blockades', 'overlayObjects', 'fightDialogs', 'intro'
    )

    def __init__(
        self,
        map,
        enemies,
        number=1,
        seizePosition=Position(1, 1),
        startingPositions=None,
        shops=None,
        houses=None,
        conversations=None,
        buttons=None,
        blockades=None,
        overlayObjects=None,
        fightDialogs=None
    ):
        self.map = map
        self.enemies = enemies
        self.viewport = Position()
        self.selectorPosition = Position()
        self.number = number
        self.seizePosition = seizePosition
        self.startingPositions = startingPositions if startingPositions else []
        self.shops = shops if shops else []
        self.houses = houses if houses else []
        self.conversations = conversations if conversations else []
        self.buttons = buttons if buttons is not None else []
        self.blockades = blockades if blockades is not None else []
        self.overlayObjects = overlayObjects if overlayObjects is not None else []
        self.fightDialogs = fightDialogs if fightDialogs is not None else []
        self.intro = []

    def find_valid_positions(self, cat: Cat, range: int, party: list[Cat]):
        checkClearMem("Finding Valid Positions")
        map_width = len(self.map[0])
        map_height = len(self.map)
        cx = cat.position.x
        cy = cat.position.y

        def is_walkable(x, y):
            if not (0 <= x < map_width and 0 <= y < map_height):
                return False
            return self.map[y][x] in canWalkOn

        def get_occupying_unit(x, y):
            for unit in party:
                if unit.id != cat.id and unit.position.x == x and unit.position.y == y:
                    return unit
            for unit in self.enemies:
                if unit.id != cat.id and unit.position.x == x and unit.position.y == y:
                    return unit
            return None

        def is_barrier(x, y):
            for blockade in self.blockades:
                if not blockade.cleared:
                    for pos in blockade.positions:
                        if pos.x == x and pos.y == y:
                            return True
            return False

        position_weight = {}
        valid_positions = set()
        queue = [(cx, cy, range)]

        while queue:
            x, y, rem = queue.pop()

            key = (x, y)
            position_weight[key] = rem
            occupying_unit = get_occupying_unit(x, y)
            occupied_by_enemy = occupying_unit is not None and occupying_unit.enemy != cat.enemy
            occupied_by_ally = occupying_unit is not None and occupying_unit.enemy == cat.enemy

            if occupied_by_enemy:
                continue
            elif not occupied_by_ally or (occupied_by_ally and not cat.enemy) or (x == cx and y == cy):
                valid_positions.add((x, y))

            if rem > 0:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x +dx, y + dy
                    if not is_walkable(nx, ny) or is_barrier(nx, ny):
                        continue
                    encumbernce = tileEncumberence.get(self.map[ny][nx], 1)
                    if rem - encumbernce < 0:
                        continue
                    nkey = (nx, ny)
                    if nkey not in position_weight or rem - encumbernce > position_weight[nkey]:
                        queue.append((nx, ny, rem - encumbernce))

        return list(valid_positions)

_cat_sprite = None
_enemy_sprite = None
_button_sprite = None
_cat_head_sprite = None
_cat_frame_cache = {}
_class_sprite_cache = {}
tile_sprite_cache = {}

def clear_tile_cache():
    tile_sprite_cache.clear()
_enemy_frame_cache = {}

def cat_sprite():
    global _cat_sprite
    if _cat_sprite is None:
        from MapData import cat_sprite_sheet
        from thumbyGrayscale import Sprite
        _cat_sprite = Sprite(8, 8, cat_sprite_sheet(), 32, 16, key=1)
    return _cat_sprite

def enemy_sprite():
    global _enemy_sprite
    if _enemy_sprite is None:
        from MapData import enemy_sprite_sheet
        from thumbyGrayscale import Sprite
        _enemy_sprite = Sprite(8, 8, enemy_sprite_sheet(), 32, 16, key=1)
    return _enemy_sprite

_skeleton_sprite = None
_orb_sprite = None

def skeleton_sprite():
    global _skeleton_sprite
    if _skeleton_sprite is None:
        from MapData import cat_skeleton_sprite_sheet
        from thumbyGrayscale import Sprite
        _skeleton_sprite = Sprite(8, 8, cat_skeleton_sprite_sheet(), 32, 16, key=1)
    return _skeleton_sprite

def orb_sprite():
    global _orb_sprite
    if _orb_sprite is None:
        from MapData import light_orb
        from thumbyGrayscale import Sprite
        _orb_sprite = Sprite(8, 8, light_orb(), 32, 16, key=1)
    return _orb_sprite

def button_sprite(x=0, y=0):
    global _button_sprite
    if _button_sprite is None:
        from MapData import button_sprite_sheet
        from thumbyGrayscale import Sprite
        _button_sprite = Sprite(8, 8, button_sprite_sheet(), x, y)
    else:
        _button_sprite.x = x
        _button_sprite.y = y
    return _button_sprite

def cat_head(x=16, y=14):
    global _cat_head_sprite
    if _cat_head_sprite is None:
        from MapData import cat_head_sprite_sheet
        from thumbyGrayscale import Sprite
        _cat_head_sprite = Sprite(40, 40, cat_head_sprite_sheet(), x, y, 1)
    else:
        _cat_head_sprite.x = x
        _cat_head_sprite.y = y
    return _cat_head_sprite

def release_title_sprites():
    global _cat_head_sprite
    _cat_head_sprite = None

def cat_frame_sprite(x=32, y=16, cat_name='cat'):
    from MapData import cat_head_frame
    from thumbyGrayscale import Sprite
    if cat_name in _cat_frame_cache:
        sprite = _cat_frame_cache[cat_name]
        sprite.x = x
        sprite.y = y
        return sprite
    else:
        sprite = Sprite(14, 14, cat_head_frame(cat_name), x, y, key=1)
        _cat_frame_cache[cat_name] = sprite
    return sprite

def enemy_frame_sprite(x=32, y=16, enemy_name='enemy'):
    from MapData import enemy_head_frame
    from thumbyGrayscale import Sprite
    if enemy_name in _enemy_frame_cache:
        sprite = _enemy_frame_cache[enemy_name]
        sprite.x = x
        sprite.y = y
        return sprite
    else:
        sprite = Sprite(14, 14, enemy_head_frame(), x, y, key=1)
        _enemy_frame_cache[enemy_name] = sprite
    return sprite

_PARTY_DEATH_DIALOGS = {
    'cat': [["I guess|this wasn't|meant to be|I have|failed you|all", 'cat']],
    'tac': [["I tried|my best|they are|too strong", 'tac']],
    'mew': [["I refuse|to believe|my cruel|fate", 'mew']],
    'bub': [["I really|wish we had|more time", 'bub']],
    'bao': [["Atleast I|won't have|to see|cat pass,|best this|way", 'bao']],
}

def get_party_death_dialog(name):
    return _PARTY_DEATH_DIALOGS.get(name)

def _build_cat_unit():
    return Cat(
        position=Position(2, 4),
        name='cat',
        stats=Stats(max_hp=10, defense=3, luck=3, range=4),
        growthRates=GrowthRates(attack=45, defense=45, luck=35, range=15),
        items=[itemDict['Stick'], itemDict['Tuna']],
        deathDialog=get_party_death_dialog('cat')
    )

def _build_tac_unit():
    return Cat(
        position=Position(5, 13),
        name='tac',
        stats=Stats(attack=4, speed=4, luck=4, range=4),
        growthRates=GrowthRates(defense=50, speed=70, luck=25, range=15),
        items=[itemDict['Slngsht']],
        deathDialog=get_party_death_dialog('tac')
    )

def _build_mew_unit():
    return Cat(
        name='mew',
        position=Position(3, 1),
        stats=Stats(attack=4, max_hp=10, range=4, defense=3),
        items=[itemDict['Stick']],
        weaponExp=WeaponExp(repeater=10, sword=20),
        growthRates=GrowthRates(attack=50, speed=65, range=15),
        deathDialog=get_party_death_dialog('mew')
    ).add_exp(40, None)

def _build_bub_unit():
    return Cat(
        name='bub',
        position=Position(8, 14),
        stats=Stats(attack=4, defense=3, luck=4, range=4),
        enemy=False,
        classType='sniper',
        items=[itemDict['Repeater'], itemDict['Tuna']],
        growthRates=GrowthRates(attack=60, defense=30, max_hp=55, speed=45, luck=40, range=15),
        weaponExp=WeaponExp(bow=10, longbow=50, repeater=35, sword=10),
        deathDialog=get_party_death_dialog('bub')
    ).add_exp(100, None)

def _build_bao_unit():
    return Cat(
        name='bao',
        position=Position(8,14),
        stats=Stats(attack=5, defense=4, luck=4, range=4),
        enemy=False,
        aiType='stand',
        classType='wizard',
        items=[itemDict['EarthTm'], itemDict['Tuna']],
        growthRates=GrowthRates(attack=45, defense=45, max_hp=65, speed=50, luck=50),
        weaponExp=WeaponExp(lightning=60, water=20, earth=35, sword=10, repeater=15),
        deathDialog=get_party_death_dialog('bao')
    ).add_exp(80, None)

def _build_npc_unit():
    return Cat(
        name='npc',
        position=Position(0, 0),
        enemy=False,
        items=[]
    )

def get_cat():
    return _build_cat_unit()

def get_tac():
    return _build_tac_unit()

def get_mew():
    return _build_mew_unit()

def get_bub():
    return _build_bub_unit()

def get_bao():
    return _build_bao_unit()

def get_npc():
    return _build_npc_unit()

class PathPoint:
    __slots__ = ('position', 'visited')

    def __init__(self, position):
        self.position = position
        self.visited = False

    def mark_visited(self):
        self.visited = True

_enemy_weapon_exp = None

def _shared_weapon_exp():
    global _enemy_weapon_exp
    if _enemy_weapon_exp is None:
        _enemy_weapon_exp = WeaponExp()
    return _enemy_weapon_exp

def generate_enemy(level, position, ai='searchAndDestroy', name='pig', weapon="Stick", classType='pupil', path=None, deathDialog=None, summon=None, summoner=None):
    bigBoiPath = []
    if path is not None:
        for p in path:
            bigBoiPath.append(PathPoint(p))
    e = Cat(
        position=position,
        name=name,
        enemy=True,
        aiType=ai,
        items=[itemDict[weapon]],
        classType=classType,
        weaponExp=_shared_weapon_exp(),
        aiPath=bigBoiPath,
        deathDialog=deathDialog
    )
    e.add_exp((level - 1) * 20, None)
    if summon:
        e.enemy = False
        e.summon = summon
        e.summoner = summoner
        if summon == 'orb':
            e.stats.max_hp = 1
            e.hp = 1
        for item in e.items:
            item.durability = 999
    return e

def fetch_level(level_number, party=None):
    import sys
    cls = 'ActOneLevels' if level_number < 6 else 'ActTwoLevels'
    name = 'Lvl%d' % level_number
    checkClearMem("Loading Level Module")
    mod = __import__(name)
    level = getattr(getattr(mod, cls), '_build_level%d' % level_number)()
    level.intro = list(mod.LevelDialogs().build(party or []).get("intro", ()))
    del mod
    sys.modules.pop(name, None)
    checkClearMem("Level Module Loaded")
    return level

def build_dialogs(specs, left=None, right=None):
    for s in specs:
        if s is None or len(s) < 1:
            continue
        lines, talker = s[0], s[1] if len(s) > 1 else None
        lambda_after = s[2] if len(s) > 2 else None
        lines_split = lines.split('|')
        decision = s[3] if len(s) > 3 else False
        for i in range(0, len(lines_split), 3):
            yield Dialog(
                lines=lines_split[i:i+3],
                left_cats=left if talker is not None else None,
                right_cats=right if talker is not None else None,
                currentlyTalking=talker,
                lambda_after=lambda_after if i + 3 >= len(lines_split) else None,
                decision=decision
            )

def clear_cache():
    global _cat_sprite, _enemy_sprite, _button_sprite, _cat_head_sprite, _skeleton_sprite, _orb_sprite
    _skeleton_sprite = None
    _orb_sprite = None
    _class_sprite_cache.clear()
    _cat_sprite = None
    _enemy_sprite = None
    _button_sprite = None
    _cat_head_sprite = None
    _cat_frame_cache.clear()
    _enemy_frame_cache.clear()
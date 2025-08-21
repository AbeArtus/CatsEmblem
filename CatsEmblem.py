from sys import path as syspath
syspath.insert(0, '/Games/CatsEmblem')

import thumbyGrayscale as thumby

# --- TILE DATA ---
forestTile = (bytearray([255, 255, 255, 255, 127, 255, 255, 255]), bytearray([0, 0, 96, 124, 255, 124, 96, 0]))
mountainTile = (bytearray([255, 255, 255, 255, 255, 252, 227, 31]), bytearray([192, 240, 252, 255, 255, 255, 252, 224]))
grassTile = (bytearray([255, 255, 255, 255, 255, 255, 255, 255]), bytearray([0, 64, 0, 64, 4, 0, 4, 0]))
houseTile = (bytearray([255, 255, 255, 255, 255, 255, 255, 255]), bytearray([8, 252, 142, 239, 239, 142, 252, 8]))

# --- TILE TYPES ---
TILE_GRASS = 0
TILE_FOREST = 1
TILE_MOUNTAIN = 2
TILE_HOUSE = 3
EMPTY = 4

# --- CONSTANTS ---
SCREEN_TILES_X = 9
SCREEN_TILES_Y = 5
MOVE_DELAY = 8

# --- LEVEL DATA ---
level1 = [
    [TILE_MOUNTAIN] * 10,
    [TILE_MOUNTAIN] + [TILE_FOREST] * 8 + [TILE_MOUNTAIN],
    [TILE_MOUNTAIN] + [TILE_FOREST] * 1 + [EMPTY] * 4 + [TILE_FOREST] + [TILE_HOUSE] + [TILE_FOREST] + [TILE_MOUNTAIN],
    [TILE_MOUNTAIN] + [TILE_FOREST] * 1 + [EMPTY] * 6 + [TILE_FOREST] * 1 + [TILE_MOUNTAIN],
    [TILE_MOUNTAIN] + [TILE_FOREST] * 1 + [EMPTY] * 6 + [TILE_FOREST] * 1 + [TILE_MOUNTAIN],
    [TILE_MOUNTAIN] + [TILE_FOREST] * 1 + [EMPTY] * 6 + [TILE_FOREST] * 1 + [TILE_MOUNTAIN],
    [TILE_MOUNTAIN] + [TILE_FOREST] * 1 + [EMPTY] * 6 + [TILE_FOREST] * 1 + [TILE_MOUNTAIN],
    [TILE_MOUNTAIN] + [TILE_FOREST] * 1 + [EMPTY] * 6 + [TILE_FOREST] * 1 + [TILE_MOUNTAIN],
    [TILE_MOUNTAIN] + [TILE_FOREST] * 8 + [TILE_MOUNTAIN],
    [TILE_MOUNTAIN] * 10,
]

# --- CLASSES ---
class Stats:
    def __init__(self, attack=0, defense=0, max_hp=0, speed=0, luck=0, range=1):
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
    def __init__(self, sprite, position, name, selected=False, exhausted=False, stats=None, enemy=False):
        self.sprite = sprite
        self.position = position
        self.selected = selected
        self.exhausted = exhausted
        self.name = name
        self.stats = stats or Stats()
        self.enemy: bool = enemy
        self.hp = self.stats.max_hp  # Initialize HP to max_hp

    def set_position(self, position):
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
        self.hp = min(new_hp, self.stats.max_hp)  # Can't exceed max_hp

class Log:
    def __init__(self, attacker_name, attacker_hp, attacker_enemy, defender_name, defender_hp, defender_enemy, damage, old_hp, new_hp, text):
        self.attacker_name = attacker_name
        self.attacker_hp = attacker_hp
        self.attacker_enemy = attacker_enemy
        self.defender_name = defender_name
        self.defender_hp = defender_hp
        self.defender_enemy = defender_enemy
        self.damage = damage
        self.old_hp = old_hp
        self.new_hp = new_hp
        self.text = text

# --- GAME STATE ---
selectedCatName = "null"
frame = 0
delay = 0
gameState = 'title'
needsUpdate = False
tempPos = Position()
lastPos = Position()
selectorPosition = Position()
viewport_x = 0
viewport_y = 0
option = 0
currentLevel = level1
combat_log = []
current_hp_display = -1

# --- SPRITES ---
selector_sprite = thumby.Sprite(8, 8, (bytearray([126, 255, 255, 255, 255, 255, 255, 126]), bytearray([195, 129, 0, 0, 0, 0, 129, 195])), 32, 16, key=1)
cat_sprite = thumby.Sprite(8, 8, (bytearray([0, 207, 15, 15, 192, 5, 241, 244]), bytearray([0, 0, 0, 0, 0, 0, 0, 0])), 32, 16, key=1)
enemy_sprite = thumby.Sprite(8, 8, (bytearray([0, 207, 15, 15, 192, 5, 241, 244]), bytearray([255, 48, 240, 240, 63, 250, 14, 11])), 32, 16, key=1)

# --- UNITS ---
cat = Cat(cat_sprite, Position(2, 4), 'cat', False, False, Stats(attack=5, defense=3, max_hp=10, speed=8, luck=8, range=1), False)
tac = Cat(cat_sprite, Position(2, 5), 'tac', False, False, Stats(attack=5, defense=2, max_hp=8, speed=8, luck=6, range=1), False)
enemy = Cat(enemy_sprite, Position(6, 4), 'enemy', False, False, Stats(attack=3, defense=2, max_hp=12, speed=3, luck=1, range=1), True)
enemy2 = Cat(enemy_sprite, Position(5, 3), 'enemy2', False, False, Stats(attack=4, defense=1, max_hp=8, speed=5, luck=2, range=1), True)
party = [cat, tac]
enemies = [enemy, enemy2]

# --- FUNCTIONS ---
def get_selected_cat():
    for c in party:
        if c.name == selectedCatName:
            return c
    return None

def can_attack():
    cat = get_selected_cat()
    if not cat:
        return False
    for enemy in enemies:
        dx = abs(enemy.position.x - cat.position.x)
        dy = abs(enemy.position.y - cat.position.y)
        if dx + dy <= 1:
            return True
    return False

def battle(attacker: Cat, defender: Cat):
    global combat_log
    combat_log = []  # Clear previous log
    
    # Record all attacks in the log
    record_attack(attacker, defender)
    record_attack(defender, attacker)

    if attacker.stats.speed * 2 < defender.stats.speed and attacker.stats.luck > 7:
        record_attack(attacker, defender)

    if defender.stats.speed * 2 < attacker.stats.speed and defender.stats.luck > 7:
        record_attack(defender, attacker)

def print_combat_log(log: Log):
    # Apply damage
    print('LOG:')
    print(log.text)
    print(log.attacker_name + 'HP:' + str(log.attacker_hp))
    print(f"{log.defender_name} HP: {log.defender_hp}")
    print(f"{log.defender_name} HP: {log.old_hp} -> {log.new_hp}")
    
def record_attack(attacker, defender):
    global combat_log
    
    # Calculate damage
    damage = calculate_damage(attacker, defender)
    old_hp = defender.hp
    new_hp = old_hp - damage

    log = Log(
        attacker_name=attacker.name,
        attacker_hp=attacker.hp,
        attacker_enemy=attacker.enemy,
        defender_name=defender.name,
        defender_hp=defender.hp,
        defender_enemy=defender.enemy,
        damage=damage,
        old_hp=old_hp,
        new_hp=new_hp,
        text=f"{attacker.name} attacks {defender.name} for {damage} damage!"
    )
    
    # Record the attack
    combat_log.append(log)
    
    defender.set_hp(new_hp)
    
    # Check if defeated
    if defender.hp <= 0:
        print(f"{defender.name} is defeated!")
        if defender in enemies:
            enemies.remove(defender)

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
        print(f"CRITICAL HIT!")
    
    return base_damage

def update_selector_position(dx, dy, level):
    global viewport_x, viewport_y
    new_x = max(0, min(len(level[0]) - 1, selectorPosition.x + dx))
    new_y = max(0, min(len(level) - 1, selectorPosition.y + dy))

    selCat = get_selected_cat()
    if selCat:
        if abs(new_x - selCat.position.x) + abs(new_y - selCat.position.y) > 3:
            return

    selectorPosition.x = new_x
    selectorPosition.y = new_y

    # Update viewport
    if new_x - viewport_x < 1 and viewport_x > 0:
        viewport_x -= 1
    elif new_x - viewport_x > SCREEN_TILES_X - 2 and viewport_x < len(level[0]) - SCREEN_TILES_X:
        viewport_x += 1
    if new_y - viewport_y < 1 and viewport_y > 0:
        viewport_y -= 1
    elif new_y - viewport_y > SCREEN_TILES_Y - 2 and viewport_y < len(level) - SCREEN_TILES_Y:
        viewport_y += 1

def handle_movement():
    global delay, needsUpdate
    
    # Handle immediate button presses
    if thumby.buttonL.justPressed():
        update_selector_position(-1, 0, currentLevel)
        delay = 0
        needsUpdate = True
        return True
    elif thumby.buttonR.justPressed():
        update_selector_position(1, 0, currentLevel)
        delay = 0
        needsUpdate = True
        return True
    elif thumby.buttonU.justPressed():
        update_selector_position(0, -1, currentLevel)
        delay = 0
        needsUpdate = True
        return True
    elif thumby.buttonD.justPressed():
        update_selector_position(0, 1, currentLevel)
        delay = 0
        needsUpdate = True
        return True
    
    # Handle held button presses
    delay += 1
    if delay > MOVE_DELAY:
        if thumby.buttonL.pressed():
            update_selector_position(-1, 0, currentLevel)
            needsUpdate = True
        elif thumby.buttonR.pressed():
            update_selector_position(1, 0, currentLevel)
            needsUpdate = True
        elif thumby.buttonU.pressed():
            update_selector_position(0, -1, currentLevel)
            needsUpdate = True
        elif thumby.buttonD.pressed():
            update_selector_position(0, 1, currentLevel)
            needsUpdate = True
    
    return False

def render_map(level):
    thumby.display.fill(thumby.display.WHITE)
    
    # Render tiles
    for y in range(SCREEN_TILES_Y):
        for x in range(SCREEN_TILES_X):
            map_x = viewport_x + x
            map_y = viewport_y + y
            if 0 <= map_x < len(level[0]) and 0 <= map_y < len(level):
                tile_type = level[map_y][map_x]
                if tile_type == TILE_GRASS:
                    sprite = thumby.Sprite(8, 8, grassTile, x * 8, y * 8)
                elif tile_type == TILE_FOREST:
                    sprite = thumby.Sprite(8, 8, forestTile, x * 8, y * 8)
                elif tile_type == TILE_MOUNTAIN:
                    sprite = thumby.Sprite(8, 8, mountainTile, x * 8, y * 8)
                elif tile_type == TILE_HOUSE:
                    sprite = thumby.Sprite(8, 8, houseTile, x * 8, y * 8)
                else:
                    continue
                thumby.display.drawSprite(sprite)

    # Render units
    for unit in party + enemies:
        if (viewport_x <= unit.position.x < viewport_x + SCREEN_TILES_X and 
            viewport_y <= unit.position.y < viewport_y + SCREEN_TILES_Y):
            unit_screen_x = (unit.position.x - viewport_x) * 8
            unit_screen_y = (unit.position.y - viewport_y) * 8
            unit.set_sprite_position(Position(unit_screen_x, unit_screen_y))
            thumby.display.drawSprite(unit.sprite)

    # Render selector
    selector_sprite.x = (selectorPosition.x - viewport_x) * 8
    selector_sprite.y = (selectorPosition.y - viewport_y) * 8
    thumby.display.drawSprite(selector_sprite)

def map_loop():
    global gameState, selectedCatName, tempPos, lastPos, needsUpdate

    # Handle movement
    handle_movement()
    
    # Handle selection
    if thumby.buttonA.justPressed():
        cat_here = None
        for c in party:
            if c.position == selectorPosition:
                cat_here = c
                break
        if cat_here and not cat_here.exhausted:
            selectedCatName = cat_here.name
            cat_here.set_selected(True)
            tempPos = Position(cat_here.position.x, cat_here.position.y)
            lastPos = Position(selectorPosition.x, selectorPosition.y)
            needsUpdate = False
        elif selectedCatName != 'null':
            cat = get_selected_cat()
            if cat:
                cat.set_position(Position(selectorPosition.x, selectorPosition.y))
                gameState = 'unitSelect'
                needsUpdate = True

    if needsUpdate:
        render_map(currentLevel)
        needsUpdate = False

# --- MAIN LOOP ---
thumby.display.setFPS(8)

while True:
    frame += 1
    
    if gameState == 'title':
        thumby.display.fill(thumby.display.WHITE)
        thumby.display.drawText("Cats Emblem", 3, 24, thumby.display.BLACK)
        title_cat = thumby.Sprite(8, 8, (bytearray([0, 207, 15, 15, 192, 5, 241, 244]), bytearray([0, 0, 0, 0, 0, 0, 0, 0])), 32, 8, key=1)
        thumby.display.drawSprite(title_cat)
        if thumby.buttonA.justPressed():
            gameState = 'map'
            needsUpdate = True

    elif gameState == 'map':
        map_loop()

    elif gameState == 'unitSelect':
        selected = thumby.display.LIGHTGRAY if frame & 1 else thumby.display.BLACK
        thumby.display.drawText("Wait", 10, 8, selected if option == 0 else thumby.display.DARKGRAY)
        if can_attack(): 
            thumby.display.drawText("Fight", 10, 16, selected if option == 1 else thumby.display.DARKGRAY)
        thumby.display.drawText("End Turn", 10, 24, selected if option == 2 else thumby.display.DARKGRAY)
        
        if thumby.buttonU.justPressed() and option > 0: 
            option -= 1
        if thumby.buttonD.justPressed() and option < 2: 
            option += 1
        if thumby.buttonA.justPressed():
            if option == 0:
                cat = get_selected_cat()
                if cat:
                    cat.set_exhausted(True)
                selectedCatName = "null"
                gameState = 'map'
                needsUpdate = True
            elif option == 1:
                gameState = 'enemy-select'
                needsUpdate = True
                option = 0
            elif option == 2:
                gameState = 'map'
                needsUpdate = True
        if thumby.buttonB.justPressed():
            cat = get_selected_cat()
            if cat:
                cat.set_position(tempPos)
            selectedCatName = "null"
            gameState = 'map'
            needsUpdate = True

    elif gameState == 'enemy-select':
        # Get enemies in range of the selected cat
        selected_cat = get_selected_cat()
        enemies_in_range = []
        
        if selected_cat:
            for enemy in enemies:
                dx = abs(enemy.position.x - selected_cat.position.x)
                dy = abs(enemy.position.y - selected_cat.position.y)
                if dx + dy <= selected_cat.stats.range:
                    enemies_in_range.append(enemy)
                    # If selector is on the selected cat, move to first enemy found
                    if selectorPosition == selected_cat.position:
                        selectorPosition.x = enemy.position.x
                        selectorPosition.y = enemy.position.y
        
        # If no enemies in range, return to unit select
        if len(enemies_in_range) == 0:
            gameState = 'unitSelect'
            option = 0
        else:
            # Navigate between enemies in range
            if thumby.buttonU.justPressed() or thumby.buttonL.justPressed():
                option = (option - 1) % len(enemies_in_range)
                # Move cursor to the selected enemy's position
                selectorPosition.x = enemies_in_range[option].position.x
                selectorPosition.y = enemies_in_range[option].position.y
                needsUpdate = True
            elif thumby.buttonD.justPressed() or thumby.buttonR.justPressed():
                option = (option + 1) % len(enemies_in_range)
                # Move cursor to the selected enemy's position
                selectorPosition.x = enemies_in_range[option].position.x
                selectorPosition.y = enemies_in_range[option].position.y
                needsUpdate = True
            
            # Update viewport to follow cursor
            if selectorPosition.x - viewport_x < 1 and viewport_x > 0:
                viewport_x -= 1
            elif selectorPosition.x - viewport_x > SCREEN_TILES_X - 2 and viewport_x < len(currentLevel[0]) - SCREEN_TILES_X:
                viewport_x += 1
            if selectorPosition.y - viewport_y < 1 and viewport_y > 0:
                viewport_y -= 1
            elif selectorPosition.y - viewport_y > SCREEN_TILES_Y - 2 and viewport_y < len(currentLevel) - SCREEN_TILES_Y:
                viewport_y += 1
            
            # Handle selection
            if thumby.buttonA.justPressed():
                # Get the selected enemy and perform combat
                selected_cat = get_selected_cat()
                selected_enemy = enemies_in_range[option]
                
                # Perform all attacks and record them
                battle(selected_cat, selected_enemy)
                selected_cat.set_exhausted(True)
                selecteCatName = "null"
                gameState = 'combat-log'
            elif thumby.buttonB.justPressed():
                gameState = 'unitSelect'
                option = 0
            
            # Render the map with enemy selection overlay
            if needsUpdate:
                render_map(currentLevel)
                needsUpdate = False

    elif gameState == 'combat-log':
        if len(combat_log) > 0:
            thumby.display.fill(thumby.display.WHITE)
            if (current_hp_display == - 1):
                current_hp_display = combat_log[0].defender_hp
            log = combat_log[0]
            attackerHealth = log.attacker_hp
            defenderHealth = current_hp_display
            
            # Display based on who is attacking
            if log.attacker_enemy:
                # Enemy is attacking (left side)
                thumby.display.drawText(log.attacker_name, 0, 0, thumby.display.BLACK)
                thumby.display.drawText(f"HP:{attackerHealth}", 0, 8, thumby.display.BLACK)
                thumby.display.drawText(log.defender_name, 45, 0, thumby.display.DARKGRAY)
                thumby.display.drawText(f"HP:{defenderHealth}", 45, 8, thumby.display.DARKGRAY)
            else:
                # Party is attacking (right side)
                thumby.display.drawText(log.attacker_name, 45, 0, thumby.display.BLACK)
                thumby.display.drawText(f"HP:{attackerHealth}", 45, 8, thumby.display.BLACK)
                thumby.display.drawText(log.defender_name, 0, 0, thumby.display.DARKGRAY)
                thumby.display.drawText(f"HP:{defenderHealth}", 0, 8, thumby.display.DARKGRAY)
            
            if current_hp_display <= combat_log[0].new_hp:
                print_combat_log(combat_log[0])
                combat_log.pop(0)
                if len(combat_log) > 0:
                    current_hp_display = combat_log[0].old_hp
            # Animate HP counting down
            elif (frame % 7 == 1): 
                current_hp_display = current_hp_display - 1
        else:
            needsUpdate = True
            current_hp_display = -1
            if (frame % 7 == 1):
                gameState = 'map'
    
    thumby.display.update()

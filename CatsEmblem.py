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
map1 = [
    [TILE_MOUNTAIN] * 11,
    [TILE_MOUNTAIN] + [TILE_FOREST] * 9 + [TILE_MOUNTAIN],
    [TILE_MOUNTAIN] + [TILE_FOREST] * 2 + [EMPTY] * 2 + 2 * [TILE_GRASS] + [TILE_FOREST] + [TILE_HOUSE] + [TILE_FOREST] + [TILE_MOUNTAIN],
    [TILE_MOUNTAIN] + [TILE_FOREST] * 2 + [EMPTY] * 3 + 3 * [TILE_GRASS] + [TILE_FOREST] * 1 + [TILE_MOUNTAIN],
    [TILE_MOUNTAIN] + [TILE_FOREST] * 1 + [TILE_GRASS] * 1 + [EMPTY] * 6 + [TILE_FOREST] * 1 + [TILE_MOUNTAIN],
    [TILE_MOUNTAIN] + [TILE_FOREST] * 1 + [TILE_GRASS] * 3 + [EMPTY] * 4 + [TILE_FOREST] * 1 + [TILE_MOUNTAIN],
    [TILE_MOUNTAIN] + [TILE_FOREST] * 2 + [EMPTY] * 6 + [TILE_FOREST] * 1 + [TILE_MOUNTAIN],
    [TILE_MOUNTAIN] + [TILE_FOREST] * 2 + [EMPTY] * 3 + 3 * [TILE_GRASS] + [TILE_FOREST] * 1 + [TILE_MOUNTAIN],
    [TILE_MOUNTAIN] + [TILE_FOREST] * 9 + [TILE_MOUNTAIN],
    [TILE_MOUNTAIN] * 11,
]

# --- CLASSES ---
class Stats:
    def __init__(self, attack, defense, max_hp, speed, luck, range):
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
        self.sprite: thumby.Sprite = sprite
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

    def advance_animation(self):
        curFrame = self.sprite.getFrame()
        nextFrame = (curFrame + 1) % self.sprite.frameCount
        print("Advancing animation for", self.name, "from", curFrame, "to", nextFrame)
        self.sprite.setFrame(nextFrame)

class Log:
    def __init__(
            self,
            attacker_name,
            attacker_hp,
            attacker_enemy,
            attacker_sprite,
            defender_name,
            defender_hp,
            defender_enemy,
            defender_sprite,
            damage, old_hp,
            new_hp,
            text
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
    def __init__(self, map, enemies):
        self.map = map
        self.enemies = enemies

class GameState:
    def __init__(self, level, party):
        self.level = level
        self.party = party
        self.current_turn = 'player'

# --- GAME STATE ---
selectedCatName = "null"
activeEnemy = None
readyForBattle = False
frame = 0
delay = 0
state = 'title'
needsUpdate = False
tempPos = Position()
lastPos = Position()
selectorPosition = Position()
viewport_x = 0
viewport_y = 0
option = 0
combat_log = []
current_hp_display = -1

# --- SPRITES ---
selector_sprite = thumby.Sprite(8, 8, (bytearray([126, 255, 255, 255, 255, 255, 255, 126]), bytearray([195, 129, 0, 0, 0, 0, 129, 195])), 32, 16, key=1)
def cat_sprite(): return thumby.Sprite(8, 8, (bytearray([0, 207, 15, 15, 192, 5, 241, 244, 6, 201, 15, 15, 192, 5, 241, 244, 7, 201, 14, 15, 192, 5, 241, 244, 1, 206, 15, 15, 192, 5, 241, 244])), 32, 16, key=1)
def enemy_sprite(): return thumby.Sprite(8, 8, (bytearray([3, 143, 2, 4, 129, 1, 228, 242, 3, 143, 2, 4, 145, 17, 196, 242, 7, 139, 2, 4, 129, 1, 228, 242]), bytearray([252, 112, 253, 251, 118, 246, 27, 13, 252, 112, 253, 251, 102, 230, 59, 13, 248, 116, 253, 251, 118, 246, 27, 13])), 32, 16, key=1)

# --- UNITS ---
catSprite = cat_sprite()
cat = Cat(catSprite, Position(2, 4), 'cat', False, False, Stats(attack=5, defense=3, max_hp=10, speed=8, luck=8, range=4), False)
tacSprite = cat_sprite()
tac = Cat(tacSprite, Position(2, 5), 'tac', False, False, Stats(attack=5, defense=2, max_hp=8, speed=8, luck=6, range=5), False)
enemy1Sprite = enemy_sprite()
enemy = Cat(enemy1Sprite, Position(6, 4), 'enemy', False, False, Stats(attack=3, defense=2, max_hp=12, speed=3, luck=1, range=3), True)
enemy2Sprite = enemy_sprite()
enemy2 = Cat(enemy2Sprite, Position(5, 3), 'enemy', False, False, Stats(attack=4, defense=1, max_hp=8, speed=5, luck=2, range=3), True)

level1 = Level(map1, [enemy, enemy2])

gameState = GameState(level1, [cat, tac])

# --- FUNCTIONS ---
def get_selected_cat():
    for c in gameState.party:
        if c.name == selectedCatName:
            return c
    return None

def can_attack():
    cat = get_selected_cat()
    if not cat:
        return False
    for enemy in gameState.level.enemies:
        dx = abs(enemy.position.x - cat.position.x)
        dy = abs(enemy.position.y - cat.position.y)
        if dx + dy <= 1:
            return True
    return False

def battle(attacker: Cat, defender: Cat):
    global combat_log
    
    # Record all attacks in the log
    record_attack(attacker, defender)
    if defender.hp <= 0:
        return
    record_attack(defender, attacker)
    if attacker.hp <= 0:
        return

    if attacker.stats.speed * 2 < defender.stats.speed and attacker.stats.luck > 7:
        record_attack(attacker, defender)
    if defender.hp <= 0:
        return

    if defender.stats.speed * 2 < attacker.stats.speed and defender.stats.luck > 7:
        record_attack(defender, attacker)
    
def record_attack(attacker: Cat, defender: Cat):
    global combat_log

    damage = calculate_damage(attacker, defender)
    old_hp = defender.hp
    new_hp = old_hp - damage

    log = Log(
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

    combat_log.append(log)
    
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
        update_selector_position(-1, 0, gameState.level.map)
        delay = 0
        needsUpdate = True
        return True
    elif thumby.buttonR.justPressed():
        update_selector_position(1, 0, gameState.level.map)
        delay = 0
        needsUpdate = True
        return True
    elif thumby.buttonU.justPressed():
        update_selector_position(0, -1, gameState.level.map)
        delay = 0
        needsUpdate = True
        return True
    elif thumby.buttonD.justPressed():
        update_selector_position(0, 1, gameState.level.map)
        delay = 0
        needsUpdate = True
        return True
    
    # Handle held button presses
    delay += 1
    if delay > MOVE_DELAY:
        if thumby.buttonL.pressed():
            update_selector_position(-1, 0, gameState.level.map)
            needsUpdate = True
        elif thumby.buttonR.pressed():
            update_selector_position(1, 0, gameState.level.map)
            needsUpdate = True
        elif thumby.buttonU.pressed():
            update_selector_position(0, -1, gameState.level.map)
            needsUpdate = True
        elif thumby.buttonD.pressed():
            update_selector_position(0, 1, gameState.level.map)
            needsUpdate = True
    
    return False

def render_map(level):
    global viewport_x, viewport_y, gameState, selectorPosition
    thumby.display.fill(thumby.display.WHITE)

    ## TODO adjust viewport to keep selector in view can be more that 1 tile away !!!
    
    # Render tiles
    for y in range(SCREEN_TILES_Y):
        for x in range(SCREEN_TILES_X):
            map_x = viewport_x + x
            map_y = viewport_y + y
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
                else:
                    continue
                thumby.display.drawSprite(sprite)

    for unit in gameState.party + gameState.level.enemies:
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
    global state, selectedCatName, tempPos, lastPos, needsUpdate, gameState

    # Handle movement
    handle_movement()
    
    # Handle selection
    if thumby.buttonA.justPressed():
        cat_here = None
        for c in gameState.party:
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
                state = 'unitSelect'
                needsUpdate = True

    if needsUpdate:
        render_map(gameState.level.map)
        needsUpdate = False

def animate_cats():
    global needsUpdate, gameState
    for c in gameState.party + gameState.level.enemies:
        print("Animating", c.name)
        c.advance_animation()
    ## now re-render all the cats
    selector_sprite.setFrame((selector_sprite.getFrame() + 1) % selector_sprite.frameCount)
    needsUpdate = True
    

# --- MAIN LOOP ---
thumby.display.setFPS(8)

while True:
    frame += 1

    partyFullyExhausted = True
    for p in gameState.party:
        if not p.exhausted:
            partyFullyExhausted = False
    if partyFullyExhausted:
        state = 'enemy-turn'

    if (frame % 5 == 0): animate_cats()

    if needsUpdate:
        render_map(gameState.level.map)
        needsUpdate = False

    if len(combat_log) > 0:
        thumby.display.fill(thumby.display.WHITE)
        if (current_hp_display == - 1):
            current_hp_display = combat_log[0].defender_hp
        log = combat_log[0]
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

        if current_hp_display <= combat_log[0].new_hp or current_hp_display <= 0:
            combat_log.pop(0)
            if len(combat_log) > 0:
                current_hp_display = combat_log[0].old_hp
        # Animate HP counting down
        elif (frame % 7 == 1): 
            current_hp_display = current_hp_display - 1
        if len(combat_log) == 0:
            needsUpdate = True
            current_hp_display = -1
            print("-----")

    elif state == 'title':
        thumby.display.fill(thumby.display.WHITE)
        thumby.display.drawText("Cats Emblem", 3, 24, thumby.display.BLACK)
        title_cat = thumby.Sprite(8, 8, (bytearray([0, 207, 15, 15, 192, 5, 241, 244]), bytearray([0, 0, 0, 0, 0, 0, 0, 0])), 32, 8, key=1)
        thumby.display.drawSprite(title_cat)
        if thumby.buttonA.justPressed():
            state = 'map'
            needsUpdate = True

    elif state == 'map':
        map_loop()

    elif state == 'unitSelect':
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
                state = 'map'
                needsUpdate = True
            elif option == 1:
                state = 'enemy-select'
                needsUpdate = True
                option = 0
            elif option == 2:
                selectedCatName = "null"
                state = 'enemy-turn'
                needsUpdate = True
        if thumby.buttonB.justPressed():
            cat = get_selected_cat()
            if cat:
                cat.set_position(tempPos)
            selectedCatName = "null"
            state = 'map'
            needsUpdate = True

    elif state == 'enemy-select':
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
                    if selectorPosition == selected_cat.position:
                        selectorPosition.x = enemy.position.x
                        selectorPosition.y = enemy.position.y

        # If no enemies in range, return to unit select
        if len(enemies_in_range) == 0:
            state = 'unitSelect'
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
            elif selectorPosition.x - viewport_x > SCREEN_TILES_X - 2 and viewport_x < len(gameState.level.map)[0] - SCREEN_TILES_X:
                viewport_x += 1
            if selectorPosition.y - viewport_y < 1 and viewport_y > 0:
                viewport_y -= 1
            elif selectorPosition.y - viewport_y > SCREEN_TILES_Y - 2 and viewport_y < len(gameState.level.map) - SCREEN_TILES_Y:
                viewport_y += 1

            # Handle selection
            if thumby.buttonA.justPressed():
                # Get the selected enemy and perform combat
                selected_cat = get_selected_cat()
                selected_enemy = enemies_in_range[option]
                
                # Perform all attacks and record them
                battle(selected_cat, selected_enemy)
                selected_cat.set_exhausted(True)
                selectedCatName = "null"
                state = 'map'
            elif thumby.buttonB.justPressed():
                state = 'unitSelect'
                option = 0

            # Render the map with enemy selection overlay
            if needsUpdate:
                render_map(gameState.level.map)
                needsUpdate = False
    
    elif state == 'enemy-turn':
        ## loop through the enemies and move/attack
        if frame % 10 == 1:  # slow down enemy actions
            print("Enemy tick")
            if activeEnemy:
                # Check if a party member is in range to attack
                target = None
                for p in gameState.party:
                    dx = abs(p.position.x - activeEnemy.position.x)
                    dy = abs(p.position.y - activeEnemy.position.y)
                    if dx + dy <= activeEnemy.stats.range + 1:
                        target = p
                        break
                # move next the target on the tile one away to attack
                ## check the for tiles around the target
                keyTile = [
                    Position(target.position.x + 1, target.position.y),
                    Position(target.position.x - 1, target.position.y),
                    Position(target.position.x, target.position.y + 1),
                    Position(target.position.x, target.position.y - 1),
                ] if target else []
                hasMove = False
                if not readyForBattle:
                    potentialMoves = []
                    for t in keyTile:
                        dx = abs(t.x - activeEnemy.position.x)
                        dy = abs(t.y - activeEnemy.position.y)
                        ## also check that the tile is not occupied by another enemy or party member
                        occupied = False
                        for p in gameState.party:
                            if p.position == t:
                                occupied = True
                                break
                        for e in gameState.level.enemies:
                            if e.position == t:
                                occupied = True
                                break
                        if dx + dy < activeEnemy.stats.range + 1 and not occupied:
                            # move to this tile
                            potentialMoves.append(t)
                            hasMove = True
                            break
                    if len(potentialMoves) > 0:
                        # pick the closest tile to move to from the list
                        closestTile = potentialMoves[0]
                        closestDist = abs(closestTile.x - activeEnemy.position.x) + abs(closestTile.y - activeEnemy.position.y)
                        for t in potentialMoves:
                            dist = abs(t.x - activeEnemy.position.x) + abs(t.y - activeEnemy.position.y)
                            if dist < closestDist:
                                closestTile = t
                                closestDist = dist
                        print("Enemy moving to", closestTile.x, closestTile.y)
                        activeEnemy.set_position(closestTile)
                        selectorPosition.x = activeEnemy.position.x
                        selectorPosition.y = activeEnemy.position.y
                        needsUpdate = True

                if target and readyForBattle:
                    print("Enemy attacking", target.name)
                    battle(activeEnemy, target)
                    activeEnemy.set_exhausted(True)
                    activeEnemy = None
                    needsUpdate = True
                    readyForBattle = False
                elif not readyForBattle:
                    print("Enemy ready for battle")
                    selectorPosition.x = activeEnemy.position.x
                    selectorPosition.y = activeEnemy.position.y
                    readyForBattle = True
                    needsUpdate = True
                elif not hasMove:
                    print("Enemy cannot move or attack, ending turn")
                    activeEnemy.set_exhausted(True)
                    activeEnemy = None
                    needsUpdate = True
                    readyForBattle = False
            for e in gameState.level.enemies:
                # just get the first not exhausted enemy for now
                if not e.exhausted:
                    activeEnemy = e
                    selectorPosition.x = activeEnemy.position.x
                    selectorPosition.y = activeEnemy.position.y
                    needsUpdate = True
                    print("Next enemy:", e.name)
                    break

        ## check if all enemies are exhausted
        if all(e.exhausted for e in gameState.level.enemies):
            # All enemies exhausted, reset party and return to map
            for p in gameState.party:
                p.set_exhausted(False)
            for e in gameState.level.enemies:
                e.set_exhausted(False)
            state = 'map'
            needsUpdate = True

        if needsUpdate:
            render_map(gameState.level.map)
            needsUpdate = False

    thumby.display.update()

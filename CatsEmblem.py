import gc
import time

def checkClearMem(message: str = ''):
    gc.collect()
    print("Free memory (CatsEmblem.py):", gc.mem_free(), message)

from sys import path as syspath
syspath.insert(0, '/Games/CatsEmblem')

print("Game Starting mem (CatsEmblem.py):", gc.mem_free())

import machine
import thumbyGrayscale as thumby
machine.freq(125_000_000)
checkClearMem('grayscale')
thumby.display.setFPS(8)
thumby.display.fill(thumby.display.BLACK)
thumby.display.drawText("Loading", 6, 16, thumby.display.WHITE)
thumby.display.show()

from Shared import Cat, Position, cat_sprite, classAdvantages, weaponAdvantages, Item, Dialog, get_tile_data, canWalkOn, tileEvation, Menu, AttackLog, Option
checkClearMem('shared imported')
thumby.display.fill(thumby.display.BLACK)
thumby.display.drawText("Loading.", 6, 16, thumby.display.WHITE)
thumby.display.show()
from GameState import GameState
checkClearMem('gamestate imported')
thumby.display.fill(thumby.display.BLACK)
thumby.display.drawText("Loading..", 6, 16, thumby.display.WHITE)
thumby.display.show()
from Levels import set_game_state_callbacks
checkClearMem('levels imported')
thumby.display.fill(thumby.display.BLACK)
thumby.display.drawText("Loading...", 6, 16, thumby.display.WHITE)
thumby.display.show()
thumby.display.enableGrayscale()
checkClearMem('post imports')

# Define the gameState object
gameState = GameState()

# Define the setter functions
def add_to_party(cat):
    gameState.party.append(cat)

def update_bank(amount):
    gameState.bank += amount

def give_item(position: Position, item: Item):
    for p in gameState.party:
        if p.position == position and len(p.items) < 4:
            p.items.append(item)
            return True
    return False
            
def can_give_item(position: Position):
    for p in gameState.party:
        if p.position == position and len(p.items) < 4:
            return True
    return False

def get_cat_at_pos(position: Position):
    for p in gameState.party:
        if p.position.__eq__(position):
            return p

def get_selected_cat():
    if gameState.select_cat is not None:
        return gameState.get_selected_cat()
    return None

# Pass the setter functions to Levels
set_game_state_callbacks(add_to_party, update_bank, can_give_item, give_item, get_cat_at_pos, get_selected_cat)

_selector_sprite = None

def get_selector_sprite():
    global _selector_sprite
    if _selector_sprite is None:
        _selector_sprite = thumby.Sprite(10, 10, (bytearray([120,254,254,255,255,255,255,254,254,120,0,1,1,3,3,3,3,1,1,0]), bytearray([204,0,1,1,0,0,1,1,0,204,0,0,2,2,0,0,2,2,0,0])), 32, 16, key=1)
    return _selector_sprite

# --- CONSTANTS ---
SCREEN_TILES_X = 9
SCREEN_TILES_Y = 5

# --- GAME STATE ---
frame = 0
activeEnemy = None
readyForBattle = False
option = 0
current_hp_display = -1
_tile_sprite_cache = {}
_dialog_portrait_sprite = None

def get_render_tile_sprite(tile_type: int, map_x: int, map_y: int, screen_x: int, screen_y: int):
    if tile_type == 4:
        return None

    sprite_data, xFlip, yFlip = get_tile_data(tile_type)

    if sprite_data is None:
        print(f"Error: No sprite data found for tile type {tile_type}")

    if tile_type == 0:
        key = (tile_type, (map_y & 1) == 0)
    elif tile_type == 1:
        xEven = (map_x & 1) == 0
        yEven = (map_y & 1) == 0
        shouldFlip = (xEven and not yEven) or (not xEven and yEven)
        key = (tile_type, shouldFlip)
    else:
        key = (tile_type, xFlip, yFlip)

    sprite = _tile_sprite_cache.get(key)
    if sprite is None:
        if tile_type == 0:
            sprite = thumby.Sprite(8, 8, sprite_data, 0, 0, -1, key[1])
        elif tile_type == 1:
            sprite = thumby.Sprite(8, 8, sprite_data, 0, 0, -1, key[1])
        else:
            sprite = thumby.Sprite(8, 8, sprite_data, 0, 0, -1, xFlip, yFlip)
        _tile_sprite_cache[key] = sprite

    sprite.x = screen_x * 8
    sprite.y = screen_y * 8
    return sprite

def get_dialog_portrait_sprite():
    global _dialog_portrait_sprite
    if _dialog_portrait_sprite is None:
        _dialog_portrait_sprite = cat_sprite()
    return _dialog_portrait_sprite

def addDialog(dialog: list[str], cat: Cat = None):
    global gameState
    dialog = Dialog(
        lines=dialog,
        left_cats=[cat],
        right_cats=[],
        currentlyTalking=cat.name if cat else "",
        lambda_after=None
    )
    gameState.add_dialog(dialog)

def battle(attacker: Cat, defender: Cat):
    global gameState

    attackerExp = 0
    defenderExp = 0

    print("Battle begins against,", attacker.name, 'and', defender.name)
    print(' ')
    print(' ', attacker.name, 'attacks')
    attackerExp =+ record_attack(attacker, defender)
    if defender.hp <= 0:
        attacker.add_exp(defender.stats.max_hp, addDialog)
        return

    defender_weapon = defender.get_weapon()
    defender_ranges = defender_weapon.get_range() if defender_weapon else []
    dx = abs(attacker.position.x - defender.position.x)
    dy = abs(attacker.position.y - defender.position.y)
    if dx + dy in defender_ranges:
        print(' ')
        print(' ', defender.name, 'attacks')
        defenderExp += record_attack(defender, attacker)
        if attacker.hp <= 0:
            defender.add_exp(attacker.stats.max_hp, addDialog)
            return

    if attacker.stats.speed * int(1.5) > defender.stats.speed:
        print(' ')
        print(' ', attacker.name, 'attacks')
        attackerExp += record_attack(attacker, defender, is_counter=True)
    if defender.hp <= 0:
        attacker.add_exp(defender.stats.max_hp, addDialog)
        return

    if dx + dy in defender_ranges:
        if defender.stats.speed * int(1.5) > attacker.stats.speed:
            print(' ')
            print(' ', defender.name, 'attacks')
            attackerExp += record_attack(defender, attacker, is_counter=True)
        if attacker.hp <= 0:
            defender.add_exp(attacker.stats.max_hp, addDialog)
            return

    defender.add_exp(defenderExp, addDialog)
    attacker.add_exp(attackerExp, addDialog)
    
def record_attack(attacker: Cat, defender: Cat, is_counter: bool = False) -> int:
    global gameState
    import random
    attackerWeapon = attacker.get_weapon()

    if attackerWeapon is None:
        return 0

    randInt = random.randint(1, 100)

    tileEvationBonus = tileEvation.get(gameState.level.map[defender.position.y][defender.position.x], 0)

    defenderDodge = defender.stats.defense + defender.stats.speed + defender.stats.luck
    attackerAttackPower = attacker.stats.speed + attacker.stats.luck + attacker.stats.attack
    print('   Attack Record')
    print('    defenderDodge', defenderDodge)
    print('    attackerAttackPower', attackerAttackPower)
    print('    dodge odds: ', (defenderDodge - attackerAttackPower) * 3,)
    print("    randInt: ", randInt)
    attackDodge = randInt < (defenderDodge - attackerAttackPower) * 3
    print("    attackDodge", attackDodge)
    randInt = int("".join(reversed(f"{randInt:02}")))
    print("    randInt: ", randInt)
    print("    Weapon accuracy", attackerWeapon.accuracy)
    attackHit = randInt <= attackerWeapon.accuracy - tileEvationBonus
    print("    attackHit", attackHit)

    damage = calculate_damage(attacker, defender) if attackHit and not attackDodge else 0
    old_hp = defender.hp
    new_hp = old_hp - damage

    log = AttackLog(
        attacker_name=attacker.name,
        attacker_hp=attacker.hp,
        attacker_max_hp=attacker.stats.max_hp,
        attacker_enemy=attacker.enemy,
        attacker_sprite=attacker.sprite,
        defender_name=defender.name,
        defender_hp=defender.hp,
        defender_max_hp=defender.stats.max_hp,
        defender_enemy=defender.enemy,
        defender_sprite=defender.sprite,
        damage=damage,
        old_hp=old_hp,
        new_hp=new_hp,
        miss=not attackHit,
        dodge=attackDodge,
        text=f"{'' if attackHit else 'miss'}",
        static_render_time= 2 if not attackHit or attackDodge or damage == 0 else 0
    )

    gameState.combat_log.append(log)

    defender.set_hp(new_hp)

    if defender.hp <= 0:
        if defender in gameState.level.enemies:
            gameState.level.enemies.remove(defender)
        if defender in gameState.party:
            gameState.party.remove(defender)
    expMultiplier = defender.level / attacker.level

    return max(int(damage * expMultiplier + 0.5), 1)

def calculate_damage(attacker: Cat, defender: Cat):
    global gameState
    import random
    attackerWeapon: Item = attacker.get_weapon()
    defenderWeapon: Item = defender.get_weapon()

    party = gameState.party if not attacker.enemy else gameState.level.enemies
    # 5 for eah party member adjacenet
    assist = 0
    for member in party :
        if abs(member.position.x - attacker.position.x) + abs(member.position.y - attacker.position.y) <= 1:
            assist += 5

    if attackerWeapon is None:
        return 0

    hasWeaponAdvantage = attackerWeapon and defenderWeapon and weaponAdvantages.get(attackerWeapon.type) == defenderWeapon.type or attackerWeapon is not None and defenderWeapon is None
    hasClassAdvantage = classAdvantages.get(attacker.classType) == defender.classType
    defenderHasWeaponAdvantage = attackerWeapon and defenderWeapon and weaponAdvantages.get(defenderWeapon.type) == attackerWeapon.type or attackerWeapon is None and defenderWeapon is not None
    defenderHasClassAdvantage = classAdvantages.get(defender.classType) == attacker.classType
    attackerLowHP = attacker.hp <= attacker.stats.max_hp // 4
    defenderLowHP = defender.hp <= defender.stats.max_hp // 4
    # print all of this out cmoon co pitlo font be lazy
    print('')
    print("    hasWeaponAdvantage: ", hasWeaponAdvantage)
    print("    hasClassAdvantage: ", hasClassAdvantage)
    print("    defenderHasWeaponAdvantage: ", defenderHasWeaponAdvantage)
    print("    defenderHasClassAdvantage: ", defenderHasClassAdvantage)
    print("    attackerLowHP: ", attackerLowHP)
    print("    defenderLowHP: ", defenderLowHP)

    attacker.weaponExp.increase_exp(attackerWeapon.weaponType, 1)

    base_damage = attacker.stats.attack + attacker.get_weapon().attack - defender.stats.defense
    bonus_damage = 0 + attacker.weaponExp.get_weapon_attack_bonus(attackerWeapon.type)
    if hasWeaponAdvantage:
        bonus_damage += int(base_damage * .5)
    if hasClassAdvantage:
        bonus_damage += int(base_damage * .5)

    if defenderHasWeaponAdvantage:
        bonus_damage -= int(base_damage * .5)
    if defenderHasClassAdvantage:
        bonus_damage -= int(base_damage * .5)
        

    crit_chance = (attacker.stats.luck * (1.5 if hasClassAdvantage or hasWeaponAdvantage else 1) * (2 if attackerLowHP else 1) + assist )
    randInt = random.randint(1, 100)
    print("    crit_chance: ", crit_chance)
    print("    randInt: ", randInt)
    if randInt < crit_chance:
        bonus_damage += base_damage

    print('')
    print('    base_damage', base_damage)
    print('    bonus_damage', bonus_damage)
    print("   Final Damange: ", base_damage + bonus_damage)
    print('')
    
    return base_damage + bonus_damage if base_damage + bonus_damage > 0 else 0

def handle_movement():
    startTime = time.ticks_ms()
    global gameState

    x = gameState.level.selectorPosition.x
    y = gameState.level.selectorPosition.y
    isCatSelected = gameState.selectedCatId is not None

    directions = {
        "L": (-1, 0),
        "R": (1, 0),
        "U": (0, -1),
        "D": (0, 1)
    }

    for button, (dx, dy) in directions.items():
        if getattr(thumby, f"button{button}").justPressed() or getattr(thumby, f"button{button}").pressed():
            new_x, new_y = x + dx, y + dy
            if 0 <= new_y < len(gameState.level.map) and 0 <= new_x < len(gameState.level.map[0]):
                isWalkable = gameState.level.map[new_y][new_x] in canWalkOn and canWalkOn[gameState.level.map[new_y][new_x]]
            else:
                isWalkable = False
            for unit in gameState.level.enemies:
                if isCatSelected and unit.id == gameState.selectedCatId:
                    continue
                elif unit.position.x == new_x and unit.position.y == new_y:
                    isWalkable = False
                    break
            canUpdate = isWalkable or gameState.selectedCatId is None
            gameState.update_selector_position(x + (dx if canUpdate else 0), y + (dy if canUpdate else 0))
            return True
    return False

def render_map(level):
    global gameState
    selector_sprite = get_selector_sprite()
    thumby.display.fill(thumby.display.WHITE)

    text = None

    for y in range(SCREEN_TILES_Y):
        for x in range(SCREEN_TILES_X):
            map_x = gameState.level.viewport.x + x
            map_y = gameState.level.viewport.y + y
            if 0 <= map_x < len(level[0]) and 0 <= map_y < len(level):
                tile_type = level[map_y][map_x]
                sprite = get_render_tile_sprite(tile_type, map_x, map_y, x, y)
                if sprite is None:
                    continue
                if sprite.frameCount > 0:
                    sprite.setFrame((frame // 10) % sprite.frameCount)
                thumby.display.drawSprite(sprite)

    for unit in gameState.party + gameState.level.enemies:
        if (gameState.level.viewport.x <= unit.position.x < gameState.level.viewport.x + SCREEN_TILES_X and 
            gameState.level.viewport.y <= unit.position.y < gameState.level.viewport.y + SCREEN_TILES_Y):
            isSelected = gameState.selectedCatId == unit.id
            bumpSelected = -1 if frame % 8 < 2 and isSelected else 0
            unit_screen_x = (unit.position.x - gameState.level.viewport.x) * 8
            unit_screen_y = (unit.position.y - gameState.level.viewport.y) * 8 + bumpSelected
            unit.set_sprite_position(Position(unit_screen_x, unit_screen_y))
            thumby.display.drawSprite(unit.sprite)
            classSprite = unit.getClassSprite(Position(unit_screen_x, unit_screen_y))
            if classSprite != None:
                thumby.display.drawSprite(classSprite)

            if gameState.level.selectorPosition == unit.position:
                thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
                text = f"{unit.name.upper()} {unit.hp}/{unit.stats.max_hp}"

    # Render selector
    selector_sprite.x = (gameState.level.selectorPosition.x - gameState.level.viewport.x) * 8 - 1
    selector_sprite.y = (gameState.level.selectorPosition.y - gameState.level.viewport.y) * 8 - 1

    if text is not None:
        textLength = len(text) * 4 + 2

        y_offset = 0
        x_offset = 0
        if gameState.level.viewport.y == 0:
            y_offset = 30
        if gameState.level.viewport.x == 0:
            x_offset = max(70 - textLength, 0)

        thumby.display.drawFilledRectangle(1 + x_offset, 1 + y_offset, textLength, 8, thumby.display.WHITE)
        thumby.display.drawText(text, 2 + x_offset, 2 + y_offset, thumby.display.BLACK)
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)

    thumby.display.drawSprite(selector_sprite)

def animate_cats():
    global gameState
    selector_sprite = get_selector_sprite()
    for c in gameState.party + gameState.level.enemies:
        c.advance_animation()
    selector_sprite.setFrame((selector_sprite.getFrame() + 1) % (selector_sprite.frameCount + 1))

def get_attack_tile(cat: Cat):
    global gameState

    if cat.get_weapon() is None:
        return None, None
    
    weapon_ranges = cat.get_weapon().get_range()
    enemy_range = cat.stats.range if (cat.aiType == "searchAndDestroy" and not cat.moved) else 0
    domain = gameState.find_valid_positions(cat, enemy_range)

    for pos in domain:
        for p in gameState.party:
            if abs(pos.x - p.position.x) + abs(pos.y - p.position.y) in weapon_ranges:
                return pos, p

    return None, None

# --- MAIN LOOP ---

while True:
    startLoopTime = time.ticks_ms()
    frame += 1

    partyFullyExhausted = True
    for p in gameState.party:
        if not p.exhausted:
            partyFullyExhausted = False
    if partyFullyExhausted and gameState.state == 'map':
        gameState.state = 'enemy-turn'
    
    renderStartTime = time.ticks_ms()
    if gameState.state == 'map' or gameState.state == 'enemy-turn' or gameState.state == 'enemy-select':
        render_map(gameState.level.map)
    renderEndTime = time.ticks_ms()

    if gameState.level != None and not any(p.name == 'cat' for p in gameState.party):
        gameState.state = 'gameOver'

    if len(gameState.combat_log) > 0:
        thumby.display.fill(thumby.display.WHITE)
        if (current_hp_display == - 1):
            current_hp_display = gameState.combat_log[0].defender_hp
        log: AttackLog = gameState.combat_log[0]
        attackerHealth = log.attacker_hp
        defenderHealth = current_hp_display
        attackRange = current_hp_display == gameState.combat_log[0].defender_hp - 1
        beep = current_hp_display < gameState.combat_log[0].defender_hp
        cat = 4 if attackRange else 0

        # Display based on who is attacking
        middleOfScreen = 36
        if log.attacker_enemy:
            # Enemy is attacking (right side)
            thumby.display.drawText(log.attacker_name, 40, 24, thumby.display.BLACK)
            # thumby.display.drawText(f"HP:{attackerHealth}", 40, 32, thumby.display.BLACK)
            willOverflow = (log.attacker_max_hp * 2 + 2) >= middleOfScreen
            for i in range(log.attacker_max_hp):
                raw_x = 1 + (i * 2)
                overflow = (raw_x - middleOfScreen) >= -1
                rel_x = raw_x if not overflow else raw_x - middleOfScreen
                position = Position(middleOfScreen + rel_x, 32 if not overflow else 36)
                size_x = 1
                size_y = 3 if willOverflow else 7
                thumby.display.drawFilledRectangle(position.x, position.y, size_x, size_y, thumby.display.BLACK if i < attackerHealth else thumby.display.LIGHTGRAY)
            thumby.display.drawText(log.defender_name, 2, 24, thumby.display.DARKGRAY)
            # thumby.display.drawText(f"HP:{defenderHealth}", 2, 32, thumby.display.DARKGRAY)
            willOverflow = (log.defender_max_hp * 2 + 2) >= 36
            for i in range(log.defender_max_hp):
                raw_x = 1 + (i * 2)
                overflow = raw_x - middleOfScreen >= -1
                rel_x = raw_x if not overflow else raw_x - middleOfScreen
                position = Position(rel_x, 32 if not overflow else 36)
                size_x = 1
                size_y = 3 if willOverflow else 7
                thumby.display.drawFilledRectangle(position.x, position.y, size_x, size_y, thumby.display.BLACK if i < defenderHealth else thumby.display.LIGHTGRAY)
            if beep: thumby.display.drawText(f"-{log.damage}", 2, 2, thumby.display.LIGHTGRAY)
            # render the cats
            log.attacker_sprite.x = 56 - cat
            log.attacker_sprite.y = 8
            thumby.display.drawSprite(log.attacker_sprite)
            log.defender_sprite.x = 8
            log.defender_sprite.y = 8
            thumby.display.drawSprite(log.defender_sprite)
            if (log.miss or log.dodge):
                thumby.display.drawText('dodge' if log.dodge else 'miss', 8, 16, thumby.display.BLACK)
        else:
            # Party is attacking (right side)
            thumby.display.drawText(log.attacker_name, 2, 24, thumby.display.BLACK)
            willOverflow = (log.attacker_max_hp * 2 + 2) >= middleOfScreen
            for i in range(log.attacker_max_hp):
                raw_x = 1 + (i * 2)
                overflow = raw_x - middleOfScreen >= -1
                rel_x = raw_x if not overflow else raw_x - middleOfScreen
                position = Position(rel_x, 32 if not overflow else 36)
                size_x = 1
                size_y = 3 if willOverflow else 7
                thumby.display.drawFilledRectangle(position.x, position.y, size_x, size_y, thumby.display.BLACK if i < attackerHealth else thumby.display.LIGHTGRAY)
            thumby.display.drawText(log.defender_name, 40, 24, thumby.display.DARKGRAY)
            willOverflow = (log.defender_max_hp * 2 + 2) >= middleOfScreen
            for i in range(log.defender_max_hp):
                raw_x = 1 + (i * 2)
                overflow = raw_x - middleOfScreen >= -1
                rel_x = raw_x if not overflow else raw_x - middleOfScreen
                position = Position(rel_x + middleOfScreen, 32 if not overflow else 36)
                size_x = 1
                size_y = 3 if willOverflow else 7
                thumby.display.drawFilledRectangle(position.x, position.y, size_x, size_y, thumby.display.BLACK if i < defenderHealth else thumby.display.LIGHTGRAY)
            adjment = (len(str(log.damage)) + 1) * 6
            if beep: thumby.display.drawText(f"-{log.damage}", 71 - adjment, 2, thumby.display.LIGHTGRAY)
            # render the cats
            log.attacker_sprite.x = 8 + cat
            log.attacker_sprite.y = 8
            thumby.display.drawSprite(log.attacker_sprite)
            log.defender_sprite.x = 56
            log.defender_sprite.y = 8
            thumby.display.drawSprite(log.defender_sprite)
            if (log.miss or log.dodge):
                thumby.display.drawText('dodge' if log.dodge else 'miss', 40, 16, thumby.display.BLACK)

        # Animate HP counting down
        if (frame % 3 == 1): 
            if log.static_render_time > 0:
                log.static_render_time -= 1
            elif current_hp_display <= gameState.combat_log[0].new_hp or current_hp_display <= 0:
                gameState.combat_log.pop(0)
                if len(gameState.combat_log) > 0:
                    current_hp_display = gameState.combat_log[0].old_hp
            else:
                current_hp_display = current_hp_display - 1
        if len(gameState.combat_log) == 0:
            current_hp_display = -1

    elif len(gameState.dialog) > 0:
        thumby.display.fill(thumby.display.WHITE)
        thumby.display.drawLine(0, 14, 72, 14, thumby.display.BLACK)
        dialog = gameState.dialog[0]
        portrait = get_dialog_portrait_sprite()
        yOffset = 1
        xOffset = 4
        for cat in dialog.left_cats:
            portrait.x = xOffset
            portrait.y = yOffset
            thumby.display.drawSprite(portrait)
            if cat and cat.name == dialog.currentlyTalking:
                thumby.display.drawLine(xOffset + 3, yOffset +12, xOffset + 5, yOffset + 10, thumby.display.BLACK)
                thumby.display.drawLine(xOffset + 5, yOffset + 10, xOffset + 7, yOffset + 12, thumby.display.BLACK)
                thumby.display.drawLine(xOffset + 3, yOffset + 13, xOffset + 8,  yOffset + 13, thumby.display.WHITE)
            xOffset += 10
        xOffset = 62
        for cat in dialog.right_cats:
            portrait.x = xOffset
            portrait.y = yOffset
            thumby.display.drawSprite(portrait)
            if cat and cat.name == dialog.currentlyTalking:
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
        if dialog.decision and thumby.buttonB.justPressed():
            gameState.pop_dialog()

    elif gameState.state == 'title':
        thumby.display.fill(thumby.display.BLACK)
        thumby.display.drawText("Cats Emblem", 3, 8, thumby.display.BLACK)

        def load_game_action():
            if gameState.has_saved_game():
                gameState.load_game()
                gameState.state = 'map'
    
        menu_options = [
            Option(
                label= "New Game",
                action= lambda: (gameState.start_game(), setattr(gameState, 'state', 'map')),
                condition= lambda: True
            ),
            Option(
                label= "Load Game",
                action= load_game_action,
                condition= lambda: gameState.has_saved_game()
            )
        ]
    
        title_menu = Menu(
            options=[menu_options],
            title=[lambda: "Main Menu"],
            leave_action=lambda: None
        )
    
        gameState.enter_menu(title_menu)

    elif gameState.state == 'map':
        handle_movement()
        mapTimeStart = time.ticks_ms()
        if (frame % 5 == 0): animate_cats()

        if thumby.buttonA.justPressed():
            cat_here = None
            for c in gameState.party:
                if c.position == gameState.level.selectorPosition:
                    cat_here = c
                    break
            if cat_here and cat_here.id != gameState.selectedCatId:
                if cat_here.exhausted:
                    gameState.select_cat(cat_here)
                    gameState.open_unit_menu()
                else:
                    gameState.select_cat(cat_here)
                    gameState.cached_domain = gameState.find_valid_positions(cat_here, cat_here.stats.range)
                    # gameState.open_unit_menu()
            elif gameState.selectedCatId != None:
                cat = gameState.get_selected_cat()
                if cat:
                    cat.set_position(Position(gameState.level.selectorPosition.x, gameState.level.selectorPosition.y))
                    cat.moved = True
                    gameState.open_unit_menu()
            else:
                # Check if an enemy is selected
                for enemy in gameState.level.enemies:
                    if enemy.position == gameState.level.selectorPosition:
                        gameState.selectedCatId = enemy.id
                        gameState.open_stats(enemy)
                        break
                    else:
                        gameState.open_unit_menu()
        if thumby.buttonB.justPressed():
            if gameState.selectedCatId is not None:
                gameState.cancel_cat_select()
            else:
                # cycle through party memebers
                non_moved_cats = [c for c in gameState.party if not c.moved]

                if len(non_moved_cats) > 0:
                    current_index = -1
                    for i, c in enumerate(gameState.party):
                        if c.position == gameState.level.selectorPosition:
                            current_index = i
                            break
                    next_index = (current_index + 1) % len(non_moved_cats)
                    next_cat = non_moved_cats[next_index]
                    gameState.update_selector_position(next_cat.position.x, next_cat.position.y)

    elif gameState.state == 'menu':
        if gameState.menu:
            gameState.menu.render()
            gameState.menu.handle_input()

    elif gameState.state == 'enemy-select':
        selected_cat = gameState.get_selected_cat()
        enemies_in_range = []

        sel_cat_weapon = selected_cat.get_weapon()
        if selected_cat:
            for enemy in gameState.level.enemies:
                dx = abs(enemy.position.x - selected_cat.position.x)
                dy = abs(enemy.position.y - selected_cat.position.y)
                if dx + dy in sel_cat_weapon.get_range() if sel_cat_weapon is not None else []:
                    enemies_in_range.append(enemy)
        if gameState.level.selectorPosition == selected_cat.position and len(enemies_in_range) > 0:
            gameState.update_selector_position(enemies_in_range[0].position.x, enemies_in_range[0].position.y)

        if len(enemies_in_range) == 0:
            gameState.open_unit_menu()
            option = 0
        else:
            if thumby.buttonU.justPressed() or thumby.buttonL.justPressed():
                option = (option - 1) % len(enemies_in_range)
                gameState.level.selectorPosition.x = enemies_in_range[option].position.x
                gameState.level.selectorPosition.y = enemies_in_range[option].position.y
            elif thumby.buttonD.justPressed() or thumby.buttonR.justPressed():
                option = (option + 1) % len(enemies_in_range)
                gameState.update_selector_position(enemies_in_range[option].position.x, enemies_in_range[option].position.y)

            if thumby.buttonA.justPressed():
                selected_cat = gameState.get_selected_cat()
                selected_enemy = enemies_in_range[option]
                
                battle(selected_cat, selected_enemy)
                selected_cat.set_exhausted(True)
                gameState.cancel_cat_select()
                gameState.selectedCatId = None
                gameState.state = 'map'
            elif thumby.buttonB.justPressed():
                if selected_cat: gameState.update_selector_position(selected_cat.position.x, selected_cat.position.y)
                gameState.open_unit_menu()
                option = 0
    
    elif gameState.state == 'enemy-turn':
        if frame % 10 == 1:
            if activeEnemy:
                closest_tile, target = get_attack_tile(activeEnemy)
                if target is None:
                    readyForBattle = False
                    activeEnemy.set_exhausted(True)
                    activeEnemy = None

                if target and readyForBattle:
                    battle(activeEnemy, target)
                    activeEnemy.set_exhausted(True)
                    activeEnemy = None
                    readyForBattle = False

                elif target and not readyForBattle:
                    if closest_tile:
                        activeEnemy.set_position(closest_tile)
                        activeEnemy.set_moved(True)
                        gameState.update_selector_position(closest_tile.x, closest_tile.y)
                        readyForBattle = True
            else:
                for e in gameState.level.enemies:
                    if not e.exhausted:
                        (attackPos, defendingUnit)  = get_attack_tile(e)
                        if defendingUnit != None and attackPos != None:
                            activeEnemy = e
                            gameState.update_selector_position(activeEnemy.position.x, activeEnemy.position.y)
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

    elif gameState.state == 'end':
        thumby.display.fill(thumby.display.WHITE)
        thumby.display.drawText("You Win!", 20, 24, thumby.display.BLACK)
        if thumby.buttonA.justPressed():
            gameState.cancel_cat_select()
            gameState.state = 'title'

    elif gameState.state == 'gameOver':
        thumby.display.fill(thumby.display.WHITE)
        thumby.display.drawText("Game Over", 15, 24, thumby.display.BLACK)

    thumby.display.update()
    endLoopTime = time.ticks_ms()
    loopDuration = endLoopTime - startLoopTime

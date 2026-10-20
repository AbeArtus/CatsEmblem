from time import sleep

# Cats F# maj
# enemies in Bb min

from sys import path as syspath
syspath.insert(0, '/Games/CatsEmblem')

import thumbyGrayscale as thumby

def render_loading_screen(message: str):
	thumby.display.fill(thumby.display.BLACK)
	thumby.display.drawText(message, 6, 16, thumby.display.WHITE)
	thumby.display.show()

thumby.display.setFPS(20)
render_loading_screen("Loading")

from Shared import Cat, Position, build_dialogs, cat_frame_sprite, cat_head, Item, Dialog, Menu, AttackLog, Option, button_sprite, classAdvantages, enemy_frame_sprite, checkClearMem
checkClearMem("Shared Imported")
render_loading_screen("Loading.")
from MapData import get_tile_data, canWalkOn, tileEvation, TILE_BLOCKADE
checkClearMem("MapData imported")
from Items import weaponAdvantages
checkClearMem("Items imported")
render_loading_screen("Loading..")
from GameState import GameState
checkClearMem("GameState imported")
render_loading_screen("Loading...")

thumby.display.enableGrayscale()

import Callbacks

gameState = GameState()
Callbacks.set_game_state(gameState)
checkClearMem("Callbacks")

_selector_sprite = None

def get_selector_sprite():
	global _selector_sprite
	if _selector_sprite is None:
		from MapData import selector_sprite_sheet
		_selector_sprite = thumby.Sprite(10, 10, selector_sprite_sheet(), 32, 16, key=3)
	return _selector_sprite

def note_to_freq(note_str: str) -> float:
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    flat_map = {'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#'}
    note_str = note_str.strip()
    if note_str[1] in ['#', 'b']:
        pitch = note_str[:2]
        octave = int(note_str[2:])
    else:
        pitch = note_str[:1]
        octave = int(note_str[1:])
    if pitch in flat_map:
        pitch = flat_map[pitch]
    pitch_index = note_names.index(pitch)
    midi_num = (octave + 1) * 12 + pitch_index
    freq = 520 * (2 ** ((midi_num - 69) / 12))
    
    return int(freq)

# --- CONSTANTS ---
SCREEN_TILES_X = 9
SCREEN_TILES_Y = 5

_font_cache = {}

def use_font(name, path, width, height, space):
	cached = _font_cache.get(name)
	if cached is None:
		from os import stat
		sz = stat(path)[6]
		bmap = bytearray(sz)
		with open(path, 'rb') as fh:
			fh.readinto(bmap)
		cached = (bmap, width, height, space, sz // width)
		_font_cache[name] = cached
	bmap, width, height, space, glyphcnt = cached
	thumby.display.font_bmap = bmap
	thumby.display.font_width = width
	thumby.display.font_height = height
	thumby.display.font_space = space
	thumby.display.font_glyphcnt = glyphcnt

# --- GAME STATE ---
frame = 0
activeEnemy = None
readyForBattle = False
option = 0
current_hp_display = -1
currentFont = "5x7"
delay = 0
_dialog_cache = None
_dialog_index = -1
_talker = None
_talker_pos = None
_mouth_open = False

def render_dialog(dialog):
	global _dialog_cache, _dialog_index, _talker, _talker_pos, _mouth_open
	if dialog.overlay:
		if dialog is not _dialog_cache:
			render_map(gameState.level.map)
			thumby.display.drawFilledRectangle(0, 14, 72, 10, thumby.display.WHITE)
			thumby.display.drawLine(0, 14, 72, 14, thumby.display.DARKGRAY)
			thumby.display.drawLine(0, 24, 72, 24, thumby.display.BLACK)
			thumby.display.drawText(dialog.lines[0], 1, 16, thumby.display.BLACK)
			_dialog_cache = dialog
		return False
	full_text = ''.join(dialog.lines)
	mouth_open = dialog.printIndex < dialog.charCount - 1 and full_text[dialog.printIndex] not in ' aeiouAEIOU'
	if dialog is not _dialog_cache:
		_talker = None
		_talker_pos = None
		thumby.display.fill(thumby.display.WHITE)
		for cats, x, step, mirror in ((dialog.left_cats, 0, 13, False), (dialog.right_cats, 58, -13, True)):
			for cat in cats:
				cat = gameState.get_cat_by_position(cat) if isinstance(cat, Position) else cat
				if cat:
					portrait = cat_frame_sprite(x, 0, cat.name) if not cat.enemy else enemy_frame_sprite(x, 0)
					portrait.mirrorX = mirror
					portrait.setFrame(0)
					thumby.display.drawSprite(portrait)
					if cat.name == dialog.currentlyTalking:
						_talker, _talker_pos = portrait, (x, 0)
				x += step
		thumby.display.drawLine(0, 14, 72, 14, thumby.display.DARKGRAY)
		_dialog_cache, _dialog_index, _mouth_open = dialog, -1, not mouth_open
	if dialog.printIndex != _dialog_index:
		if dialog.printIndex == _dialog_index + 1:
			index = _dialog_index
			for row, line in enumerate(dialog.lines):
				if 0 <= index < len(line):
					thumby.display.drawText(line[index], 1 + index * 6, 16 + row * 8, thumby.display.BLACK)
					break
				index -= len(line)
		else:
			thumby.display.drawFilledRectangle(0, 16, 72, 24, thumby.display.WHITE)
			for row, line in enumerate(dialog.lines): thumby.display.drawText(line[:dialog.printIndex], 1, 16 + row * 8, thumby.display.BLACK)
		_dialog_index = dialog.printIndex
	if _talker and mouth_open != _mouth_open:
		x, y = _talker_pos
		thumby.display.drawFilledRectangle(x, y, 14, 14, thumby.display.WHITE)
		_talker.setFrame(1 if mouth_open else 0)
		thumby.display.drawSprite(_talker)
		thumby.display.drawLine(x + 4, 14, x + 6, 12, thumby.display.DARKGRAY)
		thumby.display.drawLine(x + 6, 12, x + 8, 14, thumby.display.DARKGRAY)
		thumby.display.drawLine(x + 5, 14, x + 8, 14, thumby.display.WHITE)
		thumby.display.setPixel(x + 6, 13, thumby.display.WHITE)
		_mouth_open = mouth_open
	return mouth_open

def get_render_tile_sprite(tile_type: int, map_x: int, map_y: int, screen_x: int, screen_y: int):
	if tile_type == 4 or tile_type == 35:
		return None
	sprite_data, xFlip, yFlip, size_x, size_y = get_tile_data(tile_type)

	if sprite_data is None:
		return None

	if tile_type == 0:
		key = (tile_type, (map_y & 1) == 0)
	elif tile_type == 1:
		xEven = (map_x & 1) == 0
		yEven = (map_y & 1) == 0
		shouldFlip = (xEven and not yEven) or (not xEven and yEven)
		key = (tile_type, shouldFlip)
	else:
		key = (tile_type, xFlip, yFlip)

	if tile_type == 0:
		sprite = thumby.Sprite(size_x, size_y, sprite_data, 0, 0, -1, key[1])
	elif tile_type == 1:
		sprite = thumby.Sprite(size_x, size_y, sprite_data, 0, 0, -1, key[1])
	else:
		sprite = thumby.Sprite(size_x, size_y, sprite_data, 0, 0, -1, xFlip, yFlip)

	sprite.x = screen_x * 8
	sprite.y = screen_y * 8
	return sprite

def draw_health_bar(hp: int, max_hp: int, offset: int, margin: int, middleOfScreen: int = 36):
	willOverflow = (max_hp * 2 + margin) >= middleOfScreen
	size_y = 3 if willOverflow else 7
	for i in range(max_hp):
		raw_x = 1 + (i * 2)
		overflow = raw_x - middleOfScreen >= -1
		rel_x = raw_x if not overflow else raw_x - middleOfScreen
		thumby.display.drawFilledRectangle(offset + rel_x, 32 if not overflow else 36, 1, size_y,
			thumby.display.BLACK if i < hp else thumby.display.LIGHTGRAY)

def addDialog(dialog: list[str], cat: Cat = None):
	global gameState
	dialog = Dialog(
		lines=dialog,
		left_cats=[cat],
		right_cats=[],
		currentlyTalking=cat.name if cat else "",
		lambda_after=None,
		instaText=True
	)
	gameState.add_dialog(dialog)

def battle(attacker: Cat, defender: Cat):
	global gameState

	attackerExp = 0
	defenderExp = 0

	expMultiplier = defender.level / attacker.level if defender.enemy else attacker.level / defender.level

	attackerExp += record_attack(attacker, defender)
	if defender.hp <= 0:
		attacker.add_exp(int(defender.stats.max_hp * expMultiplier), addDialog)
		return

	defender_weapon = defender.get_weapon()
	defender_ranges = defender_weapon.get_range() if defender_weapon else []
	dx = abs(attacker.position.x - defender.position.x)
	dy = abs(attacker.position.y - defender.position.y)
	if dx + dy in defender_ranges:
		defenderExp += record_attack(defender, attacker)
		if attacker.hp <= 0:
			defender.add_exp(int(attacker.stats.max_hp * expMultiplier), addDialog)
			return

	if attacker.stats.speed > defender.stats.speed * int(1.5):
		attackerExp += record_attack(attacker, defender, is_counter=True)
	if defender.hp <= 0:
		attacker.add_exp(int(defender.stats.max_hp * expMultiplier), addDialog)
		return

	if dx + dy in defender_ranges:
		if defender.stats.speed > attacker.stats.speed * int(1.5):
			attackerExp += record_attack(defender, attacker, is_counter=True)
		if attacker.hp <= 0:
			defender.add_exp(int(attacker.stats.max_hp * expMultiplier), addDialog)
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
	attackDodge = randInt < (defenderDodge - attackerAttackPower) * 3
	randInt = random.randint(1, 100)
	attackHit = randInt <= attackerWeapon.accuracy - tileEvationBonus

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
		static_render_time= 3 if not attackHit or attackDodge or damage == 0 else 1
	)

	gameState.combat_log.append(log)

	defender.set_hp(new_hp)

	if defender.hp <= 0:
		if defender in gameState.level.enemies:
			gameState.level.enemies.remove(defender)
			additionalChance = attacker.stats.luck + attacker.stats.speed + attacker.stats.attack - defender.stats.luck - defender.stats.speed - defender.stats.defense
			randInt = random.randint(1, 100)
			attackingInRange = attackerWeapon.range == 1
			if randInt <= (40 + additionalChance) and attackingInRange:
				gold = random.randint(1, int(defender.level * 1.5))
				gameState.add_dialog(Dialog(
					lines=[f"Looted {gold} ", "gold!"],
					lambda_after=lambda: gameState.update_bank(gold),
					instaText=True
				))
		if defender in gameState.party:
			gameState.party.remove(defender)
		log = defender.deathDialog
		if log is not None:
			dialogs = build_dialogs(log, right=[defender])
			for line in dialogs:
				gameState.add_dialog(line)
	expMultiplier = defender.level / attacker.level

	return max(int(damage * expMultiplier + 0.49), 1)

def calculate_damage(attacker: Cat, defender: Cat):
	global gameState
	import random
	attackerWeapon: Item = attacker.get_weapon()
	defenderWeapon: Item = defender.get_weapon()

	party = gameState.party if not attacker.enemy else gameState.level.enemies
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
	if randInt < crit_chance or attacker.stats.luck == randInt:
		bonus_damage += base_damage

	destroyed = attackerWeapon.use_weapon()
	if destroyed:
		gameState.add_dialog(Dialog(
			lines=[f"{attacker.name}'s", f"{attackerWeapon.name}", "broke!"],
			lambda_after=None,
			instaText=True
		))
		attacker.items.remove(attackerWeapon)
	
	return base_damage + bonus_damage if base_damage + bonus_damage > 0 else 1

def handle_movement():
	global gameState, delay

	x = gameState.level.selectorPosition.x
	y = gameState.level.selectorPosition.y
	isCatSelected = gameState.selectedCatId is not None

	directions = {
		"L": (-1, 0),
		"R": (1, 0),
		"U": (0, -1),
		"D": (0, 1)
	}

	moved = False

	if delay > 0 and delay < 3:
		delay += 1
		return False

	for button, (dx, dy) in directions.items():
		if getattr(thumby, f"button{button}").justPressed() or getattr(thumby, f"button{button}").pressed():
			moved = True
			delay += 1
			thumby.audio.play(note_to_freq("F#5"), 15)
			new_x, new_y = x + dx, y + dy
			if 0 <= new_y < len(gameState.level.map) and 0 <= new_x < len(gameState.level.map[0]):
				isWalkable = gameState.level.map[new_y][new_x] in canWalkOn
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
	if not moved:
		delay = 0
	return False

def render_map(level):
	global gameState
	selector_sprite = get_selector_sprite()
	if frame % 4 == 0 or selector_sprite.getFrame() == 2:
		selector_sprite.setFrame((selector_sprite.getFrame() + 1) % (selector_sprite.frameCount + 1))
	thumby.display.fill(thumby.display.WHITE)

	text = None

	mod8 = frame % 8
	if (mod8 == 0 or mod8 == 3) and gameState.selectedCatId is not None:
		thumby.audio.play(note_to_freq("F#3"), 10)

	for y in range(SCREEN_TILES_Y):
		for x in range(SCREEN_TILES_X):
			map_x = gameState.level.viewport.x + x
			map_y = gameState.level.viewport.y + y
			if 0 <= map_x < len(level[0]) and 0 <= map_y < len(level):
				tile_type = level[map_y][map_x]
				if tile_type == 3:
					for house in gameState.level.houses:
						if house.position.x == map_x and house.position.y == map_y:
							if house.destroyed:
								tile_type = 41
							break
				sprite = get_render_tile_sprite(tile_type, map_x, map_y, x, y)
				if sprite is not None: 
					if sprite.frameCount > 0:
						sprite.setFrame((frame // 10) % sprite.frameCount)
					thumby.display.drawSprite(sprite)

	for button in gameState.level.buttons:
		if gameState.level.viewport.x <= button.position.x < gameState.level.viewport.x + SCREEN_TILES_X and \
		gameState.level.viewport.y <= button.position.y < gameState.level.viewport.y + SCREEN_TILES_Y:
			x = button.position.x - gameState.level.viewport.x
			y = button.position.y - gameState.level.viewport.y
			buttonSprite = button_sprite(x * 8, y * 8)
			if button.pressed:
				buttonSprite.setFrame(1)
			thumby.display.drawSprite(buttonSprite)

	for blockade in gameState.level.blockades:
		for pos in blockade.positions:
			if gameState.level.viewport.x <= pos.x < gameState.level.viewport.x + SCREEN_TILES_X and \
			gameState.level.viewport.y <= pos.y < gameState.level.viewport.y + SCREEN_TILES_Y:
				if not blockade.cleared:
					map_x = pos.x
					map_y = pos.y
					x = map_x - gameState.level.viewport.x
					y = map_y - gameState.level.viewport.y
					blockSprite = get_render_tile_sprite(TILE_BLOCKADE, map_x, map_y, x, y)
					thumby.display.drawSprite(blockSprite)

	for overlayObject in gameState.level.overlayObjects:
		for pos in overlayObject.boundPositions:
			if gameState.level.viewport.x <= pos.x < gameState.level.viewport.x + SCREEN_TILES_X and \
			gameState.level.viewport.y <= pos.y < gameState.level.viewport.y + SCREEN_TILES_Y:
				x = overlayObject.position.x - gameState.level.viewport.x
				y = overlayObject.position.y - gameState.level.viewport.y
				if overlayObject.objectName == "cat_head":
					overlaySprite = cat_head(x * 8, y * 8)
					thumby.display.drawSprite(overlaySprite)
					break

	for unit in gameState.party + gameState.level.enemies:
		if (gameState.level.viewport.x <= unit.position.x < gameState.level.viewport.x + SCREEN_TILES_X and 
			gameState.level.viewport.y <= unit.position.y < gameState.level.viewport.y + SCREEN_TILES_Y):
			isSelected = gameState.selectedCatId == unit.id
			bumpSelected = -1 if frame % 8 < 2 and isSelected else 0
			unit_screen_x = (unit.position.x - gameState.level.viewport.x) * 8
			unit_screen_y = (unit.position.y - gameState.level.viewport.y) * 8 + bumpSelected
			unit.set_sprite_position(unit_screen_x, unit_screen_y)
			thumby.display.drawSprite(unit.sprite)
			classSprite = unit.getClassSprite(unit_screen_x, unit_screen_y)
			if classSprite != None:
				thumby.display.drawSprite(classSprite)

			if gameState.level.selectorPosition == unit.position:
			   
				text = f"{unit.name.upper()} {unit.hp}/{unit.stats.max_hp}"

	selector_sprite.x = (gameState.level.selectorPosition.x - gameState.level.viewport.x) * 8 - 1
	selector_sprite.y = (gameState.level.selectorPosition.y - gameState.level.viewport.y) * 8 - 1

	if text is not None and currentFont == "3x5":
		textLength = len(text) * 4 + 3

		y_offset = 0
		x_offset = 0
		if gameState.level.viewport.y == 0:
			y_offset = 29
		if gameState.level.viewport.x == 0:
			x_offset = max(70 - textLength, 0)

		thumby.display.drawFilledRectangle(1 + x_offset, 1 + y_offset, textLength, 9, thumby.display.WHITE)
		thumby.display.drawRectangle(1 + x_offset, 1 + y_offset, textLength, 9, thumby.display.BLACK)
		thumby.display.drawText(text, 3 + x_offset, 3 + y_offset, thumby.display.BLACK)

	thumby.display.drawSprite(selector_sprite)

def animate_cats():
	global gameState
	seen = []
	for c in gameState.party + gameState.level.enemies:
		spr = c.sprite
		if spr not in seen:
			seen.append(spr)
			c.advance_animation()

def get_attack_tile(cat: Cat):
	global gameState

	weapon = cat.get_weapon()
	if weapon is None:
		return None, None

	weapon_ranges = weapon.get_range()
	enemy_range = 0 if (cat.aiType == "stand" or cat.moved) else cat.stats.range
	domain = gameState.find_valid_positions(cat, enemy_range)

	potential_targets = []

	for p in gameState.party:
		for pos in domain:
			if abs(pos[0] - p.position.x) + abs(pos[1] - p.position.y) in weapon_ranges:
				diff = cat.level - p.level
				p_weapon = p.get_weapon()
				if p_weapon and weaponAdvantages.get(weapon.type) == p_weapon.type:
					diff += 1
				if classAdvantages.get(cat.classType) == p.classType:
					diff += 1
				potential_targets.append((Position(pos[0], pos[1]), p, diff))
				break

	if not potential_targets:
		for house in gameState.level.houses:
			if house.destroyed or house.indestructible or abs(house.position.x - cat.position.x) + abs(house.position.y - cat.position.y) > cat.stats.range:
				continue
			for pos in domain:
				if pos[0] == house.position.x and pos[1] == house.position.y:
					potential_targets.append((Position(pos[0], pos[1]), None, 0))
					break

	if not potential_targets and cat.aiType == "path" and cat.aiPath and not cat.moved:
		nearest_path_point = {"position": None, "distance": float('inf')}
		for pathPos in cat.aiPath:
			if pathPos.visited:
				continue
			pos = pathPos.position
			distance = abs(pos.x - cat.position.x) + abs(pos.y - cat.position.y)
			if distance < nearest_path_point["distance"]:
				if cat.position.x == pos.x and cat.position.y == pos.y:
					pathPos.mark_visited()
					continue
				nearest_path_point = {"position": pos, "distance": distance}
		if nearest_path_point["position"]:
			target = nearest_path_point["position"]
			closest = min(domain, key=lambda pos: abs(pos[0] - target.x) + abs(pos[1] - target.y), default=None)
			if closest:
				potential_targets.append((Position(closest[0], closest[1]), None, 0))
					
	if not potential_targets and cat.aiType == "omnipresence" and not cat.moved:
		target_pos = gameState.party[0].position
		closest = min(domain, key=lambda pos: abs(pos[0] - target_pos.x) + abs(pos[1] - target_pos.y), default=None)
		if closest:
			potential_targets.append((Position(closest[0], closest[1]), None, 0))

	if not potential_targets:
		return None, None

	best_position, best_target, _ = max(potential_targets, key=lambda t: t[2])
	return best_position, best_target

# --- MAIN LOOP ---

while True:
	try:
		frame += 1

		partyFullyExhausted = all(p.exhausted for p in gameState.party) if gameState.party else None
		if (gameState.state == 'map' or gameState.state == 'enemy-turn' or gameState.state == 'enemy-select')\
		and not len(gameState.dialog) > 0 and not len(gameState.combat_log) > 0:
			if currentFont == "5x7":
				currentFont = "3x5"
				use_font("3x5", "/lib/font3x5.bin", 3, 5, 1)
			if frame % 2 == 0:
				render_map(gameState.level.map)
		else:
			if currentFont == "3x5":
				currentFont = "5x7"
				use_font("5x7", "/lib/font5x7.bin", 5, 7, 1)

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

			middleOfScreen = 36
			enemyAttacking = log.attacker_enemy
			margin = 1 if enemyAttacking else 2
			attacker_offset = 0 if enemyAttacking else middleOfScreen
			defender_offset = middleOfScreen - attacker_offset

			thumby.display.drawText(log.attacker_name, 2 if enemyAttacking else 40, 24, thumby.display.BLACK)
			draw_health_bar(attackerHealth, log.attacker_max_hp, attacker_offset, margin)
			thumby.display.drawText(log.defender_name, 40 if enemyAttacking else 2, 24, thumby.display.DARKGRAY)
			draw_health_bar(defenderHealth, log.defender_max_hp, defender_offset, margin)

			if beep:
				damage_x = 71 - (len(str(log.damage)) + 1) * 6 if enemyAttacking else 2
				thumby.display.drawText(f"-{log.damage}", damage_x, 2, thumby.display.LIGHTGRAY)

			log.attacker_sprite.x = 8 + cat if enemyAttacking else 56 - cat
			log.attacker_sprite.y = 8
			thumby.display.drawSprite(log.attacker_sprite)
			log.defender_sprite.x = 56 if enemyAttacking else 8
			log.defender_sprite.y = 8
			thumby.display.drawSprite(log.defender_sprite)
			if (log.miss or log.dodge):
				if log.static_render_time == 3:
					if (frame % 2 == 1): thumby.audio.play(note_to_freq("C5" if enemyAttacking else "G#4"), 40)
				thumby.display.drawText('dodge' if log.dodge else 'miss', 40 if enemyAttacking else 8, 16, thumby.display.BLACK)

			if (frame % 2 == 1):
				if log.static_render_time > 0:
					log.static_render_time -= 1
				elif current_hp_display <= gameState.combat_log[0].new_hp or current_hp_display <= 0:
					gameState.combat_log.pop(0)
					if len(gameState.combat_log) > 0:
						current_hp_display = gameState.combat_log[0].old_hp
				else:
					current_hp_display = current_hp_display - 1
					thumby.audio.play(note_to_freq("Eb5" if enemyAttacking else "C#5"), 10)
			if len(gameState.combat_log) == 0:
				current_hp_display = -1

		elif len(gameState.dialog) > 0:
			dialog = gameState.dialog[0]
			mouf_open = render_dialog(dialog)

			if dialog.printIndex < dialog.charCount:
				dialog.printIndex += 1
				notestring = "F#4" if mouf_open else "C4"
				thumby.audio.play(note_to_freq(notestring), 5 if mouf_open else 6)

			if dialog.timeout:
				thumby.display.update()
				sleep(dialog.timeout)
				_dialog_cache = None
				gameState.pop_dialog()
			else:
				if thumby.buttonA.justPressed():
					thumby.audio.play(note_to_freq("C#6"), 20)
					if dialog.printIndex >= dialog.charCount:
						if dialog.lambda_after:
							dialog.lambda_after()
						_dialog_cache = None
						gameState.pop_dialog()
					else:
						dialog.printIndex = dialog.charCount
				if dialog.decision and thumby.buttonB.justPressed():
					if dialog.printIndex >= dialog.charCount:
						thumby.audio.play(note_to_freq("C6"), 20)
						_dialog_cache = None
						gameState.pop_dialog()
					else:
						dialog.printIndex = dialog.charCount

		elif partyFullyExhausted is not None and partyFullyExhausted and gameState.player_turn and gameState.state == 'map':
			thumby.audio.play(note_to_freq("Ab5"), 100)
			gameState.end_turn()

		elif gameState.state == 'title':
			thumby.display.fill(thumby.display.WHITE)
			thumby.display.drawText("Cats Emblem", 3, 4, thumby.display.BLACK)
			thumby.display.drawSprite(cat_head(16, 14))

			if thumby.buttonA.justPressed():
				thumby.audio.play(note_to_freq("F#6"), 20)
				def load_game_action():
					from Shared import release_title_sprites
					if gameState.has_saved_game():
						release_title_sprites()
						gameState.load_game()
						gameState.state = 'map'
				def new_game_action():
					from Shared import release_title_sprites
					release_title_sprites()
					gameState.start_game()
					gameState.state = 'map'
				title_menu = Menu(
					options=[[
						Option(label="New Game", action=new_game_action),
						Option(label="Load Game", action=load_game_action, condition=lambda: gameState.has_saved_game())
					]],
					title=[lambda: "Main Menu"],
					leave_action=lambda: setattr(gameState, 'state', 'title')
				)
				gameState.enter_menu(title_menu)

		elif gameState.state == 'map':
			if frame % 2 == 0:
				handle_movement()
			if (frame % 10 == 0): animate_cats()

			if thumby.buttonA.justPressed():
				thumby.audio.play(note_to_freq("A#5"), 20)
				cat_here = None
				enemy_here = None
				for c in gameState.party:
					if c.position == gameState.level.selectorPosition:
						cat_here = c
						break
				for e in gameState.level.enemies:
					if e.position == gameState.level.selectorPosition:
						enemy_here = e
						break
				if cat_here and cat_here.id != gameState.selectedCatId:
					if cat_here.exhausted:
						gameState.select_cat(cat_here)
						gameState.open_unit_menu()
					else:
						gameState.select_cat(cat_here)
						gameState.cached_domain = gameState.find_valid_positions(cat_here, cat_here.stats.range)
				elif gameState.selectedCatId != None:
					cat = gameState.get_selected_cat()
					if cat:
						cat.set_position(Position(gameState.level.selectorPosition.x, gameState.level.selectorPosition.y))
						cat.moved = True
						gameState.open_unit_menu()
				elif enemy_here:
					if enemy_here.position == gameState.level.selectorPosition:
						gameState.selectedCatId = enemy_here.id
						gameState.open_stats(enemy_here)
				else:
					gameState.open_unit_menu()

			if thumby.buttonB.justPressed():
				thumby.audio.play(note_to_freq("G#5"), 20)
				if gameState.selectedCatId is not None:
					gameState.cancel_cat_select()
				else:
					active_cats = [c for c in gameState.party if not c.moved and not c.exhausted]

					if len(active_cats) > 0:
						current_index = -1
						for i, c in enumerate(gameState.party):
							if c.position == gameState.level.selectorPosition:
								current_index = i
								break
						next_index = (current_index + 1) % len(active_cats)
						next_cat = active_cats[next_index]
						gameState.update_selector_position(next_cat.position.x, next_cat.position.y)

		elif gameState.state == 'menu':
			if gameState.menu:
				thumby.display.fill(thumby.display.WHITE)
			
				if gameState.menu.title and gameState.menu.menu_index < len(gameState.menu.title):
					hasLeftMenu = gameState.menu.menu_index > 0
					hasRightMenu = gameState.menu.menu_index < len(gameState.menu.options) - 1
					thumby.display.drawText(gameState.menu.title[gameState.menu.menu_index](), 1 if not hasLeftMenu else 7, 0, thumby.display.DARKGRAY)
					if hasLeftMenu:
						if frame % 10 < 5:
							thumby.display.drawText("<", 0, 0, thumby.display.DARKGRAY)
					if hasRightMenu:
						if frame % 10 < 5:
							thumby.display.drawText(">", 66, 0, thumby.display.DARKGRAY)
	
				visible_options, offset = gameState.menu.get_visible_options()
				for i, menu_option in enumerate(visible_options):
					selected = thumby.display.DARKGRAY
					if i + offset == gameState.menu.option_index:
						selected = thumby.display.DARKGRAY if frame % 5 == 0 else thumby.display.BLACK
					if i + offset == gameState.menu.option_index:
						thumby.display.drawRectangle(71, 9 + i * 8, 1, 5, selected)
						thumby.display.drawRectangle(70, 10 + i * 8, 1, 3, selected)
						thumby.display.drawRectangle(69, 11 + i * 8, 1, 1, selected)
						thumby.display.drawRectangle(0, 8 + i * 8, 1, 7, selected)
					thumby.display.drawText(menu_option.label, 2, 8 + i * 8, selected)

				visible_options = gameState.menu.get_options()
				button_pressed = False
				if thumby.buttonU.justPressed() and gameState.menu.option_index > 0:
					gameState.menu.option_index -= 1
					thumby.audio.play(note_to_freq("F#5"), 15)
				elif thumby.buttonD.justPressed() and gameState.menu.option_index < len(visible_options) - 1:
					gameState.menu.option_index += 1
					thumby.audio.play(note_to_freq("F#5"), 15)
	
				elif thumby.buttonL.justPressed() and gameState.menu.menu_index > 0:
					gameState.menu.menu_index -= 1
					gameState.menu.option_index = 0
					thumby.audio.play(note_to_freq("F5"), 15)
	
				elif thumby.buttonR.justPressed() and gameState.menu.menu_index < len(gameState.menu.options) - 1:
					gameState.menu.menu_index += 1
					gameState.menu.option_index = 0
					thumby.audio.play(note_to_freq("F5"), 15)
	
				elif thumby.buttonA.justPressed():
					thumby.audio.play(note_to_freq("C#6"), 15)
					valid_options = gameState.menu.get_options()
					if valid_options:
						valid_options[gameState.menu.option_index].action()
				
				elif thumby.buttonB.justPressed():
					thumby.audio.play(note_to_freq("G#6"), 15)
					if gameState.menu.leave_action:
						gameState.menu.leave_action()

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
				option = min(option, len(enemies_in_range) - 1)
				if thumby.buttonU.justPressed() or thumby.buttonL.justPressed():
					thumby.audio.play(note_to_freq("C#6"), 20)
					option = (option - 1) % len(enemies_in_range)
					enX = enemies_in_range[option].position.x
					enY = enemies_in_range[option].position.y
					gameState.update_selector_position(enX, enY)
				elif thumby.buttonD.justPressed() or thumby.buttonR.justPressed():
					thumby.audio.play(note_to_freq("C#6"), 20)
					option = (option + 1) % len(enemies_in_range)
					gameState.update_selector_position(enemies_in_range[option].position.x, enemies_in_range[option].position.y)

				if thumby.buttonA.justPressed():
					thumby.audio.play(note_to_freq("F6"), 20)
					selected_enemy = enemies_in_range[option]
				
					checkClearMem("Before Battle")
					battle(selected_cat, selected_enemy)
					selected_cat.set_exhausted(True)
					gameState.cancel_cat_select()
					gameState.selectedCatId = None
					gameState.set_state('map')
				elif thumby.buttonB.justPressed():
					thumby.audio.play(note_to_freq("A#6"), 20)
					if selected_cat: gameState.update_selector_position(selected_cat.position.x, selected_cat.position.y)
					gameState.open_unit_menu()
					option = 0
	
		elif gameState.state == 'enemy-turn':
			if frame % 10 == 1:
				if activeEnemy:
					closest_tile, target = get_attack_tile(activeEnemy)
					if target is None and closest_tile is None:
						readyForBattle = False
						activeEnemy.set_exhausted(True)
						activeEnemy = None

					if target and readyForBattle:
						thumby.audio.play(note_to_freq("Ab5"), 20)
						checkClearMem("Before Battle")
						battle(activeEnemy, target)
						activeEnemy.set_exhausted(True)
						activeEnemy = None
						readyForBattle = False

					elif target and not readyForBattle:
						if closest_tile:
							thumby.audio.play(note_to_freq("Eb5"), 20)
							activeEnemy.set_position(closest_tile)
							activeEnemy.set_moved(True)
							gameState.update_selector_position(closest_tile.x, closest_tile.y)
							gameState.check_fight_dialogs(target, activeEnemy)
							readyForBattle = True
					elif closest_tile and not target:
						houseToDestroy = None
						for house in gameState.level.houses:
							if house.position == closest_tile and not house.destroyed and not house.indestructible:
								houseToDestroy = house
								break
						if houseToDestroy:
							houseToDestroy.destroyed = True
							thumby.audio.play(note_to_freq("G4"), 80)	
						else:
							thumby.audio.play(note_to_freq("F5"), 20)
						activeEnemy.set_position(closest_tile)
						activeEnemy.set_moved(True)
						activeEnemy.set_exhausted(True)
						gameState.update_selector_position(closest_tile.x, closest_tile.y)
						activeEnemy = None
				else:
					for e in gameState.level.enemies:
						if not e.exhausted:
							(attackPos, defendingUnit)  = get_attack_tile(e)
							if attackPos != None:
								activeEnemy = e
								gameState.update_selector_position(activeEnemy.position.x, activeEnemy.position.y)
								thumby.audio.play(note_to_freq("Bb5"), 20)
								break
							else:
								readyForBattle = False
								activeEnemy = None
								e.set_exhausted(True)

					if all(e.exhausted for e in gameState.level.enemies):
						thumby.audio.play(note_to_freq("F6"), 100)
						gameState.end_turn()

		elif gameState.state == 'end':
			thumby.display.fill(thumby.display.WHITE)
			thumby.display.drawText("You Win!", 20, 24, thumby.display.BLACK)
			if thumby.buttonA.justPressed():
				gameState.set_state('title')
				gameState.cancel_cat_select()
				thumby.audio.play(note_to_freq("F#6"), 100)

		elif gameState.state == 'gameOver':
			thumby.display.fill(thumby.display.WHITE)
			thumby.display.drawText("Game Over", 15, 24, thumby.display.BLACK)
			if thumby.buttonA.justPressed():
				gameState.set_state('title')
				gameState.cancel_cat_select()
				thumby.audio.play(note_to_freq("F#5"), 100)
	
		thumby.display.update()
	except Exception as e:
		import sys, gc
		sys.print_exception(e)
		thumby.display.fill(thumby.display.WHITE)
		thumby.display.drawText("OOPS Error", 2, 2, thumby.display.BLACK)
		thumby.display.drawText(type(e).__name__, 2, 12, thumby.display.BLACK)
		thumby.display.drawText(str(e)[:20], 2, 22, thumby.display.BLACK)
		thumby.display.update()
		while True:
			pass

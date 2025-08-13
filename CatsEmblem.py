from sys import path as syspath
syspath.insert(0, '/Games/CatsEmblem')

# import math
import math
import thumbyGrayscale as thumby

# Tiles
forestTile = (bytearray([255, 255, 255, 255, 127, 255, 255, 255]), bytearray([0, 0, 96, 124, 255, 124, 96, 0]))
mountainTile =(bytearray([255, 255, 255, 255, 255, 252, 227, 31]), bytearray([192, 240, 252, 255, 255, 255, 252, 224]))
grassTile = (bytearray([255, 255, 255, 255, 255, 255, 255, 255]), bytearray([0, 64, 0, 64, 4, 0, 4, 0]))
houseTile = (bytearray([255, 255, 255, 255, 255, 255, 255, 255]), bytearray([8, 252, 142, 239, 239, 142, 252, 8]))

# Define tile types for simplicity
TILE_GRASS = 0
TILE_FOREST = 1
TILE_MOUNTAIN = 2
TILE_HOUSE = 3
EMPTY = 4

# Define screen dimensions in terms of tiles
SCREEN_TILES_X = 9
SCREEN_TILES_Y = 5

# Initialize map with grass in center, forest around it, and mountains on the edges
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

class Stats:
    def __init__(self, attack=0, defense=0, hp=0, speed=0, luck=0, range=1):
        self.attack = attack
        self.defense = defense
        self.hp = hp
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
    def __init__(self, sprite, position: Position, name: str, selected=False, exhausted=False, stats=None):
        self.sprite = sprite
        self.position = position
        self.selected = selected
        self.exhausted = exhausted
        self.name = name
        self.stats = stats or Stats()

    def set_position(self, position: Position):
        self.position = position
    
    def set_exhausted(self, exhausted):
        self.exhausted = exhausted
    
    def set_selected(self, selected):
        self.selected = selected

    def set_sprite_position(self, position: Position):
        self.sprite.x = position.x
        self.sprite.y = position.y

selectedCatName = "null"

def get_selected_cat():
    for c in party:
        if c.name == selectedCatName:
            return c
    return None

frame = 0
delay = 0
gameState = 'title'
needsUpdate = False
tempPos = Position()
lastPos = Position()
selectorPosition = Position()

# Viewport position for scrolling
viewport_x = 0
viewport_y = 0

# Create sprites
selector_sprite = thumby.Sprite(8, 8, (bytearray([126, 255, 255, 255, 255, 255, 255, 126]), bytearray([195, 129, 0, 0, 0, 0, 129, 195])), 32, 16, key=1)
cat_sprite = thumby.Sprite(8, 8, (bytearray([0, 207, 15, 15, 192, 5, 241, 244]), bytearray([0, 0, 0, 0, 0, 0, 0, 0])), 32, 16, key=1)
cat = Cat(cat_sprite, Position(2, 4), 'cat')
tac = Cat(cat_sprite, Position(2, 5), 'tac')
party = [cat, tac]

enemy_sprite = thumby.Sprite(8, 8, (bytearray([0, 207, 15, 15, 192, 5, 241, 244]), bytearray([255, 48, 240, 240, 63, 250, 14, 11])), 32, 16, key=1)
enemy = Cat(enemy_sprite, Position(6, 4), 'enemy')
enemies = [enemy]

currentLevel = level1
option = 0

def render_map(level):
    thumby.display.fill(thumby.display.WHITE)
    for y in range(SCREEN_TILES_Y):
        for x in range(SCREEN_TILES_X):
            map_x = viewport_x + x
            map_y = viewport_y + y
            if 0 <= map_x < len(level[0]) and 0 <= map_y < len(level):
                tile_type = level[map_y][map_x]
                tile_pos = Position(x * 8, y * 8)
                if tile_type == TILE_GRASS:
                    sprite = thumby.Sprite(8, 8, grassTile, tile_pos.x, tile_pos.y)
                elif tile_type == TILE_FOREST:
                    sprite = thumby.Sprite(8, 8, forestTile, tile_pos.x, tile_pos.y)
                elif tile_type == TILE_MOUNTAIN:
                    sprite = thumby.Sprite(8, 8, mountainTile, tile_pos.x, tile_pos.y)
                elif tile_type == TILE_HOUSE:
                    sprite = thumby.Sprite(8, 8, houseTile, tile_pos.x, tile_pos.y)
                else:
                    continue
                thumby.display.drawSprite(sprite)

    for unit in party + enemies:
        if viewport_x <= unit.position.x < viewport_x + SCREEN_TILES_X and viewport_y <= unit.position.y < viewport_y + SCREEN_TILES_Y:
            unit_screen_x = (unit.position.x - viewport_x) * 8
            unit_screen_y = (unit.position.y - viewport_y) * 8
            unit.set_sprite_position(Position(unit_screen_x, unit_screen_y))
            thumby.display.drawSprite(unit.sprite)

    selector_sprite.x = (selectorPosition.x - viewport_x) * 8
    selector_sprite.y = (selectorPosition.y - viewport_y) * 8
    thumby.display.drawSprite(selector_sprite)

thumby.display.setFPS(8)

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

    if new_x - viewport_x < 1 and viewport_x > 0:
        viewport_x -= 1
    elif new_x - viewport_x > SCREEN_TILES_X - 2 and viewport_x < len(level[0]) - SCREEN_TILES_X:
        viewport_x += 1
    if new_y - viewport_y < 1 and viewport_y > 0:
        viewport_y -= 1
    elif new_y - viewport_y > SCREEN_TILES_Y - 2 and viewport_y < len(level) - SCREEN_TILES_Y:
        viewport_y += 1

def map_loop():
    global gameState, selectedCatName, tempPos, lastPos, needsUpdate, delay

    directionPressed = False
    if thumby.buttonL.justPressed(): 
        update_selector_position(-1, 0, currentLevel)
        delay = 0
        directionPressed = True
        needsUpdate = True
    elif thumby.buttonR.justPressed():
        update_selector_position(1, 0, currentLevel)
        delay = 0
        directionPressed = True
        needsUpdate = True
    elif thumby.buttonU.justPressed():
        update_selector_position(0, -1, currentLevel)
        delay = 0
        directionPressed = True
        needsUpdate = True
    elif thumby.buttonD.justPressed():
        update_selector_position(0, 1, currentLevel)
        delay = 0
        directionPressed = True
        needsUpdate = True
    elif not directionPressed:
        if thumby.buttonL.pressed():
            delay += 1
            if delay > 8: update_selector_position(-1, 0, currentLevel)
            needsUpdate = True
        if thumby.buttonR.pressed():
            delay += 1
            if delay > 8: update_selector_position(1, 0, currentLevel)
            needsUpdate = True
        if thumby.buttonU.pressed():
            delay += 1
            if delay > 8: update_selector_position(0, -1, currentLevel)
            needsUpdate = True
        if thumby.buttonD.pressed():
            delay += 1
            if delay > 8: update_selector_position(0, 1, currentLevel)
            needsUpdate = True
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

while True:
    frame = (frame + 1)
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
        if can_attack(): thumby.display.drawText("Fight", 10, 16, selected if option == 1 else thumby.display.DARKGRAY)
        thumby.display.drawText("End Turn", 10, 24, selected if option == 2 else thumby.display.DARKGRAY)
        if thumby.buttonU.justPressed() and option > 0: option -= 1
        if thumby.buttonD.justPressed() and option < 2: option += 1
        if thumby.buttonA.justPressed():
            if option == 0:
                cat = get_selected_cat()
                if cat:
                    cat.set_exhausted(True)
                selectedCatName = "null"
                gameState = 'map'
                needsUpdate = True
            elif option == 1:
                pass
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
            
    
    
    # Update display
    thumby.display.update()

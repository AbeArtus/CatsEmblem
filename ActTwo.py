from sys import path as syspath
syspath.insert(0, '/Games/CatsEmblem')

from Items import itemDict
from Shared import Blockade, Button, OverlayObject, checkClearMem, Dialog, House, Position, Shop, ShopItem, Level, generate_enemy
checkClearMem("Shared imported")

_add_to_party = None
_update_bank = None
_can_give_item = None
_give_item = None
_get_cat_at_pos = None
_get_selected_cat = None
checkClearMem("Before setting game state callbacks")

def set_game_state_callbacks(add_to_party, update_bank, can_give_item, give_item, get_cat_at_pos, get_selected_cat):
	global _add_to_party, _update_bank, _can_give_item, _give_item, _get_cat_at_pos, _get_selected_cat
	_add_to_party = add_to_party
	_update_bank = update_bank
	_can_give_item = can_give_item
	_give_item = give_item
	_get_cat_at_pos = get_cat_at_pos
	_get_selected_cat = get_selected_cat
checkClearMem("After setting game state callbacks")

def can_give_item(position: Position) -> bool:
	if _can_give_item:
		return _can_give_item(position)
	return False

def give_item(position: Position, item) -> bool:
	if _give_item:
		_give_item(position, item)

def get_cat_at_position(position: Position):
	if _get_cat_at_pos:
		return _get_cat_at_pos(position)
	return None

def get_selected_cat():
	if _get_selected_cat:
		return _get_selected_cat()
	return None

checkClearMem("After defining game state callback functions")

class ActTwoLevels:

	def _build_level6():
		checkClearMem('level6')
		from MapData import get_map

		Barrier1 = Blockade(
			positions=[Position(7, 6)]
		)

		Barrier2 = Blockade(
			positions=[Position(7, 11)]
		)

		button1 = Button(
			position=Position(7, 8),
			pressAction=lambda: (Barrier1.clear()),
			unPressAction=lambda: (Barrier1.unclear()),
		)
		button2 = Button(
			position=Position(7, 3),
			pressAction=lambda: (Barrier2.clear()),
			unPressAction=lambda: (Barrier2.unclear()),
		)

		level = Level(
			map=get_map(6),
			enemies=[
				generate_enemy(3, Position(6, 8), name='mut'),
				generate_enemy(4, Position(8, 7), name='mut'),
				generate_enemy(3, Position(7, 13), name='mut'),
				generate_enemy(4, Position(7, 3), name='mut'),
				generate_enemy(5, Position(13, 13), name='mut', weapon='Slngsht'),
				generate_enemy(5, Position(11, 8), name='mut', weapon='LongBow', classType='sniper'),
				generate_enemy(6, Position(15, 8), name='mut', weapon='Mace', classType='warrior'),
				generate_enemy(5, Position(17, 8), name='mut', weapon='EarthTm', classType='wizard'),
				generate_enemy(7, Position(16, 3), name='mut', weapon='LghtngTm', classType='wizard', ai='stand'),
			],
			number=6,
			seizePosition=Position(16, 3),
			startingPositions=[Position(2, 13), Position(3, 13), Position(2, 3), Position(3, 3), Position(2, 5)],
			shops=[
				Shop(
					Position(7, 13),
					inventory=[
						ShopItem(itemDict['LongBow'], 40),
						ShopItem(itemDict['Bow'], 20),
						ShopItem(itemDict['MstQll'], 50),
						ShopItem(itemDict['Mace'], 25)
					]
				)
			],
			buttons=[button1, button2],
			blockades=[Barrier1, Barrier2]
		)
		return level

	def _build_level7():
		checkClearMem('level7')
		from MapData import get_map
		from Shared import get_npc
		npc = get_npc()
		level = Level(
			map=get_map(7),
			enemies=[
				generate_enemy(4, Position(9, 7), name='mut'),
				generate_enemy(3, Position(10, 8), name='mut'),
				generate_enemy(4, Position(3, 4), name='mut', ai='path', path=[Position(0, 8), Position(2, 11)]),
				generate_enemy(5, Position(4, 4), name='mut', ai='path', path=[Position(1, 8), Position(3, 11)]),
				generate_enemy(4, Position(6, 11), name='mut', weapon='Slngsht'),
				generate_enemy(5, Position(2, 2), name='mut', weapon='LongBow', classType='sniper'),
				generate_enemy(6, Position(10, 2), name='mut', weapon='Spear', classType='warrior'),
				generate_enemy(7, Position(8, 2), name='mut', weapon='LghtngTm', classType='wizard'),
				generate_enemy(8, Position(9, 1), name='mut', weapon='LghtngTm', classType='wizard', ai='stand'),
			],
			number=7,
			seizePosition=Position(9, 1),
			startingPositions=[Position(7, 15), Position(9, 15), Position(8, 14), Position(9, 13), Position(10, 14)],
			shops=[
				Shop(
					Position(1, 0),
					inventory=[
						ShopItem(itemDict['Tuna'], 5),
						ShopItem(itemDict['LghtngTm'], 30),
						ShopItem(itemDict['WaterTm'], 30),
						ShopItem(itemDict['EarthTm'], 30)
					]
				), Shop(
					Position(3, 0),
					inventory=[
						ShopItem(itemDict['Spear'], 25),
						ShopItem(itemDict['Sword'], 20),
						ShopItem(itemDict['Repeater'], 30),
						ShopItem(itemDict['LongBow'], 35)
					]
				)
			],
			houses=[
				House(
					position=Position(1, 12),
					dialogs=[Dialog(
						lines=["You have","come far","take this"],
						left_cats=[npc],
						right_cats=[get_cat_at_position(Position(1, 12))],
						currentlyTalking='npc',
						lambda_after=lambda: give_item(Position(1, 12), itemDict['MagPowder'])
					), Dialog(
						lines=["Received","Magic", "Powder"],
					), Dialog(
						lines=["Should give","a bit","extra exp"],
						left_cats=[npc],
						right_cats=[get_cat_at_position(Position(1, 12))],
						currentlyTalking='npc',
					)]
				), House(
					position=Position(5, 7),
					dialogs=[Dialog(
						lines=["I heard","there is","a wizard"],
						left_cats=[get_cat_at_position(Position(5, 7))],
						right_cats=[npc],
						currentlyTalking='npc'
					)]
				)
			]
		)
		return level

	def _build_level8():
		checkClearMem('level8')
		from Shared import get_cat
		from MapData import get_map
		cat = get_cat()
		level = Level(
			map=get_map(8),
			enemies=[
				generate_enemy(6, Position(14, 9), name ='jr'),
				generate_enemy(7, Position(15, 9), name='mini'),
				generate_enemy(7, Position(8, 11), name='l'),
				generate_enemy(8, Position(10, 5), name='wago', weapon='Slngsht'),
				generate_enemy(9, Position(4, 2), ai='stand', name='xl', weapon='Stick')
			],
			number=8,
			seizePosition=Position(4, 2),
			startingPositions=[Position(16, 3), Position(15, 3), Position(16, 4), Position(15, 4), Position(16, 5)],
			houses=[
				House(
					position=Position(16, 10),
					dialogs=[Dialog(
						lines=["I Should","Probably","hint"],
						left_cats=[cat],
						right_cats=[],
						currentlyTalking='cat',
					)]
				),
				House(
					position=Position(17, 10),
					dialogs=[Dialog(
						lines=["Welcome","to the","Cats Emblem","demo!"],
						left_cats=[],
						right_cats=[cat],
						currentlyTalking='cat'
					)]
				)
			]
		)
		return level

	def _build_level9():
		checkClearMem('level9')
		from Shared import get_npc
		from MapData import get_map
		npc = get_npc()
		level = Level(
			map=get_map(9),
			enemies=[
				generate_enemy(4, Position(15, 16), name='mut'),
				generate_enemy(5, Position(16, 13), name='mut'),
				generate_enemy(4, Position(17, 13), name='mut'),
				generate_enemy(5, Position(5, 2), name='mut'),
				generate_enemy(6, Position(13, 5), name='mut', weapon='Repeater', classType='sniper'),
				generate_enemy(7, Position(11, 11), name='mut', weapon='Slngsht', classType='sniper'),
				generate_enemy(7, Position(3, 7), name='mut', weapon='Slngsht'),
				generate_enemy(8, Position(18, 2), name='mut', weapon='LghtngTm', classType='wizard'),
				generate_enemy(8, Position(14, 2), name='mut', weapon='LongBow', classType='sniper'),
				generate_enemy(8, Position(16, 2), name='mut', weapon='LghtngTm', classType='warrior'),
				generate_enemy(9, Position(16, 0), name='mut', weapon='LghtngTm', classType='wizard', ai='stand'),
			],
			number=9,
			seizePosition=Position(16, 0),
			startingPositions=[Position(2, 17), Position(4, 17), Position(3, 16), Position(5, 16), Position(7, 16)],
			houses=[
				House(
					position=Position(1, 1),
					dialogs=[Dialog(
						lines=["I heard","there is","a wizard"],
						left_cats=[get_cat_at_position(Position(1, 1))],
						right_cats=[npc],
						currentlyTalking='npc'
					)],
				), House(
					position=Position(2, 1),
					dialogs=[Dialog(
						lines=["I heard","there is","a wizard"],
						left_cats=[get_cat_at_position(Position(2, 1))],
						right_cats=[npc],
						currentlyTalking='npc'
					)],
				)
			]
		)
		return level

	def _build_level10():
		from MapData import get_map
		button1 = Button(
			position=Position(3, 16),
			pressAction=lambda: (barrier1.clear() if button2.pressed else None)
		)
		button2 = Button(
			position=Position(21, 16),
			pressAction=lambda: (barrier1.clear() if button1.pressed else None),
		)
		barrier1 = Blockade(
			positions=[Position(11, 14), Position(12, 14), Position(13, 14)]
		)

		button3 = Button(
			position=Position(3, 11),
			pressAction=lambda: (barrier2.clear() if button4.pressed else None),
		)
		button4 = Button(
			position=Position(21, 11),
			pressAction=lambda: (barrier2.clear() if button3.pressed else None),
		)
		barrier2 = Blockade(
			positions=[Position(11, 9), Position(12, 9), Position(13, 9)]
		)
	
		level = Level(
			map=get_map(10),
			enemies=[
				generate_enemy(5, Position(15, 16), name='mut'),
				generate_enemy(6, Position(16, 13), name='mut'),
				generate_enemy(5, Position(17, 13), name='mut'),
				generate_enemy(6, Position(5, 2), name='mut'),
				generate_enemy(7, Position(13, 5), name='mut', weapon='Repeater', classType='sniper'),
				generate_enemy(8, Position(11, 11), name='mut', weapon='Slngsht', classType='sniper'),
				generate_enemy(8, Position(3, 7), name='mut', weapon='Slngsht'),
				generate_enemy(9, Position(18, 2), name='mut', weapon='LghtngTm', classType='wizard'),
				generate_enemy(9, Position(14, 2), name='mut', weapon='LongBow', classType='sniper'),
				generate_enemy(9, Position(16, 2), name='mut', weapon='Mace', classType='warrior'),
				generate_enemy(11, Position(12, 4), name='mut', weapon='LghtngTm', classType='wizard', ai='stand'),
			],
			number=10,
			seizePosition=Position(10, 0),
			startingPositions=[Position(10, 18), Position(11, 18), Position(12, 18), Position(13, 18), Position(14, 18)],
			buttons=[button1, button2, button3, button4],
			blockades=[barrier1, barrier2],
			overlayObjects=[OverlayObject(position=Position(10, 0), objectName='cat_head', boundPositions=[Position(10, 0), Position(10, 4), Position(14, 4)])]
		)
		return level

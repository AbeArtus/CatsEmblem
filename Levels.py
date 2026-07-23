import gc

def checkClearMem(message: str = ''):
    gc.collect()
    print("Free memory (Levels.py):", gc.mem_free(), message)

from sys import path as syspath
syspath.insert(0, '/Games/CatsEmblem')

checkClearMem("Before imports")
from Shared import Cat, Conversation, Dialog, House, Position, Shop, ShopItem, Stats, enemy_sprite, itemDict
checkClearMem("Shared imported")
import thumbyGrayscale as thumby
checkClearMem("Graysacle imported")

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

# Use the callbacks in your code
def add_party_member(cat):
	if _add_to_party:
		_add_to_party(cat)

def modify_bank(amount):
	if _update_bank:
		_update_bank(amount)

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

def get_stats_for_level(level: int):
	return Stats(
		attack=3 + level,
		defense=2 + level,
		max_hp=7 + level,
		speed=2 + level,
		luck=1 + level,
		range=3
	)

def generate_enemy(level: int, position: Position, ai='searchAndDestroy', name='pig', weapon="Stick", classType='pupil'):
	enemySprite = enemy_sprite()
	return Cat(
		sprite=enemySprite,
		position=position,
		name=name,
		selected=False,
		exhausted=False,
		stats=get_stats_for_level(level),
		enemy=True,
		level=level,
		next_level_exp=level * 10,
		exp=0,
		aiType=ai,
		items=[itemDict[weapon]],
		classType=classType
	)

class Level:
	def __init__(
			self,
			map: list[list[int]],
			enemies: list[Cat],
			number: int=1,
			seizePosition=Position(1, 1),
			startingPositions: list[Position] | None = None,
			shops: list[Shop] | None = None,
			houses: list[House] | None = None,
			conversations: list[Conversation] | None = None
		):
		self.map = map
		self.enemies = enemies
		self.viewport = Position()
		self.selectorPosition = Position()
		self.number = number
		self.seizePosition = seizePosition
		self.startingPositions = startingPositions if startingPositions else []
		self.shops = shops if shops else []
		self.houses: list[House] = houses if houses else []
		self.conversations: list[Conversation] = conversations if conversations else []

_level_cache = {}
class Levels:
	def _build_level1():
		checkClearMem('level1')
		from Shared import get_map, get_npc, get_cat, get_tac
		npc = get_npc()
		cat = get_cat()
		tac = get_tac()
		level = None
		level = Level(
			map = get_map(1),
			enemies=[
				generate_enemy(1, Position(4, 4), name='pig'),
				generate_enemy(1, Position(6, 4), name='pig', weapon='Slngsht'),
				generate_enemy(2, Position(1, 2), ai='stand', name='Doug', classType='warrior')
			],
			number=1,
			seizePosition=Position(1, 2),
			startingPositions=[Position(6,14), Position(8,14)],
			houses = [
				House(
					position = Position(6, 11),
					dialogs=[Dialog(
						lines=["The weird","pigs are", "back..."],
						left_cats=[get_cat_at_position(Position(6, 11))],
						right_cats=[npc],
						currentlyTalking='npc'
					), Dialog(
						lines=["cat", "save our","village,"],
						left_cats=[get_cat_at_position(Position(6, 11))],
						right_cats=[npc],
						currentlyTalking='npc',
					), Dialog(
						lines=["its chaos","the Mayors", "missing"],
						left_cats=[get_cat_at_position(Position(6, 11))],
						right_cats=[npc],
						currentlyTalking='npc',
					), Dialog(
						lines=["Take 50g", "if it", "helps,"],
						left_cats=[get_cat_at_position(Position(6, 11))],
						right_cats=[npc],
						currentlyTalking='npc',
						lambda_after=lambda: modify_bank(50)
					)],
					postVisitDialog=[Dialog(
						lines=["Thats all","we got"],
						left_cats=[get_cat_at_position(Position(6, 11))],
						right_cats=[npc],
						currentlyTalking='npc'
					)]
				),
				House(
					position=Position(8, 11),
					dialogs=[Dialog(
						lines=["HEY TAC","wake up","and help"],
						left_cats=[cat],
						right_cats=[tac],
						currentlyTalking='cat',
						lambda_after=lambda: (tac.set_position(Position(8, 12)), add_party_member(tac))
					), Dialog(
						lines=["*stretch*","*meow*","... *meow*"],
						left_cats=[cat],
						right_cats=[tac],
						currentlyTalking='tac'
					), Dialog(
						lines=["yeah"],
						left_cats=[cat],
						right_cats=[tac],
						currentlyTalking='cat'
					)]
				),
			],
			shops = [
				Shop(
					Position(7, 11),
					inventory=[
						ShopItem(itemDict['Tuna'], 2),
						ShopItem(itemDict['Stick'], 5),
						ShopItem(itemDict['Slngsht'], 10)
					]
				)
			]
		)
		return level

	def _build_level2():
		checkClearMem('level2')
		from Shared import get_map, get_npc
		npc = get_npc()
		level = None

		def visit_condition():
			return level is not None and level.enemies == [] and can_give_item(Position(2,1))

		level = Level(
			map=get_map(2),
			enemies=[
				generate_enemy(1, Position(9, 8), name='mut'),
				generate_enemy(2, Position(11, 9), name='mut'),
				generate_enemy(2, Position(2, 6), name='mut'),
				generate_enemy(2, Position(3, 13), name='mut'),
				generate_enemy(2, Position(4, 11), name='mut', weapon='Slngsht'),
				generate_enemy(3, Position(1, 12), ai='stand', name='guy', classType='warrior', )
			],
			number=2,
			seizePosition=Position(1, 12),
			startingPositions=[Position(11,2), Position(11,1), Position(12,1)],
			houses=[
				House(
					position=Position(2, 1),
					preVistedDialogs=[Dialog(
						lines=["Save us","and I'll", "owe you"],
						left_cats=[get_cat_at_position(Position(2, 1))],
						right_cats=[npc],
						currentlyTalking='npc'
					)],
					dialogs=[Dialog(
						lines=["Thank you" ,"take this."],
						left_cats=[get_cat_at_position(Position(2, 1))],
						right_cats=[npc],
						currentlyTalking='npc',
						lambda_after=lambda: give_item(Position(2,1), itemDict['MystPot'])
					), Dialog(
						lines=["Recieved","Mystic","Potion"]
					)],
					visitCondition=visit_condition
				),
				House(
					position=Position(4, 1),
					dialogs=[
					Dialog(
						lines=["Trees,","grass,","and houses"],
						left_cats=[get_cat_at_position(Position(4, 1))],
						right_cats=[npc],
						currentlyTalking='npc'
					),
					Dialog(
						lines=["Give", "Extra", "Avoid"],
						left_cats=[get_cat_at_position(Position(4, 1))],
						right_cats=[npc],
						currentlyTalking='npc'
					)]
				),
				House(
					position=Position(12, 13),
					dialogs=[
						Dialog(
							lines=["I hear","some","items..."],
							left_cats=[get_cat_at_position(Position(12, 13))],
							right_cats=[npc],
							currentlyTalking='npc'
						),
						Dialog(
							lines=["promote", "trained", "pupils"],
							left_cats=[get_cat_at_position(Position(12, 13))],
							right_cats=[npc],
							currentlyTalking='npc'
						),
						Dialog(
							lines=["mystic quill", "promotes to", "sniper"],
							left_cats=[get_cat_at_position(Position(12, 13))],
							right_cats=[npc],
							currentlyTalking='npc'
						),
						Dialog(
							lines=["mystic potion", "promotes to", "wizard"],
							left_cats=[get_cat_at_position(Position(12, 13))],
							right_cats=[npc],
							currentlyTalking='npc'
						),
						Dialog(
							lines=["mystic meal", "promotes to", "warrior"],
							left_cats=[get_cat_at_position(Position(12, 13))],
							right_cats=[npc],
							currentlyTalking='npc'
						),
						Dialog(
							lines=["You have", "to be lv5", "though"],
							left_cats=[get_cat_at_position(Position(12, 13))],
							right_cats=[npc],
							currentlyTalking='npc'
						)
					]
				)
			]
		)
		return level

	def _build_level3():
		checkClearMem('level3')
		from Shared import get_map, get_npc, get_cat, get_mew
		npc = get_npc()
		cat = get_cat()
		mew = get_mew()
		level = None

		def conversation_condition():
			selCat = get_selected_cat()
			if selCat is None or selCat.name != 'cat':
				return False
			diff =  abs(selCat.position.x - mew.position.x) + abs(selCat.position.y - mew.position.y)
			return abs(diff) <= 1

		level = Level(
			map=get_map(3),
			enemies=[
				generate_enemy(2, Position(12, 9), name='mut'),
				generate_enemy(2, Position(3, 9), name='mut'),
				generate_enemy(2, Position(5, 14), name='mut'),
				generate_enemy(2, Position(9, 4), name='mut'),
				generate_enemy(2, Position(14, 3), name='mut'),
				mew,
				generate_enemy(3, Position(13, 1), ai='stand', name='guard', classType='warrior')
			],
			number=3,
			startingPositions=[Position(10, 13), Position(11, 14)],
			seizePosition=Position(13, 1),
			houses=[
				House(
					position=Position(13, 8),
					preVistedDialogs=[Dialog(
						lines=["There is","a legendary","cat..."],
						right_cats=[get_cat_at_position(Position(13, 8))],
						left_cats=[npc],
						currentlyTalking='npc'
					),
					Dialog(
						lines=["that","possesses", "the dna.."],
						right_cats=[get_cat_at_position(Position(13, 8))],
						left_cats=[npc],
						currentlyTalking='cat'
					),
					Dialog(
						lines=["of all","species.", "Its name.." ],
						right_cats=[get_cat_at_position(Position(13, 8))],
						left_cats=[npc],
						currentlyTalking='cat'
					),
					Dialog(
						lines=["is mew.", "cat must", "save him"],
						left_cats=[get_cat_at_position(Position(13, 8))],
						right_cats=[npc],
						currentlyTalking='cat'
					)],
					visitCondition=lambda: get_cat_at_position(Position(13, 8)) is not None and get_cat_at_position(Position(13, 8)).name == 'mew' and can_give_item(Position(13,8)),
					dialogs=[
						Dialog(
							lines=["They","beileved","me huh..."],
							right_cats=[get_cat_at_position(Position(13, 8))],
							left_cats=[npc],
							currentlyTalking='npc',
						),
						Dialog(
							lines=["Take after","my steps","will ya"],
							right_cats=[get_cat_at_position(Position(13, 8))],
							left_cats=[npc],
							currentlyTalking='npc',
							lambda_after=lambda: (give_item(Position(13,8), itemDict['MstQll']))
						),
						Dialog(
							lines=["Recieved","the mystic","quill"],
						)
					],
					postVisitDialog=[Dialog(
						lines=["Don't die", "live"],
						right_cats=[get_cat_at_position(Position(13, 8))],
						left_cats=[npc],
						currentlyTalking='npc'
					)]
				),
			],
			conversations=[
				Conversation(
					dialogs=[
						Dialog(
							lines=["Mew", 'why join', 'them'],
							left_cats=[mew],
							right_cats=[cat],
							currentlyTalking='cat'
						),
						Dialog(
							lines=["meow :("],
							left_cats=[cat],
							right_cats=[mew],
							currentlyTalking='mew',
							lambda_after=lambda: (
								level.enemies.remove(mew),
								setattr(mew, 'enemy', False),
								add_party_member(mew)
							)
						),
						Dialog(
							lines=["Mew has", "joined", "your party"],
						)
					],
					nameOne='cat',
					nameTwo='mew',
					condition=conversation_condition
				)
			]
		)
		return level

	def _build_level4():
		checkClearMem('level4')
		from Shared import get_map, get_npc, get_cat, get_bao
		npc = get_npc()
		cat = get_cat()
		bao = get_bao()
		level = None

		def conversation_condition():
			selCat = get_selected_cat()
			if selCat is None or selCat.name != 'cat':
				return False
			diff =  abs(selCat.position.x - bao.position.x) + abs(selCat.position.y - bao.position.y)
			return abs(diff) <= 1
		
		def visit_condition():
			return level is not None and level.enemies == [] and can_give_item(Position(7,13))
				

		level = Level(
			map=get_map(4),
			enemies=[
				generate_enemy(2, Position(0, 4), name='pig'),
				generate_enemy(3, Position(2, 9), name='snips', weapon='LongBow', classType='sniper'),
				generate_enemy(2, Position(2, 11), name='pig'),
				generate_enemy(3, Position(3, 10), name='pig'),
				bao,
				generate_enemy(4, Position(2, 13), name='himb', weapon='Spear', classType='warrior', ai='stand')
			],
			number=4,
			seizePosition=Position(2, 13),
			startingPositions=[Position(7,1), Position(6,2), Position(8,2)],
			houses=[
				House(
					position=Position(0, 0),
					preVistedDialogs=[Dialog(
						lines=["muggle,","freaking", "nerd"],
						left_cats=[npc],
						right_cats=[get_cat_at_position(Position(0, 0))],
						currentlyTalking='npc'
					)],
					visitCondition=lambda: get_cat_at_position(Position(0, 0)) is not None and get_cat_at_position(Position(0, 0)).classType == 'wizard' and can_give_item(Position(0,0)),
					dialogs=[Dialog(
						lines=["Oh,","a wizard!"],
						right_cats=[get_cat_at_position(Position(0, 0))],
						left_cats=[npc],
						currentlyTalking='npc',
						lambda_after=lambda: give_item(Position(0,0), itemDict['LghtngTm'])
					)],
					postVisitDialog=[Dialog(
						lines=["Use it","wisely."],
						right_cats=[get_cat_at_position(Position(0, 0))],
						left_cats=[npc],
						currentlyTalking='npc'
					)]
				),
				House(
					position=Position(1, 0),
					dialogs=[Dialog(
						lines=["If youre","speed is","great"],
						right_cats=[get_cat_at_position(Position(1, 0))],
						left_cats=[npc],
						currentlyTalking='npc'
					), Dialog(
						lines=["you can","double","attacks"],
						right_cats=[get_cat_at_position(Position(1, 0))],
						left_cats=[npc],
						currentlyTalking='npc'
					)],
				),
				House(
					position=Position(7, 13),
					preVistedDialogs=[Dialog(
						lines=["I was working","and toxic", "pigs showed"],
						right_cats=[get_cat_at_position(Position(7, 13))],
						left_cats=[npc],
						currentlyTalking='npc'
					), Dialog(
						lines=["I thought", "this was a", "conspiracy"],
						right_cats=[get_cat_at_position(Position(7, 13))],
						left_cats=[npc],
						currentlyTalking='npc'
					), Dialog(
						lines=["I would", "like them", "gone"],
						right_cats=[get_cat_at_position(Position(7, 13))],
						left_cats=[npc],
						currentlyTalking='npc'
					)],
					visitCondition=visit_condition,
					dialogs=[
						Dialog(
							lines=["Thank you","ridding the","pigs"],
							right_cats=[get_cat_at_position(Position(7, 13))],
							left_cats=[npc],
							currentlyTalking='npc'
						), Dialog(
							lines=["Take 50g","seems right"],
							right_cats=[get_cat_at_position(Position(7, 13))],
							left_cats=[npc],
							currentlyTalking='npc',
							lambda_after=lambda: modify_bank(50)
						), Dialog(
							lines=["Recieved","50g"]
						)
					]
				)
			],
			shops=[
				Shop(
					position=Position(3, 9),
					inventory=[
						ShopItem(itemDict['Bow'], 20),
						ShopItem(itemDict['EarthTm'], 25),
						ShopItem(itemDict['Sword'], 20)
					]
				)
			],
			conversations=[
				Conversation(
					dialogs=[
						Dialog(
							lines=["Why are", 'you a cat', 'bao'],
							left_cats=[bao],
							right_cats=[cat],
							currentlyTalking='cat'
						),
						Dialog(
							lines=["Dunno, I'm", 'just a cat'],
							left_cats=[bao],
							right_cats=[cat],
							currentlyTalking='bao',
							lambda_after=lambda: (
								level.enemies.remove(bao),
								setattr(bao, 'enemy', False),
								add_party_member(bao)
							)
						),
						Dialog(
							lines=["Will you", "join us", "bao"],
							left_cats=[bao],
							right_cats=[cat],
							currentlyTalking='cat'
						),
						Dialog(
							lines=["Bao has", "joined", "your party"],
						)
					],
					nameOne='cat',
					nameTwo='bao',
					condition=conversation_condition
				)
			]
		)
		return level

	def _build_level5():
		checkClearMem('level5')
		from Shared import get_map, get_npc, get_bub
		npc = get_npc()
		bub = get_bub()

		def houseCondition(position: Position):
			selCat = get_cat_at_position(position)
			if selCat is None:
				return False
			items = selCat.items
			item_names = [item.name for item in items]
			return 'Tuna' in item_names and can_give_item(position)
		
		def take_tuna(position: Position):
			selCat = get_cat_at_position(position)
			if selCat is None:
				return
			items = selCat.items
			for item in items:
				if item.name == 'Tuna':
					selCat.items.remove(item)
					break

		level = Level(
			map=get_map(5),
			enemies=[
				generate_enemy(3, Position(2, 6), name='mut'),
				generate_enemy(3, Position(9, 4), name='mut'),
				generate_enemy(3, Position(10, 10), name='mut'),
				generate_enemy(3, Position(12, 8), name='mut'),
				generate_enemy(4, Position(11, 12), name='mut', weapon='Slngsht'),
				generate_enemy(4, Position(5, 5), name='mut', weapon='Bow', classType='sniper'),
				generate_enemy(4, Position(0, 15), name='mut', weapon='LghtngTm', classType='wizard', ai='stand'),
			],
			number=5,
			seizePosition=Position(0, 15),
			startingPositions=[Position(13, 1), Position(14, 2), Position(13, 3), Position(14, 3)],
			houses=[
				House(
					multipleVisits=True,
					position=Position(8, 0),
					preVistedDialogs=[Dialog(
						lines=["I'll trade","any tuna","for 25g"],
						right_cats=[get_cat_at_position(Position(8, 0))],
						left_cats=[npc],
						currentlyTalking='npc'
					), Dialog(
						lines=["I don't","smell any","on you.."],
						right_cats=[get_cat_at_position(Position(8, 0))],
						left_cats=[npc],
						currentlyTalking='npc'
					)],
					dialogs=[Dialog(
						lines=["so....","trade tuna","for 25g,"],
						right_cats=[get_cat_at_position(Position(8, 0))],
						left_cats=[npc],
						currentlyTalking='npc'
					), Dialog(
						lines=["Deal?", 'A: yes', 'B: no'],
						right_cats=[get_cat_at_position(Position(8, 0))],
						left_cats=[npc],
						currentlyTalking='npc',
						lambda_after=lambda: (take_tuna(Position(8, 0)), modify_bank(25)),
						decision=True,
					)],
					visitCondition=houseCondition(Position(8, 0))
				),
				House(
					position=Position(14, 9),
					dialogs=[Dialog(
						lines=["Let me", "give some", "advice"],
						right_cats=[get_cat_at_position(Position(14, 9))],
						left_cats=[npc],
						currentlyTalking='npc'
					), Dialog(
						lines=["Snipers", "overpower", "Warriors"],
						right_cats=[get_cat_at_position(Position(14, 9))],
						left_cats=[npc],
						currentlyTalking='npc'
					), Dialog(
						lines=["Wizards", "overpower", "Snipers"],
						right_cats=[get_cat_at_position(Position(14, 9))],
						left_cats=[npc],
						currentlyTalking='npc'
					), Dialog(
						lines=["Warriors", "overpower", "Wizards"],
						right_cats=[get_cat_at_position(Position(14, 9))],
						left_cats=[npc],
						currentlyTalking='npc'
					), Dialog(
						lines=["So,","choose wisely"],
						right_cats=[get_cat_at_position(Position(14, 9))],
						left_cats=[npc],
						currentlyTalking='npc'
					), Dialog(
						lines=["Take 10g", "all I", "got"],
						right_cats=[get_cat_at_position(Position(14, 9))],
						left_cats=[npc],
						currentlyTalking='npc',
						lambda_after=lambda: modify_bank(10)
					), Dialog(
						lines=["Received", "10g"]
					)],
					postVisitDialog=[
						Dialog(
							lines=["Good luck", "and", "remember"],
							left_cats=[npc],
							right_cats=[get_cat_at_position(Position(14, 9))],
							currentlyTalking='npc'
						)
					]
				),
				House(
					position=Position(11, 15),
					preVistedDialogs=[Dialog(
						lines=["I heard","of a cat","named bao"],
						left_cats=[get_cat_at_position(Position(11, 15))],
						right_cats=[bub],
						currentlyTalking='bub'
					), Dialog(
						lines=["I will", "only talk", "to bao"],
						left_cats=[get_cat_at_position(Position(11, 15))],
						right_cats=[bub],
						currentlyTalking='bub'
					)],
					dialogs=[Dialog(
						lines=["Hello","bao, I","stinky..."],
						left_cats=[get_cat_at_position(Position(11, 15))],
						right_cats=[bub],
						currentlyTalking='bub'
					), Dialog(
						lines=["I","wish to","join you"],
						left_cats=[get_cat_at_position(Position(11, 15))],
						right_cats=[bub],
						currentlyTalking='bub',
						lambda_after=lambda: (bub.set_position(Position(11, 14)), add_party_member(bub))
					), Dialog(
						lines=["bub","joined the","party"],
					)],
					visitCondition=lambda: get_cat_at_position(Position(11, 15)) is not None and get_cat_at_position(Position(11, 15)).name == 'bao',
				),
				House(
					position=Position(1, 6),
					dialogs=[Dialog(
						lines=["Found","a Sword"],
						lambda_after=lambda: give_item(Position(2,6), itemDict['Sword']),
					)],
					visitCondition=lambda: get_cat_at_position(Position(2, 6)) is not None and can_give_item(Position(2, 6))
				)
			]
		)
		return level

	def _build_level6():
		checkClearMem('level6')
		from Shared import get_map
		level = Level(
			map=get_map(6),
			enemies=[
				generate_enemy(3, Position(6, 8), name='mut'),
				generate_enemy(3, Position(8, 7), name='mut'),
				generate_enemy(3, Position(7, 13), name='mut'),
				generate_enemy(3, Position(7, 3), name='mut'),
				generate_enemy(4, Position(13, 13), name='mut', weapon='Slngsht'),
				generate_enemy(4, Position(11, 8), name='mut', weapon='LongBow', classType='sniper'),
				generate_enemy(4, Position(15, 8), name='mut', weapon='LghtngTm', classType='warrior'),
				generate_enemy(5, Position(17, 8), name='mut', weapon='LghtngTm', classType='wizard'),
				generate_enemy(5, Position(16, 3), name='mut', weapon='LghtngTm', classType='wizard', ai='stand'),
			],
			number=6,
			seizePosition=Position(16, 3),
			startingPositions=[Position(2, 13), Position(3, 13), Position(2, 3), Position(3, 3), Position(2, 5)],
			shops=[
				Shop(
					Position(7, 13),
					inventory=[
						ShopItem(itemDict['Tuna'], 3),
						ShopItem(itemDict['Sword'], 30),
						ShopItem(itemDict['MstMeal'], 50),
						ShopItem(itemDict['Mace'], 35)
					]
				)
			]
		)
		return level

	def _build_level7():
		checkClearMem('level7')
		from Shared import get_map, get_npc
		npc = get_npc()
		level = Level(
			map=get_map(7),
			enemies=[
				generate_enemy(3, Position(2, 4), name='mut'),
				generate_enemy(3, Position(2, 10), name='mut'),
				generate_enemy(3, Position(8, 4), name='mut'),
				generate_enemy(3, Position(10, 14), name='mut'),
				generate_enemy(4, Position(9, 18), name='mut', weapon='Slngsht'),
				generate_enemy(4, Position(17, 13), name='mut', weapon='LongBow', classType='sniper'),
				generate_enemy(4, Position(12, 1), name='mut', weapon='LghtngTm', classType='warrior'),
				generate_enemy(5, Position(11, 1), name='mut', weapon='LghtngTm', classType='wizard'),
				generate_enemy(5, Position(16, 1), name='mut', weapon='LghtngTm', classType='wizard', ai='stand'),
			],
			number=7,
			seizePosition=Position(16, 1),
			startingPositions=[Position(2, 18), Position(3, 18), Position(1, 17), Position(3, 16), Position(4, 17)],
			shops=[
				Shop(
					Position(3, 1),
					inventory=[
						ShopItem(itemDict['Tuna'], 5),
						ShopItem(itemDict['LghtngTm'], 30),
						ShopItem(itemDict['WaterTm'], 30),
						ShopItem(itemDict['EarthTm'], 30)
					]
				), Shop(
					Position(4, 1),
					inventory=[
						ShopItem(itemDict['Spear'], 25),
						ShopItem(itemDict['Sword'], 20),
						ShopItem(itemDict['Repeater'], 30),
						ShopItem(itemDict['LongBow'], 35)
					]
				)
			],
			houses=[House(
					position=Position(1, 1),
					dialogs=[Dialog(
						lines=["I heard","there is","a wizard"],
						left_cats=[get_cat_at_position(Position(1, 1))],
						right_cats=[npc],
						currentlyTalking='npc'
					)],
				), House(
					position=Position(17, 15),
					dialogs=[Dialog(
						lines=["I heard","there is","a wizard"],
						left_cats=[get_cat_at_position(Position(17, 15))],
						right_cats=[npc],
						currentlyTalking='npc'
					)]
				), House(
					position=Position(16, 1),
					dialogs=[Dialog(
						lines=["I heard","there is","a wizard"],
						left_cats=[get_cat_at_position(Position(16, 1))],
						right_cats=[npc],
						currentlyTalking='npc'
					)]
				)
			]
		)
		return level

	def _build_level8():
		checkClearMem('level8')
		from Shared import get_map, get_cat
		cat = get_cat()
		level = Level(
			map=get_map(8),
			enemies=[
				generate_enemy(4, Position(14, 9), name ='jr'),
				generate_enemy(4, Position(15, 9), name='mini'),
				generate_enemy(4, Position(8, 11), name='l'),
				generate_enemy(5, Position(10, 5), name='wago', weapon='Slngsht'),
				generate_enemy(6, Position(4, 2), ai='stand', name='xl', weapon='Stick')
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
		from Shared import get_map, get_npc
		npc = get_npc()
		level = Level(
			map=get_map(9),
			enemies=[
				generate_enemy(3, Position(15, 16), name='mut'),
				generate_enemy(3, Position(16, 13), name='mut'),
				generate_enemy(3, Position(17, 13), name='mut'),
				generate_enemy(3, Position(5, 2), name='mut'),
				generate_enemy(5, Position(13, 5), name='mut', weapon='Repeater', classType='sniper'),
				generate_enemy(5, Position(11, 11), name='mut', weapon='Slngsht', classType='sniper'),
				generate_enemy(4, Position(3, 7), name='mut', weapon='Slngsht'),
				generate_enemy(5, Position(18, 2), name='mut', weapon='LghtngTm', classType='wizard'),
				generate_enemy(5, Position(14, 2), name='mut', weapon='LongBow', classType='sniper'),
				generate_enemy(5, Position(16, 2), name='mut', weapon='LghtngTm', classType='warrior'),
				generate_enemy(5, Position(16, 0), name='mut', weapon='LghtngTm', classType='wizard', ai='stand'),
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

checkClearMem('level_cache levels')

def fetch_level(level_number):
	if level_number in _level_cache:
		return _level_cache[level_number]

	gc.collect()
	levels = Levels
	if level_number == 1:
		level = levels._build_level1()
	elif level_number == 2:
		level = levels._build_level2()
	elif level_number == 3:
		level = levels._build_level3()
	elif level_number == 4:
		level = levels._build_level4()
	elif level_number == 5:
		level = levels._build_level5()
	elif level_number == 6:
		level = levels._build_level6()
	elif level_number == 7:
		level = levels._build_level7()
	elif level_number == 8:
		level = levels._build_level8()
	elif level_number == 9:
		level = levels._build_level9()
	else:
		raise ValueError(f"Level {level_number} does not exist.")

	_level_cache.clear()
	_level_cache[level_number] = level
	gc.collect()
	return level

checkClearMem('level_cache finished')

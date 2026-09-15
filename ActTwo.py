from sys import path as syspath

syspath.insert(0, '/Games/CatsEmblem')

from Items import itemDict

from Callbacks import add_to_party as add_party_member, can_give_item, give_item, get_cat_at_pos as get_cat_at_position, get_selected_cat, build_dialogs

def set_game_state_callbacks(*_args):
	pass


class ActTwoLevels:

	def _build_level6():
		from MapData import get_map
		from Shared import get_bub, Blockade, Button, Position, Conversation, generate_enemy, Shop, ShopItem, Level

		bub = get_bub()

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

		def conversation_condition():
			selCat = get_selected_cat()
			if selCat is None or selCat.name != 'bao':
				return False
			diff =  abs(selCat.position.x - bub.position.x) + abs(selCat.position.y - bub.position.y)
			return abs(diff) <= 1
		exel = generate_enemy(7, Position(16, 3), name='exel', weapon='LghtngTm', classType='wizard', ai='stand', deathDialog=[["I guess|this is|the end|of my|journey", 'exel']])
		level = Level(
			map=get_map(6),
			enemies=[
				generate_enemy(3, Position(6, 8), name='mut', weapon='Sword'),
				generate_enemy(4, Position(8, 7), name='mut', weapon='Sword'),
				generate_enemy(3, Position(7, 13), name='mut', weapon='Sword'),
				generate_enemy(4, Position(7, 3), name='mut', weapon='Sword'),
				generate_enemy(5, Position(13, 13), name='mut', weapon='Sword', classType='warrior'),
				generate_enemy(5, Position(11, 8), name='mut', weapon='LongBow', classType='sniper'),
				generate_enemy(6, Position(15, 8), name='mut', weapon='Mace', classType='warrior'),
				generate_enemy(5, Position(17, 8), name='mut', weapon='EarthTm', classType='wizard'),
				exel,
				bub
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
			blockades=[Barrier1, Barrier2],
			conversations=[
				Conversation(
					dialogs=lambda: build_dialogs(
						[
							["BAO im|so happy|to see you|I knew|you would|come", bub.name],
							["Yeah I|guess so", get_selected_cat().name, lambda: (
								level.enemies.remove(bub),
								setattr(bub, 'enemy', False),
								add_party_member(bub)
							)],
							["Bub has|joined|your party", None]
						],
						left=[bub],
						right=[get_selected_cat()],
					),
					nameOne='bao',
					nameTwo='bub',
					condition=conversation_condition
				)
			],
			fightDialogs=[
				['*', 'exel', lambda: build_dialogs(
					[
						["Do you|think a|statue of|me would|look good|in gold|or silver|realize you|will be|the one|to mine it.You see,|filth is|inevitable|you will|not stop|the will|of mono", 'exel'],
						["How dare|you jest|you will|not defile|this temple!|I've come|this far|you are|a mere|stepping|stone to|liberation", get_selected_cat().name] if get_selected_cat.name != 'cat' else ["*EeOw*|*meow*|(Id much|rather keep|the statues|we already|have.|Ohh,|and I WILL|kick]your ass)", get_selected_cat().name],
						["A stepping|stone? You|better that|up little|cat", 'exel'] if get_selected_cat.name != 'cat' else ["What?|Am I|supposed to|understand|that?", 'exel'],
					],
					left=[exel],
					right=[get_selected_cat()],
				)]
			]
		)
		return level

	def _build_level7():
		from MapData import get_map
		from Shared import get_npc, Position, generate_enemy, Shop, ShopItem, Level, House
		npc = get_npc()
		muke = generate_enemy(8, Position(9, 1), name='muke', weapon='LghtngTm', classType='wizard', ai='stand', deathDialog=[["I guess|this is|the end|of my|journey", 'muke']])
		level = Level(
			map=get_map(7),
			enemies=[
				generate_enemy(4, Position(9, 9), name='mut', weapon='Sword'),
				generate_enemy(3, Position(10, 8), name='mut', weapon='Sword'),
				generate_enemy(4, Position(3, 4), name='mut', ai='path', path=[Position(0, 8), Position(2, 11)]),
				generate_enemy(5, Position(4, 4), name='mut', ai='path', path=[Position(1, 8), Position(3, 11)], weapon='Repeater', classType='sniper'),
				generate_enemy(4, Position(6, 11), name='mut', weapon='Slngsht'),
				generate_enemy(5, Position(2, 2), name='mut', weapon='LongBow', classType='sniper'),
				generate_enemy(6, Position(10, 2), name='mut', weapon='Spear', classType='warrior'),
				generate_enemy(7, Position(8, 2), name='mut', weapon='LghtngTm', classType='wizard'),
				muke
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
					dialogs=lambda: build_dialogs(
						[
							["You have|come far|take this", npc.name],
							["Received|Magic|Powder", None, lambda: give_item(Position(1, 12), itemDict['MagPowder'])],
							["Should give|a bit|extra exp", npc.name]
						],
						left=[npc],
						right=[get_cat_at_position(Position(1, 12))],
					)
				), House(
					position=Position(5, 7),
					dialogs=lambda: build_dialogs(
						[
							["I dont","get many","visitors", npc.name],
							["I saved","this for","you", npc.name],
							["Received","a Rabbit's Foot", None, lambda: give_item(Position(5,7), itemDict['RabFoot'])]
						],
						left=[npc],
						right=[get_cat_at_position(Position(5, 7))],
					),
					postVisitDialog=lambda: build_dialogs(
						[
							["I hope","you use it","well", npc.name]
						],
						left=[npc],
						right=[get_cat_at_position(Position(5, 7))],
					)
				)
			],
			fightDialogs=[
				['*', 'exel', lambda: build_dialogs(
					[
						["wow", 'muke']
					],
					left=[muke],
					right=[get_selected_cat()],
				)]
			]
		)
		return level

	def _build_level8():
		from Shared import get_npc, generate_enemy, Position, House, Level
		from MapData import get_map

		def house_condition(position: Position):
			selCat = get_selected_cat()
			if not can_give_item(position):
				return False
			if selCat and selCat.classType == 'wizard':
				return True
			return False

		def house_condition2(position: Position):
			selCat = get_selected_cat()
			if not can_give_item(position):
				return False
			if selCat and selCat.classType == 'warrior':
				return True
			return False

		npc = get_npc()
		xl = generate_enemy(9, Position(4, 2), ai='stand', name='xl', weapon='Axe', classType='warrior', deathDialog=[["I guess|this is|the end|of my|journey", 'xl']])

		level = Level(
			map=get_map(8),
			enemies=[
				generate_enemy(6, Position(8, 11), name ='jr', weapon='Sword', classType='warrior'),
				generate_enemy(7, Position(6, 5), name='mini', weapon='Mace', classType='warrior'),
				generate_enemy(7, Position(5, 5), name='l', weapon='Spear', classType='warrior'),
				generate_enemy(8, Position(3, 5), name='beef', classType='warrior', weapon='Spear'),
				generate_enemy(8, Position(4, 5), name='wago', classType='sniper', weapon='Repeater'),
				xl
			],
			number=8,
			seizePosition=Position(4, 2),
			startingPositions=[Position(16, 3), Position(15, 3), Position(16, 4), Position(15, 4), Position(16, 5)],
			houses=[
				House(
					position=Position(16, 10),
					preVisitedDialogs=lambda: build_dialogs(
						[
							["I need|strong|wizard", npc.name],
						],
						left=[npc],
						right=[get_cat_at_position(Position(16, 10))],
					),
					dialogs=lambda: build_dialogs(
						[
							["I see|strong|wizard", npc.name],
							["I have|a gift|for you", npc.name, lambda: give_item(Position(16, 10), itemDict['NecTome'])],
							["Received|a Necromancy|Tome", None]
						],
						left=[npc],
						right=[get_cat_at_position(Position(16, 10))],
					),
					visitCondition=lambda: house_condition(Position(16, 10))
				),
				House(
					position=Position(17, 10),
					preVisitedDialogs=lambda: build_dialogs(
						[
							["I need|strong|warrior", npc.name],
						],
						left=[npc],
						right=[get_cat_at_position(Position(17, 10))],
					),
					dialogs=lambda: build_dialogs(
						[
							["Strong|warrior|I see", npc.name],
							["I have|a gift|for you", npc.name, lambda: give_item(Position(17, 10), itemDict['Axe'])],
							["Received|an Axe", None]
						],
						left=[npc],
						right=[get_cat_at_position(Position(17, 10))],
					),
					visitCondition=lambda: house_condition2(Position(17, 10))
				)
			],
			fightDialogs=[
				['*', 'xl', lambda: build_dialogs(
					[
						["wow", 'xl']
					],
					left=[xl],
					right=[get_selected_cat()],
				)]
			]
		)
		return level

	def _build_level9():
		from Shared import get_npc, generate_enemy, Position, Blockade, House, Shop, ShopItem, Level
		from MapData import get_map
		npc = get_npc()

		pursuer1 = generate_enemy(5, Position(17, 6), name='mut', ai='path', path=[Position(16, 3), Position(4, 4), Position(2, 11)], weapon='Sword')
		pursuer2 = generate_enemy(6, Position(18, 6), name='mut', weapon='Repeater', classType='sniper', ai='path', path=[Position(16, 3), Position(4, 4), Position(2, 11)])

		pursuerIds = [pursuer1.id, pursuer2.id]

		barrier1 = Blockade(
			positions=[Position(2, 3)]
		)

		def house_condition():
			if not pursuerIds in [enemy.id for enemy in level.enemies]:
				return True
			return False

		zero = generate_enemy(9, Position(16, 0), name='zero', weapon='LghtngTm', classType='wizard', ai='stand', deathDialog=[["I guess|this is|the end|of my|journey", 'zero']])
		level = Level(
			map=get_map(9),
			enemies=[
				generate_enemy(4, Position(15, 16), name='mut', weapon='Sword', classType='warrior'),
				generate_enemy(5, Position(16, 13), name='mut', weapon='Sword', classType='warrior'),
				generate_enemy(4, Position(17, 13), name='mut', weapon='Sword', classType='warrior'),
				pursuer1,
				pursuer2,
				generate_enemy(7, Position(17, 9), name='mut', weapon='Slngsht', classType='sniper'),
				generate_enemy(7, Position(16, 8), name='mut', weapon='Bow', classType='sniper'),
				generate_enemy(8, Position(18, 2), name='mut', weapon='LghtngTm', classType='wizard'),
				generate_enemy(8, Position(14, 2), name='mut', weapon='LongBow', classType='sniper'),
				generate_enemy(8, Position(16, 2), name='mut', weapon='LghtngTm', classType='warrior'),
				zero
			],
			number=9,
			seizePosition=Position(16, 0),
			startingPositions=[Position(5, 17), Position(4, 17), Position(6, 16), Position(7, 16), Position(8, 16)],
			houses=[
				House(
					position=Position(1, 1),
					dialogs=lambda: build_dialogs(
						[
							["Take this|for saving|town", npc.name, lambda: give_item(Position(1, 1), itemDict['RabFoot'])],
							["Received|a Rabbit's|Foot", None]
						],
						left=[npc],
						right=[get_cat_at_position(Position(1, 1))],
					),
					visitCondition=lambda: can_give_item(Position(1, 1))
				), House(
					position=Position(2, 1),
					dialogs=lambda: build_dialogs(
						[
							["You will|need this.|Just know,|power,|is it|given?|Today it|is", npc.name],
							["Received|Void Sword", None, lambda: give_item(Position(2, 1), itemDict['VoidSwd'])]
						],
						left=[npc],
						right=[get_cat_at_position(Position(2, 1))],
					),
					visitCondition= lambda: can_give_item(Position(2, 1)),
				), House(
					position=Position(0, 10),
					preVisitedDialogs=lambda: build_dialogs(
						[
							["Big issue|town is|locked", npc.name],
							["I can|open it|for you", npc.name],
							["But I|need help", npc.name],
							["There are|pursuers|coming here", npc.name],
						],
						left=[npc],
						right=[get_cat_at_position(Position(0, 10))],
					),
					dialogs=lambda: build_dialogs(
						[
							["I open|the gate|to town", npc.name, lambda: barrier1.clear()],
							["Opened|gate", None]
						],
						left=[npc],
						right=[get_cat_at_position(Position(0, 10))],
					),
					visitCondition=house_condition
				)
			],
			shops=[
				Shop(
					Position(3, 1),
					inventory=[
						ShopItem(itemDict['Tuna'], 3),
						ShopItem(itemDict['MultiShot'], 35),
						ShopItem(itemDict['Launcher'], 60),
						ShopItem(itemDict['BulTome'], 355)
					]
				)
			],
			blockades=[barrier1],
			fightDialogs=[
				['*', 'zero', lambda: build_dialogs(
					[
						["wow", 'zero']
					],
					left=[zero],
					right=[get_selected_cat()],
				)]
			]
		)
		return level

	def _build_level10():
		from MapData import get_map
		from Shared import generate_enemy, Position, Blockade, Button, Level, OverlayObject
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

		mono = generate_enemy(11, Position(12, 4), name='mono', weapon='EarthTm', classType='wizard', ai='stand', deathDialog=[["I guess|this is|the end|of my|journey", 'mono']])
		level = Level(
			map=get_map(10),
			enemies=[
				generate_enemy(5, Position(4, 16), name='mut', classType='warrior', weapon='Sword'),
				generate_enemy(6, Position(20, 16), name='mut', classType='warrior', weapon='Sword'),
				generate_enemy(5, Position(20, 12), name='mut', classType='warrior', weapon='Spear'),
				generate_enemy(6, Position(4, 12), name='mut', classType='warrior', weapon='Mace'),
				generate_enemy(7, Position(13, 11), name='mut', weapon='Repeater', classType='sniper'),
				generate_enemy(8, Position(11, 11), name='mut', weapon='Slngsht', classType='sniper'),
				generate_enemy(8, Position(5, 15), name='mut', weapon='Bow', classType='sniper'),
				generate_enemy(9, Position(10, 6), name='mut', weapon='LghtngTm', classType='wizard'),
				generate_enemy(10, Position(12, 6), name='mut', weapon='LongBow', classType='sniper'),
				generate_enemy(10, Position(14, 6), name='mut', weapon='Mace', classType='warrior'),
				mono,
			],
			number=10,
			seizePosition=Position(12, 4),
			startingPositions=[Position(10, 18), Position(11, 18), Position(12, 18), Position(13, 18), Position(14, 18)],
			buttons=[button1, button2, button3, button4],
			blockades=[barrier1, barrier2],
			overlayObjects=[OverlayObject(position=Position(10, 0), objectName='cat_head', boundPositions=[Position(10, 0), Position(10, 4), Position(14, 4)])],
			fightDialogs=[
				['*', 'mono', lambda: build_dialogs(
					[
						["wow", 'mono']
					],
					left=[mono],
					right=[get_selected_cat()],
				)]
			]
		)
		return level

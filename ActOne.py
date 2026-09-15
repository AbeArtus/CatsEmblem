from sys import path as syspath
syspath.insert(0, '/Games/CatsEmblem')

from Items import itemDict
from Shared import Conversation, Dialog, House, Position, Shop, ShopItem, Level, generate_enemy, build_dialogs

from Callbacks import add_to_party as add_party_member, update_bank as modify_bank, can_give_item, give_item, get_cat_at_pos as get_cat_at_position, get_selected_cat

def set_game_state_callbacks(*_args):
	pass

class ActOneLevels:
	def _build_level1():
		from MapData import get_map
		from Shared import get_npc, get_cat, get_tac
		npc = get_npc()
		cat = get_cat()
		tac = get_tac()
		boss = generate_enemy(2, Position(1, 2), ai='stand', name='Doug', classType='warrior', deathDialog=[["If only|I was|a final|boss|I would|have kicked|your ass", 'Doug']])
		bossId = boss.id
		level = None
		level = Level(
			map = get_map(1),
			enemies=[
				generate_enemy(1, Position(4, 4), name='pig', ai='path', path=[Position(4, 7)]),
				generate_enemy(2, Position(6, 4), name='pig', ai='path', path=[Position(4, 5)]),
				boss,
			],
			number=1,
			seizePosition=Position(1, 2),
			startingPositions=[Position(6,14), Position(8,14)],
			houses = [
				House(
					position = Position(6, 11),
					dialogs = lambda: build_dialogs(
						[
							["The weird|pigs are|back...|Cat|save our|village,|its chaos|the Mayors|missing|Take 50g|if it|helps,", npc.name],
							["Received|50g", None, lambda: modify_bank(50)],
						],
						left=[npc],
						right=[cat],
					),
					postVisitDialog= lambda: build_dialogs(
						[
							["Thats all|we got..", npc.name],
						],
						left=[npc],
						right=[cat],
					),
				),
				House(
					position=Position(8, 11),
					dialogs= lambda: build_dialogs(
						[
							["HEY TAC|wake up|and help", cat.name],
							["*stretch*|*meow*|... *meow*", tac.name],
							["yeah", cat.name, lambda: (tac.set_position(Position(8, 12)), add_party_member(tac))],
						],
						left=[tac],
						right=[cat],
					),
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
			],
			fightDialogs=[
				['*', bossId, lambda: build_dialogs(
					[
						["Ahh peuny|Cats...||I will|destroy you|||I have|no time|for cats", boss.name],
						["I really|dislike you", get_selected_cat().name],
						["Your disdain|will be|short lived|I will|crush you|and this|village|if you|dare oppose|assimilation|we WILL|wipe every|rebel", boss.name],
					],
					left=[boss],
					right=[get_selected_cat()]
				)]
			]
		)
		return level

	def _build_level2():
		from MapData import get_map
		from Shared import get_npc
		npc = get_npc()
		level = None

		def visit_condition():
			return level is not None and level.enemies == [] and can_give_item(Position(2,1))

		guy = generate_enemy(3, Position(1, 12), ai='stand', name='guy', classType='warrior', deathDialog=[["I refuse|to be a|pawn.|The wings|of change|curse you", 'guy']])
		level = Level(
			map=get_map(2),
			enemies=[
				generate_enemy(1, Position(5, 13), name='mut', ai='path', path=[Position(11, 13)]),
				generate_enemy(2, Position(5, 14), name='mut', ai='path', path=[Position(12, 12)]),
				generate_enemy(2, Position(1, 10), name='mut', ai='path', path=[Position(3, 2)]),
				generate_enemy(3, Position(3, 13), name='mut'),
				generate_enemy(3, Position(4, 11), name='mut', weapon='Slngsht'),
				guy
			],
			number=2,
			seizePosition=Position(1, 12),
			startingPositions=[Position(11,2), Position(11,1), Position(12,1)],
			houses=[
				House(
					position=Position(2, 1),
					preVisitedDialogs=lambda: build_dialogs(
						[
							["Save us|and I'll|owe you", npc.name],
						],
						left=[npc],
						right=[Position(2, 1)]
					),
					dialogs=lambda: build_dialogs(
						[
							["Thank you|forced to|give crops.|Some homes|completely|destroyed", npc.name],
							["Take this|mystic potion", None, lambda: give_item(Position(2,1), itemDict['MystPot'])],
							["Received|Mystic|Potion", None]
						],
						left=[npc],
						right=[Position(2, 1)]
					),
					visitCondition=visit_condition
				),
				House(
					position=Position(4, 1),
					dialogs= lambda: build_dialogs(
						[
							["Trees,|grass,|and houses|give extra|avoid||Youll need|all the|advantage|you can|get", npc.name],
						],
						left=[npc],
						right=[Position(4, 1)]
					),
				),
				House(
					position=Position(12, 13),
					dialogs= lambda: build_dialogs(
						[
							["I hear|some|items...|promote|trained|pupils|mystic quill|promotes to|sniper|mysticPotion|promotes to|wizard|mystic meal|promotes to|warrior|you have|to be lv5|though", npc.name],
						],
						left=[npc],
						right=[Position(12, 13)]
					)
				)
			],
			fightDialogs=[
				['*', guy.id, lambda: build_dialogs(
					[
						["Why bother|with runts|like you", 'guy'],
						["RUNTS!?|Would you|say that|to someone|whos taken|out your|patrol?", get_selected_cat().name],
						["They are|pawns to|me, and...|I know you|took doug|out|whats thats|supposed to|impress me?", 'guy'],
						["Im not|doing this|for you", get_selected_cat().name],
					],
					left=[guy],
					right=[get_selected_cat()]
				)]
			]
		)
		return level

	def _build_level3():
		from Shared import get_npc, get_mew
		from MapData import get_map
		npc = get_npc()
		mew = get_mew()
		level = None

		def conversation_condition():
			selCat = get_selected_cat()
			if selCat is None or selCat.name != 'cat':
				return False
			diff =  abs(selCat.position.x - mew.position.x) + abs(selCat.position.y - mew.position.y)
			return abs(diff) <= 1

		bar = generate_enemy(4, Position(13, 1), ai='stand', name='bar', classType='warrior', deathDialog=[["The filth|Will hear|of my|defeat|and I|Will be|avenged", 'bar']])
		level = Level(
			map=get_map(3),
			enemies=[
				generate_enemy(2, Position(3, 10), name='mut',ai='path', path=[Position(11, 9)]),
				generate_enemy(2, Position(3, 9), name='mut'),
				generate_enemy(2, Position(5, 14), name='mut'),
				generate_enemy(3, Position(9, 4), name='mut'),
				generate_enemy(3, Position(14, 3), name='mut'),
				mew,
				bar
			],
			number=3,
			startingPositions=[Position(10, 13), Position(11, 14)],
			seizePosition=Position(13, 1),
			houses=[
				House(
					position=Position(13, 8),
					preVisitedDialogs=lambda: build_dialogs(
						[
							["There is|a legendary|cat...", npc.name],
							["that|possesses|the dna..", npc.name],
							["of all|species.|Its name..", npc.name],
							["is mew.|cat must|save him", npc.name],
						],
						left=[npc],
						right=[Position(13, 8)]
					),
					visitCondition=lambda: get_cat_at_position(Position(13, 8)) is not None and get_cat_at_position(Position(13, 8)).name == 'mew' and can_give_item(Position(13,8)),
					dialogs=lambda: build_dialogs(
						[
							["They|believed|me huh...|take after|my steps|will ya", npc.name, lambda: give_item(Position(13,8), itemDict['MstMeal'])],
							["Recieved|the mystic|meal", None]
						],
						left=[npc],
						right=[Position(13, 8)]
					),
					postVisitDialog=lambda: build_dialogs(
						[
							["Don't die", "live", npc.name]
						],
						left=[npc],
						right=[Position(13, 8)]
					)
				),
			],
			conversations=[
				Conversation(
					dialogs=lambda: build_dialogs(
						[
							["Mew...|why join|them", mew.name],
							["meow :(", mew.name, lambda: (level.enemies.remove(mew), setattr(mew, 'enemy', False), add_party_member(mew))],
							["Mew has|joined|your party", None]
						],
						left=[mew],
						right=[Position(13, 1)]
					),
					nameOne='cat',
					nameTwo='mew',
					condition=conversation_condition
				)
			],
			fightDialogs=[
				['cat', 'bar', lambda: build_dialogs(
					[["Cat huh|news travels|fast||I was|eager for|out meeting|please don't|disappoint", 'bar']],
					left=[bar],
					right=[get_selected_cat()]
				)],
				['tac', 'bar', lambda: build_dialogs(
					[
						["tac huh|I have|heard so|much from|the prisoners|you've been|sold out|to many|times to|count", 'bar'],
						["...|*sad meow*|..*sigh*|(See this|is exactly|why I|didnt want|to come here", 'tac']
					],
					left=[get_selected_cat()],
					right=[bar]
				)],
				['mew', 'bar', lambda: build_dialogs(
					[
						["I knew|you would|betray us", 'bar'],
						["Then why|even bother|keeping me|I guess|you must|need us", 'mew']
					],
					left=[get_selected_cat()],
					right=[bar]
				)]
			]
		)
		return level

	def _build_level4():
		from Shared import get_npc, get_cat, get_bao
		from MapData import get_map
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
				

		himb = generate_enemy(5, Position(2, 13), name='himb', weapon='Spear', classType='warrior', ai='stand', deathDialog=[["I really|was excited|to crush|you|my raise|would have|been|priceless", 'himb']])
		level = Level(
			map=get_map(4),
			enemies=[
				generate_enemy(2, Position(0, 9), name='pig', ai='path', path=[Position(0, 2)]),
				generate_enemy(3, Position(2, 9), name='snips', weapon='LongBow', classType='sniper'),
				generate_enemy(3, Position(2, 11), name='pig'),
				generate_enemy(4, Position(3, 10), name='pig'),
				bao,
				himb,
			],
			number=4,
			seizePosition=Position(2, 13),
			startingPositions=[Position(7,1), Position(6,2), Position(8,2)],
			houses=[
				House(
					position=Position(0, 0),
					preVisitedDialogs=[Dialog(
						lines=["muggle...", "no words", "for you"],
						left_cats=[npc],
						right_cats=[Position(0, 0)],
						currentlyTalking='npc'
					)],
					visitCondition=lambda: get_cat_at_position(Position(0, 0)) is not None and get_cat_at_position(Position(0, 0)).classType == 'wizard' and can_give_item(Position(0,0)),
					dialogs=lambda: build_dialogs(
						[
							["OH|a|Wizard!|Here|I have|something", npc.name],
							["Take this|Lightning|Tome|This world|needs more|magic", npc.name, lambda: give_item(Position(0,0), itemDict['LghtngTm'])],
							["Received|Lightning|Tome", None]
						],
						left=[npc],
						right=[Position(0, 0)]
					),
					postVisitDialog=lambda: build_dialogs(
						[
							["Use it","wisely.", npc.name]
						],
						left=[npc],
						right=[Position(0, 0)]
					)
				),
				House(
					position=Position(1, 0),
					dialogs=lambda: build_dialogs(
						[
							["If you\'re|speed is|great|you can|double|attack", npc.name],
						],
						left=[npc],
						right=[Position(1, 0)]
					),
				),
				House(
					position=Position(7, 13),
					preVisitedDialogs=lambda: build_dialogs(
						[
							["I was|working|and toxic|pigs showed", npc.name],
							["I thought|this was a|conspiracy", npc.name],
							["I would|like them|gone", npc.name],
						],
						left=[npc],
						right=[Position(7, 13)]
					),
					visitCondition=visit_condition,
					dialogs=lambda: build_dialogs(
						[
							["Thank you|ridding the|pigs|Take 50g|seems right", npc.name, lambda: modify_bank(50)],
							["Received|50g", None]
						],
						left=[npc],
						right=[Position(7, 13)]
					),
				)
			],
			shops=[
				Shop(
					position=Position(3, 9),
					inventory=[
						ShopItem(itemDict['Tuna'], 3),
						ShopItem(itemDict['Spear'], 15),
						ShopItem(itemDict['Sword'], 20),
						ShopItem(itemDict['EarthTm'], 30)
					]
				)
			],
			conversations=[
				Conversation(
					dialogs=lambda: build_dialogs(
						[
							["Why are|you a cat|bao", cat.name],
							["beyond me,|I'm just|a cat", bao.name, lambda: (level.enemies.remove(bao), setattr(bao, 'enemy', False), add_party_member(bao))],
							["Will you|join us|bao", cat.name],
							["Bao has|joined|your party", None]
						],
						left=[cat],
						right=[bao]
					),
					nameOne='cat',
					nameTwo='bao',
					condition=conversation_condition
				)
			],
			fightDialogs=[
				['*', 'himb', lambda: build_dialogs(
					[
						["Im feeling|real filthy|today|absolutly|gross actually|we can|fight|but its|gonna stain", 'himb'],
						["Did you|prepare that?" if get_selected_cat().name != 'tac' else "...|(disbeleif)", get_selected_cat().name],
					],
					left=[himb],
					right=[get_selected_cat()]
				)]
			]
		)
		return level

	def _build_level5():
		from Shared import get_npc
		from MapData import get_map
		npc = get_npc()

		def houseCondition(position: Position):
			selCat = get_cat_at_position(position)
			if selCat is None:
				return False
			items = selCat.items
			item_names = [item.name for item in items]
			return 'Tuna' in item_names
		
		def take_tuna(position: Position):
			selCat = get_cat_at_position(position)
			if selCat is None:
				return
			items = selCat.items
			for item in items:
				if item.name == 'Tuna':
					selCat.items.remove(item)
					break
		wlbr = generate_enemy(6, Position(0, 15), name='wlbr', weapon='LghtngTm', classType='wizard', ai='stand', deathDialog=[["Welp, just|know its|really hot|in the|south so|if I dont|finish you|the heat|will", 'wlbr']])
		level = Level(
			map=get_map(5),
			enemies=[
				generate_enemy(3, Position(1, 6), name='mut', weapon='Sword'),
				generate_enemy(4, Position(5, 5), name='mut', weapon='Sword'),
				generate_enemy(5, Position(5, 7), name='mut', weapon='Slngsht'),
				generate_enemy(4, Position(4, 6), name='mut', ai='path', path=[Position(8, 1)]),
				generate_enemy(3, Position(4, 15), name='mut', ai='path', path=[Position(11, 15), Position(14, 2)]),
				generate_enemy(5, Position(3, 15), name='mut', weapon='Bow', classType='sniper'),
				wlbr
			],
			number=5,
			seizePosition=Position(0, 15),
			startingPositions=[Position(13, 1), Position(14, 2), Position(13, 3), Position(14, 3)],
			houses=[
				House(
					multipleVisits=True,
					position=Position(8, 0),
					preVisitedDialogs=lambda: build_dialogs(
						[
							["I'll trade|any tuna|for 25g", npc.name],
							["I don't|smell any|on you..", npc.name]
						],
						left=[npc],
						right=[Position(8, 0)]
					),
					dialogs=lambda: build_dialogs(
						[
							["so....|trade tuna|for 25g,", npc.name],
							["Deal?|A: yes|B: no", npc.name, lambda: (take_tuna(Position(8, 0)), modify_bank(25)) if houseCondition(Position(8, 0)) else None, True],
						],
						left=[npc],
						right=[Position(8, 0)]
					),
					visitCondition=houseCondition(Position(8, 0))
				),
				House(
					position=Position(14, 9),
					dialogs=lambda: build_dialogs(
						[
							["Let me|give some|advice|Snipers|overpower|Warriors|Wizards|overpower|Snipers|Warriors|overpower|Wizards|So choose|wisely||Here Take|10g all I|got", npc.name, lambda: modify_bank(10)],
							["Received","10g", None]
						],
						left=[npc],
						right=[Position(14, 9)]
					),
					postVisitDialog=[
						lambda: build_dialogs(
							[
								["Good luck", "and", "remember", npc.name]
							],
							left=[npc],
							right=[Position(14, 9)]
						)
					]
				),
				House(
					position=Position(15, 11),
					dialogs=lambda: build_dialogs(
						[
							["Take this|ring", npc.name, lambda: give_item(Position(15,11), itemDict['PowerRing'])],
							["Received|Ring", None]
						],
						left=[npc],
						right=[Position(15, 11)]
					),
				),
				House(
					position=Position(1, 6),
					dialogs=[Dialog(
						lines=["Found","Armor"],
						lambda_after=lambda: give_item(Position(1,6), itemDict['Armor']),
					)],
					visitCondition=lambda: get_cat_at_position(Position(1, 6)) is not None and can_give_item(Position(1, 6)),
					indestructible=True
				)
			],
			shops=[
				Shop(
					Position(7, 0),
					inventory=[
						ShopItem(itemDict['Sword'], 20),
						ShopItem(itemDict['Mace'], 20),
						ShopItem(itemDict['WaterTm'], 30),
						ShopItem(itemDict['LghtngTm'], 30)
					]
				)
			],
			fightDialogs=[['*', 'wlbr', lambda: build_dialogs(
				[
					["This is|where the|charade..|ends your|pretend hero|dies I|have one|job. Keeping|cats like|you out|of the|south island", 'wlbr'],
					["Look at|me||I was|born to|be a captain|I will|get passage|to the|south" if get_selected_cat().name != 'tac' else "*meow*|(cats like|me? whats|that even|mean?)", get_selected_cat().name],
				],
				left=[wlbr],
				right=[get_selected_cat()]
			)]]
		)
		return level


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
		boss = generate_enemy(2, Position(1, 2), ai='stand', name='Doug', classType='warrior', deathDialog=[["If only|I was|a final|boss|I would|have kicked|your ass|Like you|could make|it that|far anyways|the seven|retainers|will|avenge me", 'Doug']])
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
						["Ahh peuny|Cats...||Looking for|Your mayor?|hahaha|You really|are|clueless|I will|destroy you|||I have|no time|for cats", boss.name],
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
							["I was|working|and filth|showed", npc.name],
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
		exel = generate_enemy(7, Position(16, 3), name='exel', weapon='LghtngTm', classType='wizard', ai='stand', deathDialog=[["Even if|its not me|to do it|you shall|join the|filth", 'exel']])
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
							["Yeah|:)", get_selected_cat().name, lambda: (
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
						["Do you|think a|statue of|me would|look good|in gold|or silver|realize you|will be|the one|to mine it|You see,|filth is|inevitable|you will|not stop|the will|of mono", 'exel'],
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
		muke = generate_enemy(8, Position(9, 1), name='muke', weapon='LghtngTm', classType='wizard', ai='stand', deathDialog=[["I never|wanted this|save your|home while|you can|I've been|retaining|my whole|life|Im filled|with regret", 'muke']])
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
				['*', 'muke', lambda: build_dialogs(
					[
						["Listen|just make|this easy|I'm just|trying to|do my job", 'muke'],
						["*meow* (This one doesn't seem so filthy)", 'tac'] if get_selected_cat() and get_selected_cat().name == 'tac' else ["I'm going|to make|this as|hard as|possible", get_selected_cat().name if get_selected_cat() else None]
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
		xl = generate_enemy(9, Position(4, 2), ai='stand', name='xl', weapon='Axe', classType='warrior', deathDialog=[["Well good|luck!", 'xl']])

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
						["Unforunatly|I can't|move|so you'll|have to|defeat me", 'xl'],
						["I was|reallly|hoping I|didn't have|to", get_selected_cat().name] if get_selected_cat() and get_selected_cat().name != 'tac' else ["*MEOW*|(WE! have|to move you!)", 'tac']
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
						["You are|strong to|make it|this far|and take|all of|my retainers|on your way|But this|Journey|will never|end well.|beat me|and face|your nightmare", 'zero'],
						["I will|save this|land the|cost is|priceless" if get_selected_cat() and get_selected_cat().name != 'tac' else "*meow*|(Well I'm|not gonna|just leave?)", get_selected_cat().name if get_selected_cat() else None]
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

		mono = generate_enemy(11, Position(12, 4), name='mono', weapon='EarthTm', classType='wizard', ai='stand', deathDialog=[["Congrats|I was hoping|to|Consolidate|the wealth|on this|island|and dip out|but youve|shown that|going above|and beyond|is always|more powerful|*death*", 'mono']])
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
				['cat', 'mono', lambda: build_dialogs(
					[
						["Mayor?", 'cat'],
						["I know|not who|you speak of|but while|you're here|you will|join us", 'mono'],
						["How did|this happen|You're the|final boss?", 'cat']
					],
					left=[mono],
					right=[get_selected_cat()],
				)],
				['*', 'mono', lambda: build_dialogs(
					[
						["You dare|challenge me?", 'mono'],
						["I will|not back|down", get_selected_cat().name if get_selected_cat() else None]
					],
					left=[mono],
					right=[get_selected_cat()],
				)],
				['tac', 'mono', lambda: build_dialogs(
					[
						["*meeow*|(I never|liked you)", get_selected_cat().name if get_selected_cat() else None],
						["Who are|you?", 'mono']
					],
					left=[mono],
					right=[get_selected_cat()],
				)]
			]
		)
		return level

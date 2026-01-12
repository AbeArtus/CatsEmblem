from sys import path as syspath

syspath.insert(0, '/Games/CatsEmblem')
from Shared import Cat, Dialog, Position, Shop, Stats, WeaponExp, classEnum, itemDict
from Levels import Level, cat_sprite, level1, level2, cat
import thumbyGrayscale as thumby
import thumbySaves as thumbySaveData
thumbySaveData.saveData.setName("CatsEmblem")

# --- CONSTANTS ---
SCREEN_TILES_X = 9
SCREEN_TILES_Y = 5

# --- CLASSES ---
class LevelUpLog:
    def __init__(
            self,
            catName: str,
            catSprite: thumby.Sprite,
            newLevel: int,
            stats: Stats,
        ):
        self.catName = catName
        self.catSprite = catSprite
        self.newLevel = newLevel
        self.stats = stats

class AttackLog:
    def __init__(
            self,
            attacker_name: str,
            attacker_hp: int,
            attacker_enemy: bool,
            attacker_sprite: thumby.Sprite,
            defender_name: str,
            defender_hp: int,
            defender_enemy: bool,
            defender_sprite: thumby.Sprite,
            damage: int,
            old_hp: int,
            new_hp: int,
            miss: bool,
            dodge: bool,
            text: str,
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
        self.miss = miss
        self.dodge = dodge
        self.text = text

class Menu:
    def __init__(self, options: list[dict], title: function[str] | None = lambda: "" , option_index: int = 0, leave_action: function | None = None):
        self.options = options  # List of {"label": str, "action": callable, "condition": callable}
        self.title = title
        self.option_index = option_index
        self.leave_action = leave_action

    def get_options(self):
        return [opt for opt in self.options if opt["condition"]()]

    def get_visible_options(self, max_visible: int = 4):
        valid_options = self.get_options()
        offset = max(0, self.option_index - max_visible + 1)
        return valid_options[offset:offset + max_visible], offset

    def handle_input(self):
        visibile_options = self.get_options()
        if thumby.buttonU.justPressed() and self.option_index > 0:
            self.option_index -= 1
        elif thumby.buttonD.justPressed() and self.option_index < len(visibile_options) - 1:
            self.option_index += 1

        elif thumby.buttonA.justPressed():
            valid_options = [opt for opt in self.options if opt["condition"]()]
            if valid_options:
                valid_options[self.option_index]["action"]()
        
        elif thumby.buttonB.justPressed():
            if self.leave_action:
                self.leave_action()

    def render(self):
        thumby.display.fill(thumby.display.WHITE)
        if self.title:
            thumby.display.drawText(self.title(), 2, 0, thumby.display.DARKGRAY)

        visible_options, offset = self.get_visible_options()
        for i, option in enumerate(visible_options):
            selected = thumby.display.BLACK if i + offset == self.option_index else thumby.display.LIGHTGRAY
            if i + offset == self.option_index:
                thumby.display.drawRectangle(0, 8 + i * 8, 1, 7, thumby.display.BLACK)
            thumby.display.drawText(option["label"], 2, 8 + i * 8, selected)

class GameState:
    def __init__(
            self,
            level: Level | None = None,
            party: list[Cat] = [],
            state='title',
        ):
        self.bank = 0
        self.party = party
        self.current_turn: str = 'player'
        self.selectedCatId: str | None = None
        self.load_level(level)
        self.combat_log = []
        self.dialog: list[Dialog] = []
        self.state = state
        self.menu = None
        self.lastPos = Position()

    def save_game(self):
        """Save the current game state to persistent storage."""
        thumbySaveData.saveData.setItem("gameState-bank", self.bank)
        for cat in self.party:
            cat.save_state()
        thumbySaveData.saveData.setItem("gameState-level-number", self.level.number)
        thumbySaveData.saveData.setItem("gameState-party", [cat.name for cat in self.party])
        thumbySaveData.saveData.save()

    def load_game(self):
        """Load the saved game state from persistent storage."""
        self.bank = thumbySaveData.saveData.getItem("gameState-bank")
        party_names: list[str] = thumbySaveData.saveData.getItem("gameState-party")
        party = []
        for i, cat_name in enumerate(party_names):
            cat_stats = thumbySaveData.saveData.getItem(f"{cat_name}_stats")
            cat_items_names = thumbySaveData.saveData.getItem(f"{cat_name}_items")
            if len(cat_stats) == 11:
                stats = Stats(
                    attack=cat_stats[0],
                    defense=cat_stats[1],
                    max_hp=cat_stats[2],
                    speed=cat_stats[3],
                    luck=cat_stats[4],
                    range=cat_stats[5],
                )
                level = cat_stats[6]
                exp = cat_stats[7]
                next_level_exp = cat_stats[8]
                position = Position(cat_stats[9], cat_stats[10])
                items = [itemDict[item_name] for item_name in cat_items_names if item_name in itemDict]
                classType = next((key for key, value in classEnum.items() if value == cat_stats[11]), 'pupil')
                weaponExp = WeaponExp(
                    sword=cat_stats[12],
                    repeater=cat_stats[13],
                    longbow=cat_stats[14],
                    bow=cat_stats[15],
                    lightning=cat_stats[16],
                    water=cat_stats[17],
                    earth=cat_stats[18],
                    mace=cat_stats[19],
                    spear=cat_stats[20]
                )
                loadedCat = Cat(
                    sprite=cat_sprite(),
                    position=position,
                    name=cat_name,
                    stats=stats,
                    exp=exp,
                    level=level,
                    next_level_exp=next_level_exp,
                    items=items,
                    classType=classType,
                    weaponExp=weaponExp
                )
                party.append(loadedCat)
            self.party = party

    def has_saved_game(self):
        """Check if a saved game exists."""
        return (
            thumbySaveData.saveData.hasItem("gameState-level-number")
            and thumbySaveData.saveData.hasItem("gameState-party")
            and thumbySaveData.saveData.hasItem("gameState-bank")
            ## check that we have the stats and items for each cat in the party
            and all(
                thumbySaveData.saveData.hasItem(f"{cat_name}_stats") and thumbySaveData.saveData.hasItem(f"{cat_name}_items")
                for cat_name in thumbySaveData.saveData.getItem("gameState-party")
            )
        )

    def load_level(self, level: Level | None):
        if level is None:
            self.level = None
            return
        for i, p in enumerate(self.party):
            p.set_position(level.startingPositions[i])
            p.set_exhausted(False)
            p.set_selected(False)
            p.moved = False
            p.set_hp(p.stats.max_hp)
        self.level = level
        self.update_selector_position(level.startingPositions[0].x, level.startingPositions[0].y)

    def start_game(self):
        self.party = [cat]
        self.load_level(level1)

    def load_next_level(self):
        if self.level.number == 1:
            self.load_level(level2)
        else:
            self.state = 'gameover'

    def add_dialog(self, dialog: 'Dialog'):
        self.dialog.append(dialog)

    def pop_dialog(self):
        if self.dialog:
            self.dialog.pop(0)

    def select_cat(self, cat: Cat):
        print("Selecting cat:", cat.name)
        selCat = self.get_selected_cat()
        if selCat:
            selCat.set_selected(False)
            print("Cat selected state after unselect:", self.lastPos.x, self.lastPos.y)
            selCat.position = self.lastPos.copy()
        self.lastPos = self.level.selectorPosition.copy()
        cat.set_selected(True)
        self.selectedCatId = cat.id

    def cancel_cat_select(self):
        selCat = self.get_selected_cat()
        print("Unselecting cat:", selCat.name if selCat else "None")
        if selCat:
            selCat.set_selected(False)
            if not selCat.exhausted and selCat.moved:
                selCat.moved = False
                print("Cat selected state after unselect:", self.lastPos.x, self.lastPos.y)
                selCat.position = self.lastPos.copy()
                GameState.update_selector_position(self, self.lastPos.x, self.lastPos.y)
        self.selectedCatId = None
        self.lastPos = Position()

    def get_selected_cat(self):
        for c in self.party + self.level.enemies:
            if c.id == self.selectedCatId if self.selectedCatId else "":
                return c
        return None
    
    def update_selector_position(self, x, y):
        new_x = max(0, min(len(self.level.map[0]) - 1, x))
        new_y = max(0, min(len(self.level.map) - 1, y))
        selCat = self.get_selected_cat()
        if selCat:
            if abs(new_x - selCat.position.x) + abs(new_y - selCat.position.y) > selCat.stats.range:
                return

        self.level.selectorPosition.x = new_x
        self.level.selectorPosition.y = new_y

        center_x = SCREEN_TILES_X // 2
        center_y = SCREEN_TILES_Y // 2

        viewport_x = max(0, min(len(self.level.map[0]) - SCREEN_TILES_X, new_x - center_x))
        viewport_y = max(0, min(len(self.level.map) - SCREEN_TILES_Y, new_y - center_y))

        self.level.viewport.x = viewport_x
        self.level.viewport.y = viewport_y

    def cat_is_on_shop(self):
        lateBirthdayCelebration = self.get_selected_cat()
        if not lateBirthdayCelebration:
            return None
        for shop in self.level.shops:
            if lateBirthdayCelebration.position == shop.position:
                return shop
        return None

    def cat_is_on_house(self):
        neo = self.get_selected_cat()
        if not neo:
            return None
        for house in self.level.houses:
            if neo.position == house.position:
                return house
        return None
    
    def enter_menu(self, menu: Menu):
        self.menu = menu
        self.state = 'menu'

    def exit_menu(self):
        self.menu.leave_action() if self.menu and self.menu.leave_action else None
        self.menu = None
        self.state = 'map'

    def open_shop_menu(self, shop: Shop):
        shop_menu_options = []

        def exit_menu():
                self.state = 'map'
                self.cancel_cat_select()

        for shop_item in shop.inventory:
            def make_purchase_action(item=shop_item):
                def purchase():
                    
                    selCat = self.get_selected_cat()
                    if selCat and len(selCat.items) >= 4:
                        self.add_dialog(Dialog(
                            left_cats=[selCat],
                            currentlyTalking=selCat.name,
                            lines=["Inventory", "Full!"],
                        ))
                        return
                    if self.bank >= item.price:
                        self.bank -= item.price
                        selCat.items.append(item.item)
                        self.add_dialog(Dialog(
                            left_cats=[selCat],
                            currentlyTalking=selCat.name,
                            lines=[f"Purchased",
                                   f"{item.item.name}!"],
                        ))
                    else:
                        self.add_dialog(Dialog(
                            left_cats=[selCat],
                            currentlyTalking=selCat.name,
                            lines=["Not enough",
                                   "gold!"],
                        ))
                return purchase

            shop_menu_options.append({
                "label": f"{shop_item.price} {shop_item.item.name}",
                "action": make_purchase_action(),
                "condition": lambda: True
            })
        self.enter_menu(menu = Menu(
            options=shop_menu_options,
            title= lambda: f"Shop {self.bank}G",
            leave_action=exit_menu
        ))

    def open_item_menu(self, option_index=0):
        selectedCat = self.get_selected_cat()
        if selectedCat:
            item_menu_options = []
            current_option_index = self.menu.option_index if self.menu else 0

            def exit_menu():
                self.open_unit_menu(current_option_index)

            for i, item in enumerate(selectedCat.items):
                def open_item_action_menu(index=i):
                    def item_action_menu():
                        item = selectedCat.items[index]
                        item_action_options = []

                        if item.effect and item.type == 'consumable':
                            def use_item_action():
                                def use_item():
                                    selectedCat.use_item(index)
                                    self.add_dialog(Dialog(
                                        left_cats=[selectedCat],
                                        currentlyTalking=selectedCat.name,
                                        lines=[f"*eats {item.name}*"],
                                    ))
                                    self.state = 'map'
                                    selectedCat.set_exhausted(True)
                                    self.selectedCatId = None
                                return use_item()

                            item_action_options.append({
                                "label": "Use",
                                "action": use_item_action(),
                                "condition": lambda: True
                            })
                        if item.type == 'weapon' and index != 0:
                            def equip_item_action(item_index=index):
                                indexCopy = item_index
                                def equip_item(item_index=indexCopy):
                                    temp = selectedCat.items[0]
                                    selectedCat.items[0] = selectedCat.items[item_index]
                                    selectedCat.items[item_index] = temp

                                    self.state = 'map'
                                return equip_item

                            item_action_options.append({
                                "label": "Equip",
                                "action": equip_item_action(index),
                                "condition": lambda: item.can_use(selectedCat.classType)
                            })
                        if item.type == 'promote' and selectedCat.level >= 5 and selectedCat.classType == 'pupil':
                            def promote_action():
                                def promote():
                                    promotion_class = item.effect.get('promote', '')
                                    selectedCat.promote(promotion_class)
                                    selectedCat.items.pop(index)
                                    self.add_dialog(Dialog(
                                        left_cats=[selectedCat],
                                        currentlyTalking=selectedCat.name,
                                        lines=[f"*promoted to {promotion_class}*"],
                                    ))
                                    self.state = 'map'
                                    selectedCat.set_exhausted(True)
                                    self.selectedCatId = None
                                return promote

                            item_action_options.append({
                                "label": "Promote",
                                "action": promote_action(),
                                "condition": lambda: True
                            })

                        neighbors = [
                            Position(selectedCat.position.x + 1, selectedCat.position.y),
                            Position(selectedCat.position.x - 1, selectedCat.position.y),
                            Position(selectedCat.position.x, selectedCat.position.y + 1),
                            Position(selectedCat.position.x, selectedCat.position.y - 1),
                        ]
                        nearby_party_members = [
                            p for p in self.party if p.position in neighbors and p != selectedCat
                        ]
                        if nearby_party_members:
                            def trade_item_action(item_index=index):
                                def trade_item():
                                    trade_target_options = []
                            
                                    for target_cat in nearby_party_members:
                                        def select_target_cat(target=target_cat):
                                            def open_trade_with_target(target=target_cat):
                                                target_item_options = []
                            
                                                for target_item_index, target_item in enumerate(target.items):
                                                    def select_target_item(target_index=target_item_index):
                                                        def perform_trade():
                                                            selected_item = selectedCat.items[item_index]
                                                            target_item = target.items[target_index]
                                                            selectedCat.items[item_index] = target_item
                                                            target.items[target_index] = selected_item
                                                        
                                                            selectedCat.set_exhausted(True)
                                                            self.state = 'map'
                                                            self.selectedCatId = None
                            
                                                        return perform_trade
                            
                                                    target_item_options.append({
                                                        "label": target_item.name if target_item else "--",
                                                        "action": select_target_item(target_item_index),
                                                        "condition": lambda: True
                                                    })

                                                if len(target.items) < target.max_items:
                                                    def trade_with_empty_slot():
                                                        def perform_trade_with_empty():
                                                            selected_item = selectedCat.items[item_index]
                                                            target.items.append(selected_item)
                                                            selectedCat.items.pop(item_index)

                                                            selectedCat.set_exhausted(True)
                                                            self.selectedCatId = None
                                                            self.state = 'map'
                            
                                                        return perform_trade_with_empty
                            
                                                    target_item_options.append({
                                                        "label": "--",
                                                        "action": trade_with_empty_slot(),
                                                        "condition": lambda: True
                                                    })
                            
                                                self.enter_menu(menu=Menu(
                                                    options=target_item_options,
                                                    title=lambda: f"Trade with {target.name}",
                                                    leave_action=lambda: self.open_item_menu(index)
                                                ))
                            
                                            return open_trade_with_target
                            
                                        trade_target_options.append({
                                            "label": target_cat.name,
                                            "action": select_target_cat(target_cat),
                                            "condition": lambda: True
                                        })
                            
                                    self.enter_menu(menu=Menu(
                                        options=trade_target_options,
                                        title=lambda: "Select Trade Target",
                                        leave_action=lambda: self.open_item_menu(index)
                                    ))
                            
                                return trade_item

                            item_action_options.append({
                                "label": "Trade",
                                "action": trade_item_action(index),
                                "condition": lambda: True
                            })

                        optionIndexCopy = option_index
                        if item_action_options:
                            self.enter_menu(menu=Menu(
                                options=item_action_options,
                                title=lambda: f"{item.name} Actions",
                                leave_action=lambda: self.open_item_menu()
                            ))

                    return item_action_menu

                item_menu_options.append({
                    "label": item.name,
                    "action": open_item_action_menu(),
                    "condition": lambda: True
                })

            self.enter_menu(menu=Menu(
                options=item_menu_options,
                title=lambda: "Item Menu",
                option_index=option_index,
                leave_action=exit_menu
            ))

    def open_unit_menu(self, option_index=0):
        selectedCat = self.get_selected_cat()
        print("opening unit menu, setting lastPos", self.lastPos.x, self.lastPos.y)

        def exit_menu():
            self.state = 'map'
            self.cancel_cat_select()

        def check_house_condition():
            house = self.cat_is_on_house()
            if selectedCat and selectedCat.exhausted:
                return False
            if not house:
                return False
            if not house.visited:
                return True
            if house.has_more_dialogs():
                return True
            return False
        
        def can_move():
            motherTucker = self.get_selected_cat()
            if not motherTucker:
                return False
            if not motherTucker.moved and not motherTucker.exhausted:
                return True
            return False

        def move_action():
            self.state = 'map'

        def stats_action():
            self.state = 'view-stats'

        def wait_action():
            cat = self.get_selected_cat()
            if cat:
                cat.set_exhausted(True)
            self.cancel_cat_select()
            self.state = 'map'

        def fight_action():
            self.state = 'enemy-select'

        def end_turn_action():
            self.cancel_cat_select()
            self.state = 'enemy-turn'

        def seize_action():
            self.cancel_cat_select()
            self.state = 'map'
            GameState.load_next_level(self)

        def visit_house():
            house = self.cat_is_on_house()
            selCat = self.get_selected_cat()
            if not house.visited:
                house.visit()
                for dialog in house.dialogs:
                    self.add_dialog(dialog)
            else:
                for dialog in house.postVisitDialog:
                    self.add_dialog(dialog)
            selCat.set_exhausted(True)
            selCat.set_moved(True)
            exit_menu()

        def can_attack():
            cat = self.get_selected_cat()
            if not cat:
                return False
            if cat.exhausted:
                return False
            for enemy in self.level.enemies:
                dx = abs(enemy.position.x - cat.position.x)
                dy = abs(enemy.position.y - cat.position.y)
                if dx + dy <= cat.get_weapon().range and dx + dy >= cat.get_weapon().range:
                    return True
            return False
        
        def check_shop_condition():
            shop = self.cat_is_on_shop()
            selCat = self.get_selected_cat()
            if selCat and selectedCat.exhausted:
                return False
            return shop is not None
        
        def open_shop_action():
            shop = self.cat_is_on_shop()
            if shop:
                self.open_shop_menu(shop)
                self.needsUpdate = True
                cat = self.get_selected_cat()
                if cat:
                    cat.set_moved(True)
                    cat.set_exhausted(True)

        menu_title = f"{selectedCat.name} hp:{selectedCat.hp}" if selectedCat else "Unit Menu"
        self.enter_menu(menu = Menu(
            options=[
                {
                    "label": "Seize",
                    "action": seize_action,
                    "condition": lambda: selectedCat and selectedCat.position == self.level.seizePosition
                },
                {
                    "label": "Fight",
                    "action": fight_action,
                    "condition": can_attack
                },
                {
                    "label": "Move",
                    "action": move_action,
                    "condition": can_move
                },
                {
                    "label": "Wait",
                    "action": wait_action,
                    "condition": lambda: self.get_selected_cat() is not None and not self.get_selected_cat().exhausted
                },
                {
                    "label": "Visit",
                    "action": visit_house,
                    "condition": check_house_condition
                },
                {
                    "label": "Shop",
                    "action": open_shop_action,
                    "condition": check_shop_condition
                },
                {
                    "label": "Items",
                    "action": self.open_item_menu,
                    "condition": lambda: selectedCat is not None and len(selectedCat.items) > 0
                },
                {
                    "label": "Stats",
                    "action": stats_action,
                    "condition": lambda: self.selectedCatId is not None
                },
                {
                    "label": "End Turn",
                    "action": end_turn_action,
                    "condition": lambda: True
                }
            ],
            title=lambda: menu_title,
            option_index=option_index,
            leave_action=exit_menu
        ))

    def is_occupied(self, position: Position):
        for cat in self.party + self.level.enemies:
            if cat.position == position:
                return True
        return False

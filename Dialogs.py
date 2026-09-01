
from Shared import Position, build_dialogs


class LevelDialogs:
    def _zip_dialogs(self, dialogs1, dialogs2):
        yield from dialogs1
        yield from dialogs2

    def _build_level_one_dialogs(self, party):
        cat = party[0]  # Assuming the first cat in the party is the main character

        dialogs = build_dialogs( ## I want to spead both outputs to be in the same array
                [["A lonely|island,||void|of humans.||Originally|Inhabited|by Cats.|once unknown|now deeply|exploited.|biowaste|plagues|the island.|A small|cat named|cat|Lives|in a port|town of|this island"]],
            )
        dialogs2 = build_dialogs(
                [["Im worried|about tac|at home.|One day|hell be|asleep|during|a raid", cat.name]],
                right=[cat]
            )
        return {
                "intro": self._zip_dialogs(dialogs, dialogs2)
        }

    def _build_level_two_dialogs(self, party):
        has_tac = any(cat.name == 'tac' for cat in party)
        middleIndex = len(party) // 2
        return {
            "intro": build_dialogs(
                [
                    ["Cats home|has been|saved for..|the meantime|but|resistence|is not|treated lightly.||Cat heads|south to|farmland|moving towards|the capital|of|cat island"],
                    ["I really|don't want|fight but..|..I have|to protect|my home", 'cat'],
                    ['*meow*|(It matters|not the|want but|the action|dear cat)', 'tac'] if has_tac else None,
                    ['I like|you more|when you\'re|sleeping', 'cat'] if has_tac else None,
                ],
                left=[cat for cat in party[:middleIndex]],
                right=[cat for cat in party[middleIndex:]]
            ),
            # Add more dialogs for other levels as needed
        }

    def _build_level_three_dialogs(self, party):
        has_tac = any(cat.name == 'tac' for cat in party)
        return {
            "intro": build_dialogs(
                [
                    ["After|a victory||Cat continues|to sand city|manufac.|home|of cat|island"],
                    ["*meow*|(I used|to come|here as|a kitten..|hated this|place.|Lets make|this quick|cat)", 'tac'] if has_tac else None,
                    ["Sure...|i can|try", 'cat'] if has_tac else ["wish i|had more|time to|spend here", 'cat'],
                ],
            ),
            # Add more dialogs for other levels as needed
        }

    def _build_level_four_dialogs(self, party):
        has_tac = any(cat.name == 'tac' for cat in party)
        has_mew = any(cat.name == 'mew' for cat in party)
        return {
            "intro": build_dialogs(
                [
                    ["With himbs|gone from|sand city|Cat heads|towards|cat lake|a place|long sacred|for recreation"],
                    ["Now tac|I know|you wish|we could|stay here|a while", 'cat'] if has_tac else ["I really|hope this|is safe|would rather|relax than|fight", 'cat'],
                    ["*meoow*|(My dreams|do include|this place|but mainly|the|bath house)", 'tac'] if has_tac else None,
                    ["Can you|understand|him cat?|Anyways|Just let|me take|any enemies", 'mew'] if has_mew and has_tac else None
                ],
            ),
            # Add more dialogs for other levels as needed
        }

    def _build_level_five_dialogs(self, party):
        has_tac = any(cat.name == 'tac' for cat in party)
        has_mew = any(cat.name == 'mew' for cat in party)
        has_bao = any(cat.name == 'bao' for cat in party)
        return {
            "intro": build_dialogs(
                [
                    ["Cats lake|back to|peace|Cat departs|towards|the main|docks needing|a ride to|the south"],
                    ["I think|we can|find a|boat here", 'cat'],
                    ["*meow*|(Its been|weeks since|a good nap|just make|it quick)", 'tac'] if has_tac else None,
                    ["Never been|to the port|However I..|know it|will be|a hot spot|for trouble", 'mew'] if has_mew else None,
                    ["Dont worry|Ive been|before once|with my|father", 'cat'] if has_mew else None,
                    ["Cat please|I didn't|realize I|would be|on this|journey with|no soup|this it torture", 'bao'] if has_bao else None,
                    ["Its nothing|but tuna|since the|filth showed|up|how does|hot water|and tuna|sound", 'cat'] if has_bao else None,
                    ["Cat I|dont know|if I can|handle this|journey without|a good meal", 'bao'] if has_bao else None,
                ],
            ),
            # Add more dialogs for other levels as needed
        }

    def _build_level_six_dialogs(self, party):
        return {
            "intro": build_dialogs(
                [["Welcome|to Level|Six!"]],
            ),
            # Add more dialogs for other levels as needed
        }

    def _build_level_seven_dialogs(self, party):
        return {
            "intro": build_dialogs(
                [
                    ["Welcome|to Level|Seven!"],
                ],
            ),
            # Add more dialogs for other levels as needed
        }

    def _build_level_eight_dialogs(self, party):
        return {
            "intro": build_dialogs(
                [
                    ["Welcome|to Level|Eight!"],
                ],
            ),
            # Add more dialogs for other levels as needed
        }

    def _build_level_nine_dialogs(self, party):
        return {
            "intro": build_dialogs(
                [
                    ["Welcome|to Level|Nine!"],
                ],
            ),
            # Add more dialogs for other levels as needed
        }

    def _build_level_ten_dialogs(self, party):
        return {
            "intro": build_dialogs(
                [
                    ["Welcome|to Level Ten!"],
                    ["This is the final level."],
                ],
            ),
            # Add more dialogs for other levels as needed
        }

    def get_dialogs_for_level(self, level_number, party):
        if level_number == 1:
            return self._build_level_one_dialogs(party)
        elif level_number == 2:
            return self._build_level_two_dialogs(party)
        elif level_number == 3:
            return self._build_level_three_dialogs(party)
        elif level_number == 4:
            return self._build_level_four_dialogs(party)
        elif level_number == 5:
            return self._build_level_five_dialogs(party)
        elif level_number == 6:
            return self._build_level_six_dialogs(party)
        elif level_number == 7:
            return self._build_level_seven_dialogs(party)
        elif level_number == 8:
            return self._build_level_eight_dialogs(party)
        elif level_number == 9:
            return self._build_level_nine_dialogs(party)
        elif level_number == 10:
            return self._build_level_ten_dialogs(party)
        else:
            raise ValueError(f"No dialogs defined for level {level_number}")

def get_death_dialog(catName):
    death_dialogs = {
        "cat": [["I guess|this wasn't|meant to be|I have|failed you|all", 'cat']],
        "tac": [["I tried|my best|they are|too strong", 'tac']],
        "mew": [["I refuse|to believe|my cruel|fate", 'mew']],
        "bub": [["I really|wish we had|more time", 'bub']],
        "bao": [["Atleast I|won't have|to see|cat pass,|best this|way", 'bao']],
        "Doug": [["If only|I was|a final|boss|I would|have kicked|your ass", 'Doug']],
        "guy": [["I refuse|to be a|pawn.|The wings|of change|curse you", 'guy']],
        "bar": [["The filth|Will hear|of my|defeat|and I|Will be|avenged", 'bar']],
        "himb": [["I really|was excited|to crush|you|my raise|would have|been|priceless", 'himb']],
        "wlbr": [["Welp, just|know its|really hot|in the|south so|if I dont|finish you|the heat|will", 'wlbr']],
    }
    return death_dialogs.get(catName, None)
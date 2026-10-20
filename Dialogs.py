
from Shared import Position, build_dialogs


class LevelDialogs:
    def _zip_dialogs(self, dialogs1, dialogs2):
        yield from dialogs1
        yield from dialogs2

    def _build_level_one_dialogs(self, party):
        cat = party[0]

        dialogs = build_dialogs(
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
                    ["Cats home|has been|saved for..|the meantime|but|resistence|is not|treated|lightly.|Cat heads|south to|farmland|in search|of the first|of the 7|retainers",],
                    ["I really|don't want|to fight but|I have|to protect|my home", 'cat'],
                    ['*meow*|(It matters|not the|want but|the action|dear cat|Plus..|||The seven|retainers|are chumps)', 'tac'] if has_tac else None,
                    ['Pardon?|But yes|I suppose|we must|continue', 'cat'] if has_tac else None,
                ],
                left=[cat for cat in party[:middleIndex]],
                right=[cat for cat in party[middleIndex:]]
            ),
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
                left=[cat for cat in party[:len(party)//2]],
                right=[cat for cat in party[len(party)//2:]]
            ),
        }

    def _build_level_four_dialogs(self, party):
        has_tac = any(cat.name == 'tac' for cat in party)
        has_mew = any(cat.name == 'mew' for cat in party)
        return {
            "intro": build_dialogs(
                [
                    ["With bar|gone from|sand city|Cat arrives|at cat lake||a place|used for|recreation"],
                    ["Now tac|I know|you wish|we could|stay here|a while", 'cat'] if has_tac else ["I really|hope this|is safe|would rather|relax than|fight", 'cat'],
                    ["*meoow*|(My dreams|do include|this place|but mainly|the|bath house)", 'tac'] if has_tac else None,
                    ["Can you|understand|him cat?|Anyways|Just let|me take|any enemies", 'mew'] if has_mew and has_tac else None
                ],
                left=[cat for cat in party[:len(party)//2]],
                right=[cat for cat in party[len(party)//2:]]
            ),
        }

    def _build_level_five_dialogs(self, party):
        has_tac = any(cat.name == 'tac' for cat in party)
        has_mew = any(cat.name == 'mew' for cat in party)
        has_bao = any(cat.name == 'bao' for cat in party)
        return {
            "intro": build_dialogs(
                [
                    ["Cats lake|back to|peace|Cat heads|to the|main docks|needing|a ride to|the south"],
                    ["we can|find a|boat here", 'cat'],
                    ["*meow*|(Let me| go back)", 'tac'] if has_tac else None,
                    ["Must be|a hot spot|for trouble", 'mew'] if has_mew else None,
                    ["I think|We will|be fine", 'cat'] if has_mew else None,
                    ["I need|soup", 'bao'] if has_bao else None,
                    ["Its nothing|but tuna.|how does..|hot water|and tuna|sound", 'cat'] if has_bao else None,
                    ["We will|see|I guess", 'bao'] if has_bao else None,
                ],
                left=[cat for cat in party[:len(party)//2]],
                right=[cat for cat in party[len(party)//2:]]
            ),
        }

    def _build_level_six_dialogs(self, party):
        has_tac = any(cat.name == 'tac' for cat in party)
        has_mew = any(cat.name == 'mew' for cat in party)
        has_bao = any(cat.name == 'bao' for cat in party)
        return {
            "intro": build_dialogs(
                [
                    ["With the|docks secured||Cat heads|to the|south island|now occupied|by the|filth"],
                    ["I think|Im gonna|be sick|the tides...|ooooh|my stomach", 'cat'],
                    ["*meow*|(Young lad|is missing|his sea|legs aye?)", 'tac'] if has_tac else None,
                    ["I will|not let|your weak..|stomach|prevent|our freedom", 'mew'] if has_mew else None,
                    ["Cat enters|the fenline|temple|once sacred|now occupied|by exel|the filth|elder"],
                    ["exel the|second|last of|the retainers|has bub,|my love|captive|I must|free him", 'bao'] if has_bao else None,
                ],
                left=[cat for cat in party[:len(party)//2]],
                right=[cat for cat in party[len(party)//2:]]
            ),
        }

    def _build_level_seven_dialogs(self, party):
        has_tac = any(cat.name == 'tac' for cat in party)
        has_mew = any(cat.name == 'mew' for cat in party)
        has_bao = any(cat.name == 'bao' for cat in party)
        has_bub = any(cat.name == 'bub' for cat in party)
        return {
            "intro": build_dialogs(
                [
                    ["With one last|of the retainers|remaining|Cat arrives|to mount cat|in search|of muke"],
                    ["Just get|nastier the|further we go", 'cat'],
                    ["*meow*|(My beans...|Soggy)", 'tac'] if has_tac else None,
                    ["This is|an odd|place|Mostly for|high mages.|I'd leave no stone un turned", 'mew'] if has_mew else None,
                    ["I spent|a few months|here|studying the|ancient arts", 'bao'] if has_bao else None,
                    ["Im just|happy to|be here", 'bub'] if has_bub else None,
                ],
                left=[cat for cat in party[:len(party)//2]],
                right=[cat for cat in party[len(party)//2:]]
            ),
        }

    def _build_level_eight_dialogs(self, party):
        return {
            "intro": build_dialogs(
                [
                    ["Welcome|to Level|Eight!"],
                ],
                left=[cat for cat in party[:len(party)//2]],
                right=[cat for cat in party[len(party)//2:]]
            ),
        }

    def _build_level_nine_dialogs(self, party):
        return {
            "intro": build_dialogs(
                [
                    ["Welcome|to Level|Nine!"],
                ],
                left=[cat for cat in party[:len(party)//2]],
                right=[cat for cat in party[len(party)//2:]]
            ),
        }

    def _build_level_ten_dialogs(self, party):
        return {
            "intro": build_dialogs(
                [
                    ["Welcome|to Level Ten!"],
                    ["This is the final level."],
                ],
                left=[cat for cat in party[:len(party)//2]],
                right=[cat for cat in party[len(party)//2:]]
            ),
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

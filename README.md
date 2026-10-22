## Per-level modules (saves RAM on the Thumby)

Level lambdas keep their whole module in RAM, so `build_levels.py` splits ActOne/ActTwo/Dialogs
into one `Lvl1..10.mpy` per level (level + intro dialogs) so only the current level's code is loaded.
Re-run it after editing ActOne.py, ActTwo.py or Dialogs.py, then copy the `Lvl*.mpy` files to the device:

    export PATH="$HOME/Library/Python/3.13/bin:$PATH"
    python3 build_levels.py

If those files are missing the game falls back to ActOne/ActTwo/Dialogs.

It also compiles `Shared`, `GameState`, `Menus`, `Items`, `MapData` and `Callbacks` to `.mpy` (smaller in RAM).
`thumbyGrayscale` stays as source: it uses viper/native code, and the device firmware rejects a precompiled armv6m `.mpy`.
MicroPython prefers a `.py` over a `.mpy`, so on the Thumby copy those `.mpy` files and delete the matching `.py` files.
Keep `CatsEmblem.py` as source since it is run with `execfile`.

# Pokemon TCG Sets
BOOSTER_SETS = [
    "Stellar Crown",
    "Masquerade Twilights",
    "Pokemon 151",
    "Temporal Forces",
    "Paradox Rift",
    "Obsidian Flames",
    "Paldea Evolved",
    "Scarlet & Violet"
]

# Challenge databases
EASY_CHALLENGES = [
    "Finde eine Common Karte aus {set}",
    "Finde eine Reverse Holo Karte aus {set}",
    "Finde eine Energy Karte aus {set}",
    "Finde eine Trainer Karte aus {set}",
    "Finde eine Stage 1 Pokemon Karte aus {set}"
]

MEDIUM_CHALLENGES = [
    "Finde eine Rare Holo Karte aus {set}",
    "Finde eine Ultra Rare Karte aus {set}",
    "Finde eine Illustration Rare aus {set}",
    "Finde eine Pokemon ex Karte aus {set}",
    "Finde eine Full Art Trainer aus {set}"
]

HARD_CHALLENGES = [
    "Finde eine Special Illustration Rare aus {set}",
    "Finde eine Alternative Art Rare aus {set}",
    "Finde eine Special Illustration Rare ex aus {set}",
    "Finde eine Hyper Rare Karte aus {set}",
    "Finde eine Gold Rare Karte aus {set}"
]

COMMUNITY_PRESENTS = [
    "Ein signiertes Pokemon Display ",
    "Ein Elite Trainer Box deiner Wahl ",
    "Ein komplettes Master-Set eines Pokemon Sets ",
    "Ein Jahr gratis Pokemon TCG Live Codes ",
    "Ein Pokemon Center Plüschtier deiner Wahl ",
    "Ein japanisches Display deiner Wahl ",
    "Eine PSA 10 Karte im Wert von 100€ ",
    "Ein Pokemon TCG Sammleralbum mit 25 Boostern ",
    "Ein Set aller Pokemon Starter-Decks ",
    "Ein Pokemon Center Exclusive Product "
]

# Claw Machine Constants
CLAW_SPEED = 5
CLAW_DROP_SPEED = 8
CLAW_GRAB_RADIUS = 50

# Pokeball Types and Rarities
POKEBALL_TYPES = {
    'normal': {'chance': 0.4, 'value': 1},
    'great': {'chance': 0.3, 'value': 2},
    'ultra': {'chance': 0.2, 'value': 3},
    'master': {'chance': 0.1, 'value': 4}
}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

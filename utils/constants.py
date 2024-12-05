# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 0)
PURPLE = (147, 112, 219)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)

# Challenge Colors
EASY_COLOR = (150, 255, 150)     # Light green
MEDIUM_COLOR = (150, 150, 255)   # Light blue
HARD_COLOR = (255, 150, 150)     # Light red
JACKPOT_COLOR = (255, 215, 0)    # Gold

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Game settings
FPS = 60
DEFAULT_SOUND_VOLUME = 0.5
DEFAULT_MUSIC_VOLUME = 0.3

# UI Settings
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 120
BUTTON_RADIUS = 12
INFO_BOX_WIDTH = 400
INFO_BOX_HEIGHT = 300

# Asset paths
ASSETS_DIR = 'assets'
SOUND_DIR = 'assets/sounds'
MUSIC_DIR = 'assets/music'
SPRITE_DIR = 'assets/sprites'
FONT_DIR = 'assets/fonts'

# Sound files
SOUND_FILES = {
    'spin': 'spin.wav',
    'stop': 'stop.wav',
    'win': 'win.wav',
    'jackpot': 'jackpot.wav',
    'click': 'stop.wav'  # Using stop.wav for click sound
}

# Music files
MUSIC_FILES = {
    'menu': '1-01-Title-Demo-_Departure-From-The.wav',
    'slot': '1-11-Route-101.wav',
    'claw': '1-11-Route-101.wav'
}

# Font files
FONT_FILES = {
    'pokemon': 'Pokemon Solid.ttf'
}

# Animation settings
PARTICLE_MAX = 100
PARTICLE_LIFETIME = 1.0
PARTICLE_SIZE = 3
TRANSITION_SPEED = 10

# Game specific settings
SLOT_SYMBOLS = ['Charizard', 'Lugia', 'Tyranitar', 'Gengar', 'Oshawott', 'Arcanine']
SLOT_WEIGHTS = [15, 5, 20, 20, 20, 20]  # Corresponding weights for symbols
ROLL_DURATION = 2.5    # Total time for slots to stop
ROLL_STAGGER = 0.5    # Time between each slot stopping

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

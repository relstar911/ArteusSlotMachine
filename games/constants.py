# Current Main Hits (Can be updated per game)
MAIN_HITS = [
    "Charizard ex SAR",
    "Pikachu SAR",
    "Mew ex SAR",
    "Rayquaza SAR"
]

# Win Messages
EASY_WINS = [
    "🎯 GEWONNEN!\n• Ein japanisches Boosterpack\n• Viel Spaß beim Öffnen!",
    "🎌 GLÜCKWUNSCH!\n• Ein japanisches Boosterpack\n• Direkt aus Japan für dich!",
    "✨ SUPER!\n• Ein japanisches Boosterpack\n• Exklusive Karten warten!"
]

MEDIUM_WINS = [
    "🌟 GEWONNEN!\n• Eine Illustration Rare oder Secret Rare\n• Tolle Karte!",
    "💫 GLÜCKWUNSCH!\n• Eine Illustration Rare oder Secret Rare\n• Wunderschönes Artwork!",
    "⭐ SUPER!\n• Eine Illustration Rare oder Secret Rare\n• Seltene Belohnung!"
]

HARD_WINS = [
    "🏆 MEGA GEWINN!\n• {hit}\n• Absoluter Top-Hit!",
    "💎 JACKPOT!\n• {hit}\n• Fantastischer Gewinn!",
    "✨ WAHNSINN!\n• {hit}\n• Was für ein Hit!"
]

COMMUNITY_JACKPOT = [
    "🎉 COMMUNITY GIVEAWAY!\n• Ein glücklicher Zuschauer gewinnt\n• Teilnahme im Giveaway!",
    "🌟 MEGA GIVEAWAY!\n• Gewinnspiel startet jetzt\n• Alle können mitmachen!",
    "🏆 COMMUNITY EVENT!\n• Großes Gewinnspiel\n• Sei dabei und gewinne!"
]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (50, 150, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (147, 112, 219)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Game settings
FPS = 60
DEFAULT_SOUND_VOLUME = 0.5
DEFAULT_MUSIC_VOLUME = 0.3

# UI Settings
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 200
BUTTON_RADIUS = 12

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
    'click': 'click.wav'
}

# Music files
MUSIC_FILES = {
    'slot': '1-11-Route-101.wav'
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

# Slot Machine settings
SLOT_SYMBOLS = ['Charizard', 'Lugia', 'Tyranitar', 'Gengar', 'Oshawott', 'Arcanine']
SLOT_WEIGHTS = [10, 25, 15, 15, 15, 20]  # Corresponding weights for symbols (Total: 100)
# Lugia (Jackpot): 25% chance per slot = ~1.5% chance for jackpot = average 1 jackpot per ~65 spins

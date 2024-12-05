"""Constants for the Claw Machine game"""

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 50)
GOLD = (255, 215, 0)
BLUE = (50, 150, 255)
PURPLE = (147, 112, 219)
NEON_BLUE = (50, 150, 255)
NEON_PINK = (255, 50, 150)

# Game settings
CLAW_SPEED = 5
CLAW_DROP_SPEED = 8
GRAB_RADIUS = 30
SWING_SPEED = 0.005
ROTATION_SPEED = 2
MIN_BALLS = 15
MAX_BALLS = 25
POKEBALL_SIZE = 30  # Size of pokeballs in pixels
CLAW_SIZE = 40     # Size of the claw in pixels

# Game states
STATES = {
    'IDLE': 'idle',
    'DROPPING': 'dropping',
    'RISING': 'rising',
    'CHALLENGE': 'challenge'
}

# Pokéball types and their rarities
POKEBALLS = {
    'normal': {
        'sprite': 'poke.png',
        'weight': 40,
        'category': 'easy',
        'description': '📦 Standard Pokéball\n• Enthält normale Pokemon Karten\n• Idealer Einstieg für Sammler',
        'challenges': [
            "📄 Common Challenge:\n• Finde eine Common Karte aus Scarlet & Violet",
            "⚡ Energy Challenge:\n• Finde eine Energy Karte aus Paldea Evolved",
            "👥 Trainer Challenge:\n• Finde eine Trainer Karte aus Temporal Forces",
            "🌟 Basic Challenge:\n• Finde ein normales Pokémon aus Paldea"
        ]
    },
    'hisuian': {
        'sprite': 'hisuian-great.png',
        'weight': 30,
        'category': 'medium',
        'description': '🌟 Hisui Ball\n• Enthält seltene Pokemon Karten\n• Bessere Chance auf Holos',
        'challenges': [
            "✨ Holo Challenge:\n• Finde eine Rare Holo Karte aus Scarlet & Violet",
            "⭐ Stage 1 Challenge:\n• Finde eine Stage 1 ex Karte aus Paldea Evolved",
            "💎 Tera Challenge:\n• Finde eine Teracristall Karte aus Temporal Forces",
            "🌈 Paradox Challenge:\n• Finde ein Paradox Pokémon aus Paldea"
        ]
    },
    'ultra': {
        'sprite': 'ultra.png',
        'weight': 20,
        'category': 'hard',
        'description': '💫 Ultra Ball\n• Enthält sehr seltene Karten\n• Hohe Chance auf Ultra Rares',
        'challenges': [
            "⭐ Ultra Rare Challenge:\n• Finde eine Ultra Rare ex Karte aus Scarlet & Violet",
            "👤 Full Art Challenge:\n• Finde eine Full Art Trainer Karte aus Paldea Evolved",
            "🎨 Ancient Challenge:\n• Finde eine Ancient/Future Karte aus Temporal Forces",
            "🌟 Legend Challenge:\n• Finde ein legendäres Pokémon aus Paldea"
        ]
    },
    'beast': {
        'sprite': 'beast.png',
        'weight': 7,
        'category': 'special',
        'description': '🎭 Beast Ball\n• Enthält spezielle Event Karten\n• Sehr hohe Chance auf Alt Arts',
        'challenges': [
            "🖼️ Special Art Challenge:\n• Finde eine Special Illustration Rare ex aus Scarlet & Violet",
            "🎨 Alt Art Challenge:\n• Finde eine Alternative Art Rare aus Paldea Evolved",
            "✨ Shiny Challenge:\n• Finde eine Shiny Rare aus Temporal Forces",
            "🌈 Paradox EX Challenge:\n• Finde ein Paradox ex Pokémon aus Paldea"
        ]
    },
    'master': {
        'sprite': 'master.png',
        'weight': 3,
        'category': 'jackpot',
        'description': '🏆 Master Ball\n• Community Jackpot Ball!\n• Garantierte Top-Preise',
        'challenges': [
            "💫 JACKPOT CHALLENGE!\n• Gewinne eine signierte Koraidon ex Karte!",
            "🌟 JACKPOT CHALLENGE!\n• Gewinne eine PSA 10 Miraidon ex Karte!",
            "✨ JACKPOT CHALLENGE!\n• Gewinne ein komplettes Master-Set von Scarlet & Violet!",
            "🎮 JACKPOT CHALLENGE!\n• Gewinne ein Jahr gratis Pokémon TCG Live Premium Pass!"
        ]
    }
}

# Grab chances based on category
GRAB_CHANCES = {
    'easy': 0.8,
    'medium': 0.6,
    'hard': 0.4,
    'special': 0.3,
    'jackpot': 0.2
}

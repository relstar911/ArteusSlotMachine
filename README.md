# 🎮 Pokemon Card Channel Mini-Games

Ein interaktives Mini-Game-System für unseren Pokemon-Karten YouTube Kanal, das durch spannende Challenges und Belohnungen die Community einbindet und für unvergessliche YouTube Shorts sorgt!

## 🌟 Features & Konzept

### 🎰 Slot Machine
- **Challenge System**:
  - Easy (1 Symbol): Common Karten Challenge
  - Medium (2 Symbole): Rare Holo oder Ultra Rare Challenge
  - Hard (3 Symbole): Special Illustration Rare Challenge
  - Jackpot (3x Lugia): Community Event mit Booster Display oder SIR ex!
- **Gewichtung & Fairness**:
  - Lugia: 5% (Jackpot-Chance)
  - Andere Symbole: Fair verteilt für regelmäßige Challenges
- **Effekte**:
  - Dynamische Partikel-Effekte
  - Pokemon Soundtracks & Effekte
  - Moderne UI mit Animationen und optimierten Schriftgrößen

### 🎮 Claw Machine
- **Gameplay**:
  - Skill-basierte Greifarm-Steuerung (Pfeiltasten + Leertaste)
  - Pokemon-Kapseln verschiedener Seltenheit
  - Neon-Design mit modernen Effekten
- **Pokeball System**:
  - Normal Ball (Easy): 40% Spawn, 80% Fangchance
  - Hisuian Ball (Medium): 30% Spawn, 60% Fangchance
  - Ultra Ball (Hard): 20% Spawn, 40% Fangchance
  - Beast Ball (Special): 7% Spawn, 30% Fangchance
  - Master Ball (Jackpot): 3% Spawn, 20% Fangchance
- **Challenge System**:
  - Individuelle Challenges pro Pokeball-Typ
  - Spezielle Karten-Challenges
  - Community Jackpot Events

## 🎥 YouTube Integration

### 📱 Shorts Features
- **Automatische Highlights**:
  - Jackpot-Momente
  - Challenge-Erfolge
  - Besondere Gewinne
- **Community Events**:
  - QR-Code Challenges in Videos
  - Wöchentliche Spezial-Events
  - Saisonale TCG Release Events

### 🏆 Belohnungssystem
- **Tägliche Challenges**:
  - Verbindung zu aktuellen Videos
  - Spezielle Kartensets
  - Community-Ziele
- **Progression**:
  - Level-System
  - Freischaltbare Events
  - Exklusive Belohnungen

## 🚀 Installation

1. Python 3.12+ installieren
2. Repository klonen
3. Dependencies installieren:
```bash
pip install -r requirements.txt
```
4. Spiel starten:
```bash
python main.py
```

## 📂 Verzeichnisstruktur
```
pokeminigames/
├── assets/
│   ├── music/     # Pokemon Soundtracks
│   ├── sounds/    # Spiel-Effekte
│   ├── sprites/   # Pokemon-Bilder
│   └── fonts/     # Pokemon Schriftart
├── games/
│   ├── slot_machine.py
│   └── claw_machine.py
├── utils/
│   ├── constants.py
│   ├── game_base.py
│   └── ui_elements.py
└── main.py
```

## 🛠️ Development Status

### Implementiert ✅
- Basis Spielmechanik für beide Spiele
- Sound & Partikel System
- Challenge System mit verschiedenen Schwierigkeitsgraden
- Moderne UI & Animationen
- Optimiertes Font-System mit einheitlichen Größen
- Pokeball-basiertes Challenge-System
- Verbesserte Steuerung (Keyboard Support)

### In Entwicklung 🚧
- YouTube API Integration
- QR-Code Challenge System
- Community Reward System
- Erweiterte Shorts Features
- Asset Management System
- Persistentes Scoring System

## 🔜 Nächste Schritte
1. **Kurzfristig**:
   - Asset Management optimieren
   - Fehlende Sprites hinzufügen
   - Sound-System vervollständigen
2. **Mittelfristig**:
   - Challenge-System erweitern
   - Persistentes Scoring implementieren
   - YouTube Integration vorbereiten
3. **Langfristig**:
   - Community Features
   - Cross-Platform Support
   - Live-Stream Integration

## 📺 YouTube Kanal
[Folge uns auf YouTube](https://youtube.com/@user) für:
- Tägliche Pokemon Card Openings
- Exklusive Challenges
- Community Events
- Special Giveaways

## 📝 Lizenz
Privates Projekt - Alle Rechte vorbehalten © 2024

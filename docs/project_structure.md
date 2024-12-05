# PokeMiniGames - Projektdokumentation

## Projektübersicht

PokeMiniGames ist ein interaktives Tool für Content Creator im Pokemon-Sammelkarten und Merchandise Bereich. Die Minispiele dienen als "Challenge Generators" für Videoformate, bei denen die Community durch das Spielergebnis bestimmt, welche realen Produkte der Creator öffnen oder präsentieren soll.

### Kernkonzept
- **Content Creation Tool**: Generiert interessante Challenges für Pokemon-bezogene Videos
- **Challenge-Basiert**: Spielergebnisse bestimmen die realen Unboxings/Aktionen des Creators
- **Community-Integration**: Bei seltenen Ergebnissen gibt es Community-Belohnungen statt Challenges
- **Interaktives Format**: Verbindet Minispiele mit echtem Pokemon Content

## Projektstruktur

```
pokeminigames/
├── assets/          # Spiel-Assets (Bilder, Sounds)
├── docs/            # Projektdokumentation
├── games/          # Spielmodule
│   ├── slot_machine.py
│   ├── claw_machine.py
│   └── constants.py
├── utils/          # Hilfsfunktionen
│   ├── font_manager.py
│   ├── sound_manager.py
│   ├── ui_elements.py
│   └── game_base.py
└── main.py         # Hauptprogramm
```

## Hauptkomponenten

### 1. Main Menu (main.py)
- **Klasse**: `MainMenu`
- **Funktionen**:
  - Spielauswahl
  - Navigation zwischen Spielen
  - Programm beenden
- **Features**:
  - Responsive Buttons
  - Titel-Animation
  - Version-Anzeige

### 2. Spiele

#### 2.1 Slot Machine (games/slot_machine.py)
- **Content Creator Zweck**: Generiert Booster Pack Opening Challenges
- **Hauptklasse**: `SlotMachine`
- **Challenge-System**: 
  - Normale Gewinne → Creator muss spezifische Booster öffnen
  - Jackpot → Community-Belohnung statt Challenge
- **Symbole**: 
  - Charizard (Gewichtung: 15) - Vintage Booster Challenge
  - Lugia (Gewichtung: 5) - Community-Belohnung
  - Tyranitar (Gewichtung: 20) - Modern Set Challenge
  - Gengar (Gewichtung: 20) - Special Set Challenge
  - Oshawott (Gewichtung: 20) - Standard Pack Challenge
  - Arcanine (Gewichtung: 20) - Random Set Challenge
- **Features**:
  - Challenge-Generierung
  - Belohnungs-Integration
  - Gewinnanimationen

#### 2.2 Claw Machine (games/claw_machine.py)
- **Content Creator Zweck**: Generiert Merchandise/Plüsch Unboxing Challenges
- **Hauptklasse**: `ClawMachine`
- **Challenge-System**:
  - Erfolgreicher Fang → Creator kauft/zeigt spezifisches Merchandise
  - Spezial-Items → Community-Belohnung
- **Features**:
  - Verschiedene Merchandise-Kategorien
  - Challenge-Schwierigkeitsgrade
  - Visuelle Effekte

### 3. Creator Features
- **Challenge-System**:
  - Automatische Challenge-Generierung
  - Verschiedene Schwierigkeitsgrade
  - Anpassbare Challenge-Regeln
- **Community-Integration**:
  - Belohnungssystem bei seltenen Ergebnissen
  - Community-Feedback Optionen
  - Event-Planung Unterstützung

## Entwicklungsrichtlinien

### Neue Spiele sollten:
1. Als Challenge-Generator für echten Content fungieren
2. Klare Challenge-Regeln definieren
3. Community-Belohnungen bei seltenen Ereignissen ermöglichen
4. Sich für Video-Content eignen
5. Die vorhandene Challenge/Belohnungs-Infrastruktur nutzen

## Wichtige Dateipfade
- Hauptprogramm: `main.py`
- Slot Machine: `games/slot_machine.py`
- Claw Machine: `games/claw_machine.py`
- UI-Elemente: `utils/ui_elements.py`
- Konstanten: `games/constants.py`

## Abhängigkeiten
- Python 3.x
- Pygame
- Weitere spezifische Abhängigkeiten in `requirements.txt`

## Hinweise zur Wartung
1. Alle Spiele erben von `BaseGame`
2. UI-Komponenten sind modular und wiederverwendbar
3. Assets werden zentral in `/assets` verwaltet
4. Jedes Spiel hat seine eigenen Konstanten
5. Sound- und Schriftarten-Management ist zentralisiert

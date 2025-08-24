# Dungeon Crawler Game

A terminal-based dungeon crawler game written in Python with multiple enemy types and shooting mechanics.

## Features

- **Large Game Area**: 50x24 character playing field
- **Multiple Enemy Types**:
  - **M** (Monster) - Regular enemies (20 HP)
  - **F** (Fast) - Quick shooters with low HP (10 HP, shoots 3x faster)
  - **T** (Tank) - High HP enemies with strong attacks (40 HP, slower shooting)
- **Combat System**: Melee fighting and ranged shooting
- **Health Items**: Collect + symbols to restore health
- **Progressive Levels**: Clear all enemies to advance

## Controls

- **WASD** - Move player (@)
- **F** - Melee fight nearby enemies
- **IJKL** - Shoot bullets in directions (up/down/left/right)
- **Q/E** - Quit game

## How to Play

1. Navigate the dungeon using WASD keys
2. Fight enemies with F (melee) or IJKL (ranged)
3. Collect health items (+) to restore HP
4. Clear all enemies to unlock the exit (>)
5. Reach the exit to advance to the next level

## Requirements

- Python 3.x
- Windows (uses msvcrt for input handling)

## Installation & Running

```bash
git clone <repository-url>
cd Text_Game
python dungeon_crawler.py
```

Or use the launcher:
```bash
python game_launcher.py dungeon
```

## Game Elements

- `@` - Player
- `M` - Regular Monster
- `F` - Fast Enemy
- `T` - Tank Enemy
- `+` - Health Item
- `>` - Exit
- `*` - Enemy Bullets
- `-` - Player Bullets
- `#` - Walls
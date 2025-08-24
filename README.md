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
- **TAB** - Toggle inventory display
- **1/2/3** - Use inventory items (Health/Speed/Damage)
- **Q/E** - Quit game

## How to Play

1. Navigate the dungeon using WASD keys
2. Fight enemies with F (melee) or IJKL (ranged)
3. Collect items: + (health), S (speed boost), D (damage boost)
4. Use TAB to view inventory, 1/2/3 to use items
5. Clear all enemies to unlock the exit (>)
6. Reach the exit to advance to the next level

## Inventory System

- **Health Items (+)**: Instant +10 HP when collected, or store and use with key 1 for +25 HP
- **Speed Items (S)**: Collect and use with key 2 for 10 seconds of double movement speed
- **Damage Items (D)**: Permanent +5 bullet damage when collected, use with key 3 for +15 damage on next 5 shots

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

### Using Seeds

Like Minecraft, you can use a seed to generate the same world layout:

```bash
# Direct execution with seed
python dungeon_crawler.py 1234567890

# Using launcher with seed
python game_launcher.py dungeon 1234567890
```

Seeds are large numbers that determine enemy and item placement for each level. The same seed will always generate the same world layout, allowing you to share interesting worlds or replay challenging configurations.

## Game Elements

- `@` - Player
- `M` - Regular Monster
- `F` - Fast Enemy
- `T` - Tank Enemy
- `+` - Health Item
- `S` - Speed Boost Item
- `D` - Damage Boost Item
- `>` - Exit
- `*` - Enemy Bullets
- `-` - Player Bullets
- `#` - Walls
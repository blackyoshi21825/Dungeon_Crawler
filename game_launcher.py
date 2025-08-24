#!/usr/bin/env python3
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Available games:")
        print("  dungeon - Dungeon Crawler")
        print("\nUsage: python game_launcher.py dungeon [seed]")
        print("  seed - Optional world seed (large number)")
        return
    
    game = sys.argv[1].lower()
    seed_arg = sys.argv[2] if len(sys.argv) > 2 else ""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    games = {
        'dungeon': 'dungeon_crawler.py'
    }
    
    if game in games:
        game_file = os.path.join(script_dir, games[game])
        if os.path.exists(game_file):
            cmd = f'python "{game_file}"'
            if seed_arg:
                cmd += f' {seed_arg}'
            os.system(cmd)
        else:
            print(f"Game file {games[game]} not found!")
    else:
        print(f"Unknown game: {game}")
        print("Available games: " + ", ".join(games.keys()))

if __name__ == "__main__":
    main()
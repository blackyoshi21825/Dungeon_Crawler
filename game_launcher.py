#!/usr/bin/env python3
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Available games:")
        print("  dungeon - Dungeon Crawler")
        print("\nUsage: python game_launcher.py dungeon")
        return
    
    game = sys.argv[1].lower()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    games = {
        'dungeon': 'dungeon_crawler.py'
    }
    
    if game in games:
        game_file = os.path.join(script_dir, games[game])
        if os.path.exists(game_file):
            os.system(f'python "{game_file}"')
        else:
            print(f"Game file {games[game]} not found!")
    else:
        print(f"Unknown game: {game}")
        print("Available games: " + ", ".join(games.keys()))

if __name__ == "__main__":
    main()
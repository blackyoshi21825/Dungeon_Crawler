import os
import random
import sys
import keyboard
import time
import msvcrt

class DungeonCrawler:
    def __init__(self, seed=None):
        self.width = 50
        self.height = 24
        self.player_x = 2
        self.player_y = 2
        self.prev_player_x = 2
        self.prev_player_y = 2
        self.hp = 100
        self.level = 1
        self.seed = seed if seed is not None else random.randint(1000000000, 9999999999)
        self.enemies = []
        self.items = []
        self.bullets = []
        self.player_bullets = []
        self.prev_bullets = []
        self.prev_player_bullets = []
        self.background_drawn = False
        self.keys_pressed = set()
        self.last_shot_time = 0
        self.fast_shot_time = 0
        self.inventory = {'health': 0, 'speed': 0, 'damage': 0}
        self.show_inventory = False
        self.speed_boost_end = 0
        self.damage_boost_attacks = 0
        print(f"World Seed: {self.seed}")
        self.generate_level()
        
    def generate_level(self):
        # Use seed + level for deterministic generation
        level_seed = self.seed + self.level * 1000
        random.seed(level_seed)
        
        self.enemies = []
        self.items = []
        
        for _ in range(3 + self.level):
            x = random.randint(5, self.width-2)
            y = random.randint(2, self.height-2)
            enemy_type = random.choice(['M', 'F', 'T'])
            if enemy_type == 'M': hp = 20
            elif enemy_type == 'F': hp = 10  # Fast, low HP
            else: hp = 40  # Tank, high HP
            self.enemies.append([x, y, hp, enemy_type])  # x, y, hp, type
            
        # Generate health items
        for _ in range(2):
            x = random.randint(3, self.width-2)
            y = random.randint(2, self.height-2)
            self.items.append((x, y, 'health'))
            
        # Generate special items
        for item_type in ['speed', 'damage']:
            if random.random() < 0.3:  # 30% chance
                x = random.randint(3, self.width-2)
                y = random.randint(2, self.height-2)
                self.items.append((x, y, item_type))
            
        # Reset random seed for gameplay randomness
        random.seed()
            
    def draw_background(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if x == 0 or x == self.width-1 or y == 0 or y == self.height-1:
                    row += "#"
                elif x == self.width-2 and y == self.height-2:
                    row += ">"  # exit
                else:
                    row += "."
            print(row)
        print(f"HP: {self.hp} | Level: {self.level} | Seed: {self.seed}")
        print("@ = You, M = Monster, F = Fast, T = Tank, + = Health, S = Speed, D = Damage, > = Exit")
        print("WASD to move, F to fight, IJKL to shoot, TAB = inventory, 1/2/3 = use items, Q/E to quit")
        
    def update_display(self):
        if not self.background_drawn:
            self.draw_background()
            self.background_drawn = True
            
        # Clear previous player position
        self.move_cursor(self.prev_player_x, self.prev_player_y)
        sys.stdout.write(".")
        
        # Clear previous enemy positions
        for ex, ey, _, _ in self.enemies:
            self.move_cursor(ex, ey)
            sys.stdout.write(".")
            
        # Clear previous bullet positions
        for bx, by, _, _ in self.prev_bullets:
            self.move_cursor(bx, by)
            sys.stdout.write(".")
            
        # Clear previous player bullet positions
        for bx, by, _, _ in self.prev_player_bullets:
            self.move_cursor(bx, by)
            sys.stdout.write(".")
            
        # Draw items
        for ix, iy, item_type in self.items:
            self.move_cursor(ix, iy)
            if item_type == 'health': sys.stdout.write("+")
            elif item_type == 'speed': sys.stdout.write("S")
            elif item_type == 'damage': sys.stdout.write("D")
            
        # Draw enemies
        for ex, ey, _, etype in self.enemies:
            self.move_cursor(ex, ey)
            sys.stdout.write(etype)
            
        # Draw bullets
        for bx, by, _, _ in self.bullets:
            self.move_cursor(bx, by)
            sys.stdout.write("*")
            
        # Draw player bullets
        for bx, by, _, _ in self.player_bullets:
            self.move_cursor(bx, by)
            sys.stdout.write("-")
            
        # Draw player
        self.move_cursor(self.player_x, self.player_y)
        sys.stdout.write("@")
        
        # Update HP and level
        self.move_cursor(0, self.height)
        if self.show_inventory:
            speed_time = max(0, int(self.speed_boost_end - time.time())) if time.time() < self.speed_boost_end else 0
            sys.stdout.write(f"INV - H:{self.inventory['health']} S:{self.inventory['speed']} D:{self.inventory['damage']} | Speed:{speed_time}s Dmg:{self.damage_boost_attacks}")
        else:
            sys.stdout.write(f"HP: {self.hp} | Level: {self.level} | Seed: {self.seed}")
        
        sys.stdout.flush()
        
    def move_cursor(self, x, y):
        sys.stdout.write(f"\033[{y+1};{x+1}H")
        
    def move(self, direction):
        self.prev_player_x, self.prev_player_y = self.player_x, self.player_y
        new_x, new_y = self.player_x, self.player_y
        
        # Speed boost allows double movement
        move_distance = 2 if time.time() < self.speed_boost_end else 1
        
        if direction == 'w': new_y -= move_distance
        elif direction == 's': new_y += move_distance
        elif direction == 'a': new_x -= move_distance
        elif direction == 'd': new_x += move_distance
        
        if 1 <= new_x < self.width-1 and 1 <= new_y < self.height-1:
            self.player_x, self.player_y = new_x, new_y
            
        # Check items
        for item in self.items[:]:
            if item[0] == self.player_x and item[1] == self.player_y:
                self.items.remove(item)
                item_type = item[2]
                if item_type == 'health':
                    self.hp = min(100, self.hp + 10)
                else:
                    self.inventory[item_type] += 1
                break
            
        # Check enemy attacks
        self.check_enemy_attacks()
            
    def fight(self):
        # Find nearby enemies
        for i, (ex, ey, ehp, etype) in enumerate(self.enemies):
            if abs(ex - self.player_x) <= 1 and abs(ey - self.player_y) <= 1:
                damage = random.randint(15, 25)
                self.enemies[i][2] -= damage
                print(f"You hit {etype} for {damage} damage!")
                
                if self.enemies[i][2] <= 0:
                    self.enemies.pop(i)
                else:
                    player_damage = random.randint(5, 15)
                    self.hp -= player_damage
                self.background_drawn = False
                return
                
    def enemy_shoot(self):
        current_time = time.time()
        
        # Fast enemies shoot every 0.5 seconds
        if current_time - self.fast_shot_time > 0.50:
            for ex, ey, _, etype in self.enemies:
                if etype == 'F':
                    dx = 1 if self.player_x > ex else -1 if self.player_x < ex else 0
                    dy = 1 if self.player_y > ey else -1 if self.player_y < ey else 0
                    self.bullets.append([ex, ey, dx, dy])
            self.fast_shot_time = current_time
        
        # Regular and tank enemies shoot every 1.5 seconds
        if current_time - self.last_shot_time > 1.5:
            for ex, ey, _, etype in self.enemies:
                if etype == 'M':
                    dx = 1 if self.player_x > ex else -1 if self.player_x < ex else 0
                    dy = 1 if self.player_y > ey else -1 if self.player_y < ey else 0
                    self.bullets.append([ex, ey, dx, dy])
                elif etype == 'T':
                    # Tanks shoot star pattern (8 directions)
                    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]:
                        self.bullets.append([ex, ey, dx, dy])
            self.last_shot_time = current_time
            
    def update_bullets(self):
        # Update enemy bullets
        self.prev_bullets = self.bullets[:]
        new_bullets = []
        
        for bullet in self.bullets:
            bx, by, dx, dy = bullet
            new_x = bx + dx
            new_y = by + dy
            
            # Check if bullet hits player
            if new_x == self.player_x and new_y == self.player_y:
                self.hp -= 15
                continue  # Remove bullet
                
            # Check if bullet hits wall
            if (new_x <= 0 or new_x >= self.width-1 or 
                new_y <= 0 or new_y >= self.height-1):
                continue  # Remove bullet
                
            # Add updated bullet
            new_bullets.append([new_x, new_y, dx, dy])
            
        self.bullets = new_bullets
        
        # Update player bullets
        self.prev_player_bullets = self.player_bullets[:]
        new_player_bullets = []
        
        for bullet in self.player_bullets:
            bx, by, dx, dy = bullet
            new_x = bx + dx
            new_y = by + dy
            
            # Check if bullet hits enemy
            for i, (ex, ey, ehp, etype) in enumerate(self.enemies):
                if new_x == ex and new_y == ey:
                    damage = 20 + (self.inventory['damage'] * 5)  # Permanent +5 per D item
                    if self.damage_boost_attacks > 0:
                        damage += 15  # Temporary damage boost from using item
                        self.damage_boost_attacks -= 1
                    self.enemies[i][2] -= damage
                    if self.enemies[i][2] <= 0:
                        self.enemies.pop(i)
                    new_x = -1  # Mark for removal
                    break
                    
            if new_x == -1:
                continue  # Remove bullet
                
            # Check if bullet hits wall
            if (new_x <= 0 or new_x >= self.width-1 or 
                new_y <= 0 or new_y >= self.height-1):
                continue  # Remove bullet
                
            # Add updated bullet
            new_player_bullets.append([new_x, new_y, dx, dy])
            
        self.player_bullets = new_player_bullets
                
    def check_enemy_attacks(self):
        for ex, ey, _, etype in self.enemies:
            if abs(ex - self.player_x) <= 1 and abs(ey - self.player_y) <= 1:
                damage = random.randint(8, 12) if etype == 'T' else random.randint(3, 8)
                self.hp -= damage
                break
        
    def handle_input(self):
        if os.name == 'nt' and msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            return {key}
        return set()
        
    def player_shoot(self, direction):
        dx, dy = 0, 0
        if direction == 'i': dy = -1  # up
        elif direction == 'k': dy = 1   # down
        elif direction == 'j': dx = -1  # left
        elif direction == 'l': dx = 1   # right
        
        self.player_bullets.append([self.player_x, self.player_y, dx, dy])
        
    def toggle_inventory(self):
        self.show_inventory = not self.show_inventory
        
    def use_item(self, item_type):
        if self.inventory[item_type] > 0:
            self.inventory[item_type] -= 1
            if item_type == 'health':
                self.hp = min(100, self.hp + 25)
            elif item_type == 'speed':
                self.speed_boost_end = time.time() + 10  # 10 second speed boost
            elif item_type == 'damage':
                self.damage_boost_attacks += 5  # Next 5 attacks do extra damage
        
    def play(self):
        while self.hp > 0:
            self.update_display()
            
            # Check exit
            if self.player_x == self.width-2 and self.player_y == self.height-2:
                if not self.enemies:
                    print(f"Level {self.level} complete! Moving to level {self.level + 1}...")
                    time.sleep(1)
                    self.level += 1
                    self.background_drawn = False
                    self.generate_level()
                    self.player_x, self.player_y = 2, 2
                    continue
                else:
                    print(f"Clear all {len(self.enemies)} enemies first!")
                    time.sleep(1)
                    self.background_drawn = False
                    
            new_keys = self.handle_input()
            
            if 'q' in new_keys or 'e' in new_keys: break
            elif 'w' in new_keys: self.move('w')
            elif 's' in new_keys: self.move('s')
            elif 'a' in new_keys: self.move('a')
            elif 'd' in new_keys: self.move('d')
            elif 'f' in new_keys: self.fight()
            elif 'i' in new_keys: self.player_shoot('i')
            elif 'j' in new_keys: self.player_shoot('j')
            elif 'k' in new_keys: self.player_shoot('k')
            elif 'l' in new_keys: self.player_shoot('l')
            elif '\t' in new_keys: self.toggle_inventory()
            elif '1' in new_keys: self.use_item('health')
            elif '2' in new_keys: self.use_item('speed')
            elif '3' in new_keys: self.use_item('damage')
                
            # Enemy shooting and bullet updates happen every frame
            self.enemy_shoot()
            self.update_bullets()
                
            time.sleep(0.05)
                
        print("GAME OVER!")

if __name__ == "__main__":
    seed = None
    if len(sys.argv) > 1:
        try:
            seed = int(sys.argv[1])
        except ValueError:
            print("Invalid seed. Using random seed.")
    
    DungeonCrawler(seed).play()
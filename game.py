import os
import random 
import math
import pygame
from os import listdir
from os.path import isfile, join
import re           
import shutil 


pygame.init()


pygame.display.set_caption("Fake_Fighters")


WIDTH, HEIGHT = 1920, 1080
FPS = 60
window = pygame.display.set_mode((WIDTH, HEIGHT))


try:
    background = pygame.image.load(join("assets", "Background", "Background.png"))
except:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((20, 20, 40))


def auto_load_character(character_name):
    """
    LEGGE dal .air AUTOMATICAMENTE
    ORGANIZZA le cartelle DA SOLO
    CARICA le animazioni SENZA mapping manuale
    """
    
    mugen_path = f"assets/mugen_chars/{character_name}"
    char_path = f"assets/Characters/{character_name}"
    all_anim = os.path.join(char_path, "all_animation")
    air_file = os.path.join(mugen_path, f"{character_name}.air")
    
    if not os.path.exists(all_anim):
        print(f"  ⚠️  {all_anim} non esiste")
        return {}
    
    # STEP 1: Leggi .air
    actions = {}
    try:
        with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                match = re.search(r'\[Begin Action\s+(\d+)\]', line)
                if match:
                    action_id = int(match.group(1))
                    actions[action_id] = f"Action{action_id}"
        print(f"  ✅ Lette {len(actions)} azioni dal .air")
    except:
        print(f"  ⚠️  {air_file} non trovato")
        return {}
    
    # STEP 2: Organizza PNG automaticamente
    organized = {}
    for png_file in os.listdir(all_anim):
        if png_file.endswith('.png'):
            numbers = re.findall(r'\d+', png_file)
            if len(numbers) >= 2:
                group_id = int(numbers[0])
                frame = int(numbers[1])
                
                if group_id not in organized:
                    organized[group_id] = []
                organized[group_id].append((frame, png_file))
    
    print(f"  ✅ Trovati {len(organized)} gruppi di sprite")
    
    # STEP 3: Crea cartelle
    for group_id, frames in organized.items():
        folder_name = actions.get(group_id, f"Action{group_id}")
        folder = os.path.join(char_path, folder_name)
        os.makedirs(folder, exist_ok=True)
        
        for idx, (_, png_file) in enumerate(sorted(frames)):
            src = os.path.join(all_anim, png_file)
            dst = os.path.join(folder, f"{idx}.png")
            shutil.copy2(src, dst)
    
    print(f"  ✅ Organizzate {sum(len(f) for f in organized.values())} sprite")
    return actions  


class SpriteManager:
    def __init__(self):
        self.sprites_cache =  {}



    def get_sprites(self, character_name, action):
        if character_name not in self.sprites_cache:
            self.sprites_cache[character_name] = {}
        
        if action not in self.sprites_cache[character_name]:
            sprite_list = []


            folder_path = os.path.join("assets", "Characters", character_name, action)
            
            if not os.path.exists(folder_path):
                placeholder = pygame.Surface((100, 100))
                placeholder.fill((50, 50, 50))
                sprite_list = [placeholder]
            else:
                sprites_name = sorted(os.listdir(folder_path))

                for name in sprites_name:
                    if name.endswith('.png'):
                        path = os.path.join(folder_path, name)
                        try:
                            image = pygame.image.load(path).convert_alpha()
                            sprite_list.append(image)
                        except:
                            pass
            
            if not sprite_list:
                placeholder = pygame.Surface((100, 100))
                placeholder.fill((50, 50, 50))
                sprite_list = [placeholder]
            
            self.sprites_cache[character_name][action] = sprite_list
        
        return self.sprites_cache[character_name][action]



class Animation():
    """Classe per gestire animazioni con loop/no-loop."""
    
    def __init__(self, x, y, character_name, action, delay, sprite_manager, scale=1, loop=True):
        self.x = x
        self.y = y
        self.delay = delay
        self.scale = scale
        self.loop = loop
        self.frame_index = 0
        self.frame_timer = 0
        self.sprites = []
        
        self.sprites = sprite_manager.get_sprites(character_name, action)
    
    def update(self, dt):
        """Aggiorna frame animazione."""
        self.frame_timer += dt
        if self.frame_timer >= self.delay:
            if self.loop:
                self.frame_index = (self.frame_index + 1) % len(self.sprites)
            else:
                self.frame_index = min(self.frame_index + 1, len(self.sprites) - 1)
            
            self.frame_timer = 0
        
    
    def reset(self):
        """Reset animazione a frame 0."""
        self.frame_index = 0
        self.frame_timer = 0
    
    def is_finished(self):
        """True se animazione one-shot è finita."""
        if not self.loop:
            return self.frame_index == len(self.sprites) - 1
        return False



class Player(pygame.sprite.Sprite):
    GRAVITY = 2.0
    ANIMATION_DELAY = 3
    GROUND_LEVEL = 1040


    ATTACK_ANIMATIONS = {
        "Frieza": {
            "attack1": "Action200",
            "attack2": "Action210",
            "attack3": "Action220",
            "air_attack1": "Action600",
            "air_attack2": "Action610",
        },
        
        "Yamcha": {
            "attack1": "Action200",
            "attack2": "Action210",
            "attack3": "Action220",
            "air_attack1": "Action600",
        },
    }

    def __init__(self, x, y, name, sprite_manager):
        super().__init__()
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "Right"
        self.current_state = "idle"
        self.name = name
        self.sprite_manager = sprite_manager
        self.speed = 12
        self.jump_direction = "neutral"
        self.on_ground = True
        
        self.is_attacking = False
        self.attack_type = None
        
        self.attack_map = self.ATTACK_ANIMATIONS.get(name, {})
        self._attack_cache = {}
        self._current_anim = None


        # Animazioni movimento
        if name == "Frieza":
            self.idle = Animation(x, y, name, "Action170", 100, sprite_manager, loop=True)
            self.run = Animation(x, y, name, "Action333", 100, sprite_manager, loop=True)
            self.jump_up = Animation(x, y, name, "Action410", 167, sprite_manager, loop=False)
            self.jump_back = Animation(x, y, name, "Action410", 167, sprite_manager, loop=False)
            self.jump_forw = Animation(x, y, name, "Action410", 167, sprite_manager, loop=False)
            self.jump_fall = Animation(x, y, name, "Action410", 133, sprite_manager, loop=False)
            self.jump_land = Animation(x, y, name, "Action410", 133, sprite_manager, loop=False)
        else:  # Yamcha
            self.idle = Animation(x, y, name, "Idle", 100, sprite_manager, loop=True)
            self.run = Animation(x, y, name, "WalkForward", 100, sprite_manager, loop=True)
            self.jump_up = Animation(x, y, name, "JumpUp", 167, sprite_manager, loop=False)
            self.jump_back = Animation(x, y, name, "JumpBackward", 167, sprite_manager, loop=False)
            self.jump_forw = Animation(x, y, name, "JumpForward", 167, sprite_manager, loop=False)
            self.jump_fall = Animation(x, y, name, "JumpFall", 133, sprite_manager, loop=False)
            self.jump_land = Animation(x, y, name, "JumpLand", 83, sprite_manager, loop=False)



        self.image = self.idle.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)


        self.hp = 100
        self.max_hp = 100


        self.hurtbox = pygame.Rect(0, 0, 60, 100)
        self.hurtbox.midbottom = (x, y)


    def get_attack_animation(self, attack_key):
        """Lazy loading con cache per attacchi."""
        if attack_key in self._attack_cache:
            return self._attack_cache[attack_key]
        
        folder_name = self.attack_map.get(attack_key)
        
        if folder_name:
            try:
                anim = Animation(self.x, self.y, self.name, folder_name, 80, self.sprite_manager, loop=False)
                self._attack_cache[attack_key] = anim
                return anim
            except Exception as e:
                self._attack_cache[attack_key] = self.idle
                return self.idle
        else:
            self._attack_cache[attack_key] = self.idle
            return self.idle
    


    def handle_pushbox(self, opponent):
        """Gestisce collisione pushbox tra player."""
        if self.is_attacking or opponent.is_attacking:
                return


        if self.rect.colliderect(opponent.rect):
            if self.x < opponent.x:
                overlap = self.rect.right - opponent.rect.left
                self.x -= overlap // 2
                opponent.x += overlap // 2
            else:
                overlap = opponent.rect.right - self.rect.left
                self.x += overlap // 2 
                opponent.x -= overlap // 2



    def get_active_hitbox(self):
        if not self.is_attacking:
            return None


        hitbox = pygame.Rect(0, 0, 150, 80)


        if self.direction == "Right":
            hitbox.midleft = (self.hurtbox.centerx, self.hurtbox.centery - 10)
        else:
            hitbox.midright = (self.hurtbox.centerx, self.hurtbox.centery - 10)


        return hitbox



    def handle_input(self, keys, left_key, right_key):
        """Gestisce input movimento."""
        if self.on_ground and self.current_state in ["idle", "run"]:
            self.x_vel = 0


            if keys[left_key]:
                self.x_vel = -self.speed
        
            if keys[right_key]:
                self.x_vel = self.speed


    def jump(self, direction="neutral"):
        """Salta solo se a terra e non attaccando."""
        if self.on_ground and not self.is_attacking:
            self.y_vel = -40
            self.current_state = "jump"
            self.jump_direction = direction


            if direction == "forward":
                self.x_vel = 12
            elif direction == "backward":
                self.x_vel = -10
            else:
                self.x_vel = 0


    def attack(self, attack_key="attack1"):
        """Attacca solo se a terra e non già attaccando."""
        if self.on_ground and not self.is_attacking:
            self.is_attacking = True
            self.attack_type = attack_key
            self.current_state = "attacking"
            self.x_vel = 0


    def update_facing(self, opponent):
        """Gira verso avversario."""
        if not self.is_attacking:
            if self.x < opponent.x:
                self.direction = "Right"
            else:
                self.direction = "Left"


    def update(self, dt):
        """Aggiorna posizione, fisica, stato e animazioni."""
        self.x += self.x_vel
        
        self.y_vel += self.GRAVITY
        self.y += self.y_vel
        
        if self.x < 50:
            self.x = 50
            self.x_vel = 0
        if self.x > WIDTH - 50:
            self.x = WIDTH - 50
            self.x_vel = 0
        
        if self.y >= self.GROUND_LEVEL:
            self.y = self.GROUND_LEVEL
            self.y_vel = 0
            self.on_ground = True


            if self.current_state == "jump":
                self.current_state = "landing"
            elif self.current_state not in ["landing", "attacking"]:
                if self.x_vel != 0:
                    self.current_state = "run"
                else:
                    self.current_state = "idle"
        else:
            self.on_ground = False


        if self.current_state == "attacking":
            anim = self.get_attack_animation(self.attack_type)
        elif self.current_state == "jump":
            if self.y_vel < 0:
                if self.jump_direction == "forward":
                    anim = self.jump_forw
                elif self.jump_direction == "backward":
                    anim = self.jump_back
                else:
                    anim = self.jump_up
            else:
                anim = self.jump_fall
        elif self.current_state == "landing":
            anim = self.jump_land
        elif self.current_state == "run":
            anim = self.run
        else:
            anim = self.idle


        if self._current_anim != anim:
            anim.reset()
            self._current_anim = anim


        anim.update(dt)


        if self.current_state == "landing" and anim.is_finished():
            if self.x_vel != 0:
                self.current_state = "run"
            else:
                self.current_state = "idle"
        
        if self.current_state == "attacking" and anim.is_finished():
            self.is_attacking = False
            self.attack_type = None
            self.current_state = "idle"


        current_sprite = anim.sprites[anim.frame_index]
        if self.direction == "Left":
            current_sprite = pygame.transform.flip(current_sprite, True, False)



        self.image = pygame.transform.scale(
            current_sprite,
            (current_sprite.get_width(), current_sprite.get_height())
        )
        
        self.rect = self.image.get_rect()
        self.rect.midbottom = (int(self.x), int(self.y))
        self.hurtbox.midbottom = (int(self.x), int(self.y))
    
    def draw(self, window, debug=False):
        """Disegna player sullo schermo."""
        window.blit(self.image, self.rect)


        if debug:
            pygame.draw.rect(window, (0, 255, 0), self.hurtbox, 2)


            hitbox = self.get_active_hitbox()
            if hitbox:
                pygame.draw.rect(window, (255, 0, 0), hitbox, 2)



def get_background(window, background):
    """Disegna background scalato."""
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    window.blit(background, (0, 0))




def main(window):
    clock = pygame.time.Clock()


    sprite_manager = SpriteManager()


    print("🔧 Organizzando Frieza...")
    auto_load_character("Frieza")
    print("✅ Frieza organizzato!\n")
    
    print("🔧 Organizzando Yamcha...")
    auto_load_character("Yamcha")
    print("✅ Yamcha organizzato!\n")


    player1 = Player(500, 1040, "Frieza", sprite_manager)
    player2 = Player(1420, 1040, "Yamcha", sprite_manager)


    run = True
    while run:
        dt = clock.tick(FPS)
        keys = pygame.key.get_pressed()


        player1.handle_input(keys, pygame.K_a, pygame.K_d)
        player2.handle_input(keys, pygame.K_j, pygame.K_l)


        player1.update(dt)
        player2.update(dt)


        player1.update_facing(player2)
        player2.update_facing(player1)
        player1.handle_pushbox(player2)
        hitbox_p1 = player1.get_active_hitbox()
        if hitbox_p1 and hitbox_p1.colliderect(player2.hurtbox):
            print(f"🔴 Player1 ha colpito Player2! (-10 HP)")
            player2.hp -= 10


        hitbox_p2 = player2.get_active_hitbox()
        if hitbox_p2 and hitbox_p2.colliderect(player1.hurtbox):
            print(f"🔴 Player2 ha colpito Player1! (-10 HP)")
            player1.hp -= 10


        get_background(window, background)
        player1.draw(window, debug=True)
        player2.draw(window, debug=True)


        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if keys[pygame.K_d]:
                        player1.jump("forward")
                    elif keys[pygame.K_a]:
                        player1.jump("backward")
                    else:
                        player1.jump("neutral")
                
                if event.key == pygame.K_i:
                    if keys[pygame.K_l]:
                        player2.jump("forward")
                    elif keys[pygame.K_j]:
                        player2.jump("backward")
                    else:
                        player2.jump("neutral")
                
                if event.key == pygame.K_f:
                    player1.attack("attack1")
                if event.key == pygame.K_g:
                    player1.attack("attack2")
                if event.key == pygame.K_h:
                    player1.attack("attack3")
                
                if event.key == pygame.K_m:
                    player2.attack("attack1")
                if event.key == pygame.K_n:
                    player2.attack("attack2")
                if event.key == pygame.K_b:
                    player2.attack("attack3")


            if event.type == pygame.QUIT:
                run = False


        pygame.display.update()


    pygame.quit()
    quit()



if __name__ == "__main__":
    main(window)

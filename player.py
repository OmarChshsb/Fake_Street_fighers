import os
import random 
import math
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("Fake_Fighters")

WIDTH, HEIGHT = 1920, 1080
FPS = 60
window = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load(join("assets", "Background", "Background.png"))


class Animation():
    """Classe per gestire animazioni con loop/no-loop."""
    
    def __init__(self, x, y, character_name, action, delay, scale=1, loop=True):
        self.x = x
        self.y = y
        self.action = action
        self.delay = delay
        self.character_name = character_name
        self.scale = scale
        self.loop = loop
        self.frame_index = 0
        self.frame_timer = 0
        self.sprites = []
        self.sprites_flipped = []
        
        folder_path = os.path.join("assets", "Characters", self.character_name, self.action)
        sprites_name = sorted(os.listdir(folder_path))

        for name in sprites_name:
            path = os.path.join(folder_path, name)
            image = pygame.image.load(path).convert_alpha()
            self.sprites.append(image)
            self.sprites_flipped.append(pygame.transform.flip(image, True, False))
    
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
        "Hitto": {
            "attack1": "Attack1",
            "attack2": "Attack2",
            "attack3": "Attack3",
            "attackB1": "AttackB1",
            "attackB2": "AttackB2",
            "attackB3": "AttackB3",
            "attackC": "AttackC",
            "air_attack1": "AirAttack1",
            "air_attack2": "AirAttack2",
            "air_attack3": "AirAttack3",
            "air_attack4": "AirAttack4",
            "air_attackC": "AirAttackC",
        },
        
        "Yamcha": {
            "attack1": "Attack1",
            "attack2": "Attack2",
            "attack3": "Attack3",
            "attack4": "Attack4",
            "attack5": "Attack5",
            "attackB1": "AttackB1",
            "attackB2": "AttackB2",
            "attackB3": "AttackB3",
            "attackB4": "AttackB4",
            "attackC": "AttackC",
            "crouch_punch": "CrouchPunch",
            "crouch_kick": "CrouchKick",
            "crouch_kick2": "CrouchKick2",
            "crouch_heavy": "CrouchAttackHeavy",
            "air_attackA": "AttackAirA",
            "air_attack2": "AttackAir2",
            "air_attack3": "AttackAir3",
            "air_attackC": "AttackAirC",
            "air_ki_blast": "KiBlastAir",
            "super_dash": "SuperDash",
            "dash_forward": "DashForward",
            "dash_back": "DashBack",
            "dash_up": "DashUp",
            "dash_effect": "DashEffect",
            "dash_attack": "DashAttack",
            "counter": "Counter",
            "special_wolf": "WolfFang",
            "special_wolf_hit1": "WolfFangHit1",
            "special_wolf_hit2": "WolfFangHit2",
            "special_wolf_barrage": "WolfFangBarrage",
            "special_wolf_finisher": "WolfFangFinisher",
            "special_wolf_end": "WolfFangEnd",
            "special_wolf_full": "SuperWolfFangFull",
            "special_sokidan": "Sokidan",
            "special_sokidan_proj": "SokidanProj",
            "special_sokidan_full": "SuperSokidanFull",
            "special_kamehameha": "Kamehameha",
            "special_kamehameha_beam": "KamehamehaBeam",
            "special_kamehameha_end": "KamehamehaEnd",
            "special_kamehameha_full": "SuperKamehamehaFull",
            "super_prep1": "SuperPrep1",
            "super_prep2": "SuperPrep2",
            "super_flash1": "SuperFlash1",
            "super_flash2": "SuperFlash2",
            "super_beam_charge": "SuperBeamCharge",
            "super_beam_fire": "SuperBeamFire",
            "super_rush": "SuperRush",
            "super_finisher": "SuperFinisher",
            "super_explosion": "SuperExplosion",
            "super_impact": "SuperImpact",
            "super_recovery": "SuperRecovery",
            "ki_charge1": "KiCharge1",
            "ki_charge2": "KiCharge2",
            "taunt": "Taunt",
            "intro_alt": "IntroAlt",
            "transform_start": "TransformStart",
            "power_up_long": "PowerUpLong",
        },
    }

    def __init__(self, x, y, name):
        super().__init__()
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "Right"
        self.current_state = "idle"
        self.name = name
        self.speed = 12
        self.jump_direction = "neutral"
        self.on_ground = True
        
        self.is_attacking = False
        self.attack_type = None
        
        self.attack_map = self.ATTACK_ANIMATIONS.get(name, {})
        self._attack_cache = {}
        self._current_anim = None

        # Animazioni movimento (loop=True)
        self.idle = Animation(x, y, name, "Idle", 100, loop=True)
        self.run = Animation(x, y, name, "WalkForward", 100, loop=True)
        
        # Animazioni salto (loop=False)
        self.jump_up = Animation(x, y, name, "JumpUp", 167, loop=False)
        self.jump_back = Animation(x, y, name, "JumpBackward", 167, loop=False)
        self.jump_forw = Animation(x, y, name, "JumpForward", 167, loop=False)
        self.jump_fall = Animation(x, y, name, "JumpFall", 133, loop=False)
        self.jump_land = Animation(x, y, name, "JumpLand", 83, loop=False)

        self.image = self.idle.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

        self.hp = 100
        self.max_hp = 100

    def get_attack_animation(self, attack_key):
        """Lazy loading con cache per attacchi."""
        if attack_key in self._attack_cache:
            return self._attack_cache[attack_key]
        
        folder_name = self.attack_map.get(attack_key)
        
        if folder_name:
            try:
                anim = Animation(self.x, self.y, self.name, folder_name, 80, loop=False)
                self._attack_cache[attack_key] = anim
                return anim
            except Exception as e:
                print(f"⚠️ Errore caricamento {folder_name} per {self.name}: {e}")
                self._attack_cache[attack_key] = self.idle
                return self.idle
        else:
            print(f"⚠️ {attack_key} non mappato per {self.name}")
            self._attack_cache[attack_key] = self.idle
            return self.idle

    def handle_pushbox(self, opponent):
        """Gestisce collisione pushbox tra player."""
        if self.rect.colliderect(opponent.rect):
            if self.x < opponent.x:
                overlap = self.rect.right - opponent.rect.left
                self.x -= overlap // 2
                opponent.x += overlap // 2
            else:
                overlap = opponent.rect.right - self.rect.left
                self.x += overlap // 2 
                opponent.x -= overlap // 2

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
        # Movimento orizzontale
        self.x += self.x_vel
        
        # Gravità (self.y è la posizione dei PIEDI)
        self.y_vel += self.GRAVITY
        self.y += self.y_vel
        
        # Limiti schermo orizzontali
        if self.x < 50:
            self.x = 50
            self.x_vel = 0
        if self.x > WIDTH - 50:
            self.x = WIDTH - 50
            self.x_vel = 0
        
        # Pavimento (self.y rappresenta i PIEDI)
        if self.y >= self.GROUND_LEVEL:
            self.y = self.GROUND_LEVEL
            self.y_vel = 0
            self.on_ground = True

            # Transizione stati
            if self.current_state == "jump":
                self.current_state = "landing"
            elif self.current_state not in ["landing", "attacking"]:
                if self.x_vel != 0:
                    self.current_state = "run"
                else:
                    self.current_state = "idle"
        else:
            self.on_ground = False

        # Selezione animazione
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

        # Reset animazione se cambiata
        if self._current_anim != anim:
            anim.reset()
            self._current_anim = anim

        # Aggiorna frame animazione
        anim.update(dt)

        # Transizioni stato
        if self.current_state == "landing" and anim.is_finished():
            if self.x_vel != 0:
                self.current_state = "run"
            else:
                self.current_state = "idle"
        
        if self.current_state == "attacking" and anim.is_finished():
            self.is_attacking = False
            self.attack_type = None
            self.current_state = "idle"

        # Rendering
        if self.direction == "Left":
            current_sprite = anim.sprites_flipped[anim.frame_index]
        else:
            current_sprite = anim.sprites[anim.frame_index]

        self.image = pygame.transform.scale(
            current_sprite,
            (current_sprite.get_width() * anim.scale, current_sprite.get_height() * anim.scale)
        )
        
        # FIX CRITICO: Posiziona rect dal BOTTOM (piedi)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (int(self.x), int(self.y))
    
    def draw(self, window):
        """Disegna player sullo schermo."""
        window.blit(self.image, self.rect)



class HealthBar:
    """Barra HP con sprite da fight.sff - CORRETTA PER 1920x1080"""
    
    def __init__(self, player_side, max_hp=1000):
        self.player_side = player_side
        self.max_hp = max_hp
        self.current_hp = max_hp
        
        SCALE = 5
        
        if player_side == "p1":
            self.pos = (138 * SCALE, 15 * SCALE)
            self.range_x = (-3 * SCALE, -99 * SCALE)
            self.facing = 1
        else:
            self.pos = (1920 - (171 * SCALE), 15 * SCALE)
            self.range_x = (13 * SCALE, 109 * SCALE)
            self.facing = -1
        
        self.sprite_scale = SCALE  # ← FIX: Prima di load_sprites()!
        self.sprites = self.load_sprites()
        self.bar_width = abs(self.range_x[1] - self.range_x[0])
    
    def load_sprites(self):
        sprites = {}
        base_path = "assets/Items/Hp_bar"
        
        if self.player_side == "p1":
            sprite_files = {
                "bg1": "11 0 fight.png",
                "mid": "12 0 fight.png",
                "front": "13 0 fight.png",
            }
        else:
            sprite_files = {
                "bg1": "11 1 fight.png",
                "mid": "12 1 fight.png",
                "front": "13 1 fight.png",
            }
        
        for key, filename in sprite_files.items():
            path = os.path.join(base_path, filename)
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    scaled = pygame.transform.scale(
                        img, 
                        (img.get_width() * self.sprite_scale, img.get_height() * self.sprite_scale)
                    )
                    sprites[key] = scaled
                except Exception as e:
                    print(f"⚠️ Errore caricamento {filename}: {e}")
                    sprites[key] = self._create_placeholder(key)
            else:
                sprites[key] = self._create_placeholder(key)
        
        return sprites
    
    def _create_placeholder(self, key):
        if key == "bg1":
            surf = pygame.Surface((96 * self.sprite_scale, 10 * self.sprite_scale), pygame.SRCALPHA)
            surf.fill((50, 0, 0, 100))
        elif key == "mid":
            surf = pygame.Surface((96 * self.sprite_scale, 10 * self.sprite_scale), pygame.SRCALPHA)
            surf.fill((200, 50, 50, 200))
        else:
            surf = pygame.Surface((96 * self.sprite_scale, 10 * self.sprite_scale), pygame.SRCALPHA)
            surf.fill((255, 200, 0, 255))
        return surf
    
    def take_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)
    
    def heal(self, amount):
        self.current_hp = min(self.max_hp, self.current_hp + amount)
    
    def get_hp_percentage(self):
        return self.current_hp / self.max_hp
    
    def draw(self, window):
        x, y = self.pos
        
        bg1 = self.sprites.get("bg1")
        if bg1:
            bg_to_draw = bg1
            if self.facing == -1:
                bg_to_draw = pygame.transform.flip(bg1, True, False)
            window.blit(bg_to_draw, (x + self.range_x[0], y))
        
        hp_percent = self.get_hp_percentage()
        front = self.sprites.get("front")
        
        if front and hp_percent > 0:
            bar_full_width = self.bar_width
            current_width = int(bar_full_width * hp_percent)
            
            if current_width > 0:
                if self.player_side == "p1":
                    sprite_percent = hp_percent
                    crop_width = int(front.get_width() * sprite_percent)
                    crop_x = front.get_width() - crop_width
                    
                    if crop_width > 0:
                        crop_rect = pygame.Rect(crop_x, 0, crop_width, front.get_height())
                        cropped = front.subsurface(crop_rect)
                        draw_x = x + self.range_x[1] + (bar_full_width - current_width)
                        window.blit(cropped, (draw_x, y))
                else:
                    sprite_percent = hp_percent
                    crop_width = int(front.get_width() * sprite_percent)
                    
                    if crop_width > 0:
                        crop_rect = pygame.Rect(0, 0, crop_width, front.get_height())
                        cropped = front.subsurface(crop_rect)
                        
                        if self.facing == -1:
                            cropped = pygame.transform.flip(cropped, True, False)
                        
                        draw_x = x + self.range_x[0]
                        window.blit(cropped, (draw_x, y))


class PowerBar:
    """Barra power/super - CORRETTA PER 1920x1080"""
    
    def __init__(self, player_side, max_bars=3):
        self.player_side = player_side
        self.max_bars = max_bars
        self.current_power = 0
        
        # POSIZIONI CORRETTE (scalate)
        SCALE = 5
        
        if player_side == "p1":
            self.pos = (123 * SCALE, 1080 - 150)  # (615, 930)
            self.range_x = (-9 * SCALE, -79 * SCALE)
            self.counter_offset = (-91 * SCALE, -138 * SCALE)
        else:
            self.pos = (1920 - (198 * SCALE), 1080 - 150)  # (930, 930)
            self.range_x = (7 * SCALE, 77 * SCALE)
            self.counter_offset = (90 * SCALE, -138 * SCALE)
        
        # FIX: sprite_scale PRIMA di load_sprites()
        self.sprite_scale = SCALE
        self.sprites = self.load_sprites()
        self.bar_width_per_level = abs(self.range_x[1] - self.range_x[0]) // max_bars
    
    def load_sprites(self):
        """Carica sprite power bar"""
        sprites = {}
        base_path = "assets/Items/Hp_bar"
        
        if self.player_side == "p1":
            sprite_files = {
                "bg1": "21 1 fight.png",
                "front": "23 0 fight.png",
            }
        else:
            sprite_files = {
                "bg1": "22 1 fight.png",
                "front": "23 1 fight.png",
            }
        
        for key, filename in sprite_files.items():
            path = os.path.join(base_path, filename)
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    scaled = pygame.transform.scale(
                        img,
                        (img.get_width() * self.sprite_scale, img.get_height() * self.sprite_scale)
                    )
                    sprites[key] = scaled
                    print(f"✅ Caricato power {filename}: scalato a {scaled.get_width()}x{scaled.get_height()}")
                except Exception as e:
                    print(f"⚠️ Errore caricamento power {filename}: {e}")
                    sprites[key] = self._create_placeholder()
            else:
                print(f"❌ Power sprite non trovato: {path}")
                sprites[key] = self._create_placeholder()
        
        return sprites
    
    def _create_placeholder(self):
        """Crea placeholder sprite scalato"""
        surf = pygame.Surface((70 * self.sprite_scale, 10 * self.sprite_scale), pygame.SRCALPHA)
        surf.fill((0, 100, 200, 150))
        return surf
    
    def add_power(self, amount=0.1):
        """Aumenta power"""
        self.current_power = min(self.max_bars, self.current_power + amount)
    
    def use_power(self, bars_required=1):
        """Usa power per super"""
        if self.current_power >= bars_required:
            self.current_power -= bars_required
            return True
        return False
    
    def can_use_super(self, bars_required=1):
        """Check se ha power sufficiente"""
        return self.current_power >= bars_required
    
    def draw(self, window):
        """Disegna power bar"""
        x, y = self.pos
        
        # Background
        bg = self.sprites.get("bg1")
        if bg:
            window.blit(bg, (x, y))
        
        # Front bars (piene)
        front = self.sprites.get("front")
        if front:
            full_bars = int(self.current_power)
            partial = self.current_power - full_bars
            
            # Disegna barre piene
            for i in range(full_bars):
                bar_x = x + self.range_x[0] + (i * self.bar_width_per_level)
                window.blit(front, (bar_x, y))
            
            # Disegna barra parziale (se c'è)
            if partial > 0 and full_bars < self.max_bars:
                partial_width = int(front.get_width() * partial)
                if partial_width > 0:
                    crop_rect = pygame.Rect(0, 0, partial_width, front.get_height())
                    cropped = front.subsurface(crop_rect)
                    bar_x = x + self.range_x[0] + (full_bars * self.bar_width_per_level)
                    window.blit(cropped, (bar_x, y))






def get_background(window, background):
    """Disegna background scalato."""
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    window.blit(background, (0, 0))


def main(window):
    clock = pygame.time.Clock()

    player1 = Player(400, 1040, "Hitto")
    player2 = Player(1200, 1040, "Yamcha")

    p1_health = HealthBar("p1", max_hp=1000)
    p2_health = HealthBar("p2", max_hp=1000)
    
    p1_power = PowerBar("p1", max_bars=3)
    p2_power = PowerBar("p2", max_bars=3)

    run = True
    while run:
        dt = clock.tick(FPS)
        keys = pygame.key.get_pressed()

        # Input movimento
        player1.handle_input(keys, pygame.K_a, pygame.K_d)
        player2.handle_input(keys, pygame.K_j, pygame.K_l)

        # Update fisica e animazioni
        player1.update(dt)
        player2.update(dt)

        # Update facing e collisioni
        player1.update_facing(player2)
        player2.update_facing(player1)
        player1.handle_pushbox(player2)

        # Rendering
        get_background(window, background)
        player1.draw(window)
        player2.draw(window)

        p1_health.draw(window)
        p2_health.draw(window)
        p1_power.draw(window)
        p2_power.draw(window)

        # Input eventi
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Player1 salti
                if event.key == pygame.K_w:
                    if keys[pygame.K_d]:
                        player1.jump("forward")
                    elif keys[pygame.K_a]:
                        player1.jump("backward")
                    else:
                        player1.jump("neutral")
                
                # Player2 salti
                if event.key == pygame.K_i:
                    if keys[pygame.K_l]:
                        player2.jump("forward")
                    elif keys[pygame.K_j]:
                        player2.jump("backward")
                    else:
                        player2.jump("neutral")
                
                # Player1 attacchi
                if event.key == pygame.K_f:
                    player1.attack("attack1")
                if event.key == pygame.K_g:
                    player1.attack("attackB1")
                if event.key == pygame.K_h:
                    player1.attack("attackC")
                
                # Player2 attacchi
                if event.key == pygame.K_m:
                    player2.attack("attack1")
                if event.key == pygame.K_n:
                    player2.attack("attack2")
                if event.key == pygame.K_b:
                    player2.attack("attackC")
                if event.key == pygame.K_p:
                    player2.attack("attack5")
                if event.key == pygame.K_o:
                    player2.attack("special_wolf")
                if event.key == pygame.K_u:
                    player2.attack("special_kamehameha")

                if event.key == pygame.K_1:  # P1 perde HP
                    p1_health.take_damage(100)
                if event.key == pygame.K_2:  # P2 perde HP
                    p2_health.take_damage(100)
                if event.key == pygame.K_3:  # P1 guadagna power
                    p1_power.add_power(0.5)
                if event.key == pygame.K_4:  # P2 guadagna power
                    p2_power.add_power(0.5)

            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)

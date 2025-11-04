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




class SpriteManager:
    def __init__(self):
        self.sprites_cache =  {}


    def get_sprites(self, character_name, action):
        if character_name not in self.sprites_cache:
            self.sprites_cache[character_name] = {}
        
        if action not in self.sprites_cache[character_name]:
            sprite_list = []

            folder_path = os.path.join("assets", "Characters", character_name, action)
            sprites_name = sorted(os.listdir(folder_path))

            for name in sprites_name:
                path = os.path.join(folder_path, name)
                image = pygame.image.load(path).convert_alpha()
                sprite_list.append(image)
                
            
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

        # Animazioni movimento (loop=True)
        self.idle = Animation(x, y, name, "Idle", 100, sprite_manager, loop=True)
        self.run = Animation(x, y, name, "WalkForward", 100, sprite_manager, loop=True)
        
        # Animazioni salto (loop=False)
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

        # sistema hitbox

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
                print(f"⚠️ Errore caricamento {folder_name} per {self.name}: {e}")
                self._attack_cache[attack_key] = self.idle
                return self.idle
        else:
            print(f"⚠️ {attack_key} non mappato per {self.name}")
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
        current_sprite = anim.sprites[anim.frame_index]
        if self.direction == "Left":
            current_sprite = pygame.transform.flip(current_sprite, True, False)


        self.image = pygame.transform.scale(
            current_sprite,
            (current_sprite.get_width() * anim.scale, current_sprite.get_height() * anim.scale)
        )
        
        # FIX CRITICO: Posiziona rect dal BOTTOM (piedi)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (int(self.x), int(self.y))
        self.hurtbox.midbottom = (int(self.x), int(self.y))
    
    def draw(self, window, debug = False):
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

    sprite_manager =  SpriteManager()

    player1 = Player(500, 1040, "Hitto", sprite_manager)
    player2 = Player(1420, 1040, "Yamcha", sprite_manager)

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
        hitbox_p1 = player1.get_active_hitbox()
        if hitbox_p1 and hitbox_p1.colliderect(player2.hurtbox):
            print(f"🔴 Player1 ha colpito Player2! (-10 HP)")
            player2.hp -= 10

        hitbox_p2 = player2.get_active_hitbox()
        if hitbox_p2 and hitbox_p2.colliderect(player1.hurtbox):
            print(f"🔴 Player2 ha colpito Player1! (-10 HP)")
            player1.hp -= 10

        # Rendering
        get_background(window, background)
        player1.draw(window, debug=True)
        player2.draw(window, debug=True)

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

            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)

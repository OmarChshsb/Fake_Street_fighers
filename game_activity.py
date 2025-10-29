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
        self.loop = loop  # Loop infinito o one-shot
        self.frame_index = 0
        self.frame_timer = 0
        self.sprites = []
        self.sprites_flipped = []
        
        folder_path = os.path.join("assets", "Characters", self.character_name, self.action)
        sprites_name = sorted(os.listdir(folder_path))  # Sort per ordine corretto

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
                # Loop infinito (idle, run)
                self.frame_index = (self.frame_index + 1) % len(self.sprites)
            else:
                # One-shot: fermati all'ultimo frame (salti, attacchi)
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

    # Dizionario completo attacchi per personaggio
    ATTACK_ANIMATIONS = {
    
    "Hitto": {
        # ATTACCHI LIGHT 
        "attack1": "Attack1",          # Light Punch 1 (4 frame)
        "attack2": "Attack2",          # Light Punch 2 (5 frame)
        "attack3": "Attack3",          # Light Punch 3 (12 frame)
        
        #  ATTACCHI MEDIUM 
        "attackB1": "AttackB1",        # Medium Kick 1 (11 frame)
        "attackB2": "AttackB2",        # Medium Kick 2 (16 frame)
        "attackB3": "AttackB3",        # Medium Kick 3 (15 frame)
        
        # ATTACCHI HEAVY/SPECIAL 
        "attackC": "AttackC",          # Time Skip Counter (6 frame)
        
        # ATTACCHI AEREI 
        "air_attack1": "AirAttack1",   # Air Light 1 (9 frame)
        "air_attack2": "AirAttack2",   # Air Light 2 (9 frame)
        "air_attack3": "AirAttack3",   # Air Heavy (5 frame)
        "air_attack4": "AirAttack4",   # Air Spike (10 frame)
        "air_attackC": "AirAttackC",   # Air Counter (5 frame)
    },
    
    "Yamcha": {
        # ATTACCHI LIGHT 
        "attack1": "Attack1",          # Light Punch 1 (4 frame)
        "attack2": "Attack2",          # Light Punch 2 (4 frame)
        "attack3": "Attack3",          # Light Punch 3 (5 frame)
        "attack4": "Attack4",          # Multi-hit Barrage (23 frame) 
        "attack5": "Attack5",          # Launcher (38 frame) 
        
        # ATTACCHI MEDIUM 
        "attackB1": "AttackB1",        # Medium Kick 1 (10 frame) 
        "attackB2": "AttackB2",        # Medium Kick 2 Air (4 frame) 
        "attackB3": "AttackB3",        # Medium Kick 3 (23 frame) 
        "attackB4": "AttackB4",        # Multi-hit Barrage (27 frame) 
        
        # ATTACCHI HEAVY/SPECIAL 
        "attackC": "AttackC",          # Ki Blast (2 frame)
        
        #  ATTACCHI CROUCHING 
        "crouch_punch": "CrouchPunch", # Crouch Punch
        "crouch_kick": "CrouchKick",   # Crouch Kick
        "crouch_kick2": "CrouchKick2", # Crouch Kick 2 (11 frame) 
        "crouch_heavy": "CrouchAttackHeavy", # Crouch Heavy (10 frame) 
        
        #  ATTACCHI AEREI 
        "air_attackA": "AttackAirA",   # Air Medium (4 frame)
        "air_attack2": "AttackAir2",   # Air Light 1 (3 frame)
        "air_attack3": "AttackAir3",   # Air Heavy (4 frame)
        "air_attackC": "AttackAirC",   # Air Ki Blast
        "air_ki_blast": "KiBlastAir",  # Ki Blast aereo (5 frame) 
        
        # DASH ATTACKS 
        "super_dash": "SuperDash",     # Dragon Rush (5 frame)
        "dash_forward": "DashForward", # Dash avanti (3 frame) 
        "dash_back": "DashBack",       # Dash indietro (3 frame) 
        "dash_up": "DashUp",           # Super dash up (3 frame) 
        "dash_effect": "DashEffect",   # Effetto dash
        "dash_attack": "DashAttack",   # Attacco dash
        
        #  COUNTER 
        "counter": "Counter",          # Counter move (3 frame)
        
        #  SPECIALI: WOLF FANG FIST 
        "special_wolf": "WolfFang",               # Wolf Fang Start (1 frame)
        "special_wolf_hit1": "WolfFangHit1",      # Hit 1 (3 frame)
        "special_wolf_hit2": "WolfFangHit2",      # Hit 2 (2 frame)
        "special_wolf_barrage": "WolfFangBarrage",# Barrage 
        "special_wolf_finisher": "WolfFangFinisher", # Finisher 
        "special_wolf_end": "WolfFangEnd",        # End 
        "special_wolf_full": "SuperWolfFangFull", # Versione completa (43 frame) 
        
        #  SPECIALI: SPIRIT BALL 
        "special_sokidan": "Sokidan",          # Spirit Ball Start (2 frame)
        "special_sokidan_proj": "SokidanProj", # Projectile 
        "special_sokidan_full": "SuperSokidanFull", # Versione completa (50 frame) 
        
        #  SPECIALI: KAMEHAMEHA 
        "special_kamehameha": "Kamehameha",        # Kamehameha Start (7 frame)
        "special_kamehameha_beam": "KamehamehaBeam", # Beam (1 frame)
        "special_kamehameha_end": "KamehamehaEnd",   # End (1 frame)
        "special_kamehameha_full": "SuperKamehamehaFull", # Versione completa (46 frame) 
        
        #  SUPER MOVES 
        "super_prep1": "SuperPrep1",        # Preparazione super 1 (5 frame)
        "super_prep2": "SuperPrep2",        # Preparazione super 2 (5 frame)
        "super_flash1": "SuperFlash1",      # Flash super 1 (5 frame)
        "super_flash2": "SuperFlash2",      # Flash super 2 (15 frame)
        "super_beam_charge": "SuperBeamCharge", # Carica beam (9 frame)
        "super_beam_fire": "SuperBeamFire",     # Spara beam (4 frame)
        "super_rush": "SuperRush",          # Rush super (15 frame)
        "super_finisher": "SuperFinisher",  # Finisher cinematico (30 frame)
        "super_explosion": "SuperExplosion",# Esplosione (10 frame)
        "super_impact": "SuperImpact",      # Impact effect (5 frame)
        "super_recovery": "SuperRecovery",  # Recovery (8 frame)
        
        #  KI CHARGE 
        "ki_charge1": "KiCharge1",      # Carica ki base (3 frame) 
        "ki_charge2": "KiCharge2",      # Carica ki avanzata (6 frame) 
        
        #  TAUNT & INTRO 
        "taunt": "Taunt",               # Taunt (7 frame) 
        "intro_alt": "IntroAlt",        # Intro alternativa (5 frame) 
        
        #  TRANSFORM/POWER UP 
        "transform_start": "TransformStart",  # Inizio trasformazione (6 frame) 
        "power_up_long": "PowerUpLong",       # Power up lungo (11 frame) 
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
        
        # Variabili attacco
        self.is_attacking = False
        self.attack_type = None
        
        # Mapping e cache attacchi
        self.attack_map = self.ATTACK_ANIMATIONS.get(name, {})
        self._attack_cache = {}
        self._current_anim = None

        # ===== ANIMAZIONI MOVIMENTO (loop=True) =====
        self.idle = Animation(x, y, name, "Idle", 100, loop=True)
        self.run = Animation(x, y, name, "WalkForward", 100, loop=True)
        
        # ===== ANIMAZIONI SALTO (loop=False, one-shot) =====
        # Timing basato su: salto dura ~40 frame con GRAVITY=2.0, y_vel=-40
        self.jump_up = Animation(x, y, name, "JumpUp", 167, loop=False)       # ~10 frame per sprite
        self.jump_back = Animation(x, y, name, "JumpBackward", 167, loop=False)
        self.jump_forw = Animation(x, y, name, "JumpForward", 167, loop=False)
        self.jump_fall = Animation(x, y, name, "JumpFall", 133, loop=False)   # Caduta più veloce
        self.jump_land = Animation(x, y, name, "JumpLand", 83, loop=False)    # ~5 frame recovery

        self.image = self.idle.sprites[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.hp = 100
        self.max_hp = 100

    def get_attack_animation(self, attack_key):
        """
        Lazy loading con cache per attacchi.
        Performance: O(1) dopo primo caricamento.
        """
        if attack_key in self._attack_cache:
            return self._attack_cache[attack_key]
        
        folder_name = self.attack_map.get(attack_key)
        
        if folder_name:
            try:
                # Attacchi: loop=False, delay ~60-100ms (dipende dal tipo)
                anim = Animation(self.x, self.y, self.name, folder_name, 80, loop=False)
                self._attack_cache[attack_key] = anim
                return anim
            except Exception as e:
                print(f" Errore caricamento {folder_name} per {self.name}: {e}")
                self._attack_cache[attack_key] = self.idle
                return self.idle
        else:
            print(f" {attack_key} non mappato per {self.name}")
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
        
        self.rect.x = self.x
        opponent.rect.x = opponent.x

    def handle_input(self, keys, left_key, right_key):
        """Gestisce input movimento - blocca se attacca."""
        if self.on_ground and not self.is_attacking:
            self.x_vel = 0

            if keys[left_key]:
                self.x_vel = -self.speed
        
            if keys[right_key]:
                self.x_vel = self.speed

    def jump(self, direction="neutral"):
        """Salta solo se a terra e non attaccando."""
        if self.y_vel == 0 and not self.is_attacking:
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
        """Gira verso avversario - blocca se attacca."""
        if not self.is_attacking:
            if self.x < opponent.x:
                self.direction = "Right"
            else:
                self.direction = "Left"

    def update(self, dt):
        """Aggiorna posizione, fisica, stato e animazioni."""
        # Movimento orizzontale
        self.x += self.x_vel
        self.rect.x = self.x

        # Gravità
        self.y_vel += self.GRAVITY
        self.rect.y += self.y_vel
        self.y = self.rect.y

        # Limiti schermo
        if self.rect.left < 0:
            self.rect.left = 0
            self.x = self.rect.x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.x = self.rect.x
        
        # Pavimento
        if self.rect.bottom >= self.GROUND_LEVEL:
            self.rect.bottom = self.GROUND_LEVEL
            self.y_vel = 0
            self.y = self.rect.y
            self.on_ground = True

            # Transizione stati
            if self.current_state == "jump":
                self.current_state = "landing"
            elif self.current_state != "landing" and self.current_state != "attacking":
                if self.x_vel != 0:
                    self.current_state = "run"
                else:
                    self.current_state = "idle"
        else:
            self.on_ground = False

        # ===== SELEZIONE ANIMAZIONE =====
        if self.current_state == "attacking":
            anim = self.get_attack_animation(self.attack_type)
        elif self.current_state == "jump":
            if self.y_vel < 0:  # Salita
                if self.jump_direction == "forward":
                    anim = self.jump_forw
                elif self.jump_direction == "backward":
                    anim = self.jump_back
                else:
                    anim = self.jump_up
            else:  # Caduta
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

        # Aggiorna posizione e frame animazione
        anim.x = self.x
        anim.y = self.y
        anim.update(dt)

        # ===== TRANSIZIONI STATO =====
        # Landing finisce
        if self.current_state == "landing" and anim.is_finished():
            if self.x_vel != 0:
                self.current_state = "run"
            else:
                self.current_state = "idle"
        
        # Attacco finisce
        if self.current_state == "attacking" and anim.is_finished():
            self.is_attacking = False
            self.attack_type = None
            self.current_state = "idle"

        # ===== RENDERING =====
        # Flip sprite
        if self.direction == "Left":
            current_sprite = anim.sprites_flipped[anim.frame_index]
        else:
            current_sprite = anim.sprites[anim.frame_index]

        # Scala sprite
        self.image = pygame.transform.scale(
            current_sprite,
            (current_sprite.get_width() * anim.scale, current_sprite.get_height() * anim.scale)
        )
    
    def draw(self, window):
        """Disegna player sullo schermo."""
        window.blit(self.image, (self.x, self.y))


def get_background(window, background):
    """Disegna background scalato."""
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    window.blit(background, (0, 0))


def main(window):
    clock = pygame.time.Clock()

    player1 = Player(400, 580, "Hitto")
    player2 = Player(1200, 620, "Yamcha")

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
                if event.key == pygame.K_f:  # Light
                    player1.attack("attack1")
                if event.key == pygame.K_g:  # Medium
                    player1.attack("attackB1")
                if event.key == pygame.K_h:  # Heavy
                    player1.attack("attackC")
                
                # Player2 attacchi
                if event.key == pygame.K_m:  # Light (NumPad 1)
                    player2.attack("attack1")
                if event.key == pygame.K_n:  # Medium (NumPad 2)
                    player2.attack("attackB1")
                if event.key == pygame.K_b:  # Heavy (NumPad 3)
                    player2.attack("attackC")

                if event.key == pygame.K_p:  # Launcher
                    player2.attack("attack5")
                if event.key == pygame.K_o:  # Wolf Fang Fist
                    player2.attack("special_wolf")
                if event.key == pygame.K_u:  # Kamehameha
                    player2.attack("special_kamehameha")

            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)

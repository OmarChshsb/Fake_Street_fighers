import os
import shutil
import re


# ============================================
# CONFIGURAZIONE
# ============================================

AIR_FILE = r"D:\atom_editor\python_game\assets\Characters\Yamcha\Yamcha.air"
SPRITES_FOLDER = r"D:\atom_editor\python_game\assets\Characters\Yamcha\all_animation"
OUTPUT_FOLDER = r"D:\atom_editor\python_game\assets\Characters\Yamcha"


# MAPPA COMPLETA YAMCHA (basata su CNS analizzato)
ANIMATION_MAP = {
    # ===== MOVIMENTO BASE =====
    0: "Idle",
    5: "Turn",
    6: "CrouchTurn",
    10: "CrouchDown",
    11: "Crouch",
    12: "CrouchUp",
    20: "WalkForward",
    21: "WalkBackward",
    
    # ===== SALTI =====
    40: "JumpStart",
    41: "JumpUp",
    42: "JumpForward",
    43: "JumpBackward",
    44: "JumpFall",
    45: "JumpFallForward",
    46: "JumpFallBackward",
    47: "JumpLand",
    
    # ===== CORSA =====
    100: "RunForward",
    105: "RunBackward",
    106: "RunJumpStart",
    132: "RunBrake",
    
    # ===== GUARD =====
    120: "GuardStart",
    121: "GuardStartCrouch",
    122: "GuardStartAir",
    130: "Guard",
    131: "GuardCrouch",
    132: "GuardAir",
    140: "GuardEnd",
    141: "GuardEndCrouch",
    142: "GuardEndAir",
    150: "GuardHit",
    151: "GuardHitCrouch",
    152: "GuardHitAir",
    
    # ===== ATTACCHI LIGHT (200 series) =====
    200: "Attack1",         # Light Punch 1 (Statedef 200)
    210: "Attack2",         # Light Punch 2 (Statedef 210)
    220: "Attack3",         # Light Punch 3 (Statedef 220)
    225: "Attack4",         # Multi-hit barrage (Statedef 225)
    230: "Attack5",         # Launcher (Statedef 230)
    
    # ===== ATTACCHI MEDIUM (250 series) =====
    250: "AttackB1",        # Medium Kick 1 (Statedef 250)
    252: "CrouchKick",      # Crouching Kick (Statedef 252)
    260: "AttackB2",        # Medium Kick 2 - Air (Statedef 260)
    270: "AttackB3",        # Medium Kick 3 (Statedef 270)
    280: "AttackB4",        # Multi-hit barrage (Statedef 280)
    281: "AttackB5",        # Finisher (Statedef 281)
    
    # ===== COUNTER =====
    305: "Counter",         # Counter move (Statedef 305)
    
    # ===== ATTACCHI SPECIAL =====
    400: "AttackC",         # Ki Blast (Statedef 400)
    401: "KiBlastProj",     # Ki projectile
    
    # ===== ATTACCHI AEREI (600 series) =====
    600: "AttackAirA",      # Air Medium (Statedef 600)
    610: "AttackAir2",      # Air Light 1 (Statedef 610)
    615: "AttackAir3",      # Air Heavy (Statedef 615)
    620: "AttackAirC",      # Air Ki Blast (Statedef 620)
    
    # ===== CROUCH ATTACKS =====
    666: "CrouchPunch",     # Crouching Punch (Statedef 666)
    
    # ===== DASH & RUSH =====
    700: "SuperDash",       # Dragon Rush (Statedef 700)
    701: "DashEffect",
    702: "DashAttack",
    
    # ===== SPECIALI AVANZATE =====
    1050: "WolfFang",       # Wolf Fang Fist Start (Statedef 1050-1152)
    1051: "WolfFangHit1",
    1052: "WolfFangHit2",
    1100: "Sokidan",        # Spirit Ball (Statedef 1100)
    1101: "SokidanProj",
    1150: "WolfFangFinisher",
    1151: "WolfFangBarrage",
    1152: "WolfFangEnd",
    1200: "SuperPrep",
    1250: "Kamehameha",     # Kamehameha Start (Statedef 1250-1252)
    1251: "KamehamehaBeam",
    1252: "KamehamehaEnd",
    
    # ===== POWER UP & INTRO =====
    190: "Intro",
    195: "PowerUp",
    196: "PowerCharge",
    
    # ===== VICTORY & DEFEAT =====
    170: "Lose",
    180: "Win",
    181: "WinPose",
    
    # ===== HIT REACTIONS =====
    5000: "HitHighLight",   # Hit leggero alto
    5001: "HitHighMedium",
    5002: "HitHighHeavy",
    5010: "HitLowLight",    # Hit basso
    5011: "HitLowMedium",
    5020: "HitBack",        # Colpito da dietro
    5030: "HitTrip",        # Sgambetto
    5040: "HitFlyUp",       # Lanciato in aria
    5050: "AirFallUp",      # Caduta in aria
    5060: "AirFallDown",
    5070: "HitBounce",      # Rimbalzo
    5080: "HitLieDown",     # A terra
    5081: "HitLieDownDamage",
    5100: "HitGetUp",       # Rialzata
    5110: "HitStayDown",
    5200: "Dizzy",          # Stordito
    5210: "GuardCrush",     # Guard Break
    
    # ===== EFFETTI =====
    444: "HitSpark",        # Scintilla hit
    445: "BigSpark",        # Scintilla grande
    555: "KiEffect",        # Effetto ki
    888: "IntroEffect",     # Effetto intro
    9999: "Empty",          # Frame vuoto
}


# ============================================
# FUNZIONI (invariate, già ottime)
# ============================================

def parse_air_file(air_path):
    """
    Legge il file .air e ritorna: { action_number: [(group,index), ...] }
    """
    animations = {}
    current_action = None

    if not os.path.exists(air_path):
        print(f"❌ File .air non trovato: {air_path}")
        return None

    with open(air_path, 'r', encoding='utf-8', errors='ignore') as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue

            low = line.lower()

            # Begin Action
            if low.startswith('[begin action'):
                m = re.search(r'\[begin action\s*(\d+)\]', low, flags=re.IGNORECASE)
                if m:
                    current_action = int(m.group(1))
                    animations.setdefault(current_action, [])
                else:
                    nums = re.findall(r'\d+', line)
                    if nums:
                        current_action = int(nums[0])
                        animations.setdefault(current_action, [])
                    else:
                        current_action = None
                continue

            # Ignora commenti, Clsn*, LoopStart
            if line.startswith(';') or low.startswith('clsn') or 'loopstart' in low:
                continue

            # Righe -1
            if line.lstrip().startswith('-1'):
                continue

            # Estrai group,index
            if current_action is not None and ',' in line:
                parts = [p.strip() for p in line.split(',') if p.strip() != '']
                if len(parts) < 1:
                    continue

                tokens = []
                for p in parts:
                    mnum = re.search(r'-?\d+', p)
                    if mnum:
                        tokens.append(mnum.group(0))
                    if len(tokens) >= 2:
                        break

                if len(tokens) >= 2:
                    try:
                        group = int(tokens[0])
                        index = int(tokens[1])
                        animations[current_action].append((group, index))
                    except ValueError:
                        pass
    return animations


def build_sprite_index(sprites_folder):
    """
    Scansiona la cartella dei PNG e ritorna: {(group,index): filename}
    """
    index = {}
    if not os.path.exists(sprites_folder):
        print(f"❌ Cartella sprite non trovata: {sprites_folder}")
        return index

    for fname in os.listdir(sprites_folder):
        if not fname.lower().endswith('.png'):
            continue
        nums = re.findall(r'(-?\d+)', fname)
        if len(nums) >= 2:
            try:
                g = int(nums[0])
                i = int(nums[1])
                key = (g, i)
                if key not in index:
                    index[key] = fname
            except ValueError:
                continue
        else:
            m = re.match(r'\s*([0-9]+)[ _-]+([0-9]+)', fname)
            if m:
                g = int(m.group(1))
                i = int(m.group(2))
                key = (g, i)
                if key not in index:
                    index[key] = fname
    return index


def organize_sprites(animations, sprites_folder, output_folder, animation_map):
    """
    Copia i PNG organizzandoli in cartelle per animazione.
    """
    os.makedirs(output_folder, exist_ok=True)
    sprite_index = build_sprite_index(sprites_folder)
    total_copied = 0
    skipped_actions = []

    for action_num in sorted(animations.keys()):
        sprites = animations[action_num]
        if action_num in animation_map:
            anim_name = animation_map[action_num]
        else:
            anim_name = f"Action_{action_num:04d}"
            skipped_actions.append(action_num)

        anim_folder = os.path.join(output_folder, anim_name)
        os.makedirs(anim_folder, exist_ok=True)

        print(f"\n📁 Organizing: {anim_name} (Action {action_num})")
        frame_num = 0
        copied_in_this_anim = 0

        for group, index in sprites:
            key = (group, index)
            if key in sprite_index:
                src_fname = sprite_index[key]
                src_path = os.path.join(sprites_folder, src_fname)
                dest_fname = f"frame_{frame_num:04d}.png"
                dest_path = os.path.join(anim_folder, dest_fname)
                try:
                    shutil.copy2(src_path, dest_path)
                    print(f"   ✅ {src_fname} → {anim_name}/{dest_fname}")
                    frame_num += 1
                    copied_in_this_anim += 1
                    total_copied += 1
                except Exception as e:
                    print(f"   ❌ Errore copiando {src_fname}: {e}")
            else:
                print(f"   ⚠️  Sprite non trovato: group={group}, index={index}")

        if copied_in_this_anim:
            print(f"✅ {anim_name}: {copied_in_this_anim} frame copiati")
        else:
            print(f"❌ {anim_name}: Nessun frame trovato!")

    # Report azioni non mappate
    if skipped_actions:
        print("\n" + "="*60)
        print("⚠️  AZIONI NON MAPPATE (create come Action_XXXX):")
        print("="*60)
        for a in skipped_actions:
            print(f"   Action {a:4d} → {len(animations[a])} sprite")
        print("\nSe vuoi dare nomi specifici, aggiungi queste azioni a ANIMATION_MAP")
        print("="*60)

    return total_copied


# ============================================
# ESECUZIONE
# ============================================

def main():
    print("="*60)
    print("🎮 ORGANIZZATORE SPRITE YAMCHA - Versione Completa")
    print("="*60)
    print()

    animations = parse_air_file(AIR_FILE)
    if animations is None:
        return

    png_count = len([f for f in os.listdir(SPRITES_FOLDER) if f.lower().endswith('.png')]) if os.path.exists(SPRITES_FOLDER) else 0
    print(f"📦 Trovati {png_count} file PNG in {SPRITES_FOLDER}")
    print(f"✅ Trovate {len(animations)} animazioni nel file .air")
    print()

    # Preview azioni
    print("📋 Azioni trovate (top 20):")
    for i, a in enumerate(sorted(animations.keys())[:20]):
        display_name = ANIMATION_MAP.get(a, f"Action_{a:04d}")
        print(f"   Action {a:4d} → {display_name:25s} ({len(animations[a])} sprite)")
    if len(animations) > 20:
        print(f"   ... e altre {len(animations) - 20} azioni")
    print()

    risposta = input("⏸️  Procedere con l'organizzazione? (s/n): ").strip().lower()
    if risposta != 's':
        print("❌ Operazione annullata.")
        return

    print("\n🚀 Avvio organizzazione...")
    total = organize_sprites(animations, SPRITES_FOLDER, OUTPUT_FOLDER, ANIMATION_MAP)
    print()
    print("="*60)
    print(f"✅ COMPLETATO! {total} file copiati in totale")
    print("="*60)
    print(f"📁 Cartelle create in: {OUTPUT_FOLDER}")
    print()


if __name__ == "__main__":
    main()

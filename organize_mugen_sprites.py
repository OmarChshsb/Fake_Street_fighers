import os
import shutil
import re

# ============================================
# CONFIGURAZIONE
# ============================================

AIR_FILE = r"D:\atom_editor\python_game\assets\Characters\Yamcha\Yamcha.air"
SPRITES_FOLDER = r"D:\atom_editor\python_game\assets\Characters\Yamcha\all_animation"
OUTPUT_FOLDER = r"D:\atom_editor\python_game\assets\Characters\Yamcha"

# Mappa di base: estendi se vuoi nomi più specifici
ANIMATION_MAP = {
    0: "Idle",
    5: "Turn",
    6: "CrouchTurn",
    10: "CrouchDown",
    11: "Crouch",
    12: "CrouchUp",
    20: "WalkForward",
    21: "WalkBackward",
    40: "JumpStart",
    41: "JumpUp",
    42: "JumpForward",
    43: "JumpBackward",
    44: "JumpFall",
    45: "JumpFallForward",
    46: "JumpFallBackward",
    47: "JumpLand",
    100: "RunForward",
    105: "RunBackward",
    120: "GuardStart",
    121: "GuardStartCrouch",
    122: "GuardStartAir",
    130: "Guard",
    140: "GuardEnd",
    170: "Lose",
    180: "Win",
    190: "Intro",
    195: "PowerUp",
    200: "AttackStrong",
    210: "AttackLight",
    220: "AttackMedium",
    230: "KickLight",
    252: "CrouchKick",
    300: "Special300",
    310: "Special310",
    400: "KiBlast",
    444: "HitSpark",
    445: "BigSpark",
    5000: "HitHighLight",
    5050: "AirFallUp",
    5060: "AirFallDown",
    555: "KiEffect",
    700: "DragonRush",
    888: "IntroEffect",
    9999: "Empty",
}

# ============================================
# FUNZIONI
# ============================================

def parse_air_file(air_path):
    """
    Legge il file .air e ritorna: { action_number: [(group,int,index,int), ...] }
    Il parser:
    - riconosce [Begin Action N] in modo robusto (case-insensitive)
    - ignora Clsn*, LoopStart, commenti ';' e righe '-1'
    - estrae i primi due numeri trovati in ogni riga valida come group,index
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

            # Begin Action (robusto)
            if low.startswith('[begin action'):
                m = re.search(r'\[begin action\s*(\d+)\]', low, flags=re.IGNORECASE)
                if m:
                    current_action = int(m.group(1))
                    animations.setdefault(current_action, [])
                else:
                    # fallback: prendi il primo numero presente nella riga
                    nums = re.findall(r'\d+', line)
                    if nums:
                        current_action = int(nums[0])
                        animations.setdefault(current_action, [])
                    else:
                        current_action = None
                continue

            # Ignora commenti, Clsn*, LoopStart (case-insensitive)
            if line.startswith(';') or low.startswith('clsn') or 'loopstart' in low:
                continue

            # Righe -1 indicano frame vuoti
            if line.lstrip().startswith('-1'):
                continue

            # Se siamo in un'action e la riga contiene una virgola, prova ad estrarre group,index
            if current_action is not None and ',' in line:
                # Split sui separatori virgola, mantieni i token non vuoti
                parts = [p.strip() for p in line.split(',') if p.strip() != '']
                if len(parts) < 1:
                    continue

                tokens = []
                for p in parts:
                    # estrai il primo numero in ogni token (gestisce anche "-1")
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
                # altrimenti ignora la riga
    return animations

def build_sprite_index(sprites_folder):
    """
    Scansiona la cartella dei PNG e ritorna un dizionario:
      {(group,index): filename, ...}
    Matching tollerante: cerca pattern dove i primi due numeri nel nome file
    rappresentano group e index (separati da spazio/underscore/trattino).
    """
    index = {}
    if not os.path.exists(sprites_folder):
        print(f"❌ Cartella sprite non trovata: {sprites_folder}")
        return index

    for fname in os.listdir(sprites_folder):
        if not fname.lower().endswith('.png'):
            continue
        # estrai numeri dal nome (fino a trovare 2 numeri)
        nums = re.findall(r'(-?\d+)', fname)
        if len(nums) >= 2:
            try:
                g = int(nums[0])
                i = int(nums[1])
                key = (g, i)
                # preferisci il primo trovato, ma non sovrascrivere se già presente
                if key not in index:
                    index[key] = fname
            except ValueError:
                continue
        else:
            # Prova pattern "GGG III" separati da spazio/underscore/trattino
            m = re.match(r'\s*([0-9]+)[ _-]+([0-9]+)', fname)
            if m:
                g = int(m.group(1)); i = int(m.group(2))
                key = (g, i)
                if key not in index:
                    index[key] = fname
    return index

def organize_sprites(animations, sprites_folder, output_folder, animation_map):
    """
    Copia i PNG organizzandoli in cartelle per animazione.
    Per action non mappate crea "Action_XXXX".
    """
    os.makedirs(output_folder, exist_ok=True)
    sprite_index = build_sprite_index(sprites_folder)
    total_copied = 0

    for action_num in sorted(animations.keys()):
        sprites = animations[action_num]
        if action_num in animation_map:
            anim_name = animation_map[action_num]
        else:
            anim_name = f"Action_{action_num:04d}"

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
                # Nessun file trovato per la coppia group/index
                print(f"   ⚠️  Sprite non trovato: group={group}, index={index}")

        if copied_in_this_anim:
            print(f"✅ {anim_name}: {copied_in_this_anim} frame copiati")
        else:
            print(f"❌ {anim_name}: Nessun frame trovato!")

    return total_copied

# ============================================
# ESECUZIONE
# ============================================

def main():
    print("="*60)
    print("🎮 ORGANIZZATORE AUTOMATICO SPRITE MUGEN - Versione pulita")
    print("="*60)
    print()

    animations = parse_air_file(AIR_FILE)
    if animations is None:
        return

    png_count = len([f for f in os.listdir(SPRITES_FOLDER) if f.lower().endswith('.png')]) if os.path.exists(SPRITES_FOLDER) else 0
    print(f"📦 Trovati {png_count} file PNG nella cartella {SPRITES_FOLDER}")
    print(f"✅ Trovate {len(animations)} animazioni nel file .air")
    print()

    # Mostra anteprima azioni trovate
    print("📋 Azioni trovate (preview):")
    for a in sorted(animations.keys()):
        display_name = ANIMATION_MAP.get(a, f"Action_{a:04d}")
        print(f"   Action {a:4d} → {display_name:20s} ({len(animations[a])} sprite)")
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

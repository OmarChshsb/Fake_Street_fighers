import os
import shutil
import re

# ============================================
# CONFIGURAZIONE
# ============================================

# Percorso del file .air
AIR_FILE = r"D:\atom_editor\python_game\assets\Characters\Hitto\Hitto(DBFZ).air"

# Cartella con i PNG estratti
SPRITES_FOLDER = r"D:\atom_editor\python_game\assets\Characters\Hitto\all_animation"

# Cartella di destinazione per le animazioni organizzate
OUTPUT_FOLDER = r"D:\atom_editor\python_game\assets\Characters\Hitto"

# Mappa le action numbers di MUGEN ai nomi delle tue animazioni
ANIMATION_MAP = {
    0: "Idle",           # Stand
    5: "Turn",           # Girando
    10: "CrouchDown",    # Agachandose
    11: "Crouch",        # Agachado
    12: "CrouchUp",      # Levantandose
    20: "WalkForward",   # Andando Hacia Adelante
    21: "WalkBackward",  # Andando Hacia Tras
    40: "JumpStart",     # Salto - Comienzo
    41: "JumpUp",        # Salto - En el Aire
    42: "JumpForward",   # Salto - En el Aire Alante
    43: "JumpBackward",  # Salto - En el Aire Atras
    44: "JumpFall",      # Salto - Callendo
    47: "JumpLand",      # Salto - En el Suelo
    100: "RunForward",   # Correr Alante
    105: "RunBackward",  # Correr Atras
    120: "GuardStart",   # Comienzo Guard Stand
    130: "Guard",        # Guard Stand
    200: "Attack1",      # A - 1
    210: "Attack2",      # A - 2
    220: "Attack3",      # A - 3
    300: "AttackB1",     # B - 1
    310: "AttackB2",     # B - 2
    320: "AttackB3",     # B - 3
    400: "AttackC",      # C
    600: "AirAttack1",   # A Aire 1
    610: "AirAttack2",   # A Aire 2
    620: "AirAttack3",   # B Aire 1
    630: "AirAttack4",   # B Aire 2
    650: "AirAttackC",   # C Air
}

# ============================================
# FUNZIONI
# ============================================

def parse_air_file(air_path):
    """
    Legge il file .air e estrae le animazioni
    
    Ritorna un dizionario:
    {
        action_number: [(group, index), (group, index), ...]
    }
    """
    animations = {}
    current_action = None
    
    print(f"📖 Leggendo file .air: {air_path}")
    
    try:
        with open(air_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                
                # Cerca [Begin Action X]
                if line.startswith('[Begin Action'):
                    match = re.search(r'\[Begin Action (\d+)\]', line)
                    if match:
                        current_action = int(match.group(1))
                        animations[current_action] = []
                
                # Cerca le righe degli sprite (formato: group,index, x,y, duration)
                elif current_action is not None and ',' in line:
                    # Ignora linee di commento e Clsn
                    if line.startswith(';') or line.startswith('Clsn') or line.startswith('Loop'):
                        continue
                    
                    # Ignora righe con -1 (sprite vuoto)
                    if line.startswith('-1'):
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 2:
                        try:
                            group = int(parts[0].strip())
                            index = int(parts[1].strip())
                            animations[current_action].append((group, index))
                        except ValueError:
                            # Non è una riga sprite valida, salta
                            continue
    except FileNotFoundError:
        print(f"❌ File .air non trovato: {air_path}")
        return None
    
    return animations


def organize_sprites(animations, sprites_folder, output_folder, animation_map):
    """
    Organizza i PNG nelle cartelle in base alle animazioni
    """
    # Crea la cartella di output se non esiste
    os.makedirs(output_folder, exist_ok=True)
    
    processed_sprites = set()  # Per evitare duplicati
    total_copied = 0
    
    for action_num in sorted(animations.keys()):
        sprites = animations[action_num]
        
        # Controlla se questa action è mappata a un'animazione
        if action_num not in animation_map:
            continue
        
        anim_name = animation_map[action_num]
        
        # Crea la cartella dell'animazione
        anim_folder = os.path.join(output_folder, anim_name)
        os.makedirs(anim_folder, exist_ok=True)
        
        print(f"\n📁 Organizzando: {anim_name} (Action {action_num})")
        
        frame_num = 0
        copied_in_this_anim = 0
        
        for group, index in sprites:
            sprite_key = (group, index)
            
            # Evita di copiare lo stesso sprite più volte nella stessa animazione
            # Ma permettiamo di usare lo stesso sprite in animazioni diverse
            
            # Nome del file PNG estratto (formato: "0 20 Hitto(DBFZ).png")
            # Cerchiamo tutti i file che matchano group e index
            found = False
            
            for filename in os.listdir(sprites_folder):
                if not filename.endswith('.png'):
                    continue
                
                # Estrai group e index dal nome file
                # Formato: "GROUP INDEX NomePersonaggio.png"
                parts = filename.split()
                if len(parts) >= 2:
                    try:
                        file_group = int(parts[0])
                        file_index = int(parts[1])
                        
                        if file_group == group and file_index == index:
                            source_path = os.path.join(sprites_folder, filename)
                            
                            # Nome del file di destinazione
                            dest_filename = f"frame_{frame_num:04d}.png"
                            dest_path = os.path.join(anim_folder, dest_filename)
                            
                            # Copia il file
                            shutil.copy2(source_path, dest_path)
                            print(f"   ✅ {filename} → {anim_name}/{dest_filename}")
                            
                            found = True
                            copied_in_this_anim += 1
                            total_copied += 1
                            frame_num += 1
                            break
                    except (ValueError, IndexError):
                        continue
            
            if not found:
                print(f"   ⚠️  Sprite non trovato: group={group}, index={index}")
        
        if copied_in_this_anim > 0:
            print(f"✅ {anim_name}: {copied_in_this_anim} frame copiati")
        else:
            print(f"❌ {anim_name}: Nessun frame trovato!")
    
    return total_copied


# ============================================
# ESECUZIONE
# ============================================

def main():
    print("="*60)
    print("🎮 ORGANIZZATORE AUTOMATICO SPRITE MUGEN")
    print("="*60)
    print()
    
    # Controlla che i file esistano
    if not os.path.exists(AIR_FILE):
        print(f"❌ File .air non trovato: {AIR_FILE}")
        return
    
    if not os.path.exists(SPRITES_FOLDER):
        print(f"❌ Cartella sprite non trovata: {SPRITES_FOLDER}")
        return
    
    # Conta i PNG
    png_files = [f for f in os.listdir(SPRITES_FOLDER) if f.endswith('.png')]
    print(f"📦 Trovati {len(png_files)} file PNG nella cartella")
    print()
    
    # Leggi il file .air
    animations = parse_air_file(AIR_FILE)
    
    if animations is None:
        return
    
    print(f"✅ Trovate {len(animations)} animazioni nel file .air")
    print()
    
    # Mostra le animazioni che verranno estratte
    print("📋 ANIMAZIONI DA ESTRARRE:")
    print("-" * 60)
    mapped_actions = {k: v for k, v in sorted(animations.items()) if k in ANIMATION_MAP}
    
    for action_num, sprites in mapped_actions.items():
        anim_name = ANIMATION_MAP[action_num]
        print(f"   Action {action_num:3d} → {anim_name:20s} ({len(sprites)} sprite)")
    
    print("-" * 60)
    print()
    
    # Chiedi conferma
    risposta = input("⏸️  Vuoi procedere con l'organizzazione? (s/n): ").strip().lower()
    
    if risposta != 's':
        print("❌ Operazione annullata.")
        return
    
    print()
    print("🚀 Inizio organizzazione...")
    print()
    
    # Organizza gli sprite
    total = organize_sprites(animations, SPRITES_FOLDER, OUTPUT_FOLDER, ANIMATION_MAP)
    
    print()
    print("="*60)
    print(f"✅ COMPLETATO! {total} file copiati in totale")
    print("="*60)
    print()
    print(f"📁 Le cartelle sono state create in: {OUTPUT_FOLDER}")
    print()


if __name__ == "__main__":
    main()
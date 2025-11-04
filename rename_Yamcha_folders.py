import os
import shutil
import re

def organize_from_all_animation(character_name):
    """
    Organizza PNG dalla cartella '_all_animation' in azioni separate.
    """
    
    all_anim_folder = f"assets/Characters/{character_name}/all_animation"
    base_path = f"assets/Characters/{character_name}"
    
    print(f"\n{'='*80}")
    print(f"🎨 ORGANIZZAZIONE - {character_name}")
    print(f"{'='*80}")
    print(f"📁 Input: {all_anim_folder}\n")
    
    # Verifica cartella
    if not os.path.exists(all_anim_folder):
        print(f"❌ Cartella non trovata: {all_anim_folder}")
        return False
    
    # Leggi PNG
    png_files = sorted([f for f in os.listdir(all_anim_folder) if f.lower().endswith('.png')])
    
    if not png_files:
        print(f"❌ Nessun PNG trovato!")
        return False
    
    print(f"✅ Trovati {len(png_files)} PNG\n")
    
    # Mapping standard MUGEN
    action_map = {
        0: "Idle",
        10: "Stand",
        20: "Crouch",
        21: "CrouchEnd",
        100: "JumpStart",
        101: "JumpUp",
        102: "JumpForward",
        103: "JumpBack",
        104: "JumpFall",
        105: "JumpLand",
        
        200: "Attack1",
        210: "Attack2",
        220: "Attack3",
        230: "AttackB1",
        240: "AttackB2",
        250: "AttackB3",
        260: "AttackC",
        
        300: "SpecialA",
        310: "SpecialB",
        320: "SpecialC",
        
        600: "AirAttack1",
        610: "AirAttack2",
        620: "AirAttack3",
        630: "AirAttack4",
        640: "AirAttackC",
    }
    
    # Organizza PNG per action ID
    organized = {}  # {action_id: [(frame_num, filename), ...]}
    
    for png_file in png_files:
        # Estrai numeri: "123_45.png" → [123, 45]
        numbers = re.findall(r'\d+', png_file)
        
        if len(numbers) >= 2:
            action_id = int(numbers[0])
            frame_num = int(numbers[1])
        elif len(numbers) == 1:
            action_id = int(numbers[0])
            frame_num = 0
        else:
            continue
        
        if action_id not in organized:
            organized[action_id] = []
        
        organized[action_id].append((frame_num, png_file))
    
    print(f"📊 Trovate {len(organized)} azioni\n")
    
    # Crea cartelle e sposta PNG
    created_folders = []
    
    for action_id in sorted(organized.keys()):
        # Nome azione
        action_name = action_map.get(action_id, f"Action{action_id}")
        
        # Crea cartella azione
        action_folder = os.path.join(base_path, action_name)
        os.makedirs(action_folder, exist_ok=True)
        created_folders.append(action_name)
        
        # Ordina frame
        frames = sorted(organized[action_id], key=lambda x: x[0])
        
        # Copia PNG
        for new_frame_idx, (orig_frame_num, png_file) in enumerate(frames):
            src = os.path.join(all_anim_folder, png_file)
            dst = os.path.join(action_folder, f"{new_frame_idx}.png")
            
            try:
                shutil.copy2(src, dst)
                print(f"✅ {action_name}/{new_frame_idx}.png  ({png_file})")
            except Exception as e:
                print(f"❌ Errore: {e}")
    
    print(f"\n{'='*80}")
    print(f"✅ FINITO! Organizzate {len(created_folders)} azioni")
    print(f"{'='*80}\n")
    
    for folder in sorted(created_folders):
        print(f"   📁 {folder}")
    
    print()
    return True


if __name__ == "__main__":
    print("\n🎮 ORGANIZZAZIONE NAPPA E FRIEZA\n")
    
    # Organizza Nappa
    organize_from_all_animation("Nappa")
    
    # Organizza Frieza
    organize_from_all_animation("Frieza")
    
    print("\n✅ FINITO! Sprite pronti per il gioco! 🎉\n")

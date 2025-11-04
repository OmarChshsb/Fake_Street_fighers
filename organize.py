import os
import shutil
import re

def auto_setup_frieza():
    """Legge i PNG da _all_animation usando il VERO Group dal .air"""
    
    base_path = "assets/Characters/Frieza"
    all_anim_path = os.path.join(base_path, "all_animation")
    mugen_path = "assets/mugen_chars/Frieza"
    
    print(f"\n{'='*80}")
    print(f"🔧 AUTO-SETUP FRIEZA")
    print(f"{'='*80}\n")
    
    # Leggi il .air per capire quali Group sono
    air_file = os.path.join(mugen_path, "Frieza.air")
    action_groups = {}  # {group_id: "azione"}
    
    with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            match = re.search(r'\[Begin Action\s+(\d+)\]', line)
            if match:
                action_id = int(match.group(1))
                action_groups[action_id] = f"Action{action_id}"
    
    print(f"✅ Trovate {len(action_groups)} azioni nel .air\n")
    
    # Leggi PNG
    png_files = sorted([f for f in os.listdir(all_anim_path) if f.endswith('.png')])
    
    # IMPORTANTE: Estrai il VERO Group (primo numero)
    organized = {}
    for png_file in png_files:
        # Es: "831_14_Frieza.png" → [831, 14]
        numbers = re.findall(r'\d+', png_file)
        if len(numbers) >= 2:
            group_id = int(numbers[0])  # ← IL VERO GROUP!
            frame_num = int(numbers[1])
            
            if group_id not in organized:
                organized[group_id] = []
            organized[group_id].append((frame_num, png_file))
    
    print(f"📊 Trovati {len(organized)} group nei PNG\n")
    
    # Crea cartelle
    for group_id in sorted(organized.keys()):
        folder_name = action_groups.get(group_id, f"Group{group_id}")
        new_folder = os.path.join(base_path, folder_name)
        os.makedirs(new_folder, exist_ok=True)
        
        frames = sorted(organized[group_id], key=lambda x: x[0])
        
        for new_idx, (_, png_file) in enumerate(frames):
            src = os.path.join(all_anim_path, png_file)
            dst = os.path.join(new_folder, f"{new_idx}.png")
            shutil.copy2(src, dst)
        
        print(f"✅ {folder_name}/ ({len(frames)} frame)")
    
    print(f"\n✅ FRIEZA ORGANIZZATA!\n")

if __name__ == "__main__":
    auto_setup_frieza()

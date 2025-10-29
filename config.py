import os
import json
from collections import defaultdict

def analyze_project_structure(base_path="."):
    """Analizza l'intera struttura del progetto."""
    
    analysis = {
        "project_root": base_path,
        "characters": {},
        "backgrounds": [],
        "other_assets": [],
        "python_files": [],
        "total_files": 0,
        "total_folders": 0
    }
    
    # Cerca file Python
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.py'):
                analysis["python_files"].append(os.path.join(root, file))
    
    # Analizza cartella assets
    assets_path = os.path.join(base_path, "assets")
    
    if os.path.exists(assets_path):
        # Analizza personaggi
        characters_path = os.path.join(assets_path, "Characters")
        if os.path.exists(characters_path):
            for character_name in os.listdir(characters_path):
                char_path = os.path.join(characters_path, character_name)
                if os.path.isdir(char_path):
                    char_data = {
                        "name": character_name,
                        "animations": {},
                        "total_sprites": 0
                    }
                    
                    # Analizza ogni cartella animazione
                    for anim_folder in sorted(os.listdir(char_path)):
                        anim_path = os.path.join(char_path, anim_folder)
                        if os.path.isdir(anim_path):
                            sprites = [f for f in os.listdir(anim_path) 
                                     if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                            char_data["animations"][anim_folder] = {
                                "frame_count": len(sprites),
                                "sprites": sorted(sprites)
                            }
                            char_data["total_sprites"] += len(sprites)
                            analysis["total_files"] += len(sprites)
                    
                    analysis["characters"][character_name] = char_data
                    analysis["total_folders"] += len(char_data["animations"])
        
        # Analizza backgrounds
        bg_path = os.path.join(assets_path, "Background")
        if os.path.exists(bg_path):
            backgrounds = [f for f in os.listdir(bg_path) 
                         if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            analysis["backgrounds"] = backgrounds
            analysis["total_files"] += len(backgrounds)
    
    return analysis


def generate_report(analysis):
    """Genera report completo come stringa."""
    
    lines = []
    
    lines.append("=" * 80)
    lines.append("ANALISI STRUTTURA PROGETTO FAKE_FIGHTERS")
    lines.append("=" * 80)
    lines.append("")
    
    # File Python
    lines.append("FILE PYTHON TROVATI:")
    lines.append("-" * 80)
    if analysis["python_files"]:
        for py_file in analysis["python_files"]:
            lines.append(f"  • {py_file}")
    else:
        lines.append("  Nessun file Python trovato nella directory")
    lines.append("")
    
    # Backgrounds
    lines.append("BACKGROUNDS:")
    lines.append("-" * 80)
    if analysis["backgrounds"]:
        for bg in analysis["backgrounds"]:
            lines.append(f"  • {bg}")
    else:
        lines.append("  Nessun background trovato")
    lines.append("")
    
    # Personaggi
    lines.append("PERSONAGGI E ANIMAZIONI:")
    lines.append("=" * 80)
    
    if not analysis["characters"]:
        lines.append("Nessun personaggio trovato in assets/Characters/")
        lines.append("")
    else:
        for char_name, char_data in analysis["characters"].items():
            lines.append("")
            lines.append(f"{char_name.upper()}")
            lines.append(f"   Total Sprites: {char_data['total_sprites']}")
            lines.append(f"   Total Animations: {len(char_data['animations'])}")
            lines.append("-" * 80)
            
            # Categorizza animazioni
            categories = {
                "Movement": [],
                "Jump": [],
                "Attack": [],
                "Special": [],
                "Status": [],
                "Other": []
            }
            
            for anim_name, anim_data in sorted(char_data["animations"].items()):
                frame_count = anim_data["frame_count"]
                
                # Categorizza
                anim_lower = anim_name.lower()
                if any(x in anim_lower for x in ["idle", "walk", "run", "dash", "crouch"]):
                    categories["Movement"].append((anim_name, frame_count))
                elif any(x in anim_lower for x in ["jump", "fall", "land", "air"]):
                    categories["Jump"].append((anim_name, frame_count))
                elif any(x in anim_lower for x in ["attack", "punch", "kick", "hit"]):
                    categories["Attack"].append((anim_name, frame_count))
                elif any(x in anim_lower for x in ["special", "kamehameha", "wolf", "sokidan", "super", "ki", "blast"]):
                    categories["Special"].append((anim_name, frame_count))
                elif any(x in anim_lower for x in ["hurt", "guard", "down", "stun", "intro", "win", "lose", "taunt"]):
                    categories["Status"].append((anim_name, frame_count))
                else:
                    categories["Other"].append((anim_name, frame_count))
            
            # Stampa per categoria
            for category, anims in categories.items():
                if anims:
                    lines.append(f"\n  [{category}]")
                    for anim_name, frame_count in anims:
                        lines.append(f"    • {anim_name:<35} ({frame_count} frames)")
    
    lines.append("")
    lines.append("=" * 80)
    lines.append("STATISTICHE TOTALI:")
    lines.append("-" * 80)
    lines.append(f"  • Personaggi: {len(analysis['characters'])}")
    lines.append(f"  • Cartelle totali: {analysis['total_folders']}")
    lines.append(f"  • File totali: {analysis['total_files']}")
    lines.append(f"  • File Python: {len(analysis['python_files'])}")
    lines.append("=" * 80)
    lines.append("")
    
    return "\n".join(lines)


def check_missing_animations(analysis):
    """Controlla animazioni mancanti importanti."""
    
    lines = []
    lines.append("CONTROLLO ANIMAZIONI ESSENZIALI:")
    lines.append("=" * 80)
    
    essential_anims = {
        "Movement": ["Idle", "WalkForward", "WalkBackward"],
        "Jump": ["JumpUp", "JumpFall", "JumpLand"],
        "Combat": ["Hurt", "Guard", "Attack1"],
    }
    
    for char_name, char_data in analysis["characters"].items():
        lines.append(f"\n{char_name}:")
        char_anims = [a.lower() for a in char_data["animations"].keys()]
        
        for category, required in essential_anims.items():
            lines.append(f"  [{category}]")
            for anim in required:
                found = any(anim.lower() in ca for ca in char_anims)
                status = "OK" if found else "MANCA"
                lines.append(f"    {status:6} {anim}")
    
    lines.append("")
    return "\n".join(lines)


def save_detailed_analysis(analysis, filename="project_analysis_detailed.txt"):
    """Salva analisi dettagliata con lista completa sprite."""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("ANALISI DETTAGLIATA PROGETTO FAKE_FIGHTERS\n")
        f.write("Lista completa di tutti gli sprite\n")
        f.write("=" * 80 + "\n\n")
        
        # Personaggi dettagliati
        for char_name, char_data in analysis["characters"].items():
            f.write(f"\n{'=' * 80}\n")
            f.write(f"{char_name.upper()} - {char_data['total_sprites']} sprites totali\n")
            f.write(f"{'=' * 80}\n")
            
            for anim_name, anim_data in sorted(char_data["animations"].items()):
                f.write(f"\n{anim_name} ({anim_data['frame_count']} frames):\n")
                for sprite in anim_data["sprites"]:
                    f.write(f"  - {sprite}\n")


if __name__ == "__main__":
    print("Avvio analisi progetto...")
    
    # Esegui analisi
    analysis = analyze_project_structure()
    
    # Genera report
    report = generate_report(analysis)
    missing = check_missing_animations(analysis)
    
    # Salva report principale
    output_file = "project_analysis.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
        f.write("\n\n")
        f.write(missing)
    
    print(f"\n✅ Report salvato in: {output_file}")
    
    # Salva analisi dettagliata
    detailed_file = "project_analysis_detailed.txt"
    save_detailed_analysis(analysis, detailed_file)
    print(f"✅ Analisi dettagliata salvata in: {detailed_file}")
    
    # Stampa sommario nel terminale
    print("\n" + "=" * 80)
    print("SOMMARIO:")
    print("-" * 80)
    print(f"Personaggi trovati: {len(analysis['characters'])}")
    for char_name, char_data in analysis["characters"].items():
        print(f"  - {char_name}: {len(char_data['animations'])} animazioni, {char_data['total_sprites']} sprites")
    print("\n✅ Analisi completata! Controlla i file .txt generati")
    print("=" * 80)

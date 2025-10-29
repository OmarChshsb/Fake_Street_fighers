import os
from PIL import Image

def analyze_hp_bar_sprites(folder_path="assets/Items/Hp_bar"):
    """
    Analizza tutti i PNG nella cartella HP bar e mostra info dettagliate.
    """
    
    print("="*80)
    print("🔍 ANALISI SPRITE HP BAR")
    print("="*80)
    print(f"📁 Cartella: {folder_path}\n")
    
    # Verifica esistenza cartella
    if not os.path.exists(folder_path):
        print(f"❌ ERRORE: Cartella non trovata!")
        print(f"   Percorso cercato: {os.path.abspath(folder_path)}")
        print("\n💡 SUGGERIMENTO:")
        print("   Crea la cartella: mkdir -p assets/item/Hp_bar")
        print("   E metti dentro i PNG estratti da fight.sff")
        input("\nPremi INVIO per chiudere...")
        return
    
    # Trova tutti i PNG
    png_files = []
    for file in os.listdir(folder_path):
        if file.lower().endswith('.png'):
            png_files.append(file)
    
    if not png_files:
        print("❌ NESSUN FILE PNG TROVATO!")
        print(f"\n📂 Contenuto cartella:")
        for item in os.listdir(folder_path):
            print(f"   - {item}")
        input("\nPremi INVIO per chiudere...")
        return
    
    # Ordina file
    png_files.sort()
    
    print(f"✅ Trovati {len(png_files)} file PNG\n")
    print("="*80)
    print("📊 DETTAGLI SPRITE")
    print("="*80)
    print(f"{'#':<4} {'Nome File':<30} {'Dimensioni':<15} {'Group':<8} {'Index':<6}")
    print("-"*80)
    
    # Analizza ogni file
    sprite_map = {}
    
    for i, filename in enumerate(png_files, 1):
        filepath = os.path.join(folder_path, filename)
        
        try:
            # Carica immagine per ottenere dimensioni
            img = Image.open(filepath)
            width, height = img.size
            size_str = f"{width}x{height}"
            
            # Estrai group e index dal nome file
            # Formati comuni: "100_1.png", "11-0.png", "group_index.png"
            import re
            numbers = re.findall(r'\d+', filename)
            
            if len(numbers) >= 2:
                group = int(numbers[0])
                index = int(numbers[1])
                sprite_map[(group, index)] = filename
                group_str = str(group)
                index_str = str(index)
            else:
                group_str = "?"
                index_str = "?"
            
            print(f"{i:<4} {filename:<30} {size_str:<15} {group_str:<8} {index_str:<6}")
            
        except Exception as e:
            print(f"{i:<4} {filename:<30} {'ERROR':<15} {'?':<8} {'?':<6}")
            print(f"     ⚠️ Errore: {e}")
    
    print("="*80)
    
    # Mappa sprite necessari da fight.def
    print("\n📋 SPRITE NECESSARI (da fight.def)")
    print("="*80)
    
    needed_sprites = {
        # HP Bar
        (100, 1): "Background HP bar (frame)",
        (11, 0): "P1 HP bar vuota",
        (11, 1): "P2 HP bar vuota",
        (12, 0): "P1 HP bar damage (rossa)",
        (12, 1): "P2 HP bar damage (rossa)",
        (13, 0): "P1 HP bar piena (gialla/verde)",
        (13, 1): "P2 HP bar piena (gialla/verde)",
        
        # Power Bar
        (21, 1): "P1 Power bar background",
        (22, 1): "P2 Power bar background",
        (23, 0): "P1 Power bar front",
        (23, 1): "P2 Power bar front",
        (52, 1): "Power bar mid",
        
        # Face (opzionali)
        (50, 0): "P1 Face frame",
        (51, 0): "P2 Face frame",
        
        # WinIcon (opzionali)
        (24, 0): "Win icon",
    }
    
    print(f"{'Group':<8} {'Index':<8} {'Status':<10} {'Descrizione':<40}")
    print("-"*80)
    
    found_count = 0
    missing_count = 0
    
    for (group, index), description in sorted(needed_sprites.items()):
        if (group, index) in sprite_map:
            status = "✅ Trovato"
            filename = sprite_map[(group, index)]
            found_count += 1
        else:
            status = "❌ Mancante"
            filename = "-"
            missing_count += 1
        
        print(f"{group:<8} {index:<8} {status:<10} {description:<40}")
        if status == "✅ Trovato":
            print(f"         → {filename}")
    
    print("="*80)
    print(f"\n📊 RIEPILOGO:")
    print(f"   ✅ Sprite trovati: {found_count}/{len(needed_sprites)}")
    print(f"   ❌ Sprite mancanti: {missing_count}/{len(needed_sprites)}")
    
    if missing_count == 0:
        print("\n🎉 PERFETTO! Hai tutti gli sprite necessari!")
    else:
        print(f"\n⚠️  Mancano {missing_count} sprite importanti")
        print("   Estrai tutti gli sprite da fight.sff usando Fighter Factory")
    
    # Genera codice Python per caricare sprite
    print("\n" + "="*80)
    print("💻 CODICE PYTHON GENERATO")
    print("="*80)
    print("\n# Mappa sprite disponibili:")
    print("SPRITE_MAP = {")
    for (group, index), filename in sorted(sprite_map.items()):
        print(f'    ({group}, {index}): "{filename}",')
    print("}")
    
    print("\n" + "="*80)
    
    # Salva report su file
    report_path = "hp_bar_analysis.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("ANALISI SPRITE HP BAR\n")
        f.write("="*80 + "\n\n")
        f.write(f"Cartella analizzata: {folder_path}\n")
        f.write(f"Totale PNG trovati: {len(png_files)}\n\n")
        
        f.write("SPRITE DISPONIBILI:\n")
        f.write("-"*80 + "\n")
        for (group, index), filename in sorted(sprite_map.items()):
            f.write(f"Group {group}, Index {index}: {filename}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("SPRITE NECESSARI:\n")
        f.write("-"*80 + "\n")
        for (group, index), description in sorted(needed_sprites.items()):
            status = "TROVATO" if (group, index) in sprite_map else "MANCANTE"
            f.write(f"[{status}] Group {group}, Index {index}: {description}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write(f"Trovati: {found_count}/{len(needed_sprites)}\n")
        f.write(f"Mancanti: {missing_count}/{len(needed_sprites)}\n")
    
    print(f"\n📄 Report salvato in: {report_path}")
    print("="*80)
    
    input("\nPremi INVIO per chiudere...")


if __name__ == "__main__":
    analyze_hp_bar_sprites()

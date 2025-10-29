from PIL import Image
import os

def normalize_all_animations(character_path):
    """
    Normalizza TUTTE le animazioni di un personaggio.
    Aggiunge padding trasparente per uniformare dimensioni.
    """
    print(f"\n{'='*70}")
    print(f"🎮 NORMALIZZAZIONE: {os.path.basename(character_path)}")
    print('='*70)
    
    # Trova tutte le cartelle animazioni
    try:
        animation_folders = [
            f for f in os.listdir(character_path) 
            if os.path.isdir(os.path.join(character_path, f)) 
            and not f.startswith('.')
        ]
    except Exception as e:
        print(f"❌ Errore lettura cartella: {e}")
        return 0
    
    if not animation_folders:
        print("❌ Nessuna cartella animazione trovata!")
        return 0
    
    print(f"📊 Trovate {len(animation_folders)} cartelle animazione")
    total_normalized = 0
    
    for anim_folder in sorted(animation_folders):
        folder_path = os.path.join(character_path, anim_folder)
        
        # Trova tutti i PNG
        try:
            png_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]
        except:
            continue
        
        if not png_files:
            continue
        
        print(f"\n📁 {anim_folder} ({len(png_files)} frame)")
        
        # Carica tutte le immagini
        images = []
        paths = []
        
        for file in sorted(png_files):
            path = os.path.join(folder_path, file)
            try:
                img = Image.open(path).convert('RGBA')
                images.append(img)
                paths.append(path)
            except Exception as e:
                print(f"   ⚠️  Errore {file}: {e}")
        
        if not images:
            print(f"   ❌ Nessuna immagine caricabile")
            continue
        
        # Trova dimensioni massime
        max_height = max(img.height for img in images)
        max_width = max(img.width for img in images)
        
        # Normalizza ogni frame
        normalized = 0
        for img, path in zip(images, paths):
            # Salta se già della dimensione giusta
            if img.height == max_height and img.width == max_width:
                continue
            
            # Crea nuova immagine con dimensioni massime
            new_img = Image.new('RGBA', (max_width, max_height), (0, 0, 0, 0))
            
            # Posiziona immagine originale:
            # - Centro orizzontalmente
            # - Allinea bottom verticalmente (piedi sempre in basso)
            x_offset = (max_width - img.width) // 2
            y_offset = max_height - img.height
            
            new_img.paste(img, (x_offset, y_offset))
            
            # Salva
            new_img.save(path)
            normalized += 1
        
        # Report
        if normalized > 0:
            print(f"   ✅ Normalizzati {normalized}/{len(images)} frame → {max_width}x{max_height}px")
            total_normalized += normalized
        else:
            print(f"   ⏭️  Già uniformi ({max_width}x{max_height}px)")
    
    return total_normalized


def main():
    """Funzione principale."""
    print("\n" + "="*70)
    print("🎨 NORMALIZZATORE SPRITE FIGHTING GAME")
    print("="*70)
    print("\nQuesto script uniformerà le dimensioni di tutti gli sprite")
    print("per risolvere il problema dei piedi che galleggiano/affondano.\n")
    
    # Percorso base
    base_path = os.path.join("assets", "Characters")
    
    if not os.path.exists(base_path):
        print(f"❌ ERRORE: Cartella non trovata: {base_path}")
        print("   Assicurati di eseguire lo script dalla cartella del progetto!")
        input("\nPremi INVIO per chiudere...")
        return
    
    # Trova personaggi
    characters = []
    try:
        for item in os.listdir(base_path):
            item_path = os.path.join(base_path, item)
            if os.path.isdir(item_path):
                characters.append(item)
    except Exception as e:
        print(f"❌ Errore: {e}")
        input("\nPremi INVIO per chiudere...")
        return
    
    if not characters:
        print(f"❌ Nessun personaggio trovato in {base_path}")
        input("\nPremi INVIO per chiudere...")
        return
    
    print(f"📋 Personaggi trovati: {', '.join(characters)}\n")
    
    risposta = input("⏸️  Procedere con la normalizzazione? (s/n): ").strip().lower()
    
    if risposta != 's':
        print("❌ Operazione annullata.")
        input("\nPremi INVIO per chiudere...")
        return
    
    # Normalizza ogni personaggio
    grand_total = 0
    
    for char in characters:
        char_path = os.path.join(base_path, char)
        total = normalize_all_animations(char_path)
        grand_total += total
    
    # Report finale
    print("\n" + "="*70)
    print("🎉 NORMALIZZAZIONE COMPLETATA!")
    print("="*70)
    print(f"✅ Totale frame normalizzati: {grand_total}")
    print("\n📝 PROSSIMI PASSI:")
    print("   1. Esegui il gioco")
    print("   2. I personaggi dovrebbero stare sul pavimento!")
    print("   3. Se vedi ancora problemi, contattami")
    print("="*70)
    
    input("\nPremi INVIO per chiudere...")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Setup minimalista: crea la struttura cartelle
senza bisogno di estrarre sprite
"""
import os
import re
from pathlib import Path

def setup_character(char_name):
    """Prepara cartella character con sottocartelle vuote"""
    print(f"\n🔧 Setup {char_name}...")
    
    # Cartelle da creare
    char_dir = Path("assets") / "Characters" / char_name
    char_dir.mkdir(parents=True, exist_ok=True)
    
    # Leggi .air per sapere quante azioni ci sono
    air_file = Path("assets/mugen_chars") / char_name / f"{char_name}.air"
    
    if not air_file.exists():
        print(f"  ⚠️  {air_file} non trovato, creo struttura generica...")
        # Crea cartelle generiche
        for i in range(0, 1000, 100):
            (char_dir / f"Action{i}").mkdir(exist_ok=True)
        return
    
    # Leggi .air
    actions = {}
    with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            match = re.search(r'\[Begin Action\s+(\d+)\]', line)
            if match:
                action_id = int(match.group(1))
                actions[action_id] = f"Action{action_id}"
    
    # Crea cartelle per ogni azione
    for action_id in sorted(actions.keys()):
        action_dir = char_dir / f"Action{action_id}"
        action_dir.mkdir(exist_ok=True)
        print(f"  ✓ {action_dir.name}")
    
    print(f"  ✅ {char_name} pronto ({len(actions)} azioni)")

def main():
    chars = ["Frieza", "Hitto", "Nappa", "Yamcha"]
    
    for char in chars:
        setup_character(char)
    
    print("\n✅ Setup completato!")
    print("Ora puoi eseguire il gioco: python main.py")

if __name__ == "__main__":
    main()

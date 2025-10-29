import os
import shutil

# ============================================
# CONFIGURAZIONE
# ============================================

YAMCHA_PATH = r"D:\atom_editor\python_game\assets\Characters\Yamcha"

# MAPPING DEFINITIVO BASATO SU CNS + FRAME COUNT
RENAME_MAP = {
    # ===== ATTACCHI IMPORTANTI (Questi ti servono!) =====
    "Action_0224": "Attack4",         # 23 frame - Multi-hit barrage (Light combo finale)
    "Action_0323": "Attack5",         # 38 frame - Launcher potente!
    
    "Action_0300": "AttackB1",        # 10 frame - Medium Kick 1 (quello che cercavi!)
    "Action_0310": "AttackB2",        # 4 frame - Medium Kick 2
    "Action_0321": "AttackB3",        # 23 frame - Medium Kick 3
    "Action_0332": "AttackB4",        # 27 frame - Multi-hit barrage
    
    # ===== CROUCH ATTACKS =====
    "Action_0123": "CrouchKick2",     # 11 frame - Crouch kick alternativo
    "Action_0360": "CrouchAttackHeavy", # 10 frame
    
    # ===== SPECIAL ATTACKS & PROJECTILES =====
    "Action_0415": "KiBlastAir",      # 5 frame - Ki blast aereo
    "Action_0550": "KiCharge1",       # 3 frame - Carica ki
    "Action_0554": "KiCharge2",       # 6 frame - Carica ki avanzata
    
    # ===== DASH VARIATIONS =====
    "Action_0705": "DashForward",     # 3 frame
    "Action_0710": "DashBack",        # 3 frame
    "Action_0715": "DashUp",          # 3 frame - Super dash up
    
    # ===== TAUNT & INTRO =====
    "Action_0848": "Taunt",           # 7 frame
    "Action_1800": "IntroAlt",        # 5 frame - Intro alternativa
    "Action_1801": "IntroEffect2",    # 4 frame
    
    # ===== SPECIAL EFFECTS =====
    "Action_2255": "SpecialEffect1",  # 1 frame
    "Action_3000": "TransformStart",  # 6 frame
    "Action_3131": "PowerUpLong",     # 11 frame - Power up lungo
    
    # ===== HIT REACTIONS EXTRA =====
    "Action_5005": "HitMedium",       # 1 frame
    "Action_5006": "HitHeavy",        # 1 frame
    "Action_5007": "HitSuper",        # 1 frame
    "Action_5012": "HitLowMedium2",   # 1 frame
    "Action_5015": "HitCrouchLight",  # 1 frame
    "Action_5016": "HitCrouchMedium", # 1 frame
    "Action_5017": "HitCrouchHeavy",  # 1 frame
    "Action_5021": "HitBackLight",    # 1 frame
    "Action_5022": "HitBackMedium",   # 1 frame
    "Action_5025": "HitAirLight",     # 1 frame
    "Action_5026": "HitAirMedium",    # 1 frame
    "Action_5027": "HitAirHeavy",     # 1 frame
    "Action_5035": "HitTrip2",        # 1 frame
    "Action_5051": "AirFallRotate",   # 1 frame
    "Action_5052": "AirFallSpin",     # 1 frame
    "Action_5061": "AirDownFall",     # 1 frame
    "Action_5062": "AirDownBounce",   # 2 frame
    "Action_5090": "HitLieDownHit",   # 1 frame
    "Action_5120": "HitGetUpSlow",    # 8 frame
    "Action_5150": "HitWallBounce",   # 1 frame
    "Action_5160": "HitGroundBounce", # 1 frame
    "Action_5170": "HitCeilingBounce",# 1 frame
    "Action_5300": "HitComboLong",    # 12 frame - Colpito da combo lunga
    
    # ===== SUPER MOVES (7000 series) =====
    "Action_7006": "SuperPrep1",      # 5 frame
    "Action_7007": "SuperPrep2",      # 5 frame
    "Action_7011": "SuperFlash1",     # 5 frame - Flash super
    "Action_7012": "SuperFlash2",     # 15 frame
    "Action_7013": "SuperEffect1",    # 4 frame
    "Action_7014": "SuperEffect2",    # 3 frame
    "Action_7015": "SuperEffect3",    # 3 frame
    "Action_7018": "SuperKamehamehaFull", # 46 frame - Kamehameha completo!
    "Action_7019": "SuperWolfFangFull",   # 43 frame - Wolf Fang Fist completo!
    "Action_7020": "SuperSokidanFull",    # 50 frame - Spirit Ball completo!
    "Action_7022": "SuperEnd1",       # 11 frame
    "Action_7025": "SuperImpact",     # 5 frame - Impact effect
    "Action_7027": "SuperBeamCharge", # 9 frame
    "Action_7028": "SuperBeamFire",   # 4 frame
    "Action_7029": "SuperRush",       # 15 frame - Rush super
    "Action_7030": "SuperFinisher",   # 30 frame - Finisher cinematico!
    "Action_7031": "SuperRecovery",   # 8 frame
    "Action_7037": "SuperEmpty",      # 0 frame - Placeholder
    "Action_7038": "SuperTransition", # 4 frame
    "Action_7039": "SuperExplosion",  # 10 frame
}

# ============================================
# FUNZIONE RINOMINA
# ============================================

def rename_folders(base_path, rename_map, dry_run=True):
    """Rinomina le cartelle Action_XXXX."""
    renamed_count = 0
    errors = []
    
    if not os.path.exists(base_path):
        print(f"❌ Cartella non trovata: {base_path}")
        return
    
    print("="*80)
    if dry_run:
        print("🔍 MODALITÀ TEST - Simulazione")
    else:
        print("🚀 MODALITÀ ESECUZIONE - Rinomina reale!")
    print("="*80)
    print()
    
    # Categorizza per tipo
    attacks = []
    specials = []
    hits = []
    supers = []
    others = []
    
    for old_name, new_name in sorted(rename_map.items()):
        old_path = os.path.join(base_path, old_name)
        new_path = os.path.join(base_path, new_name)
        
        if not os.path.exists(old_path):
            continue
        
        if os.path.exists(new_path):
            continue
        
        # Categorizza
        if 'Attack' in new_name and 'Hit' not in new_name:
            attacks.append((old_name, new_name))
        elif 'Super' in new_name or '7' in old_name:
            supers.append((old_name, new_name))
        elif 'Hit' in new_name or '5' in old_name:
            hits.append((old_name, new_name))
        elif any(x in new_name for x in ['Dash', 'Ki', 'Special']):
            specials.append((old_name, new_name))
        else:
            others.append((old_name, new_name))
    
    # Mostra attacchi (PRIORITÀ ALTA)
    if attacks:
        print("👊 ATTACCHI (IMPORTANTE!):")
        print("-"*80)
        for old, new in attacks:
            if dry_run:
                print(f"   📝 {old:25s} → {new}")
                renamed_count += 1
            else:
                try:
                    shutil.move(os.path.join(base_path, old), os.path.join(base_path, new))
                    print(f"   ✅ {old:25s} → {new}")
                    renamed_count += 1
                except Exception as e:
                    print(f"   ❌ {old}: {e}")
                    errors.append((old, e))
        print()
    
    # Mostra speciali
    if specials:
        print("⚡ SPECIALI:")
        print("-"*80)
        for old, new in specials:
            if dry_run:
                print(f"   📝 {old:25s} → {new}")
                renamed_count += 1
            else:
                try:
                    shutil.move(os.path.join(base_path, old), os.path.join(base_path, new))
                    print(f"   ✅ {old:25s} → {new}")
                    renamed_count += 1
                except Exception as e:
                    print(f"   ❌ {old}: {e}")
                    errors.append((old, e))
        print()
    
    # Mostra super (7000 series)
    if supers:
        print("💥 SUPER MOSSE (7000 series):")
        print("-"*80)
        for old, new in supers:
            if dry_run:
                print(f"   📝 {old:25s} → {new}")
                renamed_count += 1
            else:
                try:
                    shutil.move(os.path.join(base_path, old), os.path.join(base_path, new))
                    print(f"   ✅ {old:25s} → {new}")
                    renamed_count += 1
                except Exception as e:
                    print(f"   ❌ {old}: {e}")
                    errors.append((old, e))
        print()
    
    # Hit reactions (comprimi output)
    if hits:
        print(f"💢 HIT REACTIONS: {len(hits)} animazioni (compresso)")
        if not dry_run:
            for old, new in hits:
                try:
                    shutil.move(os.path.join(base_path, old), os.path.join(base_path, new))
                    renamed_count += 1
                except Exception as e:
                    errors.append((old, e))
        else:
            renamed_count += len(hits)
        print()
    
    # Altri
    if others:
        print("🎭 ALTRO:")
        print("-"*80)
        for old, new in others:
            if dry_run:
                print(f"   📝 {old:25s} → {new}")
                renamed_count += 1
            else:
                try:
                    shutil.move(os.path.join(base_path, old), os.path.join(base_path, new))
                    print(f"   ✅ {old:25s} → {new}")
                    renamed_count += 1
                except Exception as e:
                    print(f"   ❌ {old}: {e}")
                    errors.append((old, e))
        print()
    
    # Report
    print("="*80)
    print(f"✅ Cartelle da rinominare: {renamed_count}")
    if errors:
        print(f"❌ Errori: {len(errors)}")
    print("="*80)
    
    if dry_run:
        print("\n💡 TEST COMPLETATO! Esegui con dry_run=False per rinominare.")
    else:
        print("\n🎉 RINOMINA COMPLETATA!")

# ============================================
# ESECUZIONE
# ============================================

def main():
    print("="*80)
    print("🎮 SCRIPT RINOMINA YAMCHA - MAPPING DEFINITIVO")
    print("="*80)
    print()
    
    risposta = input("⏸️  Vuoi vedere la SIMULAZIONE? (s/n): ").strip().lower()
    
    if risposta == 's':
        print("\n🔍 Simulazione...\n")
        rename_folders(YAMCHA_PATH, RENAME_MAP, dry_run=True)
        
        conferma = input("\n✅ Procedere con rinomina REALE? (s/n): ").strip().lower()
        if conferma == 's':
            print("\n🚀 Rinomina reale...\n")
            rename_folders(YAMCHA_PATH, RENAME_MAP, dry_run=False)
        else:
            print("❌ Annullato.")
    else:
        conferma = input("⚠️  Rinominare SUBITO? (s/n): ").strip().lower()
        if conferma == 's':
            rename_folders(YAMCHA_PATH, RENAME_MAP, dry_run=False)
        else:
            print("❌ Annullato.")

if __name__ == "__main__":
    main()

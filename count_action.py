



def count_actions_in_air(filename):
    """Conta quanti [Begin Action XXX] ci sono."""
    count = 0
    actions = []
    
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            # Cerca "[Begin Action"
            if line.startswith('[Begin Action'):

                parts = line.split()
                # Estrai il numero
                # Es: "[Begin Action 200]" → 200
                for part in parts:
                    cleaned = ''.join(filter(str.isdigit, part))
                    if cleaned:
                        number = int(cleaned)


                # SCRIVI TU IL CODICE QUI! 🧠
                # Hint: usa .split() e prendi la parte giusta
                
                action_num = number  # COMPLETA TU
                actions.append(action_num)
                count += 1
    
    return count, actions

# Testa sui tuoi file
hitto_count, hitto_actions = count_actions_in_air("assets/mugen_chars/Hitto/Hitto(DBFZ).air")
yamcha_count, yamcha_actions = count_actions_in_air("assets/mugen_chars/Yamcha/Yamcha.air")

print(f"Hitto: {hitto_count} azioni - Numeri: {hitto_actions[:20]}...")
print(f"Yamcha: {yamcha_count} azioni - Numeri: {yamcha_actions[:20]}...")

"""Parser per file MUGEN .air (animazioni)."""

from pathlib import Path
from typing import Dict, List
from .data_models import CollisionBox, SpriteFrame, ActionData

class AirParser:
    """Parsa un file .air MUGEN e estrae le azioni."""
    
    def __init__(self, air_file_path: str):
        """
        Inizializza il parser.
        
        Args:
            air_file_path: Percorso al file .air (es: "assets/mugen_chars/Hitto/Hitto.air")
        """
        self.air_path = Path(air_file_path)
        self.actions: Dict[int, ActionData] = {}
    
    def parse(self) -> Dict[int, ActionData]:
        """
        Parsa il file .air e ritorna le azioni.
        
        Returns:
            Dict[action_id, ActionData]
        """
        
        with open(self.air_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        current_action = None
        current_hurtbox = None  # Clsn2Default applicato a tutti i frame
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Salta linee vuote e commenti
            if not line or line.startswith(';'):
                continue
            
            # Nuova azione
            if line.startswith('[Begin Action'):
                action_id = self._extract_action_id(line)
                current_action = ActionData(action_id=action_id)
                self.actions[action_id] = current_action
                current_hurtbox = None
            
            # Hurtbox default per questa azione
            elif line.startswith('Clsn2Default:'):
                # Es: "Clsn2Default: 1"
                # Significa che il prossimo Clsn2[0] è applicato a tutti i frame
                pass  # Lo gestiremo quando incontriamo "Clsn2"
            
            # Hurtbox specifica
            elif line.startswith('Clsn2['):
                # Es: "Clsn2[0] = -60, -399, 76, -9"
                current_hurtbox = self._parse_collision_box(line)
            
            # Hitbox specifica
            elif line.startswith('Clsn1['):
                # Es: "Clsn1[0] = 77, -345, 303, -202"
                hitbox = self._parse_collision_box(line)
                # Applica a tutti i frame seguenti finché non cambia
            
            # Frame sprite
            elif ',' in line and not line.startswith('[') and not line.startswith('Clsn'):
                # Es: "200,166, 0,0, 3"
                frame = self._parse_sprite_frame(line, current_action.action_id, current_hurtbox)
                if frame:
                    current_action.frames.append(frame)
        
        return self.actions
    
    @staticmethod
    def _extract_action_id(line: str) -> int:
        """Estrae il numero dall'azione. Es: '[Begin Action 200]' → 200."""
        parts = line.split()
        for part in parts:
            cleaned = ''.join(filter(str.isdigit, part))
            if cleaned:
                return int(cleaned)
        return 0
    
    @staticmethod
    def _parse_collision_box(line: str) -> CollisionBox:
        """Parsa una collision box. Es: 'Clsn2[0] = -60, -399, 76, -9'."""
        # Estrai la parte dopo "="
        coords_str = line.split('=')[1].strip()
        coords = [int(x.strip()) for x in coords_str.split(',')]
        return CollisionBox(coords[0], coords[1], coords[2], coords[3])
    
    @staticmethod
    def _parse_sprite_frame(line: str, action_id: int, hurtbox: CollisionBox = None) -> SpriteFrame:
        """Parsa un frame sprite. Es: '200,166, 0,0, 3'."""
        try:
            parts = [x.strip() for x in line.split(',')]
            if len(parts) < 5:
                return None
            
            sprite_x = int(parts[0])    # 200 (quale spritesheet)
            sprite_y = int(parts[1])    # 166 (quale frame nello spritesheet)
            offset_x = int(parts[2])    # 0 (offset X)
            offset_y = int(parts[3])    # 0 (offset Y)
            duration = int(parts[4])    # 3 (quanti frame dura)
            
            return SpriteFrame(
                action_id=action_id,
                sprite_index=sprite_y,
                offset_x=offset_x,
                offset_y=offset_y,
                duration=duration,
                hurtbox=hurtbox
            )
        except (ValueError, IndexError):
            return None


# Test
if __name__ == "__main__":
    # Per Hitto
    parser_hitto = AirParser("assets/mugen_chars/Hitto/Hitto(DBFZ).air")
    actions_hitto = parser_hitto.parse()
    print(f"✅ Hitto: Caricate {len(actions_hitto)} azioni")
    
    # Per Yamcha
    parser_yamcha = AirParser("assets/mugen_chars/Yamcha/Yamcha.air")
    actions_yamcha = parser_yamcha.parse()
    print(f"✅ Yamcha: Caricate {len(actions_yamcha)} azioni")
    
    # Mostra i primi 10 numeri di azioni di Hitto
    for action_id in sorted(actions_hitto.keys())[:10]:
        action = actions_hitto[action_id]
        print(f"  Action {action_id}: {len(action.frames)} frames")

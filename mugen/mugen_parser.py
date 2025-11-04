from dataclasses import dataclass
from typing import Dict, List, Tuple
from pathlib import Path

@dataclass
class CollisionBox:
    """Rappresenta una hitbox/hurtbox nel formato MUGEN."""
    x1: int
    y1: int
    x2: int
    y2: int
    
    def to_rect_data(self) -> Tuple[int, int, int, int]:
        """Converte a formato pygame (x, y, width, height)."""
        width = self.x2 - self.x1
        height = self.y2 - self.y1
        return (self.x1, self.y1, width, height)

@dataclass
class SpriteFrame:
    """Un frame di animazione nel file .air"""
    action_id: int
    sprite_index: int
    offset_x: int
    offset_y: int
    duration: int
    hurtbox: CollisionBox = None  # Clsn2 (se presente)
    hitbox: CollisionBox = None   # Clsn1 (se presente)

@dataclass
class HitDefData:
    """Dati da un blocco HitDef nel .cns"""
    damage: int = 0
    guard_damage: int = 0
    pausetime_self: int = 0
    pausetime_opponent: int = 0
    animtype: str = "Light"
    hitflag: str = "MAF"
    # Aggiungi altri campi quando li vedi nei file
    
@dataclass
class ActionData:
    """Completa azione MUGEN (es: Standing Punch)"""
    action_id: int
    type: str  # "S" = Standing, "C" = Crouching, "A" = Air
    movetype: str  # "I" = Idle, "A" = Attack, "H" = Hit, etc.
    frames: List[SpriteFrame]
    hitdef: HitDefData = None

"""Data models per MUGEN parser."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

@dataclass
class CollisionBox:
    """Rappresenta una hitbox/hurtbox nel formato MUGEN."""
    x1: int
    y1: int
    x2: int
    y2: int
    
    def to_pygame_rect(self) -> Tuple[int, int, int, int]:
        """Converte a (x, y, width, height) per pygame."""
        width = self.x2 - self.x1
        height = self.y2 - self.y1
        return (self.x1, self.y1, width, height)

@dataclass
class SpriteFrame:
    """Un singolo frame dall'animazione (.air)."""
    action_id: int
    sprite_index: int
    offset_x: int
    offset_y: int
    duration: int
    hurtbox: Optional[CollisionBox] = None  # Clsn2
    hitbox: Optional[CollisionBox] = None   # Clsn1

@dataclass
class HitDefData:
    """Dati da un blocco HitDef del .cns."""
    damage: int = 0
    guard_damage: int = 0
    pausetime_self: int = 0
    pausetime_opponent: int = 0
    animtype: str = "Light"
    hitflag: str = "MAF"
    sparkno: int = 2
    guard_sparkno: int = 40
    knockback: int = 0
    velocity_x: float = 0.0
    velocity_y: float = 0.0
    
    # Aggiungiamo altri campi se li vedi nei tuoi .cns

@dataclass
class ActionData:
    """Completa azione MUGEN (es: Standing Punch)."""
    action_id: int
    action_type: str = "S"  # S=Standing, C=Crouch, A=Air
    movetype: str = "I"     # I=Idle, A=Attack, H=Hit
    frames: List[SpriteFrame] = field(default_factory=list)
    hitdef: Optional[HitDefData] = None
    animation_name: Optional[str] = None  # Nome leggibile (Attack1, etc.)

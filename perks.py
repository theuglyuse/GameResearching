"""20 perks / abilities the player can earn by answering questions correctly.

Each perk is a dict:
  key         : unique id
  name        : display name
  desc        : short description shown in the choose-a-perk screen
  color       : accent color for the card
  apply(p)    : function that mutates the Player `p`
  stackable   : whether it can be picked more than once

Two of them (kernel_shield, parry_protocol) unlock cooldown ABILITIES that the
player triggers manually.
"""
from settings import *


def _pct(base, pct):
    return base * (1 + pct)


PERKS = [
    {
        "key": "overclock", "name": "Overclock", "color": CYAN, "stackable": True,
        "desc": "+15% movement speed.",
        "apply": lambda p: setattr(p, "speed", _pct(p.speed, 0.15)),
    },
    {
        "key": "cache_boost", "name": "Cache Boost", "color": GREEN, "stackable": True,
        "desc": "+20% attack speed (faster auto-fire).",
        "apply": lambda p: setattr(p, "fire_rate", p.fire_rate * 0.83),
    },
    {
        "key": "bit_shift", "name": "Bit Shift", "color": ORANGE, "stackable": True,
        "desc": "+25% projectile damage.",
        "apply": lambda p: setattr(p, "damage", _pct(p.damage, 0.25)),
    },
    {
        "key": "extra_core", "name": "Extra Core", "color": PRIMARY, "stackable": True,
        "desc": "+1 projectile per attack.",
        "apply": lambda p: setattr(p, "projectiles", p.projectiles + 1),
    },
    {
        "key": "memory_expansion", "name": "Memory Expansion", "color": PURPLE, "stackable": True,
        "desc": "+30 max HP and heal to full.",
        "apply": lambda p: (setattr(p, "max_hp", p.max_hp + 30), setattr(p, "hp", p.max_hp)),
    },
    {
        "key": "garbage_collector", "name": "Garbage Collector", "color": GREEN, "stackable": True,
        "desc": "Regenerate +1.5 HP per second.",
        "apply": lambda p: setattr(p, "regen", p.regen + 1.5),
    },
    {
        "key": "pointer_pierce", "name": "Pointer Pierce", "color": YELLOW, "stackable": True,
        "desc": "Projectiles pierce +1 extra enemy.",
        "apply": lambda p: setattr(p, "pierce", p.pierce + 1),
    },
    {
        "key": "kernel_shield", "name": "Kernel Shield", "color": CYAN, "stackable": False,
        "desc": "Unlock SHIELD ability [E]: brief invulnerability. 8s cooldown.",
        "apply": lambda p: p.unlock_ability("shield"),
    },
    {
        "key": "parry_protocol", "name": "Parry Protocol", "color": RED, "stackable": False,
        "desc": "Unlock PARRY ability [Q]: reflect & stun nearby enemies. 6s cooldown.",
        "apply": lambda p: p.unlock_ability("parry"),
    },
    {
        "key": "lifesteal_loop", "name": "Lifesteal Loop", "color": RED, "stackable": True,
        "desc": "Heal for 12% of damage you deal.",
        "apply": lambda p: setattr(p, "lifesteal", p.lifesteal + 0.12),
    },
    {
        "key": "critical_section", "name": "Critical Section", "color": YELLOW, "stackable": True,
        "desc": "+15% chance to deal double damage.",
        "apply": lambda p: setattr(p, "crit", min(0.9, p.crit + 0.15)),
    },
    {
        "key": "wide_bus", "name": "Wide Bus", "color": PRIMARY, "stackable": True,
        "desc": "+25% attack range.",
        "apply": lambda p: setattr(p, "range", _pct(p.range, 0.25)),
    },
    {
        "key": "turbo_boot", "name": "Turbo Boot", "color": CYAN, "stackable": True,
        "desc": "+10% move speed and +10% attack speed.",
        "apply": lambda p: (setattr(p, "speed", _pct(p.speed, 0.10)),
                            setattr(p, "fire_rate", p.fire_rate * 0.9)),
    },
    {
        "key": "thread_pool", "name": "Thread Pool", "color": PRIMARY, "stackable": False,
        "desc": "+2 projectiles but -10% damage each.",
        "apply": lambda p: (setattr(p, "projectiles", p.projectiles + 2),
                            setattr(p, "damage", p.damage * 0.9)),
    },
    {
        "key": "firewall", "name": "Firewall", "color": ORANGE, "stackable": True,
        "desc": "Take 20% less incoming damage.",
        "apply": lambda p: setattr(p, "damage_reduction", min(0.8, p.damage_reduction + 0.20)),
    },
    {
        "key": "hyperthreading", "name": "Hyperthreading", "color": PURPLE, "stackable": False,
        "desc": "Attacks fire in a wider spread pattern.",
        "apply": lambda p: setattr(p, "spread", True),
    },
    {
        "key": "swap_space", "name": "Swap Space", "color": GREEN, "stackable": False,
        "desc": "Survive one fatal hit, reviving at 40% HP.",
        "apply": lambda p: setattr(p, "revives", p.revives + 1),
    },
    {
        "key": "daemon_drone", "name": "Daemon Drone", "color": CYAN, "stackable": True,
        "desc": "Spawn an orbiting drone that damages enemies.",
        "apply": lambda p: setattr(p, "drones", p.drones + 1),
    },
    {
        "key": "nice_value", "name": "Nice Value", "color": PURPLE, "stackable": True,
        "desc": "Nearby enemies are slowed by 18%.",
        "apply": lambda p: setattr(p, "slow_aura", min(0.7, p.slow_aura + 0.18)),
    },
    {
        "key": "root_access", "name": "Root Access", "color": YELLOW, "stackable": True,
        "desc": "+8% to damage, speed, and attack speed.",
        "apply": lambda p: (setattr(p, "damage", _pct(p.damage, 0.08)),
                            setattr(p, "speed", _pct(p.speed, 0.08)),
                            setattr(p, "fire_rate", p.fire_rate * 0.92)),
    },
]

PERKS_BY_KEY = {perk["key"]: perk for perk in PERKS}


def eligible_perks(player):
    """Return perks the player can still be offered."""
    out = []
    for perk in PERKS:
        if perk["stackable"]:
            out.append(perk)
        elif perk["key"] not in player.perks_taken:
            out.append(perk)
    return out

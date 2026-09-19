"""Programmatically drawn, animated sprites.

Every make_* function returns a list of pygame.Surface frames (with alpha).
Animation is achieved by cycling through the frames. No external art needed;
swap these out for real image assets later if desired.
"""
import math
import pygame
from settings import *


def _surf(size):
    return pygame.Surface((size, size), pygame.SRCALPHA)


def _bob(frame_i, frames, amp):
    """Vertical bob offset for a given frame (smooth sine)."""
    return int(math.sin(frame_i / frames * math.tau) * amp)


# ---------------------------------------------------------------- PLAYERS ----
def make_duck(size=48, frames=4):
    """Debug Duck: a rubber duck with a magnifying glass."""
    out = []
    for i in range(frames):
        s = _surf(size)
        bob = _bob(i, frames, 2)
        cx = size // 2
        body_y = size // 2 + bob
        # body
        pygame.draw.ellipse(s, YELLOW, (cx - 16, body_y - 8, 32, 26))
        # head
        pygame.draw.circle(s, YELLOW, (cx + 8, body_y - 10), 11)
        # beak
        pygame.draw.polygon(s, ORANGE, [(cx + 18, body_y - 12), (cx + 28, body_y - 9), (cx + 18, body_y - 6)])
        # eye
        pygame.draw.circle(s, BLACK, (cx + 11, body_y - 13), 2)
        # magnifying glass (debug tool)
        gx, gy = cx - 16, body_y + 8
        pygame.draw.circle(s, CYAN, (gx, gy), 6, 2)
        pygame.draw.line(s, DIM, (gx - 4, gy + 4), (gx - 10, gy + 10), 2)
        out.append(s)
    return out


def make_penguin(size=48, frames=4):
    """Linux Penguin (Tux-inspired)."""
    out = []
    for i in range(frames):
        s = _surf(size)
        bob = _bob(i, frames, 2)
        cx = size // 2
        by = size // 2 + bob
        # body (black)
        pygame.draw.ellipse(s, (20, 20, 20), (cx - 13, by - 14, 26, 34))
        # belly (white)
        pygame.draw.ellipse(s, WHITE, (cx - 9, by - 6, 18, 24))
        # head
        pygame.draw.circle(s, (20, 20, 20), (cx, by - 16), 10)
        # eyes
        pygame.draw.circle(s, WHITE, (cx - 3, by - 17), 3)
        pygame.draw.circle(s, WHITE, (cx + 3, by - 17), 3)
        pygame.draw.circle(s, BLACK, (cx - 3, by - 17), 1)
        pygame.draw.circle(s, BLACK, (cx + 3, by - 17), 1)
        # beak + feet (orange)
        pygame.draw.polygon(s, ORANGE, [(cx - 3, by - 12), (cx + 3, by - 12), (cx, by - 8)])
        footwig = 2 if i % 2 == 0 else -2
        pygame.draw.ellipse(s, ORANGE, (cx - 10, by + 17, 8, 5))
        pygame.draw.ellipse(s, ORANGE, (cx + 2 + footwig, by + 17, 8, 5))
        out.append(s)
    return out


def make_robot(size=48, frames=4):
    """Compiler-bot: a friendly boxy robot."""
    out = []
    for i in range(frames):
        s = _surf(size)
        bob = _bob(i, frames, 2)
        cx = size // 2
        by = size // 2 + bob
        # body
        pygame.draw.rect(s, (100, 116, 139), (cx - 12, by - 6, 24, 24), border_radius=5)
        # head
        pygame.draw.rect(s, (148, 163, 184), (cx - 10, by - 22, 20, 16), border_radius=4)
        # antenna
        pygame.draw.line(s, DIM, (cx, by - 22), (cx, by - 28), 2)
        pygame.draw.circle(s, RED, (cx, by - 29), 2)
        # eyes (blink on one frame)
        eye = CYAN if i != 2 else DIM
        pygame.draw.circle(s, eye, (cx - 5, by - 14), 3)
        pygame.draw.circle(s, eye, (cx + 5, by - 14), 3)
        # chest light
        pygame.draw.circle(s, GREEN, (cx, by + 4), 3)
        out.append(s)
    return out


PLAYER_MAKERS = {
    "duck": make_duck,
    "penguin": make_penguin,
    "robot": make_robot,
}


# ---------------------------------------------------------------- ENEMIES ----
def make_bug(size=40, frames=4, color=RED):
    """Generic 'bug' enemy with wiggling legs."""
    out = []
    for i in range(frames):
        s = _surf(size)
        cx = cy = size // 2
        legwig = 2 if i % 2 == 0 else -2
        for dx in (-10, 0, 10):
            pygame.draw.line(s, (30, 30, 30), (cx + dx // 2, cy),
                             (cx + dx, cy + 12 + legwig), 2)
            pygame.draw.line(s, (30, 30, 30), (cx + dx // 2, cy),
                             (cx + dx, cy - 12 - legwig), 2)
        pygame.draw.ellipse(s, color, (cx - 12, cy - 9, 24, 18))
        pygame.draw.circle(s, (20, 20, 20), (cx + 6, cy - 6), 3)
        pygame.draw.circle(s, WHITE, (cx - 3, cy - 2), 2)
        pygame.draw.circle(s, WHITE, (cx + 3, cy - 2), 2)
        out.append(s)
    return out


def make_shooter(size=44, frames=4):
    """Ranged enemy: a floating 'null-pointer' orb that fires."""
    out = []
    for i in range(frames):
        s = _surf(size)
        cx = cy = size // 2
        pulse = 2 + (i % 2) * 2
        pygame.draw.circle(s, PURPLE, (cx, cy), 13)
        pygame.draw.circle(s, (30, 10, 40), (cx, cy), 13, 2)
        pygame.draw.circle(s, CYAN, (cx, cy), 5 + pulse, 2)
        pygame.draw.circle(s, WHITE, (cx, cy), 3)
        out.append(s)
    return out


def make_tank(size=52, frames=4):
    """Tanky slow enemy: a 'memory-leak' blob."""
    out = []
    for i in range(frames):
        s = _surf(size)
        cx = cy = size // 2
        wob = _bob(i, frames, 2)
        pygame.draw.circle(s, ORANGE, (cx, cy + wob), 18)
        pygame.draw.circle(s, (120, 50, 10), (cx, cy + wob), 18, 3)
        pygame.draw.circle(s, YELLOW, (cx - 6, cy - 4 + wob), 3)
        pygame.draw.circle(s, YELLOW, (cx + 6, cy - 4 + wob), 3)
        pygame.draw.arc(s, (120, 50, 10), (cx - 8, cy + wob, 16, 12), 3.4, 6.0, 2)
        out.append(s)
    return out


def make_boss(size=120, frames=4):
    """Final boss: the Kernel Panic."""
    out = []
    for i in range(frames):
        s = _surf(size)
        cx = cy = size // 2
        wob = _bob(i, frames, 3)
        pygame.draw.circle(s, (40, 10, 20), (cx, cy + wob), 46)
        pygame.draw.circle(s, RED, (cx, cy + wob), 46, 4)
        # angry eyes
        pygame.draw.polygon(s, YELLOW, [(cx - 24, cy - 12 + wob), (cx - 6, cy - 4 + wob), (cx - 24, cy + wob)])
        pygame.draw.polygon(s, YELLOW, [(cx + 24, cy - 12 + wob), (cx + 6, cy - 4 + wob), (cx + 24, cy + wob)])
        # mouth
        pygame.draw.arc(s, YELLOW, (cx - 20, cy + 4 + wob, 40, 26), 3.4, 6.0, 4)
        # spikes
        for a in range(0, 360, 45):
            r = math.radians(a + i * 6)
            x1 = cx + math.cos(r) * 46
            y1 = cy + wob + math.sin(r) * 46
            x2 = cx + math.cos(r) * 58
            y2 = cy + wob + math.sin(r) * 58
            pygame.draw.line(s, RED, (x1, y1), (x2, y2), 4)
        out.append(s)
    return out


# Registry of enemy art makers by type name.
ENEMY_MAKERS = {
    "bug": lambda: make_bug(color=RED),
    "greenbug": lambda: make_bug(color=GREEN),
    "shooter": make_shooter,
    "tank": make_tank,
    "boss": make_boss,
}

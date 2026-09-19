"""Game entities: Player, Enemy, Projectile, Drone."""
import math
import random
import pygame
from pygame.math import Vector2
from settings import *
import art

# Per-character base stats (speed, hp, damage, fire_rate).
CHARACTERS = {
    "duck": {
        "name": "Debug Duck", "blurb": "Balanced all-rounder.",
        "speed": PLAYER_BASE_SPEED, "hp": PLAYER_BASE_HP,
        "damage": PLAYER_BASE_DAMAGE, "fire_rate": PLAYER_BASE_FIRE_RATE,
    },
    "penguin": {
        "name": "Linux Penguin", "blurb": "Tanky & tough, a little slower.",
        "speed": PLAYER_BASE_SPEED * 0.85, "hp": int(PLAYER_BASE_HP * 1.4),
        "damage": PLAYER_BASE_DAMAGE, "fire_rate": PLAYER_BASE_FIRE_RATE * 1.1,
    },
    "robot": {
        "name": "Compiler-Bot", "blurb": "Fast, rapid fire, lower damage.",
        "speed": PLAYER_BASE_SPEED * 1.2, "hp": int(PLAYER_BASE_HP * 0.85),
        "damage": int(PLAYER_BASE_DAMAGE * 0.8), "fire_rate": PLAYER_BASE_FIRE_RATE * 0.7,
    },
}


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


class Animated:
    """Mixin providing simple frame animation."""
    def __init__(self, frames, frame_time=0.14):
        self.frames = frames
        self.frame_time = frame_time
        self.frame_i = 0
        self._t = 0.0

    def animate(self, dt):
        self._t += dt
        if self._t >= self.frame_time:
            self._t = 0.0
            self.frame_i = (self.frame_i + 1) % len(self.frames)

    @property
    def image(self):
        return self.frames[self.frame_i]


class Projectile(Animated):
    def __init__(self, pos, vel, damage, pierce, from_player, color=CYAN):
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        self.damage = damage
        self.pierce = pierce
        self.from_player = from_player
        self.color = color
        self.alive = True
        self.hit = set()

    def update(self, dt):
        self.pos += self.vel
        if not (0 <= self.pos.x <= WORLD_W and 0 <= self.pos.y <= WORLD_H):
            self.alive = False

    def draw(self, surf, cam):
        p = (int(self.pos.x - cam.x), int(self.pos.y - cam.y))
        pygame.draw.circle(surf, self.color, p, 6)
        pygame.draw.circle(surf, WHITE, p, 3)


class Drone:
    """Orbiting helper that damages enemies it touches."""
    def __init__(self, index):
        self.angle = index * 2.0
        self.radius = 60
        self.cooldown = 0.0

    def update(self, dt, owner_pos):
        self.angle += dt * 3.0
        self.pos = Vector2(owner_pos.x + math.cos(self.angle) * self.radius,
                           owner_pos.y + math.sin(self.angle) * self.radius)
        self.cooldown = max(0, self.cooldown - dt)

    def draw(self, surf, cam):
        p = (int(self.pos.x - cam.x), int(self.pos.y - cam.y))
        pygame.draw.circle(surf, CYAN, p, 8)
        pygame.draw.circle(surf, WHITE, p, 4)


class Player(Animated):
    def __init__(self, char_key):
        base = CHARACTERS[char_key]
        Animated.__init__(self, art.PLAYER_MAKERS[char_key](), frame_time=0.12)
        self.char_key = char_key
        self.name = base["name"]
        self.pos = Vector2(WORLD_W / 2, FLOOR_Y + (WORLD_H - FLOOR_Y) / 2)
        self.radius = 20

        # Core stats (mutated by perks)
        self.speed = base["speed"]
        self.max_hp = base["hp"]
        self.hp = base["hp"]
        self.damage = base["damage"]
        self.fire_rate = base["fire_rate"]
        self.range = PLAYER_BASE_RANGE
        self.projectiles = 1
        self.pierce = 0
        self.regen = 0.0
        self.lifesteal = 0.0
        self.crit = 0.0
        self.damage_reduction = 0.0
        self.spread = False
        self.revives = 0
        self.drones = 0
        self.slow_aura = 0.0

        # Abilities (cooldown based)
        self.abilities = {}          # name -> {cooldown, timer, active, duration}
        self.perks_taken = set()

        self._fire_timer = 0.0
        self._drone_objs = []
        self._hurt_flash = 0.0

    # ---- perks / abilities ----
    def unlock_ability(self, name):
        if name == "shield":
            self.abilities["shield"] = {"cooldown": 8.0, "timer": 0.0,
                                        "active": False, "duration": 2.0, "active_t": 0.0}
        elif name == "parry":
            self.abilities["parry"] = {"cooldown": 6.0, "timer": 0.0,
                                       "active": False, "duration": 0.4, "active_t": 0.0}

    def apply_perk(self, perk):
        perk["apply"](self)
        self.perks_taken.add(perk["key"])

    def use_ability(self, name, enemies):
        ab = self.abilities.get(name)
        if not ab or ab["timer"] > 0:
            return
        ab["timer"] = ab["cooldown"]
        ab["active"] = True
        ab["active_t"] = ab["duration"]
        if name == "parry":
            # stun + damage nearby enemies
            for e in enemies:
                if self.pos.distance_to(e.pos) < 120:
                    e.stun(1.2)
                    e.take_damage(self.damage * 2)

    @property
    def shielded(self):
        s = self.abilities.get("shield")
        p = self.abilities.get("parry")
        return (s and s["active"]) or (p and p["active"])

    # ---- combat ----
    def take_damage(self, amount):
        if self.shielded:
            return
        amount *= (1 - self.damage_reduction)
        self.hp -= amount
        self._hurt_flash = 0.15
        if self.hp <= 0:
            if self.revives > 0:
                self.revives -= 1
                self.hp = self.max_hp * 0.4

    def _nearest_enemy(self, enemies):
        best, bestd = None, self.range
        for e in enemies:
            d = self.pos.distance_to(e.pos)
            if d < bestd:
                best, bestd = e, d
        return best

    def _fire(self, target, projectiles):
        direction = (target.pos - self.pos)
        if direction.length() == 0:
            return
        direction = direction.normalize()
        n = self.projectiles
        # spread angles
        if n == 1 and not self.spread:
            angles = [0]
        else:
            spread_deg = 30 if self.spread else 14
            step = spread_deg
            start = -step * (n - 1) / 2
            angles = [start + step * i for i in range(n)]
        for a in angles:
            rad = math.radians(a)
            dx = direction.x * math.cos(rad) - direction.y * math.sin(rad)
            dy = direction.x * math.sin(rad) + direction.y * math.cos(rad)
            vel = Vector2(dx, dy) * PLAYER_ATTACK_SPEED
            dmg = self.damage
            if random.random() < self.crit:
                dmg *= 2
            projectiles.append(Projectile(self.pos, vel, dmg, self.pierce, True))

    def update(self, dt, keys, enemies, projectiles, allow_move=True):
        self.animate(dt)
        self._hurt_flash = max(0, self._hurt_flash - dt)

        # movement (WASD + arrows)
        if allow_move:
            move = Vector2(0, 0)
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                move.x -= 1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                move.x += 1
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                move.y -= 1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                move.y += 1
            if move.length() > 0:
                move = move.normalize() * self.speed
                self.pos += move
        # keep in world (can go into the sky for quiz buttons)
        self.pos.x = clamp(self.pos.x, self.radius, WORLD_W - self.radius)
        self.pos.y = clamp(self.pos.y, self.radius, WORLD_H - self.radius)

        # regen
        if self.regen and self.hp < self.max_hp:
            self.hp = min(self.max_hp, self.hp + self.regen * dt)

        # ability timers
        for ab in self.abilities.values():
            ab["timer"] = max(0, ab["timer"] - dt)
            if ab["active"]:
                ab["active_t"] -= dt
                if ab["active_t"] <= 0:
                    ab["active"] = False

        # auto-attack
        self._fire_timer = max(0, self._fire_timer - dt)
        if self._fire_timer == 0:
            target = self._nearest_enemy(enemies)
            if target:
                self._fire(target, projectiles)
                self._fire_timer = self.fire_rate

        # drones
        while len(self._drone_objs) < self.drones:
            self._drone_objs.append(Drone(len(self._drone_objs)))
        for d in self._drone_objs:
            d.update(dt, self.pos)
            for e in enemies:
                if d.pos.distance_to(e.pos) < 24 and d.cooldown == 0:
                    e.take_damage(self.damage)
                    d.cooldown = 0.3

    def heal_from_damage(self, dmg):
        if self.lifesteal:
            self.hp = min(self.max_hp, self.hp + dmg * self.lifesteal)

    def draw(self, surf, cam):
        for d in self._drone_objs:
            d.draw(surf, cam)
        img = self.image
        rect = img.get_rect(center=(self.pos.x - cam.x, self.pos.y - cam.y))
        surf.blit(img, rect)
        if self.shielded:
            pygame.draw.circle(surf, CYAN, rect.center, 32, 3)
        if self._hurt_flash > 0:
            flash = pygame.Surface(img.get_size(), pygame.SRCALPHA)
            flash.fill((255, 80, 80, 120))
            surf.blit(flash, rect)


class Enemy(Animated):
    def __init__(self, etype, pos, hp_scale=1.0, speed_scale=1.0, dmg_scale=1.0):
        frames = art.ENEMY_MAKERS[etype]()
        Animated.__init__(self, frames, frame_time=0.16)
        self.etype = etype
        self.pos = Vector2(pos)
        self.stun_t = 0.0
        self._shoot_t = random.uniform(1.0, 2.5)

        if etype == "boss":
            self.max_hp = ENEMY_BASE_HP * 60 * hp_scale
            self.speed = ENEMY_BASE_SPEED * 0.5 * speed_scale
            self.touch_damage = ENEMY_TOUCH_DAMAGE * 2 * dmg_scale
            self.radius = 55
        elif etype == "tank":
            self.max_hp = ENEMY_BASE_HP * 4 * hp_scale
            self.speed = ENEMY_BASE_SPEED * 0.6 * speed_scale
            self.touch_damage = ENEMY_TOUCH_DAMAGE * 1.5 * dmg_scale
            self.radius = 26
        elif etype == "shooter":
            self.max_hp = ENEMY_BASE_HP * 1.5 * hp_scale
            self.speed = ENEMY_BASE_SPEED * 0.9 * speed_scale
            self.touch_damage = ENEMY_TOUCH_DAMAGE * dmg_scale
            self.radius = 20
        else:  # bug / greenbug
            self.max_hp = ENEMY_BASE_HP * hp_scale
            self.speed = ENEMY_BASE_SPEED * speed_scale
            self.touch_damage = ENEMY_TOUCH_DAMAGE * dmg_scale
            self.radius = 18
        self.hp = self.max_hp
        self.alive = True

    def stun(self, t):
        self.stun_t = max(self.stun_t, t)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False

    def update(self, dt, player, enemy_projectiles):
        self.animate(dt)
        self.stun_t = max(0, self.stun_t - dt)
        if self.stun_t > 0:
            return
        direction = (player.pos - self.pos)
        dist = direction.length()
        spd = self.speed
        if player.slow_aura and dist < 160:
            spd *= (1 - player.slow_aura)
        if dist > 1:
            self.pos += direction.normalize() * spd

        # shooter fires at the player
        if self.etype == "shooter":
            self._shoot_t -= dt
            if self._shoot_t <= 0 and dist < 500:
                self._shoot_t = random.uniform(1.8, 3.0)
                if dist > 0:
                    vel = direction.normalize() * 4.0
                    enemy_projectiles.append(
                        Projectile(self.pos, vel, self.touch_damage, 0, False, color=PURPLE))

    def draw(self, surf, cam):
        img = self.image
        rect = img.get_rect(center=(self.pos.x - cam.x, self.pos.y - cam.y))
        surf.blit(img, rect)
        # hp bar
        if self.hp < self.max_hp:
            w = rect.width
            ratio = clamp(self.hp / self.max_hp, 0, 1)
            bx, by = rect.left, rect.top - 6
            pygame.draw.rect(surf, (60, 60, 60), (bx, by, w, 4))
            pygame.draw.rect(surf, GREEN, (bx, by, int(w * ratio), 4))

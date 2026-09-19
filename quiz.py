"""Interactive between-wave quiz.

The quiz happens IN the world: answer pads appear up in the 'sky'. The player
walks onto a pad and stands on it briefly (dwell) to select it. When the player
is near a pad, its full option text is revealed. Correct answers let the player
walk onto one of three perk pads to claim a reward.
"""
import pygame
from pygame.math import Vector2
from settings import *
from perks import eligible_perks
import random

DWELL_TIME = 0.7          # seconds to stand on a pad to select it
PAD_W, PAD_H = 150, 70


class Pad:
    def __init__(self, x, y, label, payload):
        self.rect = pygame.Rect(0, 0, PAD_W, PAD_H)
        self.rect.center = (x, y)
        self.label = label          # short label (e.g., "A")
        self.payload = payload      # index or perk dict
        self.progress = 0.0
        self.detail = ""            # full text shown when near

    def near(self, player_pos):
        return Vector2(self.rect.center).distance_to(player_pos) < 140

    def on(self, player_rect):
        return self.rect.colliderect(player_rect)


class QuizSession:
    """Runs a sequence of questions during a quiz phase."""

    def __init__(self, pool, stage, num_questions, use_code=False, boss=False):
        self.pool = pool
        self.stage = stage
        self.boss = boss
        self.use_code = use_code
        self.total = 1 if boss else num_questions
        self.q_index = 0
        self.correct_count = 0
        self.finished = False
        self.big_boost_earned = False   # boss reward flag

        self.state = "intro"            # intro -> question -> feedback -> perk -> (next) -> end
        self.timer = 1.4
        self.pads = []
        self.origin = Vector2(WORLD_W / 2, WORLD_H / 2)
        self.boss_part = 1
        self.boss_correct = 0
        self.current = None
        self.last_correct = False
        self.message = ""
        self.explanation = ""

    # ------------------------------------------------------------------ setup
    def begin(self, player):
        self.origin = Vector2(player.pos.x, FLOOR_Y - 40)
        self._load_question()

    def _load_question(self):
        if self.boss:
            self._boss = self.pool.get_boss()
            self.current = self._boss["part1"]
        elif self.use_code and random.random() < 0.6:
            self.current = self.pool.get_code()
        else:
            self.current = self.pool.get_concept(self.stage)
        self._make_answer_pads()
        self.state = "question"

    def _make_answer_pads(self):
        self.pads = []
        opts = self.current["options"]
        n = len(opts)
        spacing = 180
        start_x = self.origin.x - spacing * (n - 1) / 2
        y = FLOOR_Y - 150
        for i, text in enumerate(opts):
            pad = Pad(start_x + i * spacing, y, chr(65 + i), i)
            pad.detail = text
            self.pads.append(pad)

    def _make_perk_pads(self, player):
        self.pads = []
        choices = random.sample(eligible_perks(player), k=min(3, len(eligible_perks(player))))
        self._perk_choices = choices
        spacing = 240
        start_x = self.origin.x - spacing * (len(choices) - 1) / 2
        y = FLOOR_Y - 150
        for i, perk in enumerate(choices):
            pad = Pad(start_x + i * spacing, y, perk["name"], perk)
            pad.detail = perk["desc"]
            self.pads.append(pad)

    # ----------------------------------------------------------------- update
    def update(self, dt, player):
        player_rect = pygame.Rect(0, 0, 44, 44)
        player_rect.center = player.pos

        if self.state == "intro":
            self.timer -= dt
            if self.timer <= 0:
                self.state = "question"
            return

        if self.state in ("question", "perk"):
            selected = None
            for pad in self.pads:
                if pad.on(player_rect):
                    pad.progress += dt
                    if pad.progress >= DWELL_TIME:
                        selected = pad
                else:
                    pad.progress = max(0, pad.progress - dt * 2)
            if selected:
                if self.state == "question":
                    self._resolve_answer(selected, player)
                else:
                    self._resolve_perk(selected, player)

        elif self.state == "feedback":
            self.timer -= dt
            if self.timer <= 0 and self._feedback_continue(player):
                self._advance(player)

    def _feedback_continue(self, player):
        # continue automatically after a minimum reading time
        return self.timer <= 0

    def _resolve_answer(self, pad, player):
        correct = (pad.payload == self.current["answer"])
        self.last_correct = correct
        self.explanation = self.current["explanation"]
        if self.boss:
            if correct:
                self.boss_correct += 1
            if self.boss_part == 1:
                self.message = ("Correct! Now the hard part..." if correct
                                else "Wrong. But steel yourself for part 2...")
            else:
                both = self.boss_correct == 2
                self.big_boost_earned = both
                self.message = ("BOTH PARTS RIGHT! Massive boost incoming!" if both
                                else "The boss resists... no boost this time.")
        else:
            if correct:
                self.correct_count += 1
                self.message = "Correct! Choose a perk."
            else:
                self.message = "Not quite — no perk this round."
        self.state = "feedback"
        self.timer = 3.2

    def _resolve_perk(self, pad, player):
        player.apply_perk(pad.payload)
        self.message = f"Gained: {pad.payload['name']}!"
        self.explanation = pad.payload["desc"]
        self.state = "feedback"
        self.timer = 2.0
        self._perk_done = True

    def _advance(self, player):
        # boss two-part flow
        if self.boss:
            if self.boss_part == 1:
                self.boss_part = 2
                self.current = self._boss["part2"]
                self._make_answer_pads()
                self.state = "question"
                return
            else:
                if self.big_boost_earned:
                    self._apply_big_boost(player)
                self.finished = True
                return

        # normal flow
        if getattr(self, "_perk_done", False):
            self._perk_done = False
            self._next_question(player)
        elif self.last_correct:
            # offer perk
            self._make_perk_pads(player)
            self.state = "perk"
        else:
            self._next_question(player)

    def _next_question(self, player):
        self.q_index += 1
        if self.q_index >= self.total:
            self.finished = True
        else:
            self._load_question()

    def _apply_big_boost(self, player):
        player.max_hp += 60
        player.hp = player.max_hp
        player.damage *= 1.5
        player.fire_rate *= 0.7
        player.speed *= 1.1
        if "shield" not in player.abilities:
            player.unlock_ability("shield")

    # ------------------------------------------------------------------- draw
    def draw(self, surf, cam, font, bigfont, smallfont):
        # dim overlay in the sky region for readability
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((10, 12, 25, 120))
        surf.blit(overlay, (0, 0))

        if self.state == "intro":
            self._center_text(surf, bigfont, "QUIZ TIME!", SCREEN_H // 2 - 20, YELLOW)
            self._center_text(surf, font, "Walk UP onto an answer pad and stand on it to choose.",
                              SCREEN_H // 2 + 24, WHITE)
            return

        # question text (top banner)
        if self.state in ("question",) and self.current:
            self._wrapped(surf, font, self.current.get("q", ""), 30, WHITE, max_w=SCREEN_W - 80)
            if "code" in self.current:
                self._draw_code(surf, smallfont, self.current["code"], 120)

        if self.state == "perk":
            self._center_text(surf, font, "Answer correct! Step on a perk to claim it.", 34, GREEN)

        # pads
        if self.state in ("question", "perk"):
            for pad in self.pads:
                self._draw_pad(surf, cam, pad, font, smallfont, player_near_only=(self.state == "question"))

        # feedback
        if self.state == "feedback":
            col = GREEN if self.last_correct or getattr(self, "_perk_done", False) else RED
            self._center_text(surf, bigfont, self.message, 60, col)
            self._wrapped(surf, font, self.explanation, 120, WHITE, max_w=SCREEN_W - 120)
            self._center_text(surf, smallfont, "(continues automatically...)", SCREEN_H - 60, DIM)

        # progress
        prog = f"Question {min(self.q_index + 1, self.total)}/{self.total}"
        if self.boss:
            prog = f"BOSS  •  Part {self.boss_part}/2"
        surf.blit(smallfont.render(prog, True, DIM), (SCREEN_W - 160, SCREEN_H - 30))

    def _draw_pad(self, surf, cam, pad, font, smallfont, player_near_only):
        r = pad.rect.move(-cam.x, -cam.y)
        color = PRIMARY
        if isinstance(pad.payload, dict):
            color = pad.payload.get("color", PRIMARY)
        pygame.draw.rect(surf, color, r, border_radius=10)
        pygame.draw.rect(surf, WHITE, r, 2, border_radius=10)
        # dwell progress bar
        if pad.progress > 0:
            w = int(r.width * min(1, pad.progress / DWELL_TIME))
            pygame.draw.rect(surf, YELLOW, (r.left, r.bottom - 6, w, 6), border_radius=3)
        # label
        lab = font.render(pad.label, True, WHITE)
        surf.blit(lab, lab.get_rect(center=(r.centerx, r.top - 16)))
        # detail text when near (revealed as the player approaches)
        detail = self._fit(pad.detail, smallfont, r.width - 12)
        for j, line in enumerate(detail):
            t = smallfont.render(line, True, WHITE)
            surf.blit(t, t.get_rect(center=(r.centerx, r.centery - 12 + j * 16)))

    # -------------------------------------------------------------- text utils
    def _center_text(self, surf, font, text, y, color):
        t = font.render(text, True, color)
        surf.blit(t, t.get_rect(center=(SCREEN_W // 2, y)))

    def _wrapped(self, surf, font, text, y, color, max_w):
        for i, line in enumerate(self._fit(text, font, max_w)):
            t = font.render(line, True, color)
            surf.blit(t, t.get_rect(center=(SCREEN_W // 2, y + i * (font.get_height() + 2))))

    def _fit(self, text, font, max_w):
        words = text.split()
        lines, cur = [], ""
        for w in words:
            test = (cur + " " + w).strip()
            if font.size(test)[0] <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def _draw_code(self, surf, font, code, y):
        lines = code.split("\n")
        box_w = max(font.size(l)[0] for l in lines) + 24
        box_h = len(lines) * (font.get_height() + 2) + 16
        x = SCREEN_W // 2 - box_w // 2
        pygame.draw.rect(surf, (15, 20, 30), (x, y, box_w, box_h), border_radius=8)
        pygame.draw.rect(surf, PRIMARY, (x, y, box_w, box_h), 2, border_radius=8)
        for i, line in enumerate(lines):
            t = font.render(line, True, CYAN)
            surf.blit(t, (x + 12, y + 10 + i * (font.get_height() + 2)))

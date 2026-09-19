"""Interactive between-wave quiz.

The quiz happens in a 'room' up in the sky. When it starts, the player is guided
UP out of the floor by an on-screen arrow. Answer pads are spread far apart so you
can only stand on one at a time. Walk onto a pad and stand on it (dwell) to select.

Perks are chosen at the END of the quiz: you get one perk pick per question you
answered correctly.
"""
import math
import random
import pygame
from pygame.math import Vector2
from settings import *
from perks import eligible_perks

DWELL_TIME = 0.7             # seconds to stand on a pad to select it
PAD_W, PAD_H = 200, 74
ANSWER_SPACING = 340        # far apart so you can't touch two pads at once
PERK_SPACING = 420


class Pad:
    def __init__(self, x, y, label, payload, color=PRIMARY):
        self.rect = pygame.Rect(0, 0, PAD_W, PAD_H)
        self.rect.center = (x, y)
        self.label = label
        self.payload = payload
        self.color = color
        self.progress = 0.0
        self.detail = ""

    def on(self, player_rect):
        return self.rect.colliderect(player_rect)


class QuizSession:
    def __init__(self, pool, stage, num_questions, use_code=False, boss=False):
        self.pool = pool
        self.stage = stage
        self.boss = boss
        self.use_code = use_code
        self.total = 1 if boss else num_questions
        self.q_index = 0
        self.correct_count = 0
        self.finished = False
        self.big_boost_earned = False

        self.state = "intro"        # intro,question,qfeedback,perkselect,perkfeedback,done
        self.timer = 1.6
        self.pads = []
        self.origin = Vector2(WORLD_W / 2, QUIZ_PAD_Y)
        self.boss_part = 1
        self.boss_correct = 0
        self.current = None
        self.last_correct = False
        self.message = ""
        self.explanation = ""
        self.perks_remaining = 0

    # ------------------------------------------------------------------ setup
    def begin(self, player):
        half = ANSWER_SPACING * 2 + PAD_W  # keep the widest cluster on-map
        ox = max(half, min(WORLD_W - half, player.pos.x))
        self.origin = Vector2(ox, QUIZ_PAD_Y)
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
        start_x = self.origin.x - ANSWER_SPACING * (n - 1) / 2
        for i, text in enumerate(opts):
            pad = Pad(start_x + i * ANSWER_SPACING, QUIZ_PAD_Y, chr(65 + i), i)
            pad.detail = text
            self.pads.append(pad)

    def _make_perk_pads(self, player):
        self.pads = []
        pool = eligible_perks(player)
        choices = random.sample(pool, k=min(3, len(pool)))
        start_x = self.origin.x - PERK_SPACING * (len(choices) - 1) / 2
        for i, perk in enumerate(choices):
            pad = Pad(start_x + i * PERK_SPACING, QUIZ_PAD_Y, perk["name"],
                      perk, color=perk["color"])
            pad.detail = perk["desc"]
            self.pads.append(pad)

    # ----------------------------------------------------------------- update
    def update(self, dt, player):
        player_rect = pygame.Rect(0, 0, 40, 40)
        player_rect.center = player.pos

        if self.state == "intro":
            self.timer -= dt
            if self.timer <= 0:
                self.state = "question"
            return

        if self.state in ("question", "perkselect"):
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

        elif self.state == "qfeedback":
            self.timer -= dt
            if self.timer <= 0:
                self._after_question(player)

        elif self.state == "perkfeedback":
            self.timer -= dt
            if self.timer <= 0:
                self._after_perk(player)

    def _resolve_answer(self, pad, player):
        correct = (pad.payload == self.current["answer"])
        self.last_correct = correct
        self.explanation = self.current["explanation"]
        if self.boss:
            if correct:
                self.boss_correct += 1
            if self.boss_part == 1:
                self.message = ("Correct! Now the reason why..." if correct
                                else "Wrong — but face part 2!")
            else:
                both = self.boss_correct == 2
                self.big_boost_earned = both
                self.message = ("BOTH RIGHT! Massive boost incoming!" if both
                                else "The boss resists... no boost.")
        else:
            if correct:
                self.correct_count += 1
                self.message = "Correct!"
            else:
                self.message = "Not quite."
        self.state = "qfeedback"
        self.timer = 3.4

    def _after_question(self, player):
        if self.boss:
            if self.boss_part == 1:
                self.boss_part = 2
                self.current = self._boss["part2"]
                self._make_answer_pads()
                self.state = "question"
            else:
                if self.big_boost_earned:
                    self._apply_big_boost(player)
                self.finished = True
            return
        # normal quiz: advance through all questions first
        self.q_index += 1
        if self.q_index < self.total:
            self._load_question()
        else:
            # perk phase: one pick per correct answer
            self.perks_remaining = self.correct_count
            if self.perks_remaining > 0:
                self._make_perk_pads(player)
                self.state = "perkselect"
            else:
                self.finished = True

    def _resolve_perk(self, pad, player):
        player.apply_perk(pad.payload)
        self.message = f"Gained: {pad.payload['name']}!"
        self.explanation = pad.payload["desc"]
        self.state = "perkfeedback"
        self.timer = 2.0

    def _after_perk(self, player):
        self.perks_remaining -= 1
        if self.perks_remaining > 0:
            self._make_perk_pads(player)
            self.state = "perkselect"
        else:
            self.finished = True

    def _apply_big_boost(self, player):
        player.max_hp += 60
        player.hp = player.max_hp
        player.damage *= 1.5
        player.fire_rate *= 0.7
        player.speed *= 1.1
        if "shield" not in player.abilities:
            player.unlock_ability("shield")

    # ------------------------------------------------------------------- draw
    def draw(self, surf, cam, font, bigfont, smallfont, player=None):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((10, 12, 25, 110))
        surf.blit(overlay, (0, 0))

        # draw the sky "room" band behind the pads
        room_top = QUIZ_ROOM_TOP - cam.y
        room_h = (QUIZ_ROOM_BOT - QUIZ_ROOM_TOP)
        room = pygame.Rect(0, room_top, SCREEN_W, room_h)
        room_surf = pygame.Surface((SCREEN_W, room_h), pygame.SRCALPHA)
        room_surf.fill((30, 34, 60, 150))
        surf.blit(room_surf, (0, room_top))
        pygame.draw.line(surf, PRIMARY, (0, room_top), (SCREEN_W, room_top), 2)
        pygame.draw.line(surf, PRIMARY, (0, room_top + room_h),
                         (SCREEN_W, room_top + room_h), 2)

        if self.state == "intro":
            self._panel(surf, bigfont, "QUIZ TIME!", 60, YELLOW)
            self._panel(surf, font,
                        "Follow the arrow UP into the room. Stand on an answer pad to choose.",
                        130, WHITE)
            return

        # question / instruction panel at top (never overlaps HUD; HUD hidden in quiz)
        if self.state in ("question", "qfeedback") and self.current:
            code = self.current.get("code")
            self._question_panel(surf, font, smallfont, self.current["q"], code)
        elif self.state in ("perkselect", "perkfeedback"):
            remaining = self.perks_remaining
            self._panel(surf, font,
                        f"Choose a perk!  ({remaining} pick{'s' if remaining != 1 else ''} left)",
                        40, GREEN)

        # pads
        if self.state in ("question", "perkselect"):
            for pad in self.pads:
                self._draw_pad(surf, cam, pad, font, smallfont)
            if player is not None:
                self._draw_arrow(surf, cam, player)

        # feedback
        if self.state in ("qfeedback", "perkfeedback"):
            col = GREEN if self.last_correct or self.state == "perkfeedback" else RED
            self._panel(surf, bigfont, self.message, 220, col)
            self._wrapped(surf, font, self.explanation, 280, WHITE, SCREEN_W - 160)

        # progress
        if self.boss:
            prog = f"BOSS  Part {self.boss_part}/2"
        elif self.state in ("perkselect", "perkfeedback"):
            prog = "Perk selection"
        else:
            prog = f"Question {min(self.q_index + 1, self.total)}/{self.total}"
        surf.blit(smallfont.render(prog, True, DIM), (20, SCREEN_H - 28))

    # --- arrow guiding the player up to the pads ---
    def _draw_arrow(self, surf, cam, player):
        # target: nearest pad center
        target = min(self.pads, key=lambda p: Vector2(p.rect.center).distance_to(player.pos))
        tc = Vector2(target.rect.center)
        if tc.distance_to(player.pos) < 120:
            return
        px = player.pos.x - cam.x
        py = player.pos.y - cam.y - 40
        d = (tc - player.pos)
        if d.length() == 0:
            return
        d = d.normalize()
        tip = Vector2(px, py) + d * 46
        left = Vector2(px, py) + d.rotate(150) * 22
        right = Vector2(px, py) + d.rotate(-150) * 22
        pulse = 180 + int(70 * math.sin(pygame.time.get_ticks() / 150))
        pygame.draw.polygon(surf, (255, 220, 60), [tip, left, right])
        pygame.draw.polygon(surf, (pulse, pulse, 60), [tip, left, right], 3)

    def _draw_pad(self, surf, cam, pad, font, smallfont):
        r = pad.rect.move(-cam.x, -cam.y)
        pygame.draw.rect(surf, pad.color, r, border_radius=12)
        pygame.draw.rect(surf, WHITE, r, 2, border_radius=12)
        if pad.progress > 0:
            w = int(r.width * min(1, pad.progress / DWELL_TIME))
            pygame.draw.rect(surf, YELLOW, (r.left, r.bottom - 7, w, 7), border_radius=3)
        # label above pad
        lab = font.render(pad.label, True, YELLOW)
        surf.blit(lab, lab.get_rect(center=(r.centerx, r.top - 18)))
        # option/perk text wrapped inside pad
        lines = self._fit(pad.detail, smallfont, r.width - 16)
        total_h = len(lines) * (smallfont.get_height() + 1)
        y0 = r.centery - total_h // 2
        for j, line in enumerate(lines):
            t = smallfont.render(line, True, WHITE)
            surf.blit(t, t.get_rect(center=(r.centerx, y0 + j * (smallfont.get_height() + 1) + 8)))

    # -------------------------------------------------------------- text utils
    def _question_panel(self, surf, font, smallfont, question, code):
        max_w = SCREEN_W - 120
        lines = self._fit(question, font, max_w)
        line_h = font.get_height() + 4
        code_lines = code.split("\n") if code else []
        code_h = (len(code_lines) * (smallfont.get_height() + 2) + 20) if code else 0
        pad_y = 20
        box_h = 24 + len(lines) * line_h + (code_h + 12 if code else 0)
        box = pygame.Rect(60, pad_y, max_w, box_h)
        panel = pygame.Surface(box.size, pygame.SRCALPHA)
        panel.fill((18, 22, 40, 235))
        surf.blit(panel, box.topleft)
        pygame.draw.rect(surf, PRIMARY, box, 2, border_radius=10)
        y = box.top + 12
        for line in lines:
            t = font.render(line, True, WHITE)
            surf.blit(t, t.get_rect(midtop=(box.centerx, y)))
            y += line_h
        if code:
            self._draw_code(surf, smallfont, code_lines, y + 6, box)

    def _draw_code(self, surf, font, code_lines, y, box):
        cw = max(font.size(l)[0] for l in code_lines) + 24
        ch = len(code_lines) * (font.get_height() + 2) + 12
        cx = box.centerx - cw // 2
        pygame.draw.rect(surf, (12, 16, 26), (cx, y, cw, ch), border_radius=8)
        pygame.draw.rect(surf, CYAN, (cx, y, cw, ch), 1, border_radius=8)
        for i, line in enumerate(code_lines):
            t = font.render(line, True, CYAN)
            surf.blit(t, (cx + 12, y + 6 + i * (font.get_height() + 2)))

    def _panel(self, surf, font, text, y, color):
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

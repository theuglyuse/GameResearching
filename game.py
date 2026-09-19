"""Main game: states, camera, waves, stages, HUD."""
import random
import pygame
from pygame.math import Vector2
from settings import *
from entities import Player, Enemy, Projectile, CHARACTERS
from questions import QuestionPool
from quiz import QuizSession
import art

CODE_FROM_STAGE = 3

# Enemy types unlocked as stages progress.
STAGE_ENEMY_TYPES = {
    1: ["bug"],
    2: ["bug", "greenbug"],
    3: ["bug", "greenbug", "shooter"],
    4: ["bug", "greenbug", "shooter", "tank"],
    5: ["bug", "greenbug", "shooter", "tank"],
}


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.big = pygame.font.SysFont("consolas", 40, bold=True)
        self.font = pygame.font.SysFont("consolas", 22)
        self.small = pygame.font.SysFont("consolas", 16)
        self.tiny = pygame.font.SysFont("consolas", 13)

        # Pre-render character preview animations for the select screen
        self.char_previews = {k: art.PLAYER_MAKERS[k]() for k in CHARACTERS}
        self._anim_t = 0.0
        self._anim_i = 0

        self.state = "title"
        self.pool = QuestionPool()
        self.running = True

    # ------------------------------------------------------------- new game
    def start_run(self, char_key):
        self.player = Player(char_key)
        self.enemies = []
        self.projectiles = []
        self.enemy_projectiles = []
        self.cam = Vector2(0, 0)
        self.stage = 1
        self.wave = 1
        self.mode = "wave"           # "wave" or "boss"
        self.score = 0
        self.correct_total = 0
        self.quiz = None
        self.quiz_purpose = None
        self.spawn_delay = 0.0
        self.pool = QuestionPool()
        self._spawn_wave()
        self.state = "play"

    # --------------------------------------------------------------- waves
    def _spawn_wave(self):
        types = STAGE_ENEMY_TYPES[self.stage]
        count = 4 + self.stage * 2 + self.wave
        for _ in range(count):
            etype = random.choice(types)
            side = random.choice((-1, 1))
            x = clamp(self.player.pos.x + side * (SCREEN_W / 2 + random.randint(60, 300)),
                      40, WORLD_W - 40)
            y = random.uniform(FLOOR_Y + 30, WORLD_H - 40)
            scale = 1 + (self.stage - 1) * 0.25
            self.enemies.append(Enemy(etype, (x, y), hp_scale=scale,
                                      speed_scale=1 + (self.stage - 1) * 0.06,
                                      dmg_scale=scale))

    def _spawn_boss(self):
        self.enemies.append(Enemy("boss", (self.player.pos.x, FLOOR_Y + 120),
                                  hp_scale=1.0))
        # a few adds
        for _ in range(6):
            side = random.choice((-1, 1))
            x = clamp(self.player.pos.x + side * 500, 40, WORLD_W - 40)
            self.enemies.append(Enemy("shooter", (x, random.uniform(FLOOR_Y + 40, WORLD_H - 40))))

    def _wave_cleared(self):
        if self.mode == "boss":
            # boss defeated -> boss quiz
            self._start_quiz(num=1, use_code=False, boss=True, purpose="boss")
            return
        if self.stage < NUM_STAGES:
            if self.wave < WAVES_PER_STAGE:
                self.wave += 1
                self.spawn_delay = 1.2
            else:
                self._start_quiz(num=5, use_code=self.stage >= CODE_FROM_STAGE,
                                 boss=False, purpose="stage")
        else:  # final stage
            if self.wave < WAVES_PER_STAGE:
                self.wave += 1
                self.spawn_delay = 1.2
            else:
                # final test, then boss
                self._start_quiz(num=7, use_code=True, boss=False, purpose="final_test")

    def _start_quiz(self, num, use_code, boss, purpose):
        self.quiz = QuizSession(self.pool, self.stage, num, use_code=use_code, boss=boss)
        self.quiz.begin(self.player)
        self.quiz_purpose = purpose
        self.state = "quiz"

    def _end_quiz(self):
        purpose = self.quiz_purpose
        self.correct_total += self.quiz.correct_count
        # drop the player back onto the floor before combat resumes
        self.player.pos.y = (PLAY_FLOOR_TOP + PLAY_FLOOR_BOT) / 2
        self.quiz = None
        if purpose == "stage":
            self.stage += 1
            self.wave = 1
            self.mode = "wave"
            self.spawn_delay = 1.0
            self.state = "play"
        elif purpose == "final_test":
            self.mode = "boss"
            self._spawn_boss()
            self.state = "play"
        elif purpose == "boss":
            self.state = "victory"

    # -------------------------------------------------------------- camera
    def _update_camera(self):
        self.cam.x = clamp(self.player.pos.x - SCREEN_W / 2, 0, WORLD_W - SCREEN_W)
        self.cam.y = clamp(self.player.pos.y - SCREEN_H / 2, 0, WORLD_H - SCREEN_H)

    # ----------------------------------------------------------- main loop
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)
            self._handle_events()
            self._update(dt)
            self._draw()
            pygame.display.flip()
        pygame.quit()

    def _handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.running = False
                if self.state == "title":
                    self.state = "select"
                elif self.state == "select":
                    if e.key == pygame.K_1:
                        self.start_run("duck")
                    elif e.key == pygame.K_2:
                        self.start_run("penguin")
                    elif e.key == pygame.K_3:
                        self.start_run("robot")
                elif self.state == "play":
                    if e.key == pygame.K_e:
                        self.player.use_ability("shield", self.enemies)
                    elif e.key == pygame.K_q:
                        self.player.use_ability("parry", self.enemies)
                elif self.state in ("gameover", "victory"):
                    if e.key == pygame.K_RETURN:
                        self.state = "select"

    # ------------------------------------------------------------- update
    def _update(self, dt):
        self._anim_t += dt
        if self._anim_t > 0.14:
            self._anim_t = 0.0
            self._anim_i += 1

        if self.state == "play":
            self._update_play(dt)
        elif self.state == "quiz":
            keys = pygame.key.get_pressed()
            # player moves freely (can go up into the quiz room)
            self.player.update(dt, keys, [], self.projectiles,
                               allow_move=True, floor_bound=False)
            self._update_camera()
            self.quiz.update(dt, self.player)
            if self.quiz.finished:
                self._end_quiz()

    def _update_play(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys, self.enemies, self.projectiles)
        self._update_camera()

        # spawn delay between waves
        if self.spawn_delay > 0:
            self.spawn_delay -= dt
            if self.spawn_delay <= 0 and not self.enemies:
                self._spawn_wave()

        # enemies (move + apply touch damage per second)
        for en in self.enemies:
            en.update(dt, self.player, self.enemy_projectiles)
            if self.player.pos.distance_to(en.pos) < en.radius + self.player.radius:
                self.player.take_damage(en.touch_damage * dt)

        # player projectiles vs enemies
        for pr in self.projectiles:
            pr.update(dt)
            for en in self.enemies:
                if en.alive and id(en) not in pr.hit and \
                        pr.pos.distance_to(en.pos) < en.radius + 6:
                    en.take_damage(pr.damage)
                    self.player.heal_from_damage(pr.damage)
                    pr.hit.add(id(en))
                    if len(pr.hit) > pr.pierce:
                        pr.alive = False
                    if not en.alive:
                        self.score += 10
                    break

        # enemy projectiles vs player
        for pr in self.enemy_projectiles:
            pr.update(dt)
            if pr.pos.distance_to(self.player.pos) < self.player.radius + 6:
                self.player.take_damage(pr.damage)
                pr.alive = False

        # cleanup
        self.enemies = [e for e in self.enemies if e.alive]
        self.projectiles = [p for p in self.projectiles if p.alive]
        self.enemy_projectiles = [p for p in self.enemy_projectiles if p.alive]

        # death
        if self.player.hp <= 0:
            self.state = "gameover"
            return

        # wave cleared?
        if not self.enemies and self.spawn_delay <= 0:
            self._wave_cleared()

    # --------------------------------------------------------------- draw
    def _draw(self):
        if self.state == "title":
            self._draw_title()
        elif self.state == "select":
            self._draw_select()
        elif self.state in ("play", "quiz"):
            self._draw_world()
            if self.state == "quiz":
                self.quiz.draw(self.screen, self.cam, self.font, self.big,
                               self.small, player=self.player)
                self._draw_quiz_hud()
            else:
                self._draw_hud()
        elif self.state == "gameover":
            self._draw_end("GAME OVER", RED)
        elif self.state == "victory":
            self._draw_end("YOU BEAT THE KERNEL PANIC!", GREEN)

    def _draw_world(self):
        # sky gradient
        for y in range(0, FLOOR_Y - int(self.cam.y), 4):
            t = clamp((y + self.cam.y) / FLOOR_Y, 0, 1)
            col = [int(SKY_TOP[i] + (SKY_BOT[i] - SKY_TOP[i]) * t) for i in range(3)]
            pygame.draw.rect(self.screen, col, (0, y, SCREEN_W, 4))
        # floor
        floor_screen_y = FLOOR_Y - int(self.cam.y)
        pygame.draw.rect(self.screen, FLOOR_TOP,
                         (0, floor_screen_y, SCREEN_W, SCREEN_H - floor_screen_y))
        pygame.draw.line(self.screen, PRIMARY, (0, floor_screen_y),
                         (SCREEN_W, floor_screen_y), 3)
        # floor grid for depth
        for gx in range(0, WORLD_W, 80):
            sx = gx - int(self.cam.x)
            if 0 <= sx <= SCREEN_W and floor_screen_y < SCREEN_H:
                pygame.draw.line(self.screen, FLOOR_BOT, (sx, floor_screen_y),
                                 (sx, SCREEN_H), 1)

        for pr in self.enemy_projectiles:
            pr.draw(self.screen, self.cam)
        for en in self.enemies:
            en.draw(self.screen, self.cam)
        for pr in self.projectiles:
            pr.draw(self.screen, self.cam)
        self.player.draw(self.screen, self.cam)

    def _correct_counter(self, live_quiz=0):
        text = f"Correct  {self.correct_total + live_quiz}"
        t = self.font.render(text, True, GREEN)
        r = t.get_rect(topright=(SCREEN_W - 20, 18))
        pygame.draw.rect(self.screen, (18, 22, 40),
                         r.inflate(20, 10), border_radius=8)
        pygame.draw.rect(self.screen, GREEN, r.inflate(20, 10), 1, border_radius=8)
        self.screen.blit(t, r)

    def _draw_quiz_hud(self):
        # minimal HUD during quiz so nothing overlaps the question
        self._correct_counter(live_quiz=self.quiz.correct_count if self.quiz else 0)

    def _draw_hud(self):
        p = self.player
        # HP bar
        pygame.draw.rect(self.screen, (40, 40, 40), (20, 20, 260, 22), border_radius=6)
        ratio = clamp(p.hp / p.max_hp, 0, 1)
        col = GREEN if ratio > 0.4 else (YELLOW if ratio > 0.2 else RED)
        pygame.draw.rect(self.screen, col, (20, 20, int(260 * ratio), 22), border_radius=6)
        self.screen.blit(self.small.render(f"HP {int(max(0, p.hp))}/{int(p.max_hp)}",
                                           True, WHITE), (28, 22))
        # stage / wave / score
        if self.mode == "boss":
            info = f"STAGE {self.stage}  -  BOSS FIGHT"
        else:
            info = f"STAGE {self.stage}/{NUM_STAGES}   WAVE {self.wave}/{WAVES_PER_STAGE}"
        self.screen.blit(self.font.render(info, True, WHITE), (20, 50))
        self.screen.blit(self.small.render(f"Score {self.score}", True, DIM), (20, 78))
        self.screen.blit(self.small.render(f"Enemies {len(self.enemies)}", True, DIM), (140, 78))

        # correct counter (top-right)
        self._correct_counter()

        # abilities — only show the ones the player has unlocked
        unlocked = [(n, k) for n, k in (("shield", "E"), ("parry", "Q")) if n in p.abilities]
        x = SCREEN_W - 20 - len(unlocked) * 90
        for name, key in unlocked:
            ab = p.abilities[name]
            box = pygame.Rect(x, 52, 80, 40)
            ready = ab["timer"] <= 0
            pygame.draw.rect(self.screen, PRIMARY if ready else (50, 50, 60), box, border_radius=6)
            pygame.draw.rect(self.screen, WHITE, box, 2, border_radius=6)
            self.screen.blit(self.tiny.render(f"[{key}] {name[:5]}", True, WHITE), (x + 6, 58))
            if not ready:
                self.screen.blit(self.tiny.render(f"{ab['timer']:.1f}s", True, YELLOW), (x + 6, 74))
            else:
                self.screen.blit(self.tiny.render("READY", True, GREEN), (x + 6, 74))
            x += 90

        # controls hint (only mention unlocked abilities)
        hint = "WASD/Arrows move  -  auto-attack"
        if "shield" in p.abilities:
            hint += "  -  E shield"
        if "parry" in p.abilities:
            hint += "  -  Q parry"
        self.screen.blit(self.tiny.render(hint, True, DIM), (20, SCREEN_H - 24))

    def _draw_title(self):
        self.screen.fill(BLACK)
        self._center(self.big, "OS QUEST: SURVIVOR", 200, PRIMARY)
        self._center(self.font, "Learn Operating Systems. Survive the swarm.", 260, WHITE)
        self._center(self.font, "Press any key to start", 360, YELLOW)
        self._center(self.small, "A study game for the OS course", 420, DIM)

    def _draw_select(self):
        self.screen.fill(BLACK)
        self._center(self.big, "CHOOSE YOUR CHARACTER", 60, WHITE)
        keys = list(CHARACTERS.keys())
        for i, key in enumerate(keys):
            cx = SCREEN_W // 2 + (i - 1) * 300
            cy = 260
            base = CHARACTERS[key]
            # card
            card = pygame.Rect(cx - 130, cy - 120, 260, 320)
            pygame.draw.rect(self.screen, (30, 34, 52), card, border_radius=12)
            pygame.draw.rect(self.screen, PRIMARY, card, 2, border_radius=12)
            # animated preview (scaled up)
            frames = self.char_previews[key]
            img = frames[self._anim_i % len(frames)]
            big_img = pygame.transform.scale(img, (96, 96))
            self.screen.blit(big_img, big_img.get_rect(center=(cx, cy - 50)))
            self._center_at(self.font, base["name"], cx, cy + 20, WHITE)
            self._center_at(self.small, base["blurb"], cx, cy + 50, DIM)
            self._center_at(self.tiny, f"HP {base['hp']}  SPD {base['speed']:.1f}", cx, cy + 90, CYAN)
            self._center_at(self.tiny, f"DMG {base['damage']}  RATE {base['fire_rate']:.2f}s",
                            cx, cy + 110, CYAN)
            self._center_at(self.font, f"[{i+1}]", cx, cy + 150, YELLOW)
        self._center(self.small, "Press 1, 2 or 3 to select", 520, WHITE)

    def _draw_end(self, text, color):
        self.screen.fill(BLACK)
        self._center(self.big, text, 220, color)
        self._center(self.font, f"Final Score: {self.score}", 290, WHITE)
        self._center(self.font, f"Reached Stage {self.stage}", 330, DIM)
        self._center(self.font, "Press ENTER to play again", 410, YELLOW)

    # ------------------------------------------------------------- helpers
    def _center(self, font, text, y, color):
        t = font.render(text, True, color)
        self.screen.blit(t, t.get_rect(center=(SCREEN_W // 2, y)))

    def _center_at(self, font, text, x, y, color):
        t = font.render(text, True, color)
        self.screen.blit(t, t.get_rect(center=(x, y)))

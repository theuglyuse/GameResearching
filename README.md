# OS Quest: Survivor 🖥️🐧

A **survivor.io-style 2D action game** for learning **Operating Systems** concepts,
built with Python + pygame. Survive waves of enemies, and between stages answer OS
questions to earn perks and abilities. Get answers right to stand a chance against
the final **Kernel Panic** boss.

> There's also an older browser-based quiz version in the git history (HTML/CSS/JS).
> This Python version is the current game.

## How to run
```bash
pip install -r requirements.txt
python main.py
```

## Controls
| Action | Keys |
|--------|------|
| Move | **WASD** or **Arrow keys** |
| Attack | **Automatic** (targets nearest enemy) |
| Shield ability | **E** (once unlocked via a perk) |
| Parry ability | **Q** (once unlocked via a perk) |
| Select character | **1 / 2 / 3** |
| Quit | **Esc** |

## How it plays
1. **Choose a character** — Debug Duck (balanced), Linux Penguin (tanky), Compiler-Bot (fast).
2. **Survive waves** of enemies in a side-view arena. The world is larger than the
   screen and the camera follows you. The **floor** is the lower half; the **sky**
   above is where quizzes appear.
3. After ~3 waves, a **quiz** starts. Walk **up** onto an answer pad and **stand on it**
   to select. Correct answers let you step onto one of **three perk pads** to claim a reward.
4. It gets progressively harder each stage. From stage 3, some questions show **code snippets**.
5. **Stage 5** ends with a final test, then the **boss** — beat its **two-part question**
   (concept + the reason why) for a massive boost.

## Perks (20)
Movement/attack-speed boosts, extra projectiles, piercing, lifesteal, crits, drones,
firewall damage reduction, revive, slow aura, and unlockable **Shield** / **Parry**
cooldown abilities. See `perks.py`.

## Project structure
| File | Purpose |
|------|---------|
| `main.py` | Launcher |
| `settings.py` | Screen/world size, tuning constants |
| `art.py` | Programmatically-drawn animated sprites (no art assets needed) |
| `entities.py` | Player, Enemy variants, Projectile, Drone |
| `perks.py` | The 20 perks/abilities |
| `questions.py` | OS question bank + code snippets + boss two-part question |
| `quiz.py` | Interactive step-on-a-pad quiz system |
| `game.py` | Game loop, camera, waves, stages, HUD |

## Extending
- **Add questions:** edit `questions.py` (concept tiers 1–5, `CODE`, `BOSS_QUESTIONS`).
- **Add perks:** append to `PERKS` in `perks.py`.
- **New enemies:** add art in `art.py` and a branch in `entities.Enemy`.
- **Swap in real art:** replace the `make_*` functions in `art.py` with image loads.

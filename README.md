# OS Quest 🖥️

An educational, quiz-style browser game for learning core **Operating Systems** concepts.

Built as a college-course learning aid: pick a topic (or take the full challenge),
answer conceptual multiple-choice questions, and get an **explanation after every answer**
so you actually learn — not just test.

## Topics covered
- Processes & Threads
- CPU Scheduling
- Memory Management
- Deadlocks
- Synchronization
- File Systems

## How to run
Just open `index.html` in any web browser. No installation or build step needed.

## Files
| File | Purpose |
|------|---------|
| `index.html` | Page structure / screens (start, quiz, results) |
| `style.css`  | Styling and layout |
| `script.js`  | Game logic (state, rendering, scoring) |
| `questions.js` | The question bank — add questions here |

## Adding questions
Open `questions.js` and add an object to the relevant topic array:

```js
{
  question: "Your question?",
  options: ["A", "B", "C", "D"],
  answer: 2,               // index of the correct option (0-based)
  explanation: "Why the answer is correct — this teaches the concept."
}
```

## Roadmap ideas
- [ ] Timer / countdown per question
- [ ] Difficulty levels
- [ ] More question types (true/false, match, ordering steps)
- [ ] Persistent high scores (localStorage)
- [ ] Sound effects & animations

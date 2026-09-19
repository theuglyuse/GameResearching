// Question bank: concept questions (tiers 1-5), code-snippet questions, and the
// two-part boss question. A QuestionPool serves non-repeating, option-shuffled
// questions until a tier/pool is exhausted.

export const CONCEPT = {
  1: [
    { q: "What is a process?",
      options: ["A program stored on disk", "A program in execution",
        "A reserved block of the CPU cache", "A file waiting to be printed",
        "A hardware interrupt line"],
      answer: 1,
      explanation: "A process is a program in execution. The program on disk is passive; once loaded into memory with its own registers, stack and program counter, it becomes an active process." },
    { q: "Which part of the OS decides which process runs next on the CPU?",
      options: ["The loader", "The compiler", "The CPU scheduler", "The file system", "The linker"],
      answer: 2,
      explanation: "The CPU (short-term) scheduler picks which ready process gets the CPU next. It runs very frequently, so it must be fast." },
    { q: "What is the main job of an operating system?",
      options: ["To compile source code", "To manage hardware resources and provide services to programs",
        "To design CPUs", "To render 3D graphics only", "To connect to the internet only"],
      answer: 1,
      explanation: "An OS is a resource manager: it manages the CPU, memory, I/O and files, and provides abstractions so programs don't touch hardware directly." },
    { q: "Which of these is stored in a Process Control Block (PCB)?",
      options: ["The user's password", "The process state, program counter and registers",
        "The monitor resolution", "The Wi-Fi signal strength", "The BIOS version"],
      answer: 1,
      explanation: "The PCB holds everything the OS needs to manage a process: its state, program counter, CPU registers, memory limits, open files, and scheduling info." },
  ],
  2: [
    { q: "What is the key advantage of threads sharing an address space?",
      options: ["They can never cause bugs", "Communication between them is fast and cheap",
        "They never need scheduling", "They run on separate computers", "They eliminate the need for a CPU"],
      answer: 1,
      explanation: "Threads of one process share code, data and heap, so sharing data is cheap. The trade-off: you must synchronize access to avoid race conditions." },
    { q: "In Round Robin scheduling, what is the critical tuning parameter?",
      options: ["Priority", "Time quantum (time slice)", "Arrival order", "Number of CPUs", "Page size"],
      answer: 1,
      explanation: "Round Robin gives each process a fixed time quantum, then preempts it. Too large behaves like FCFS; too small wastes time on context switches." },
    { q: "A context switch requires the OS to...",
      options: ["Reboot the machine", "Save the old process's state and load the next one's",
        "Delete the running process", "Recompile the program", "Format the disk"],
      answer: 1,
      explanation: "During a context switch the running process's context (registers, PC) is saved to its PCB and the next process's context is restored. This is pure overhead." },
    { q: "Which scheduling algorithm gives the minimum average waiting time in theory?",
      options: ["FCFS", "Round Robin", "Shortest Job First", "Last Come First Served", "Random"],
      answer: 2,
      explanation: "Shortest Job First is provably optimal for average waiting time, but it needs to know/predict each job's CPU burst length in advance." },
  ],
  3: [
    { q: "A 'page fault' occurs when...",
      options: ["A page of memory is physically damaged", "The requested page is not currently in physical RAM",
        "Two processes read the same page", "The CPU overheats", "A file is deleted"],
      answer: 1,
      explanation: "A page fault means the page a program accessed isn't in RAM. The OS traps, fetches the page from disk (swap), possibly evicts another page, then resumes." },
    { q: "Paging primarily solves which problem of contiguous allocation?",
      options: ["Internal fragmentation", "External fragmentation", "Deadlock", "Starvation", "Race conditions"],
      answer: 1,
      explanation: "Paging removes external fragmentation: any free frame can hold any page, so memory need not be contiguous. A little internal fragmentation can remain in the last page." },
    { q: "What is a race condition?",
      options: ["Two CPUs running at different clock speeds",
        "When the result depends on the timing/order of concurrent access to shared data",
        "A type of deadlock", "A scheduling policy", "A disk defragmentation step"],
      answer: 1,
      explanation: "A race condition happens when concurrent threads access shared data and the outcome depends on their interleaving. Synchronization (locks/semaphores) prevents it." },
    { q: "What is a 'critical section'?",
      options: ["The most important function in a program",
        "Code that accesses shared data and must run mutually exclusively",
        "The kernel's boot loader", "A damaged disk sector", "The main() function"],
      answer: 1,
      explanation: "A critical section accesses shared resources; only one thread may be inside it at a time. A correct solution needs mutual exclusion, progress, and bounded waiting." },
  ],
  4: [
    { q: "Which is NOT one of the four necessary conditions for deadlock?",
      options: ["Mutual exclusion", "Hold and wait", "Preemption", "No preemption", "Circular wait"],
      answer: 2,
      explanation: "The four Coffman conditions are mutual exclusion, hold-and-wait, NO preemption, and circular wait. Allowing preemption actually helps PREVENT deadlock." },
    { q: "The Banker's Algorithm is a form of deadlock...",
      options: ["Detection", "Avoidance", "Recovery", "Prevention", "Ignorance"],
      answer: 1,
      explanation: "The Banker's Algorithm is deadlock AVOIDANCE: it grants a request only if the system stays in a 'safe state' where every process can still finish." },
    { q: "Which page-replacement algorithm can suffer Belady's anomaly?",
      options: ["LRU", "Optimal (OPT)", "FIFO", "Least Frequently Used", "Most Recently Used"],
      answer: 2,
      explanation: "Belady's anomaly = more frames causing MORE faults. It can happen with FIFO. Stack algorithms like LRU and OPT are immune to it." },
    { q: "Conceptually, how does a mutex differ from a binary semaphore?",
      options: ["They are always identical", "A mutex has ownership (only the locker may unlock it)",
        "A semaphore allows many threads at once", "A mutex cannot be locked", "A semaphore cannot reach zero"],
      answer: 1,
      explanation: "Both allow one thread at a time, but a mutex has ownership: the thread that locked it must unlock it. A semaphore can be signaled by any thread." },
  ],
  5: [
    { q: "In a resource-allocation graph with single-instance resources, a cycle means...",
      options: ["Efficient scheduling", "A guaranteed deadlock", "High throughput", "A page fault", "Nothing at all"],
      answer: 1,
      explanation: "With single-instance resources a cycle in the resource-allocation graph is both necessary AND sufficient for deadlock. With multiple instances it's only necessary." },
    { q: "What is 'thrashing' in virtual memory?",
      options: ["Deleting many files at once", "Spending more time paging in/out than doing useful work",
        "Overheating the CPU", "A fast disk-cache hit", "Encrypting the swap file"],
      answer: 1,
      explanation: "Thrashing occurs when processes have too few frames, so they constantly page-fault. The system spends most of its time swapping pages instead of doing real work." },
    { q: "What does a journaling file system's journal give you?",
      options: ["Faster reads only", "Recovery to a consistent state after a crash",
        "File compression", "Automatic encryption", "Unlimited storage"],
      answer: 1,
      explanation: "A journal records intended changes before applying them, so after a crash the FS can replay or roll back operations and stay consistent." },
    { q: "Why can the Test-and-Set instruction implement a lock correctly?",
      options: ["It is faster than other instructions",
        "It reads and writes a value atomically in one indivisible step",
        "It disables the network", "It runs only in user mode", "It never touches memory"],
      answer: 1,
      explanation: "Test-and-Set is atomic: it reads the old value and sets a new one without interruption. That atomicity is exactly what's needed to build a spinlock safely." },
  ],
};

export const CODE = [
  { code: "sem = Semaphore(1)\n\nsem.acquire()\n# ... critical section ...\nsem.release()",
    q: "What OS concept does this pattern implement?",
    options: ["A round-robin scheduler", "Mutual exclusion for a critical section",
      "A page replacement policy", "A deadlock recovery routine", "Disk defragmentation"],
    answer: 1,
    explanation: "A semaphore initialized to 1 used as acquire()/release() around a critical section enforces mutual exclusion: only one thread is inside at a time." },
  { code: "pid = fork()\nif pid == 0:\n    print('child')\nelse:\n    print('parent')",
    q: "After fork() succeeds, how many processes print a line?",
    options: ["Zero", "One", "Two", "Three", "It depends on the CPU"],
    answer: 2,
    explanation: "fork() creates a child copy. The parent gets the child's PID (nonzero) and the child gets 0, so both processes run: two lines." },
  { code: "lockA.acquire()\nlockB.acquire()   # Thread 1\n\n# Thread 2 does:\nlockB.acquire()\nlockA.acquire()",
    q: "What risk does this code create?",
    options: ["A memory leak", "A deadlock from inconsistent lock ordering",
      "A page fault", "Faster execution", "Nothing, it is safe"],
    answer: 1,
    explanation: "Two threads acquire the same locks in opposite orders. Each can hold one and wait for the other, a circular wait, i.e. classic deadlock. Fix: always lock in the same order." },
  { code: "while True:\n    p = pick_shortest_ready_job()\n    run_to_completion(p)",
    q: "Which scheduling policy does this loop resemble?",
    options: ["Round Robin", "First-Come First-Served", "Shortest Job First (non-preemptive)",
      "Priority with aging", "Multilevel feedback queue"],
    answer: 2,
    explanation: "It always runs the shortest available job to completion: non-preemptive Shortest Job First. Great average waiting time, but long jobs can starve." },
  { code: "counter = 0\n# Two threads each run:\nfor i in range(1000):\n    counter += 1",
    q: "Without synchronization, what is the final value of counter?",
    options: ["Exactly 2000, always", "Somewhere between 1000 and 2000 (nondeterministic)",
      "Always 1000", "Always 0", "Exactly 4000"],
    answer: 1,
    explanation: "counter += 1 is read-modify-write, not atomic. The two threads' operations interleave and lost updates occur (a race condition), so the result varies." },
];

export const BOSS_QUESTIONS = [
  { part1: { q: "BOSS - Part 1: A deadlock needs four conditions at once. Which strategy attacks the 'circular wait' condition?",
      options: ["Give every process infinite memory", "Impose a global ordering on resource acquisition",
        "Increase the time quantum", "Use a larger page size", "Disable interrupts forever"],
      answer: 1,
      explanation: "Requiring all processes to request resources in one global order makes a cycle impossible, breaking the circular-wait condition." },
    part2: { q: "BOSS - Part 2: WHY does a consistent global lock ordering prevent deadlock?",
      options: ["It makes the CPU faster", "It removes the possibility of a cyclic wait-for chain among processes",
        "It gives each process its own CPU", "It compresses memory", "It disables preemption"],
      answer: 1,
      explanation: "Deadlock needs a cycle in the wait-for graph. If everyone acquires resources in the same order, no cycle can form, so circular-wait can never hold." } },
  { part1: { q: "BOSS - Part 1: Which technique lets a system run programs whose combined size exceeds physical RAM?",
      options: ["Busy waiting", "Virtual memory with demand paging", "Round-robin scheduling", "Journaling", "Spinlocks"],
      answer: 1,
      explanation: "Virtual memory with demand paging keeps only needed pages in RAM and the rest on disk, so total program size can exceed physical memory." },
    part2: { q: "BOSS - Part 2: WHY does demand paging make this possible?",
      options: ["It deletes unused programs", "Pages are loaded only when accessed, so unused pages need not occupy RAM",
        "It overclocks the CPU", "It merges all processes into one", "It disables the MMU"],
      answer: 1,
      explanation: "Because pages are brought in lazily on first access, memory holds only the working set. Rarely used pages stay on disk, so RAM isn't the hard limit." } },
];

function shuffleOptions(q) {
  const idx = q.options.map((_, i) => i);
  for (let i = idx.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [idx[i], idx[j]] = [idx[j], idx[i]];
  }
  const out = {
    q: q.q,
    options: idx.map((i) => q.options[i]),
    answer: idx.indexOf(q.answer),
    explanation: q.explanation,
  };
  if (q.code) out.code = q.code;
  return out;
}

const clampTier = (t) => Math.max(1, Math.min(5, t));

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

export class QuestionPool {
  constructor() {
    this.usedConcept = new Set();
    this.usedCode = new Set();
    this.usedGlobal = new Set();   // question texts already asked this run
  }

  // Candidate concept questions for a tier (includes neighbouring tiers so a
  // single quiz always has enough DISTINCT questions to draw from).
  _conceptCandidates(tier) {
    const tiers = [...new Set([tier, tier - 1, tier + 1].filter((t) => t >= 1 && t <= 5))];
    const arr = [];
    for (const t of tiers) for (const q of CONCEPT[t]) arr.push(q);
    return arr;
  }

  // Draw `n` questions guaranteed unique within this quiz, preferring ones not
  // yet asked this run. Only reuses older questions if the bank runs dry.
  drawUnique(n, tier, useCode) {
    tier = clampTier(tier);
    let candidates = this._conceptCandidates(tier).slice();
    if (useCode) candidates = candidates.concat(CODE);
    // de-duplicate by question text
    const byText = new Map();
    for (const q of candidates) if (!byText.has(q.q)) byText.set(q.q, q);
    candidates = [...byText.values()];

    const chosen = [];
    const chosenText = new Set();
    const take = (list) => {
      for (const q of list) {
        if (chosen.length >= n) break;
        if (!chosenText.has(q.q)) { chosen.push(q); chosenText.add(q.q); }
      }
    };
    take(shuffle(candidates.filter((q) => !this.usedGlobal.has(q.q))));
    if (chosen.length < n) take(shuffle(candidates.filter((q) => !chosenText.has(q.q))));

    for (const q of chosen) this.usedGlobal.add(q.q);
    return chosen.map(shuffleOptions);
  }
  getConcept(tier) {
    tier = clampTier(tier);
    const pool = CONCEPT[tier];
    let avail = pool.map((_, i) => i).filter((i) => !this.usedConcept.has(`${tier}:${i}`));
    if (avail.length === 0) {
      for (const k of [...this.usedConcept]) if (k.startsWith(`${tier}:`)) this.usedConcept.delete(k);
      avail = pool.map((_, i) => i);
    }
    const idx = avail[Math.floor(Math.random() * avail.length)];
    this.usedConcept.add(`${tier}:${idx}`);
    return shuffleOptions(pool[idx]);
  }
  getCode() {
    let avail = CODE.map((_, i) => i).filter((i) => !this.usedCode.has(i));
    if (avail.length === 0) { this.usedCode.clear(); avail = CODE.map((_, i) => i); }
    const idx = avail[Math.floor(Math.random() * avail.length)];
    this.usedCode.add(idx);
    return shuffleOptions(CODE[idx]);
  }
  getBoss() {
    return BOSS_QUESTIONS[Math.floor(Math.random() * BOSS_QUESTIONS.length)];
  }
}

"""Question bank for the between-wave quizzes.

Three kinds of questions:
  * CONCEPT questions (grouped by difficulty tier 1-5)
  * CODE questions (a snippet -> what does it do / output)
  * BOSS question (two parts: a concept + the reason why)

All multiple-choice questions have ~5 options.
`answer` is the 0-based index of the correct option.
`explanation` teaches the concept and expands on it.

A QuestionPool tracks what has been asked so questions don't repeat until
the pool is exhausted.
"""
import random

# --------------------------------------------------------- CONCEPT QUESTIONS
# Tiered by difficulty (1 = easiest). The stage number selects the tier so the
# quiz gets harder as you progress.
CONCEPT = {
    1: [
        {
            "q": "What is a process?",
            "options": [
                "A program stored on disk",
                "A program in execution",
                "A reserved block of the CPU cache",
                "A file waiting to be printed",
                "A hardware interrupt line",
            ],
            "answer": 1,
            "explanation": "A process is a program in execution. The program on disk is passive; "
                           "once loaded into memory with its own registers, stack and program counter, "
                           "it becomes an active process.",
        },
        {
            "q": "Which part of the OS decides which process runs next on the CPU?",
            "options": ["The loader", "The compiler", "The CPU scheduler",
                        "The file system", "The linker"],
            "answer": 2,
            "explanation": "The CPU (short-term) scheduler picks which ready process gets the CPU next. "
                           "It runs very frequently, so it must be fast.",
        },
        {
            "q": "What is the main job of an operating system?",
            "options": [
                "To compile source code",
                "To manage hardware resources and provide services to programs",
                "To design CPUs",
                "To render 3D graphics only",
                "To connect to the internet only",
            ],
            "answer": 1,
            "explanation": "An OS is a resource manager: it manages the CPU, memory, I/O and files, "
                           "and provides an abstraction/interface so programs don't touch hardware directly.",
        },
        {
            "q": "Which of these is stored in a Process Control Block (PCB)?",
            "options": [
                "The user's password",
                "The process state, program counter and registers",
                "The monitor resolution",
                "The Wi-Fi signal strength",
                "The BIOS version",
            ],
            "answer": 1,
            "explanation": "The PCB holds all the info the OS needs to manage a process: its state, "
                           "program counter, CPU registers, memory limits, open files, and scheduling info.",
        },
    ],
    2: [
        {
            "q": "What is the key advantage of threads sharing an address space?",
            "options": [
                "They can never cause bugs",
                "Communication between them is fast and cheap",
                "They never need scheduling",
                "They run on separate computers",
                "They eliminate the need for a CPU",
            ],
            "answer": 1,
            "explanation": "Threads of one process share code, data and heap, so sharing data is cheap. "
                           "The trade-off: you must synchronize access to avoid race conditions.",
        },
        {
            "q": "In Round Robin scheduling, what is the critical tuning parameter?",
            "options": ["Priority", "Time quantum (time slice)", "Arrival order",
                        "Number of CPUs", "Page size"],
            "answer": 1,
            "explanation": "Round Robin gives each process a fixed time quantum, then preempts it. "
                           "Too large behaves like FCFS; too small wastes time on context switches.",
        },
        {
            "q": "A context switch requires the OS to...",
            "options": [
                "Reboot the machine",
                "Save the old process's state and load the next one's",
                "Delete the running process",
                "Recompile the program",
                "Format the disk",
            ],
            "answer": 1,
            "explanation": "During a context switch the running process's context (registers, PC) is saved "
                           "to its PCB and the next process's context is restored. This is pure overhead.",
        },
        {
            "q": "Which scheduling algorithm gives the minimum average waiting time in theory?",
            "options": ["FCFS", "Round Robin", "Shortest Job First",
                        "Last Come First Served", "Random"],
            "answer": 2,
            "explanation": "Shortest Job First is provably optimal for average waiting time, but it needs "
                           "to know/predict each job's CPU burst length in advance.",
        },
    ],
    3: [
        {
            "q": "A 'page fault' occurs when...",
            "options": [
                "A page of memory is physically damaged",
                "The requested page is not currently in physical RAM",
                "Two processes read the same page",
                "The CPU overheats",
                "A file is deleted",
            ],
            "answer": 1,
            "explanation": "A page fault means the page a program accessed isn't in RAM. The OS traps, "
                           "fetches the page from disk (swap), possibly evicts another page, then resumes.",
        },
        {
            "q": "Paging primarily solves which problem of contiguous allocation?",
            "options": ["Internal fragmentation", "External fragmentation",
                        "Deadlock", "Starvation", "Race conditions"],
            "answer": 1,
            "explanation": "Paging removes external fragmentation: any free frame can hold any page, so "
                           "memory need not be contiguous. A little internal fragmentation can remain in the last page.",
        },
        {
            "q": "What is a race condition?",
            "options": [
                "Two CPUs running at different clock speeds",
                "When the result depends on the timing/order of concurrent access to shared data",
                "A type of deadlock",
                "A scheduling policy",
                "A disk defragmentation step",
            ],
            "answer": 1,
            "explanation": "A race condition happens when concurrent threads access shared data and the outcome "
                           "depends on their interleaving. Synchronization (locks/semaphores) prevents it.",
        },
        {
            "q": "What is a 'critical section'?",
            "options": [
                "The most important function in a program",
                "Code that accesses shared data and must run mutually exclusively",
                "The kernel's boot loader",
                "A damaged disk sector",
                "The main() function",
            ],
            "answer": 1,
            "explanation": "A critical section accesses shared resources; only one thread may be inside it at "
                           "a time. A correct solution needs mutual exclusion, progress, and bounded waiting.",
        },
    ],
    4: [
        {
            "q": "Which is NOT one of the four necessary conditions for deadlock?",
            "options": ["Mutual exclusion", "Hold and wait", "Preemption",
                        "No preemption", "Circular wait"],
            "answer": 2,
            "explanation": "The four Coffman conditions are mutual exclusion, hold-and-wait, NO preemption, "
                           "and circular wait. Allowing preemption actually helps PREVENT deadlock.",
        },
        {
            "q": "The Banker's Algorithm is a form of deadlock...",
            "options": ["Detection", "Avoidance", "Recovery", "Prevention", "Ignorance"],
            "answer": 1,
            "explanation": "The Banker's Algorithm is deadlock AVOIDANCE: it grants a request only if the "
                           "system stays in a 'safe state' where every process can still finish.",
        },
        {
            "q": "Which page-replacement algorithm can suffer Belady's anomaly?",
            "options": ["LRU", "Optimal (OPT)", "FIFO",
                        "Least Frequently Used", "Most Recently Used"],
            "answer": 2,
            "explanation": "Belady's anomaly = more frames causing MORE faults. It can happen with FIFO. "
                           "Stack algorithms like LRU and OPT are immune to it.",
        },
        {
            "q": "Conceptually, how does a mutex differ from a binary semaphore?",
            "options": [
                "They are always identical",
                "A mutex has ownership (only the locker may unlock it)",
                "A semaphore allows many threads at once",
                "A mutex cannot be locked",
                "A semaphore cannot reach zero",
            ],
            "answer": 1,
            "explanation": "Both allow one thread at a time, but a mutex has ownership: the thread that "
                           "locked it must unlock it. A semaphore can be signaled by any thread.",
        },
    ],
    5: [
        {
            "q": "In a resource-allocation graph with single-instance resources, a cycle means...",
            "options": [
                "Efficient scheduling",
                "A guaranteed deadlock",
                "High throughput",
                "A page fault",
                "Nothing at all",
            ],
            "answer": 1,
            "explanation": "With single-instance resources a cycle in the resource-allocation graph is both "
                           "necessary AND sufficient for deadlock. With multiple instances it's only necessary.",
        },
        {
            "q": "What is 'thrashing' in virtual memory?",
            "options": [
                "Deleting many files at once",
                "Spending more time paging in/out than executing useful work",
                "Overheating the CPU",
                "A fast disk-cache hit",
                "Encrypting the swap file",
            ],
            "answer": 1,
            "explanation": "Thrashing occurs when processes have too few frames, so they constantly page-fault. "
                           "The system spends most of its time swapping pages instead of doing real work.",
        },
        {
            "q": "What does a journaling file system's journal give you?",
            "options": [
                "Faster reads only",
                "Recovery to a consistent state after a crash",
                "File compression",
                "Automatic encryption",
                "Unlimited storage",
            ],
            "answer": 1,
            "explanation": "A journal records intended changes before applying them, so after a crash the FS "
                           "can replay or roll back operations and stay consistent.",
        },
        {
            "q": "Why can the Test-and-Set instruction implement a lock correctly?",
            "options": [
                "It is faster than other instructions",
                "It reads and writes a value atomically in one indivisible step",
                "It disables the network",
                "It runs only in user mode",
                "It never touches memory",
            ],
            "answer": 1,
            "explanation": "Test-and-Set is atomic: it reads the old value and sets a new one without "
                           "interruption. That atomicity is exactly what's needed to build a spinlock safely.",
        },
    ],
}

# ------------------------------------------------------------- CODE QUESTIONS
# Shown from CODE_SNIPPET_WAVE onward. `code` is a multi-line string.
CODE = [
    {
        "code": "sem = Semaphore(1)\n\nsem.acquire()\n# ... critical section ...\nsem.release()",
        "q": "What OS concept does this pattern implement?",
        "options": [
            "A round-robin scheduler",
            "Mutual exclusion for a critical section",
            "A page replacement policy",
            "A deadlock recovery routine",
            "Disk defragmentation",
        ],
        "answer": 1,
        "explanation": "A semaphore initialized to 1 used as acquire()/release() around a critical section "
                       "enforces mutual exclusion: only one thread is inside at a time.",
    },
    {
        "code": "pid = fork()\nif pid == 0:\n    print('child')\nelse:\n    print('parent')",
        "q": "After fork() succeeds, how many processes print a line?",
        "options": ["Zero", "One", "Two", "Three", "It depends on the CPU"],
        "answer": 2,
        "explanation": "fork() creates a child copy. The parent gets the child's PID (nonzero) and the child "
                       "gets 0, so both processes run — one prints 'child', the other 'parent': two lines.",
    },
    {
        "code": "lockA.acquire()\nlockB.acquire()   # Thread 1\n\n# Thread 2 does:\nlockB.acquire()\nlockA.acquire()",
        "q": "What risk does this code create?",
        "options": [
            "A memory leak",
            "A deadlock from inconsistent lock ordering",
            "A page fault",
            "Faster execution",
            "Nothing, it is safe",
        ],
        "answer": 1,
        "explanation": "Two threads acquire the same locks in opposite orders. Each can hold one and wait "
                       "for the other — a circular wait, i.e. classic deadlock. Fix: always lock in the same order.",
    },
    {
        "code": "while True:\n    p = pick_shortest_ready_job()\n    run_to_completion(p)",
        "q": "Which scheduling policy does this loop resemble?",
        "options": [
            "Round Robin",
            "First-Come First-Served",
            "Shortest Job First (non-preemptive)",
            "Priority with aging",
            "Multilevel feedback queue",
        ],
        "answer": 2,
        "explanation": "It always runs the shortest available job to completion — non-preemptive Shortest Job "
                       "First. Great average waiting time, but long jobs can starve.",
    },
    {
        "code": "counter = 0\n# Two threads each run:\nfor i in range(1000):\n    counter += 1",
        "q": "Without synchronization, what is the final value of counter?",
        "options": [
            "Exactly 2000, always",
            "Somewhere between 1000 and 2000 (nondeterministic)",
            "Always 1000",
            "Always 0",
            "Exactly 4000",
        ],
        "answer": 1,
        "explanation": "counter += 1 is read-modify-write, not atomic. The two threads' operations interleave "
                       "and lost updates occur — a race condition — so the result varies, often below 2000.",
    },
]

# --------------------------------------------------------------- BOSS FIGHT
# Two-part question: answer BOTH parts correctly for a huge boost.
BOSS_QUESTIONS = [
    {
        "part1": {
            "q": "BOSS — Part 1: A deadlock requires four conditions to hold simultaneously. "
                 "Which single strategy attacks the 'circular wait' condition?",
            "options": [
                "Give every process infinite memory",
                "Impose a global ordering on resource acquisition",
                "Increase the time quantum",
                "Use a larger page size",
                "Disable interrupts forever",
            ],
            "answer": 1,
            "explanation": "Requiring all processes to request resources in one global order makes a cycle "
                           "impossible, breaking the circular-wait condition.",
        },
        "part2": {
            "q": "BOSS — Part 2: WHY does a consistent global lock ordering prevent deadlock?",
            "options": [
                "It makes the CPU faster",
                "It removes the possibility of a cyclic wait-for chain among processes",
                "It gives each process its own CPU",
                "It compresses memory",
                "It disables preemption",
            ],
            "answer": 1,
            "explanation": "Deadlock needs a cycle in the wait-for graph. If everyone acquires resources in the "
                           "same order, no cycle can form, so the circular-wait condition can never be satisfied.",
        },
    },
    {
        "part1": {
            "q": "BOSS — Part 1: Which technique lets a system run programs whose combined size "
                 "exceeds physical RAM?",
            "options": [
                "Busy waiting",
                "Virtual memory with demand paging",
                "Round-robin scheduling",
                "Journaling",
                "Spinlocks",
            ],
            "answer": 1,
            "explanation": "Virtual memory with demand paging keeps only needed pages in RAM and the rest on "
                           "disk, so total program size can exceed physical memory.",
        },
        "part2": {
            "q": "BOSS — Part 2: WHY does demand paging make this possible?",
            "options": [
                "It deletes unused programs",
                "Pages are loaded only when accessed, so unused pages need not occupy RAM",
                "It overclocks the CPU",
                "It merges all processes into one",
                "It disables the MMU",
            ],
            "answer": 1,
            "explanation": "Because pages are brought in lazily on first access, memory holds only the working "
                           "set. Rarely used pages stay on disk, so RAM isn't the hard limit on program size.",
        },
    },
]


class QuestionPool:
    """Serves random, non-repeating questions until exhausted, then resets."""

    def __init__(self):
        self._used_concept = set()
        self._used_code = set()

    def get_concept(self, tier):
        tier = max(1, min(5, tier))
        pool = CONCEPT[tier]
        available = [i for i in range(len(pool)) if (tier, i) not in self._used_concept]
        if not available:
            # exhausted this tier -> reset it
            self._used_concept = {k for k in self._used_concept if k[0] != tier}
            available = list(range(len(pool)))
        idx = random.choice(available)
        self._used_concept.add((tier, idx))
        return _shuffled(pool[idx])

    def get_code(self):
        available = [i for i in range(len(CODE)) if i not in self._used_code]
        if not available:
            self._used_code.clear()
            available = list(range(len(CODE)))
        idx = random.choice(available)
        self._used_code.add(idx)
        q = _shuffled(CODE[idx])
        q["code"] = CODE[idx]["code"]
        return q

    def get_boss(self):
        return random.choice(BOSS_QUESTIONS)


def _shuffled(q):
    """Return a copy of the question with its options shuffled (answer index fixed up)."""
    opts = list(enumerate(q["options"]))
    random.shuffle(opts)
    new_options = [text for _, text in opts]
    new_answer = next(i for i, (orig, _) in enumerate(opts) if orig == q["answer"])
    out = {
        "q": q["q"],
        "options": new_options,
        "answer": new_answer,
        "explanation": q["explanation"],
    }
    if "code" in q:
        out["code"] = q["code"]
    return out

// Question bank for the OS Quiz Game.
// Each topic has an array of questions.
// Question shape:
// {
//   question: string,
//   options: [string, string, string, string],
//   answer: number (index of correct option),
//   explanation: string  // shown after answering, to teach the concept
// }

const QUESTION_BANK = {
  "Processes & Threads": [
    {
      question: "What is a process?",
      options: [
        "A program stored on disk",
        "A program in execution",
        "A section of memory reserved for the OS",
        "A hardware interrupt handler"
      ],
      answer: 1,
      explanation:
        "A process is a program in execution. The program itself is a passive entity on disk; it becomes a process (an active entity) once loaded into memory and running."
    },
    {
      question: "Which of the following is NOT typically part of a process's memory layout?",
      options: ["Stack", "Heap", "Text (code) segment", "The CPU scheduler"],
      answer: 3,
      explanation:
        "A process's address space includes the text (code), data, heap, and stack segments. The CPU scheduler is part of the OS kernel, not the process's memory."
    },
    {
      question: "What is the main advantage of threads over separate processes?",
      options: [
        "Threads cannot crash",
        "Threads share the same address space, making communication cheaper",
        "Threads never need synchronization",
        "Threads run on separate machines"
      ],
      answer: 1,
      explanation:
        "Threads within a process share the same address space (code, data, heap), so sharing data is fast and cheap. This also means synchronization IS needed to avoid race conditions."
    },
    {
      question: "A context switch occurs when the CPU switches from one process to another. What is stored/restored?",
      options: [
        "Only the program counter",
        "The process's entire memory",
        "The process's context/state (registers, PC, etc.) via the PCB",
        "Nothing — switching is instantaneous"
      ],
      answer: 2,
      explanation:
        "During a context switch, the state of the running process (registers, program counter, etc.) is saved into its Process Control Block (PCB), and the next process's state is restored. This has overhead."
    }
  ],

  "CPU Scheduling": [
    {
      question: "Which scheduling algorithm can cause 'starvation' of low-priority processes?",
      options: ["Round Robin", "First-Come First-Served", "Priority Scheduling", "FIFO"],
      answer: 2,
      explanation:
        "In Priority Scheduling, low-priority processes may wait indefinitely if higher-priority processes keep arriving. 'Aging' (gradually increasing priority of waiting processes) is a common fix."
    },
    {
      question: "What is the key parameter that defines Round Robin scheduling?",
      options: ["Priority level", "Time quantum (time slice)", "Burst length", "Arrival time"],
      answer: 1,
      explanation:
        "Round Robin gives each process a fixed time quantum. If it doesn't finish, it's preempted and moved to the back of the ready queue. A small quantum = more responsiveness but more context-switch overhead."
    },
    {
      question: "Which algorithm gives the minimum average waiting time (in theory)?",
      options: [
        "First-Come First-Served",
        "Round Robin",
        "Shortest Job First (SJF)",
        "Last-Come First-Served"
      ],
      answer: 2,
      explanation:
        "Shortest Job First is provably optimal for minimizing average waiting time. Its drawback: it requires knowing (or predicting) the CPU burst length in advance."
    },
    {
      question: "The 'convoy effect' — short processes waiting behind a long one — is a problem in which algorithm?",
      options: ["SJF", "First-Come First-Served (FCFS)", "Priority", "Multilevel Queue"],
      answer: 1,
      explanation:
        "FCFS is non-preemptive, so a long process arriving first forces all later (possibly short) processes to wait, hurting average waiting time. This is the convoy effect."
    }
  ],

  "Memory Management": [
    {
      question: "What is the purpose of virtual memory?",
      options: [
        "To make the CPU faster",
        "To let programs use more memory than physically available",
        "To store files permanently",
        "To eliminate the need for RAM"
      ],
      answer: 1,
      explanation:
        "Virtual memory lets a process use an address space larger than physical RAM by keeping only needed pages in memory and the rest on disk (swap), loaded on demand via paging."
    },
    {
      question: "A 'page fault' occurs when:",
      options: [
        "A page is corrupted",
        "The requested page is not currently in physical memory",
        "The CPU overheats",
        "Two processes access the same page"
      ],
      answer: 1,
      explanation:
        "A page fault happens when a program accesses a page not currently in RAM. The OS then fetches it from disk into memory, possibly evicting another page."
    },
    {
      question: "What problem does paging primarily solve compared to contiguous allocation?",
      options: [
        "Internal fragmentation",
        "External fragmentation",
        "CPU scheduling",
        "Deadlock"
      ],
      answer: 1,
      explanation:
        "Paging eliminates external fragmentation because any free frame can be used for any page — memory need not be contiguous. (Some internal fragmentation can still occur in the last page.)"
    },
    {
      question: "Which page replacement algorithm can suffer from Belady's anomaly?",
      options: ["LRU", "Optimal", "FIFO", "None of them"],
      answer: 2,
      explanation:
        "Belady's anomaly is when adding more frames INCREASES page faults. It can occur with FIFO. Stack-based algorithms like LRU and Optimal are immune to it."
    }
  ],

  "Deadlocks": [
    {
      question: "Which of these is NOT one of the four necessary conditions for deadlock?",
      options: ["Mutual exclusion", "Hold and wait", "Preemption", "Circular wait"],
      answer: 2,
      explanation:
        "The four Coffman conditions are: Mutual Exclusion, Hold and Wait, NO Preemption, and Circular Wait. 'Preemption' (allowing resources to be taken away) actually PREVENTS deadlock."
    },
    {
      question: "The Banker's Algorithm is used for deadlock:",
      options: ["Detection", "Avoidance", "Recovery", "Prevention"],
      answer: 1,
      explanation:
        "The Banker's Algorithm is a deadlock AVOIDANCE technique. It only grants a resource request if the system remains in a 'safe state' where all processes can eventually finish."
    },
    {
      question: "What does a cycle in a resource-allocation graph (with single instances) indicate?",
      options: [
        "Efficient scheduling",
        "A deadlock",
        "High CPU usage",
        "A page fault"
      ],
      answer: 1,
      explanation:
        "With single-instance resources, a cycle in the resource-allocation graph means deadlock. (With multiple instances, a cycle is necessary but not sufficient.)"
    }
  ],

  "Synchronization": [
    {
      question: "What is a race condition?",
      options: [
        "When two CPUs run at different speeds",
        "When the outcome depends on the timing/order of concurrent operations on shared data",
        "A scheduling algorithm",
        "A type of deadlock"
      ],
      answer: 1,
      explanation:
        "A race condition occurs when multiple threads access shared data concurrently and the result depends on their timing. Proper synchronization (locks, semaphores) prevents it."
    },
    {
      question: "A 'critical section' is:",
      options: [
        "The most important function in a program",
        "A code segment that accesses shared resources and must not be executed by more than one thread at a time",
        "The kernel's main loop",
        "A section of disk"
      ],
      answer: 1,
      explanation:
        "A critical section is code that accesses shared data; only one thread should be inside it at a time. Solutions must ensure mutual exclusion, progress, and bounded waiting."
    },
    {
      question: "What is the difference between a binary semaphore and a mutex (conceptually)?",
      options: [
        "They are exactly the same in all cases",
        "A mutex has ownership (only the locker can unlock); a semaphore does not",
        "A semaphore can only be 0",
        "A mutex allows many threads at once"
      ],
      answer: 1,
      explanation:
        "Though a binary semaphore and a mutex both allow one thread at a time, a mutex has the concept of ownership — the thread that locks it must unlock it. A semaphore can be signaled by any thread."
    }
  ],

  "File Systems": [
    {
      question: "What is an inode in a Unix-like file system?",
      options: [
        "The file's name",
        "A data structure storing metadata about a file (permissions, size, block pointers)",
        "The first block of every file",
        "A network address"
      ],
      answer: 1,
      explanation:
        "An inode stores a file's metadata: permissions, owner, size, timestamps, and pointers to data blocks — but NOT the file's name (names live in directory entries that map to inode numbers)."
    },
    {
      question: "Which file allocation method suffers from external fragmentation?",
      options: ["Linked allocation", "Indexed allocation", "Contiguous allocation", "Inode allocation"],
      answer: 2,
      explanation:
        "Contiguous allocation requires each file to occupy consecutive blocks, leading to external fragmentation over time (free space split into small unusable gaps)."
    },
    {
      question: "What is the main purpose of a file system journal?",
      options: [
        "To speed up reading files",
        "To help recover to a consistent state after a crash",
        "To compress files",
        "To encrypt data"
      ],
      answer: 1,
      explanation:
        "A journaling file system records intended changes in a journal before applying them, so after a crash it can replay or roll back operations to keep the file system consistent."
    }
  ]
};

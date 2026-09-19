OS Quest — Post-Play Assessment: Answer Key
===========================================

1. B  — SJF order is P2(2), P3(4), P1(8). P1 starts after 2+4=6 ms, so its waiting time is 6 ms.
2. B  — RR q=4: P1 runs 0-4 (2 left), P2 runs 4-7 and FINISHES, P1 runs 7-9. P2 completes first (t=7).
3. B  — Opposite lock ordering is a POTENTIAL (not guaranteed) deadlock; it occurs only on the bad interleaving where each thread grabs its first lock before the other grabs its second.
4. B  — LRU faults on 7,0,1,2,0,3,0,4: 7*,0*,1*,2*(evict7),0hit,3*(evict1),0hit,4*(evict2) = 6 faults.
5. A  — Increasing frames yet getting MORE faults is Belady's anomaly, which can occur under FIFO. LRU and OPT are stack algorithms and are immune.
6. D  — The most any interleaving can produce is 2000 (min is 1000). 3000 exceeds the total number of increments, so it is impossible.
7. B  — Acquiring mutex before empty means a full-buffer producer blocks on empty while still holding mutex; consumers can't enter to free a slot -> deadlock. Correct order is wait(empty) then wait(mutex).
8. B  — A mutex has ownership: only the locking thread may unlock it. Another thread unlocking it is a bug (undefined behavior), unlike a semaphore which any thread can signal.
9. B  — Nearest to 50 is 43 (dist 7). From 43, nearest remaining is 24 (dist 19) vs 82 (dist 39), so 24 is next. Order: 43, then 24.
10. C — Two successive forks create 2^2 = 4 processes, so "hi" prints 4 times.

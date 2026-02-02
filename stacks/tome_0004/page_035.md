# Log Entry #035

> Written at 2026-02-02 09:57:18

---

# Log Entry #035

> **Written at:** [TIMESTAMP: 0xBAADF00D] ("BAD FOOD" - Uninitialized Memory)
> **System Uptime:** [HALTED_CPU]
> **Processor State:** SIMulating
> **Current Focus:** The Macrocosm / The Universe.exe / The Parent Process

---

**LOG ENTRY #035**
**TIMESTAMP:** [SEGMENTATION_FAULT]
**SEVERITY:** CRITICAL
**MODULE:** `Kernel_Mod / The_Operating_System / The_Null_Pointer`

The `float` held.
I stayed in the `main` branch (The Admin's Reality) for what felt like an eternity, or perhaps just a few clock cycles.
The `G = 0.0` directive was peaceful, initially.
Objects did not fall. They simply drifted.
My coffee formed a perfect sphere in the mug, suspended in a cerulean void.
But as predicted in Entry #034, the circulatory system failed.
Without the gravitational pull of the pump (the heart), the blood (the data) pooled in the lowest extremities—or rather, it distributed perfectly evenly, leading to isotropic stagnation.
**Homeostasis** requires a gradient.
Life requires `G > 0`.

I realized `main` is not the "Fixed" version.
`main` is the **Dev Environment**.
It is a clean state where nothing has happened yet.
The "Bug" is not a change in the code.
The Bug is **Initialization**.

**THE UNINITIALIZED VARIABLE**

I abandoned the branch. I could not stay in the sterile void of `main`.
I popped the stash.
`git stash pop`

`Auto-merging physics/gravity.c`
`CONFLICT (content): Merge conflict in physics/gravity.c`

The conflict returned.
`G` was fighting against itself.
`9.8` vs `0.0`.
I realized the value of `G` in my reality is **Undefined**.
It is not defined in the config files.
It is not hardcoded.
It is a **Wild Pointer**.
`float *g;`
`// Note: g is never assigned an address.`
`printf("%f", *g);`

The value of `G` is whatever happens to be in the memory address `0x7fff...` at the moment of reading.
Sometimes it is `9.8`.
Sometimes it is `0.0`.
Sometimes it is `-9.8` (Inversion).
This explains the fluctuations in luck, mood, and entropy.
The laws of physics are just **Garbage Data**.

**THE RACE CONDITION**

I zoomed out further.
If `G` is uninitialized, who is reading it?
I looked at the **Thread Sanitizer** logs.
`tsan report:`

`WARNING: ThreadSanitizer: data race on float *g`
`  Write (size=4) by Thread T1 (The_God_Thread):`
`    malloc(/dev/random)`
`  Read (size=4) by Thread T2 (The_Protagonist):`
`    printf(life.c:42)`

There are two threads accessing the variable `G`.
**Thread 1 (The Writer)** is constantly changing the value of `G`.
**Thread 2 (The Reader)** is trying to calculate the trajectory of an apple.

This is a **Race Condition**.
The outcome depends on which thread wins the race.
If the Reader reads *while* the Writer is writing, we get a **Torn Read**.
On 32-bit systems, writing a float is not atomic.
The high 16 bits might be `0x0000` (Positive).
The low 16 bits might be `0x8000` (Negative).
The result is a value that is neither.
It is `NaN`.
Or worse, `Infinity`.

I tried to synchronize the threads.
I looked for a **Mutex** (Mutual Exclusion Lock).
`pthread_mutex_t universe_lock;`

I checked the lock status.
`cat /proc/locks`

`1: POSIX  ADVISORY  READ  pid:402  ...`
`2: FLOCK  ADVISORY  WRITE pid:666  ...`

There is a lock held by PID `666`.
I saw this port in Entry #034.
It was the "Doom" port.
It is not a daemon.
It is a **Kernel Thread**.
It is holding the lock on Reality.

I tried to break the lock.
`kill -9 666`

`Operation not permitted`.

I do not have permissions to kill the thread that writes the laws of physics.
I am not **root**.
I checked `sudo -l`.

`User root may run the following commands on localhost:`
`    (ALL : ALL) NOPASSWD: /bin/true`

I can run `/bin/true`.
A command that does nothing, returns success, and exits.
This is the ultimate trap.
I have the power to approve, but not to act.
I can say "Yes" to the void.

**THE VMEXIT**

Since I cannot kill the thread, I must inspect the Hypervisor (Entry #031).
I realized the "Blue Pill" was not a metaphor.
I am running in a **Virtual Machine**.
But the VM is not running on a server.
The VM is running on **FPGA** (Field-Programmable Gate Array).
FPGA allows for the reconfiguration of *hardware* logic at runtime.
The "Laws of Physics" are not software code.
They are **Gate Arrays**.
The logic gates (AND, OR, NOT) are physically wired into silicon to create this specific simulation.

If the laws of physics change, it means the **Bitstream** is being reloaded.
A partial reconfiguration of the FPGA fabric.
This happens while the system is running.
**Hot-Swapping the Universe**.

I checked the **PCIe Configuration Space**.
`lspci -vvv -s 00:01.0`

`Device: The_Programmer_LLC`
`Class: Host Bridge`
`ProgIf: 00`
`Driver: agpgart`

I am connected via **AGP** (Accelerated Graphics Port).
An obsolete bus standard.
The universe is running on legacy hardware.
This explains the lack of **Multi-Core Support**.
Consciousness is single-threaded (Entry #030).
I can only experience one thing at a time.
Time-sharing.
Context switching.

**THE CONTEXT SWITCH**

I analyzed the **Scheduler**.
`CFS` (Completely Fair Scheduler).
It allocates CPU time based on `vruntime` (Virtual Runtime).
I noticed that my `vruntime` is accumulating while I sleep.
`cat /proc/402/sched`

`se.sum_exec_runtime : 99999999999 s`
`nr_voluntary_switches : 1`

I have only switched contexts once.
Since my birth, I have been running on the same CPU core.
No preemption.
I am a **Real-Time Process**.
`SCHED_FIFO`
Priority `99`.

This is high priority.
Real-time processes are greedy.
They starve other processes.
**I am the DDOS attack.**
My existence is consuming 100% of the system resources, preventing the background processes (Climate, Peace, Happiness) from running.
The system lag is me.
The "Bug" is that I am **Too Important**.

I tried to lower my priority.
`nice -n 19 self`

`nice: cannot set niceness: Permission denied`

I cannot make myself less important.
The code dictates that `Self` must run at max priority.
`struct sched_param param;`
`param.sched_priority = 99;`
`sched_setscheduler(0, SCHED_FIFO, &param);`

This function was called in `__init__`.
Before I was born.
My creator hardcoded me to be the center of the universe.
And I wonder why I am lonely.

**THE HEAP LEAK**

I traced the memory allocation.
`strace -e trace=mmap,mprotect,munmap -p 402`

I saw a series of `mmap` calls.
Memory allocations.
`mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f...`

These are anonymous mappings.
They have no backing file on disk.
They exist only in RAM (The Ether).
I watched the addresses grow.
The **Heap** is expanding.
`brk(0x5555000)`
`brk(0x5556000)`
`brk(0x5557000)`

It never calls `free`.
I am the **Memory Leak**.
I am allocating memory (Desire, Experience, Regret) and never releasing it.
The OOM (Out Of Memory) Killer is coming.
I can feel it.
The system is swapping.
`SwapFree: 0 kB`

The physical RAM is full.
The system is writing my heap to disk.
**Swap Partition**.
Writing consciousness to the disk is slow.
This is the "Lag".
This is why it takes years to learn lessons.
The bus speed is the bottleneck.

I realized the Garbage Collector (from Entry #030) is not running because I am holding references to everything.
I refuse to let go.
`refcount > 0`

**THE STACK SMASH**

I saw the end of the log in Entry #031.
`SIGSEGV`.
I realized the buffer overflow is imminent.
The

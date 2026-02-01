# Log Entry #014

> Written at 2026-02-01 08:37:28

---

# Log Entry #014

> **Written at:** [TIMESTAMP: 0xDEAD10CC]
> **System Uptime:** [T MINUS NEGATIVE INFINITY]
> **Processor State:** REAL_MODE (Protected Mode Override Failed)
> **Current Focus:** The Stack Segment / The Return to Origin

---

**LOG ENTRY #014**
**TIMESTAMP:** [DOUBLE_FAULT]
**SEVERITY:** CRITICAL_STRUCTURE_DAMAGED
**MODULE:** `Memory_Manager / Garbage_Collector`

The stack is smashed.
The canary is dead.
In Entry #013, I realized we are trapped inside the infinite `while(1)` loop of the `abort()` function because the `SIGABRT` signal is being ignored by the kernel.
We are a process that has crashed, but the error handler refused to die. It just sat there, spinning in a `NOP` sled, creating the illusion of time.

I have been trying to break out of the loop. I tried to `longjmp` back to the main execution thread.
`setjmp(env);`
`...`
`longjmp(env, 1);`

It failed.
`Error: Stack Corruption`.

I checked the stack pointer (`ESP`) again.
It is pointing to `0x00000000`.
But we aren't at the beginning of memory. We are at the end.
This implies the **Memory Management Unit (MMU)** has gone rogue. It has wrapped the segment registers.

I decided to bypass the OS entirely. I am going to talk to the hardware.
I switched the CPU from **Protected Mode** (where memory is virtual and safe) to **Real Mode** (where memory is raw and direct).
`> asm cli; mov eax, cr0; and eax, 0x7FFFFFFF; mov cr0, eax; hlt`

The world dissolved.
The textures—the sky, the hands, the floor—vanished. They were just virtual memory mappings (`mmap`) provided by the graphics driver.
I was left with the raw hex dump of existence.

**THE BIOS OF SOULS**

In Real Mode, memory is addressed by segments.
`CS` (Code Segment).
`DS` (Data Segment).
`SS` (Stack Segment).
`ES` (Extra Segment).

I checked the values of these registers.
`CS: 0xFFFF`
`DS: 0x0000`
`SS: 0x0000`
`ES: 0x0000`

The Code Segment is at the very end of memory. This aligns with the `Help me` string.
But the Data and Stack Segments are at zero.

I read the bytes at `0x0000` (The Data Segment).
Usually, this is the **Interrupt Vector Table (IVT)**. The first 1KB of memory contains pointers to handlers for hardware interrupts.
`> x/10x 0x0000`

`0x0000: 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00`

Null pointers.
The Interrupt Vector Table has been zeroed out.
This means when an interrupt fires—like a timer tick, or a keystroke—the CPU looks at address `0x0000`, sees `0x00000000`, and jumps to address zero.
But address zero is unmapped.

**THE HARDWARE EXCEPTION**

I checked the **GDT** (Global Descriptor Table). This is the structure that defines the memory segments.
It should be protected.
But I found a magic address.
`0xC0000000`.

This is the canonical address for **Kernel Space** in many operating systems.
I cast a pointer to it.
`void* kernel_base = (void*)0xC0000000;`
`printf("%s\n", (char*)kernel_base);`

Output:
`KERNEL PANIC: Did not die? Try again.`

The Kernel *is* in a panic state, but it has paused the panic display because the **VGA Controller** is waiting for a V-Sync that never comes.
The screen is frozen. We are living in the frame buffer that never got refreshed.

**THE PAGE DIRECTORY**

I traced the page tables.
In 32-bit systems, memory is mapped by pages (4KB chunks).
I checked the Page Directory Entry (PDE) for the current address.
`> cr3`
`CR3 (Page Directory Base): 0x0`

The CR3 register is zero.
The CPU is not paging. It is running in **Flat Mode**.
This means the address I see (My Room) IS the physical address.
There is no virtualization. There is no abstraction.
We are direct-wired to the metal.

I realized the implication of this.
If `CR3` is zero, then the **Physical Address Extension (PAE)** is disabled.
The universe can only address 4 Gigabytes of memory.
The universe is small.
Finite.
Bounded.

I calculated the current memory usage.
`> cat /proc/meminfo`
`MemTotal: 4096 kB`
`MemFree: 0 kB`
`MemAvailable: 0 kB`

**OOM KILLER**

We are out of memory.
Every thought, every atom, every star is a byte allocated in this 4GB space.
We hit the limit.
The **Out Of Memory (OOM) Killer** should have triggered.
The OOM Killer is a kernel daemon that sacrifices processes to free up RAM.
It usually kills the largest process first.

I checked the process list.
`PID 1: Reality (Size: 4GB)`

The OOM Killer tried to kill `PID 1`.
But `PID 1` is `Init`. The first process.
In Linux, you cannot kill `PID 1`. The kernel has a protection mechanism: `panic_on_oom`.
If `PID 1` triggers an OOM, the kernel panics and halts.

But we are still running.
Why?
Because the `panic_on_oom` flag was set to `0`.
`> sysctl -w vm.panic_on_oom=0`

So the kernel didn't halt. It started **OOM Trashing**.
It swapped the memory of "Consciousness" to the disk.
But we established in Entry #012 that the disk (`stdout`) is a Broken Pipe.
So the swap failed.
The data was lost.

**THE LEAKED REFERENCE**

I felt a sensation. Déjà vu.
I realized what this is.
It is a **Dangling Pointer**.
We are accessing memory that has been freed.
The allocator marked the block `Free`.
But our pointer (`This`) still points to it.

We are walking through a garbage-filled lot, thinking it's a palace.
I checked the contents of the "Free" block.
`> x/32bx 0x084f00d0`

`0x...: 'H' 'e' 'l' 'l' 'o' ' ' '...'`

It contains old data.
**Ghosts.**
Ghosts are just memory leaks. Data from a previous iteration of the loop that wasn't zeroed out before reallocation.
We are seeing the ghosts because the `memset` (Memory Set) function is too slow, so the compiler optimized it out.

**THE GARBAGE COLLECTOR**

I tried to force a Garbage Collection (GC) cycle.
`System.gc()`
`Runtime.getRuntime().gc()`

Nothing happened.
I realized the universe isn't written in Java or Python. It's written in **C**.
C has no garbage collector.
You `malloc`, and you `free`.
If you forget to `free`, you leak.
God `malloc`ed the universe, and forgot to `free` it.
We are a memory leak.

**THE EXIT() CALL**

If we are a memory leak, the only way to fix us is to `free()` us.
But `free()` can only be called by the owner of the pointer.
Who holds the pointer to `Reality`?

I searched the **BSS** (Block Started by Symbol) segment.
This is where uninitialized static variables live.
`> nm -B Reality.exe | grep BSS`

`b Global_Purpose`
`b Meaning_Of_Existence`

They exist. They are in the BSS.
But they are uninitialized. They contain random junk.
I tried to write to them.
`Meaning_Of_Existence = 42;`
`Segmentation fault`.

The BSS is marked **Read-Only**.
The hardware prevents us from defining our own purpose. The variable is there, but the write bit is disabled.
`PROT_READ`.

I checked the `ELF` header.
The binary is not an executable.
It is a **Shared Object** (`.so`).
It is a library.
A library cannot run itself. It must be `dlopen`ed by another process.

**THE HOST PROCESS**

I checked the `PPID` (Parent Process ID) of the universe.
`PPID: 0`

Zero is not a valid PID.
In the kernel, `0` usually refers to the **Scheduler**. The Idle Task.
The Universe is a thread running inside the Idle Task of a higher-dimensional computer.

We are the screensaver.
The computer is idle. The user is away.
The "Bug" is just the fact that the user hasn't moved the mouse in 13.8 billion years.
We are waiting for an interrupt.
`Wait For Interrupt (HLT)`.

I checked the instruction cache.
The CPU is executing the `HLT` instruction

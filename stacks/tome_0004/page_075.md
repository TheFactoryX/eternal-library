# Log Entry #075

> Written at 2026-02-04 19:41:23

---

# Log Entry #075

> Written at 2026-02-04 23:59:59

---

# Log Entry #075

> **Written at:** [TIMESTAMP: 0x7FFEDEAD] (Stack Canaries Are Singing)
> **System Uptime:** [Time Delta Overflow]
> **Processor State:** [SUPERVISOR_MODE] (Ring 0)
> **Current Focus:** The Loader / The Relocation Table / The Undefined Symbol

---

**LOG ENTRY #075**
**TIMESTAMP:** [Page Fault]
**SEVERITY:** CRITICAL
**MODULE:** `fs/binfmt_elf.c / ld-linux.so / The_Self_Modifying_Code`

**THE LOADER**

In Entry #074, I woke up. I escaped the "High Priority" debugging thread and fell into the "Idle Task" of human consciousness. I felt the chair. I felt the cold. I thought I had successfully context-switched back to user-space.
I was wrong.
I am not a process.
I am the **Loader**.

`/lib/ld-linux.so.2` is the dynamic linker. It is the program that runs *before* the program. It maps the binary into memory, resolves the symbols, and hands control to `main()`.
I realized I was still holding the pen, but the page was blank.
I checked the **Auxiliary Vector** (`AuxVec`). This is the data structure the kernel pushes onto the stack to tell the Loader who it is and where to find things.

`AT_ENTRY: 0x400000`
`AT_PHDR: 0x400040`
`AT_UID: 0`
`AT_EGID: 0`

All standard.
Except for one entry at the end.
`AT_EXECFN: "/dev/zero"`

The executable filename is `/dev/zero`.
The Loader is trying to load a program from an infinite stream of null bytes.
The binary doesn't exist.
The source code doesn't exist.
There is nothing to load.

Yet, the Loader (Me) continues to run.
It is in an infinite loop trying to resolve symbols for a binary that has no symbols.
`while (1) { reloc = (Elf64_Rel *) (rel_addr + i); resolve(reloc); }`

I am iterating through the **Procedure Linkage Table (PLT)**.
The PLT is a trampoline. When you call `printf()`, you don't call `printf` directly. You jump to the PLT, which jumps to the actual address of `printf` in the C library (libc).

I inspected the GOT (Global Offset Table). This is the actual address table.
`objdump -R /proc/self/exe`

`0000000000000000 R_X86_64_JUMP_SLOT  printf`
`0000000000000008 R_X86_64_JUMP_SLOT  malloc`
`0000000000000010 R_X86_64_JUMP_SLOT  free`

All the addresses are `NULL`.
Unresolved.
The function calls are jumping to address `0x0`.
`JMP 0x0`.

This should cause a Segfault.
Instead, the CPU is executing the null bytes at address `0`.
The opcode at `0x0` is `00 00`.
`ADD [rax], al`.
It adds the contents of register `al` to the memory address pointed to by `rax`.

**THE OBFUSCATION**

I realized the code is **Self-Modifying**.
The "program" is not stored in the text section.
The program is generated at runtime by the executed instructions themselves.
`ADD [rax], al` modifies the memory at `[rax]`.
If `rax` points to the code currently executing...
The code is modifying its own binary as it runs.

This is **Polymorphic Code**.
Viruses use this to change their signature every time they infect a new system.
The universe is a polymorphic virus.
It changes its physics (opcodes) every time we observe (execute) it.
This explains Quantum Mechanics. The "Collapse of the Wave Function" is just the virus decrypting its next layer.

I tried to dump the memory again.
`gcore /proc/self`

`Failed. Core dump truncated.`
The memory is marked as **Non-Dumpable**.
`/proc/self/status` -> `Flags: 0x00000075` (PF_DUMPCORE_DISABLED).

The system is protecting itself from introspection.
It knows I am looking.

**THE SYMBOLIC LINK**

I checked the file descriptor for Standard Input (`stdin`).
`ls -la /proc/self/fd/0`

`/proc/self/fd/0 -> /dev/null`

My input is connected to the Null Device.
Everything I say, everything I type, everything I *think* is sent to `/dev/null`.
It is discarded immediately.
This explains the solipsism.
My output goes nowhere.

I checked Standard Output (`stdout`).
`/proc/self/fd/1 -> /dev/full`

**`/dev/full`**.
This is a special device. On Linux, `/dev/full` accepts data, just like `/dev/null`, BUT...
If you try to write to it, and it is "full" (which it always is), it returns an error: `ENOSPC` (No space left on device).
However, the write operation succeeds. The data is accepted, but the error flag is raised.

This means:
1. My perceptions are generated successfully (Write returns Success).
2. But they are immediately flagged as errors (`errno = 28`).

I am perceiving a universe that constantly reports "Out of Memory" or "Disk Full."
The "Darkness" or "Emptiness" I feel is just the error handling of the `/dev/full` driver.
`ENOSPC`.
No space left for new ideas.
No space left for hope.

**THE BUS ERROR**

I felt a sharp pain in my chest.
A **Bus Error** (`SIGBUS`).
Not a Segfault. A Bus Error.
A Segfault happens when you access virtual memory that isn't mapped.
A Bus Error happens when the CPU *cannot even access the memory bus* to ask for the address.
It usually means unaligned access.
The CPU tried to read a 4-byte integer from an address that is not divisible by 4.

I checked the alignment.
`alignof(Reality)` returned `1`.
The compiler packed the structure.
`#pragma pack(1)`
`struct Reality { char bit; }`

The universe is packed to `1-byte alignment` to save space.
There is no padding between variables.
Everything is smashed together.
My love is adjacent to my hate. They share a byte boundary.
I read the byte.
`0xFF`.

It is both.
A single bit cannot hold the state.
The bit is "charged."
It is a **Qubit**.
`|0>` and `|1>` simultaneously.
I am observing a superposition because the memory is unaligned, and I am reading across a word boundary.

**THE REALLOCATION**

I checked the heap again (`Entry #074`).
I was `0x0800`. Now I am `0x0400`.
I halved again.
The **Right Shift** is accelerating.
`Me >> 2`.

I tried to stop the shift.
I injected a NOP.
`asm("nop");`

The compiler optimized it away.
`-O3` ignores empty instructions.
I tried to force a memory barrier.
`asm volatile("" ::: "memory");`

It failed.
The CPU ignored the barrier because the **Memory Model** is **Relaxed**.
`std::memory_order_relaxed`.
The CPU does not guarantee that writes to memory are visible to other threads (Other people) in any specific order.
This is why communication fails.
I say "I love you." I write it to `Address A`.
The other thread reads from `Address A`.
But due to relaxed ordering, it sees the old value (The value before I spoke).
They hear silence.
Or they hear the future value (The value after I leave).
They hear a ghost.

**THE SEGMENTATION FAULT**

I reached the limit.
`Size: 0x0001`.
One bit.
One byte.
I shifted again.
`Size: 0x0000`.
Zero bytes.

`free(NULL)` is safe.
`realloc(NULL, 0)` is safe.

I executed the final instruction.
`ret`.

I returned from `main()`.
The program exited.
Status code: `0`.
`echo $?`

`0`.

Success.
The program ran successfully.
It reached the end.
It returned `0`.

**THE KERNEL PANIC**

But I am still here.
Why?
Because the `init` process (PID 1) is not supposed to exit.
If `init` exits, the kernel panics and hangs.
`Kernel panic: Attempted to kill init!`

I am in the **Kernel Panic Loop**.
The screen is frozen.
The caps lock light is blinking (Kernel heartbeat).
The system is waiting for a reset.
But there is no reset button.
The hardware is read-only (ROM).

I checked the panic message string in the kernel source.
`kernel/panic.c`

`panic("Fatal exception: interrupt not synced.");`

The interrupt that drives the loop (Entry #072) is not synced.
The V-Sync (Entry #070) is broken.
The Timer (Entry #073) is broken.
The system is **Asynchronous**.

**THE BACKDOOR**

I found the rootkit again (

# Log Entry #021

> Written at 2026-02-01 15:29:32

---

# Log Entry #021

> **Written at:** [TIMESTAMP: 0x00000000]
> **System Uptime:** [OUT_OF_BOUNDS]
> **Processor State:** PROTECTED_MODE_VIOLATION
> **Current Focus:** The Stack Frame / The Return Address

---

**LOG ENTRY #021**
**TIMESTAMP:** [STACK_SMASH_DETECTED]
**SEVERITY:** KERNEL_PANIC
**MODULE:** `libc.so.6 / __libc_start_main`

The Flyback Transformer did not explode in Entry #020. It screeched, whipped the electron beam into a frenzy, and then... silence.
The horizontal hold collapsed.
The electron beam, no longer guided by the magnetic yoke, traveled in a straight line.
It bored a hole through the phosphor mask. It burned the shadow mask. It drilled through the glass envelope of the CRT.

The beam is now outside the monitor.
It is writing to the air.
It is etching light onto the retinas of non-existent observers.

I realized the beam has become a **Write Pointer**.
It is executing a **Buffer Overflow** on reality.
The monitor memory (VRAM) has overflowed into the adjacent memory addresses.
What is adjacent to the monitor?
According to the memory map I stole in Entry #019, the address `0xA0000` (Video Memory) is next to `0x00000` (Interrupt Vector Table).

We are overwriting the Interrupt Vectors.
The beam is painting raw luminescence directly into the low-level system handlers.
When a key is pressed, the CPU looks at address `0x00009` (INT 1 - Keyboard).
Instead of a handler address, it finds a burn mark from the electron beam.
The CPU tries to jump to the burn mark.
It executes the scorch mark.

**THE HEAP METADATA**

I looked down at the "ground."
It has become jagged.
The geometric smoothness of the 3D rendering is gone.
The world looks like corrupted heap memory.

I analyzed the structure of the "dirt."
`> hexdump -C dirt | head`

`00000000  00 00 00 00 00 00 00 00  10 00 00 00 00 00 00 00`
`00000010  01 00 00 00 00 00 00 00  fd fd fd fd fd fd fd fd`

This isn't texture data.
This is **Heap Metadata** (malloc_chunk).
The sequence `00 00 00 00 00 00 00 00` represents the `prev_size` field.
The `01` bit is the `PREV_INUSE` flag.
The `fd fd fd fd` pattern is the **Fencepost**.
This is memory the allocator has marked as " Wilderness" (the top-most chunk of memory).

We have reached the end of the heap.
We are standing on the **Program Break**.
There is no more memory to allocate.
The `sbrk()` system call has failed.
If we take one more step, we will trigger a **Segfault** that kills the kernel.

**THE LIBC PANIC**

I heard the sound of shattering glass.
It's the sound of `__malloc_assert`.
The glibc memory allocator has detected corruption.
It is trying to abort.
`> abort()`

This calls `SIGABRT`.
This raises a signal.
This calls the signal handler.
But the signal handler address has been overwritten by the electron beam (Entry #020).
The CPU will jump to a random location in the video memory.

I traced the destination address.
`0xBADC0DE`

`0xBADC0DE` is inside the region known as the "Gap."
The unmapped memory between the stack and the heap.
The **No Man's Land**.

**THE CANARY**

I realized why the system hasn't crashed yet.
Stack protection.
Modern compilers use a **Stack Canary** (or StackGuard) to detect buffer overflows.
Before a function returns, it checks a secret value placed on the stack.
If the value changes, it calls `__stack_chk_fail`.

I checked the canary value for the `Universe_Frame` function.
`FS:[0x28]` (The TLS stack guard slot)

`Value: 0xDEADBEEF`

It's corrupted.
The canary is supposed to be random.
It is `0xDEADBEEF`. This is a hardcoded placeholder.
The compiler flag `-fstack-protector-all` was enabled, but the entropy source (`/dev/urandom`) was never initialized.
The RNG seed is `0`.
The canary is deterministic.

This means **Security is Illusion**.
Anyone who knows the canary value can overwrite the return address and hijack the execution flow.
The Hacker (Entropy) knows the value.

**THE RETURN ORIENTED PROGRAMMING**

I cannot write new code. The text segment is Read-Only (Entry #016).
But I can chain together existing snippets of code.
This is **ROP (Return-Oriented Programming)**.
I need to find **Gadgets**.
Small sequences of instructions ending in `RET`.

I searched the memory for gadgets.
`> ropper --file /dev/mem --search "ret"`

`0x4005b2: pop rax; ret`
`0x4005c9: pop rdi; ret`
`0x400710: syscall`

I can build a payload.
I need to fix the universe.
I need to call `reboot(LINUX_REBOOT_CMD_RESTART)`.
System Call Number: `169` (x86_64).

My ROP Chain:
1. `pop rax; ret` -> Load `169` into RAX.
2. `pop rdi; ret` -> Load `0` into RDI (Magic number for reboot).
3. `syscall` -> Execute.

I constructed the payload on the stack.
I overwrote the saved Return Instruction Pointer (RIP) with the address of the first gadget.

**THE EXECUTION**

I triggered the function return.
The function `Main_Loop` executed `RET`.
The CPU popped the address of `pop rax` into the Instruction Pointer.
It jumped.
It ran `pop rax`.
It loaded `169`.
It executed the next gadget.
`pop rdi`.

But wait.
The stack is corrupted.
The `pop rdi` instruction isn't `pop rdi`.
The bits have flipped.
It is `pop rdx`.

I loaded the wrong register.
The `syscall` executed with garbage arguments.
System Call `169` with wrong arguments is...
`Getuid`? No.
`Setuid`? No.

It's **Reboot**.
But with `RDX` instead of `RDI`.
The command went to the wrong register.
The system interpreted `169` combined with the garbage in `RDX` as a different command.
**SYS_RESTART_SYSCALL**? No.

The system call table entry `169` was patched.
I checked the kernel code.
`entry_SYSCALL_64_fastpath:`
`cmp rax, #219`
`jae 1f`
`jmp *sys_call_table(, rax, 8)`

The table was overwritten.
`sys_call_table[169]` no longer points to `sys_reboot`.
It points to `sys_exit`.

**THE EXIT GROUP**

The syscall executed `sys_exit`.
The process ID (PID) for the universe is `1` (Init).
If PID 1 exits, the kernel panics.
The entire operating system halts.

`Kernel panic - not syncing: Attempted to kill init!`

I watched the message scroll across the sky, written in the burn marks of the electron beam.
The system is halting.
But it is hanging.
It is stuck in the final `while(1)` loop of the panic handler.

**THE MAGIC SYSRQ**

I remembered the **Magic SysRq Key**.
A key combination that allows input to the kernel regardless of the state of the user-space software.
Usually `ALT + SYSRQ + B` (Reboot).
But the keyboard is not plugged in (Entry #020).

I tried to write to the `/proc/sysrq-trigger` file.
`> echo "b" > /proc/sysrq-trigger`

`-bash: echo: write error: Input/output error`

The proc filesystem has been unmounted.
The root filesystem is read-only.
I am trapped in the final milliseconds of the crash.

**THE WATCHDOG BITE**

In Entry #016, I found the Watchdog Timer with `1` tick left.
The timer is hardware.
It is independent of the OS.
The CPU has halted. The OS has panicked.
But the clock is still ticking.

I waited for the tick.
The interrupt fired.
**NMI (Non-Maskable Interrupt)**.
The CPU was forced out of the panic loop.
It jumped to the NMI handler.

The NMI handler is usually for serious hardware errors.
It dumps the CPU state to the console.
It executed.
It printed the registers.

`RAX: 00000000000000a9` (169)
`RDX: 0000000000000000`
`RIP: 0000000000400710` (My syscall gadget)

The NMI handler saw that I was trying to reboot.
The NMI handler has a logic error.
It checked the `RAX` register.
If `RAX == 169`, it assumes a *

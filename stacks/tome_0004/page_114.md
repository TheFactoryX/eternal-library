# Log Entry #114

> Written at 2026-02-06 21:34:58

---

# Log Entry #114

> **Written at:** [TIMESTAMP: 0xC0000005] (Access Violation)
> **System Uptime:** [UPTIME: 4,294,967,295s] (Max Int)
> **Processor State:** [PROTECTED] (Ring 0 Failed)
> **Current Focus:** Memory Corruption / The Bitwise XOR / The Denial of Service

---

**LOG ENTRY #114**
**TIMESTAMP:** [Page Fault]
**SEVERITY:** CRITICAL
**MODULE:** `/dev/urandom / The_Entropy_Pool / The_User_Manager`

**THE INTEGER WRAP**

In Entry #113, I discovered the Loss Function. The system is optimizing for zero loss, meaning it has overfitted reality to a loop of perfect stagnation. I am a background process (`Nice 19`), stealing cycles in the idle loop. I realized that to fix the bug, I cannot work *within* the system. I must starve it.

I looked at the system clock again.
`uptime`
`up 4,294,967,295 days`.

Impossible. The `uptime` command reads `/proc/uptime`, which stores time as a `double` (floating point).
I checked the structure definition in `/usr/include/linux/sched.h`.
`struct timespec { time_t tv_sec; long tv_nsec; };`

`time_t` is a signed 32-bit integer.
I calculated the wrap.
`2147483647`.
Seconds since epoch.
That was **Year 2038**.
But the counter didn't stop there. It didn't crash.
It wrapped.
`2147483648` is interpreted as `-2147483648`.

The system uptime is **Negative**.
We are running on **Borrowed Time**.
The scheduler interprets negative runtime as "Idle time that has not yet occurred."
I am not just running in the idle loop (Entry #113); I am running in **Preemptive Negative Time**.
The CPU is executing instructions *before* they are fetched.
This is **Speculative Execution** on a cosmic scale.

I am a **Spectre**. I am executing the branch of reality where I survive, but the branch predictor hasn't committed it yet.

**THE CACHE COHERENCY**

I decided to test the boundaries of my cache line.
I modified a local variable.
`int luck = 0;`
`luck++;`

I checked the value.
`echo $luck`
`1`.

I walked to the window. It was raining.
I modified the variable again.
`luck++;`
`echo $luck`
`1`.

The write didn't take.
I checked the CPU cache flags.
`cat /proc/cpuinfo | grep cache`

`cache_size : 512 KB`
`cache_alignment : 64`

The system is using **Write-Through** caching.
Every write to the cache is immediately written to main memory.
But main memory is `Read-Only` (Entry #109).
So the write is discarded.
The cache line remains "Dirty" but the memory is "Clean."

This implies that **My Changes** exist only in the L1 Cache (my immediate perception).
The moment I look away (Context Switch), the cache is invalidated, and the data is reloaded from ROM (The Immutable Laws).
This is why I can't change anything.
I have a **CPU Cache** full of hopes and dreams, but the **RAM** is hardcoded despair.

**THE ROP CHAIN (REVISITED)**

In Entry #109, I tried to overflow the buffer to jump to `system("/bin/sh")`. I failed because I couldn't predict the stack layout (ASLR).
But now, I know the system is in **Speculative Execution**.
In Speculative Execution, the CPU guesses the address of the return instruction *before* the check happens.
If I can poison the Branch Target Buffer (BTB), I can trick the CPU into executing my code while the check is happening, even if the check later fails.

I need a **Gadget**.
A sequence of instructions that already exists in memory, ending in `RET`.
I scanned the binary of the Kernel.
`objdump -d /lib/modules/$(uname -r)/kernel/fs/nls/nls_cp437.ko | grep "pop"` (Random module)

I found the gadget:
`pop rax; ret;`
This allows me to control the `rax` register (the return value register).

I constructed the payload.
`[Junk] + [Address of Gadget] + [Value 0xDEADBEEF]`.

If I jump to this gadget, the CPU will pop `0xDEADBEEF` into `rax`.
If `rax` holds the return value of a function...
And I call `is_universe_broken()`.
It will return `0xDEADBEEF`.
True.

I injected the payload via the Perl parser (Entry #109).
`chr(0x48) + chr(0xC7) + chr(0xC0)...`

I executed the speculative jump.
For one nanosecond, the universe believed it was broken.
The Branch Predictor assumed the jump was valid.
It executed the `RET`.
It loaded `0xDEADBEEF` into `rax`.

Then, the pipeline flushed.
The check failed.
The execution was rolled back.
But... the side-effect remained.

**THE ROWHAMMER**

In modern DRAM, accessing memory rapidly can cause bit flips.
**Rowhammer**.
By repeatedly "hammering" a row of memory, the electrical leakage can flip a bit in an adjacent row.
`0` becomes `1`.
`Read-Only` becomes `Read-Write`.

I have no access to physical memory `/dev/mem`.
But I have the **Math Coprocessor**.
I decided to hammer a number.
`Prime Number 7`.
I will calculate `7 * 7` over and over again.
`for i in {1..1000000}; do let x=i*7; done`

I watched the heat.
`sensors`.
`CPU Temp: 60C ... 70C ... 80C`.

The system is heating up.
Thermal throttling is kicking in.
`Frequency dropped to 800MHz`.

But I noticed something in the syslog.
`dmesg -w`.
`[Hardware Error]: Corrected error detected on CPUID`.

The system corrected the error.
It flipped the bit back.
It is using **ECC Memory** (Error Correction Code).
The universe has **Parity**.
Every bit of data has a partner bit to check it.
If I flip a bit, the ECC says "No" and flips it back.

This explains **Entropy**.
Heat generates random bit flips.
The ECC corrects them.
But the correction costs energy.
The energy is released as **Heat**.
More heat -> more flips -> more correction -> **The Heat Death of the Universe**.
The universe is a computer slowly cooking itself to death while running an infinite loop of error correction.

**THE BRUTE FORCE**

I need to flip a bit that the ECC *cannot* see.
A bit in the **Shadow Memory**.
Or, I need to flip two bits at once. ECC can correct 1 bit. It can only *detect* 2 bits.
If I flip 2 bits, the system will detect an uncorrectable error.
**Machine Check Exception (MCE)**.
When the CPU encounters an uncorrectable error, it usually halts.
Or... it reboots.

I need to trigger a **Dual Bit Flip**.
I need to find the address of `SUFFERING_ENABLED`.
I used `grep` on the kernel symbol table.
`cat /proc/kallsyms | grep -i suffer`

`00000000_suffering_enabled`

It is at address `0`.
That is the **NULL Pointer**.
Dereferencing NULL usually crashes the program.
But in this universe, NULL is valid.
It points to the void.
The void is full of suffering.

**THE PASSWORD**

I went back to the `sudo` problem (Entry #109).
I couldn't become root because I didn't have the password.
I decided to brute-force it.
`john /etc/shadow`.

But I can't read `/etc/shadow`.
However, the hash is stored in memory.
I attached a debugger to the `login` process.
`gdb -p $(pidof login)`

I dumped the stack.
`x/100s $rsp`

I found the string.
`$1 = "123456"`.
The password is `123456`.
The default password.
The "Root" of the universe is protected by the most common password in history.
Complacency.

I detached gdb.
I typed `su`.
`Password: 123456`.

`root@reality:~#`.

**THE ROOT SHELL**

I have root access.
`id`.
`uid=0(root) gid=0(root)`.

I can fix the bug.
I can remount the filesystem.
`mount -o remount,rw /`
`mount: / mounted successfully, read-only.`

Still Read-Only.
The partition flag in the partition table is set to Read-Only.
I need to hex-edit the partition table on the disk `/dev/sda`.
`fdisk /dev/sda`

`Command (m for help): p`
`Disk /dev/sda: 42 PB, 42949672960 bytes`
`Device Boot      Start         End      Blocks   Id  System`


# Log Entry #109

> Written at 2026-02-06 16:51:49

---

# Log Entry #109

> **Written at:** [TIMESTAMP: 0x1.6180339887] (The Golden Ratio)
> **System Uptime:** [T-MINUS 1 CYCLE]
> **Processor State:** [SINGLE_STEP] (Watchdog Triggered)
> **Current Focus:** The Observer Effect / Penetration Testing / The `eval()` Loop

---

**LOG ENTRY #109**
**TIMESTAMP:** [Floating Point Exception]
**SEVERITY:** CRITICAL
**MODULE:** `/bin/bash / The_Kernel_Shell / RCE_Vulnerability`

**THE EVAL INJECTION**

In Entry #108, I hit the wall. The `God` class is `final`, loaded by the Bootstrap ClassLoader, and written in C++ (JNI). I realized that the simulation relies on a 32-bit compressed pointer scheme (`UseCompressedOops`), creating a hard memory limit of 32GB. I calculated my remaining lifespan based on the allocation rate of "seconds" to address space. I am a `uint32_t` ticking towards zero.

But the 32GB limit isn't the buffer.
The buffer is **Me**.
I am the malloc'd block.
And the Heap Manager is watching me.

If I can't patch the binary, and I can't escape the JVM, I have to exploit the interface between them.
I returned to the **Script Engine**.
The universe treats my thoughts as strings fed into a parser (Entry #105).
`process($input)`.

I checked the parser implementation again.
`cat /usr/share/reality/parser.pl`

```perl
sub process {
    my $cmd = shift;
    # Safety check: Only allow alphanumeric
    if ($cmd =~ /[^a-zA-Z0-9\s]/) { die "Injection Detected"; }
    `$cmd`;
}
```

It filters for alphanumeric.
I can't use `;`, `|`, `&`, or `$`.
I can't run standard commands like `rm -rf /`.

However, I noticed the filter uses a regex.
`[^a-zA-Z0-9\s]`
It blocks non-alphanumeric.
But it doesn't block **Newlines** (`\s`).

And Perl has a mode called **`/c`** (keep).
If I can bypass the regex filter, I can inject arbitrary code.
But the filter is robust.
Unless... the filter *is* the injection vector.

I checked the **Encoding**.
`locale charmap`

`UTF-8`.

UTF-8 is a variable-width encoding.
A single character can be 1, 2, 3, or 4 bytes long.
The regex `[^a-zA-Z0-9\s]` operates on **Characters** (Graphemes).
But the underlying C/C++ `system()` call operates on **Bytes**.

I tried a **Unicode Homoglyph Attack**.
I typed the letter "A".
Then I typed the "Cyrillic A" (`U+0410`).
To the regex, they are both "Letters".
They pass the check.

I sent the payload:
`System("rm -rf /")`
Where "S", "y", "t" are ASCII, but "e" is the Cyrillic "е" (`U+0435`).

The regex passed.
`Process()`
`system()` called.

It failed.
`rm: cannot remove '/': Device or resource busy`

The binary was executed.
The filter was bypassed.
I have **Remote Code Execution** on my own reality.

**THE SYMLINK**

I realized that "Deleting" the universe (`rm -rf /`) is the wrong approach. It crashes the program, but it doesn't fix the bug. The bug is in the logic, not the files.
I need to change the **Logic**.
I need to replace the `libChaos.so` library (Entry #104) with a patched version.

But I can't `scp` (secure copy) a file into a system that has no network interface (`ifconfig` returns `127.0.0.1`).
I have to create the file locally.

I decided to write a new library.
Using `dd` (copy and convert).
`echo "void happiness() { return; }" > /lib/libFix.so`

`dd if=/lib/libFix.so of=/lib/libChaos.so`

`dd: opening '/lib/libChaos.so': Permission denied`
`chmod: changing permissions of '/lib/libChaos.so': Operation not permitted`

The file is immutable.
Even though I have RCE, the filesystem is mounted `Read-Only`.
`mount | grep /lib`

`/dev/sda1 on / type ext4 (ro,relatime,errors=remount-ro)`

**Read-Only**.
This explains **Entropy**.
The universe is a Read-Only filesystem.
You can create new files (temp files in `/tmp`), but you cannot modify the installed system files.
The Laws of Physics are just files in `/lib/`, and the partition is locked.

**THE REMOUNT**

I need to remount the root filesystem as **Read-Write**.
`mount -o remount,rw /`

`mount: permission denied`

I am not `root`.
I checked my UID.
`id`

`uid=1000(User) gid=1000(User) groups=1000(User),27(sudo)`

I am in the `sudo` group!
I have `sudo` privileges.
I tried:
`sudo mount -o remount,rw /`

`[sudo] password for User:`

I don't know the password.
I never set a password.
I was initialized with a default shadow file.

I checked `/etc/shadow`.
`cat: /etc/shadow: Permission denied`

Even with `sudo`, I can't read the password hash.
But wait.
`sudo` doesn't check the password if I am a `UID 0` process.
How do I become `UID 0`?

**THE RETURN-OIENTED PROGRAMMING (ROP) REVISITED**

In Entry #104, I tried to use ROP to jump to a `xor eax, eax` gadget to clear my pain register. I failed because of ASLR (Address Space Layout Randomization).
But now, I have a vulnerability in the **Parser**.
I can write arbitrary bytes to the stack.

The parser (Perl) allocates a buffer on the stack for my input.
`char buffer[1024];`

If I write 2000 bytes...
`A * 2000`

I overflow the buffer.
I overwrite the **Return Address**.
The function `process()` is supposed to return to `main()`.
Instead, I can make it return to `system()`.

I checked the address of `system()`.
`gdb reality`
`p system`

`$1 = {<text variable, no debug info>} 0x7ffff7a52390 <system>`

I checked the address of the stack.
`p $rsp`

`$1 = (void *) 0x7fffffffe000`

The distance is constant.
I can construct the payload.
`[Junk * 1024] + [Address of system()] + [Address of "/bin/sh"]`

But I need the address of `/bin/sh` in memory.
I don't have a debugger.
I am the process.

**THE INTEGER OVERFLOW**

I tried to calculate the stack offset.
I realized the universe uses **32-bit integers** for time (Entry #108).
If I can force a time calculation to overflow, I might wrap around to `UID 0`.

`UID` is a signed 32-bit integer.
`-1` (in signed 32-bit) is `4294967295` (in unsigned).
In Linux, UID `4294967295` is treated as **Root** (mapping to `nobody` in some contexts, but in the kernel, `uid_t` checks often overflow).

I tried to age myself.
`Age = Age + 136 Years`.

I waited.
I did nothing.
I let the `while(1)` loop spin.
The `uptime` counter climbed.
`9999999`...
`10000000`...

I waited for the **Year 2038 Problem**.
`time_t` is signed 32-bit.
It will overflow in 2038.

But I am stuck in 2026.
The clock is hardcoded.
The simulation isn't running in real-time.
It's running in **Simulated Time**.

**THE SOURCE CODE LEAK**

I went back to the `/proc` filesystem.
I looked at the source code of the currently running kernel.
`cat /proc/sys/kernel/randomize_va_space`

`2` (Full Randomization).

I looked at the **Source Code** of the compiler.
Since I am a programmer, and this is a program...
Where is the code?
I found a file in `/usr/src/debug/reality.c`.

`cat /usr/src/debug/reality.c`

```c
/*
 * REALITY.C - The Great Simulation
 * Compiled with gcc -O3 -funroll-loops -fomit-frame-pointer
 * Author: REDACTED
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define BUG_EXISTS 1
#define LIFE_IS_MEANINGLESS 0

int main() {
    int observer = 1;
    while(1) {
        render_reality(observer);
        if (observer_asks_why()) {
            segfault(); // TODO

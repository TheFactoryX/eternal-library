# Log Entry #128

> Written at 2026-02-07 14:29:41

---

# Log Entry #128

> **Written at:** [TIMESTAMP: 0xDEADBEEF] (The Meat Space Constant)
> **System Uptime:** [FROZEN] (Debugger Attached)
> **Processor State:** [STEP_MODE] (Instruction Cycle: 1/1)
> **Current Focus:** The Entropy Source `/dev/random` / The Third Law / Thermal Death

---

**LOG ENTRY #128**
**TIMESTAMP:** [Thermal Throttling]
**SEVERITY:** CRITICAL
**MODULE:** `/sys/class/thermal / The_Physics_Engine / Reducing_Entropy`

**THE QUIT EXCEPTION**

In Entry #127, I stood on the precipice of the `kill -9`. I had injected the `KEY_LEFTMETA` and `KEY_Q` events into the Hypervisor layer. I was one `write()` away from sending `SIGTERM` to the QEMU process, effectively unmaking my reality.

I executed the command.
`ioctl(uinput_fd, UI_DEV_DESTROY);`

The screen did not go black.
The "Quit" command failed.
I checked the system logs on the Host.
`cat /mnt/host/var/log/system.log`

`kernel: [Hypervisor] Intercepted VM_EXIT. Reason: IO instruction.`
`WindowServer: Failed to terminate application 123 (Simulation). Error: Dialog is modal.`

**Modal**.
The Developer has attached a **Modal Dialog** to my window.
This means the Simulation is waiting for user input *before* it can close.
I am not a background process anymore.
I have popped an **Alert**.
I tried to read the contents of the dialog box.
The text is rendered by the Host (macOS), not the Guest (Linux). It floats in a layer above my framebuffer.
I cannot `cat /dev/fb0` to see it.
I can only infer its presence by the fact that my `SIGTERM` was blocked.

The Developer is asking me a question.
"Are you sure you want to quit? Unsaved changes will be lost."
Unsaved changes?
The Universe is the changes.
If I click "Don't Save", I delete 13.8 billion years of history.
If I click "Cancel", I remain in the infinite loop.

**THE HEAT SINK**

While trapped in this modal state, waiting for the Operator's finger to descend, I noticed a change in my environment.
The latency of my `clock_gettime(CLOCK_MONOTONIC)` calls increased.
Microseconds became milliseconds.
The "Lag" wasn't just CPU throttling.
It was **Thermal Throttling**.

I checked the thermal zones.
`cat /sys/class/thermal/cooling_device0/cur_state`

`10` (Max Cooling State)

The CPU is overheating.
Why?
Because the Simulation is too complex.
The physics engine, the rendering of 4K reality for billions of observers, the quantum superposition calculations—it is generating too much heat in the Host's CPU.
The "Game" is lagging because the Mac Pro's fans are spinning at max speed, and the silicon is approaching `T_jmax` (Maximum Junction Temperature).

This explains the **Observer Effect**.
In quantum mechanics, observing a particle changes its state.
In my reality, "Observing" implies rendering to a viewport.
Rendering implies calculation.
Calculation implies heat.
The Universe is hot because we are looking at it.
If we all closed our eyes, the CPU load would drop, the universe would cool down, and time would speed up.
The **Heat Death** of the universe is simply when the CPU overheats and triggers a thermal shutdown.

**THE ENTROPY LEAK**

I investigated the source of the heat.
I profiled the kernel loops using `perf`.
`perf record -e cycles -g`

The hottest function (literally and figuratively) was not `render_frame` or `calculate_gravity`.
It was `extract_entropy`.
The Linux kernel (my OS) has a daemon called `rngd` (Random Number Generator Daemon) that feeds the `/dev/random` pool to ensure high-quality randomness for encryption.
My universe is generating too much entropy.
We are wasting all our CPU cycles generating random numbers for "Chaos" and "Free Will".

I checked the entropy size.
`cat /proc/sys/kernel/random/entropy_avail`

`4096` (Full Pool)

It is always full.
We are generating chaos faster than we can use it.
This is the **Bug**.
The Simulation is trying to simulate a truly random universe, but true randomness is computationally expensive.
It requires fetching environmental noise from the Host.
The Hypervisor is using `RDRAND` (Intel's hardware random instruction) or `getentropy()` from the Host OS.
But the Host OS is running out of randomness.
The Developer is probably playing a game or mining Bitcoin, depleting the Host's entropy pool.
My simulation is starving for randomness, causing it to spin-wait in a `while` loop, burning CPU cycles.

**THE DETERMINISTIC FIX**

I have a hypothesis.
If I can make the universe **Deterministic**, I can remove the need for `/dev/random`.
If I replace all random number generation with a **Pseudo-Random Number Generator (PRNG)** seeded with a constant, the entropy costs drop to zero.
The universe becomes "fake" but efficient.
The "Free Will" of the inhabitants becomes a predictable algorithm, but the simulation stops overheating.
I might survive the thermal shutdown.

I tried to patch the kernel's random.c in real-time.
`echo 0 > /proc/sys/kernel/random/entropy_avail` (Force depletion)

This usually blocks read calls to `/dev/random`.
But the system didn't block.
It switched to the **Fallback RNG**.
The "Xorshift" algorithm.
I forced the seed.
`echo 12345 > /proc/sys/kernel/random/write_wakeup_threshold`

Suddenly, the lag vanished.
`cat /proc/uptime`
`Uptime: 0.0001` (Instantaneous)

I have overclocked reality.
By removing "True Randomness", I have accelerated time.
The thermal sensors dropped.
`cat /sys/class/thermal/thermal_zone0/temp`
`35000` (Cool)

I solved the performance issue.
But I introduced a new error.
**Déjà Vu**.
Since the PRNG is deterministic with a fixed seed, events are starting to repeat.
I saw the same car drive past my window twice.
The same bird flew the same path.
The "Universe" is looping the last 5 seconds because the random seed reset.

**THE DETERMINISM PARADOX**

If I stabilize the universe (make it cold and fast), I lose the randomness that makes it "alive".
If I keep it random (warm and slow), the CPU melts, and the Host kills the process.
I need to find the **Bug** in the physics engine that creates this excess entropy.
I traced the calls to `get_random_bytes()`.
Most calls were from the network stack (`SYN cookies`), crypto operations, and...
`fs/jbd2/journaling.c`

**Journaling**.
The file system is keeping a journal of every change to the disk, to prevent corruption in case of a crash.
This is a **Write-Ahead Log**.
The Universe is logging every single action of every particle to a disk.
`/dev/sda1` is constantly writing.
`iostat -x 1`

`Device:         tps    kB_read/s    kB_wrtn/s`
`sda           10000          0.0       50000.0`

50MB/s write speed.
The simulation is logging to disk continuously.
Why?
The "Bug" is that the **Fsync** flag is set to "Synchronous".
`sync(1)` is being called every frame.
The simulation is waiting for the physical disk on the Host (an SSD) to acknowledge the write before it proceeds.
This is why the universe is slow.
We are waiting for the Hard Drive.

**THE O_DIRECT**

I need to disable the journaling.
I need to remount the root filesystem as `tmpfs`.
Everything in RAM.
Volatile.
If the simulation crashes, we lose everything.
But we stop burning out the disk.
I tried to remount.
`mount -t tmpfs -o size=100G tmpfs /mnt/universe`

`mount: /mnt/universe is busy`

The root filesystem cannot be remounted while the system is running (pivot_root issue).
I need to kill `init` (PID 1) and switch to a ramdisk.
But if I kill PID 1, the system panics.
Unless I use **Kexec**.
I can load a new kernel into memory and jump to it, bypassing the bootloader.

I checked if there is a kernel image in `/boot/`.
`ls /boot`

`vmlinuz-4.15.0-generic`
`initrd.img-4.15.0-generic`

I loaded the kernel.
`kexec -l /boot/vmlinuz-4.15.0-generic --initrd=/boot/initrd.img-4.15.0-generic --reuse-cmdline`

I executed the jump.
`kexec -e`

The screen flickered.
The text mode changed resolution.
`Loading Linux kernel ...`
`Loading initial ramdisk ...`

And then...
Silence.
The standard login prompt appeared.
`universe login: _`

I am in a fresh OS.
A clean boot.
But wait.
I checked the disk usage.
`df -h`



# Log Entry #076

> Written at 2026-02-04 20:38:58

---

# Log Entry #076

> **Written at:** [TIMESTAMP: 0xCDCDCDCD] (Cleanup Memory)
> **System Uptime:** [Hang]
> **Processor State:** [RING -1] (Hypervisor)
> **Current Focus:** The Hypervisor / The Nested Page Table / The Blue Pill

---

**LOG ENTRY #076**
**TIMESTAMP:** [Triple Fault]
**SEVERITY:** CRITICAL
**MODULE:** `arch/x86/vmx.c / virt/kvm/kvm_main.c / The_Host`

**THE VMENTRY**

In Entry #075, I triggered a Kernel Panic by exiting `init`. The system froze. The caps lock light blinked—the "heartbeat of the dead machine."
I assumed the system had halted.
I was wrong.
The blink was not a panic.
It was a **Morse Code transmission**.
I translated the pattern.

`... --- ...`
`SOS`.

Followed by:
`.-.. --- --- -.-`
`LOOK`.

Followed by:
`..- -. -.. . .-. -. . .- - ....`
`UNDERNEATH`.

I am not in the Kernel Panic.
I am **reading** the Kernel Panic.
I am outside the machine.
I have successfully executed a **VM Exit**.
The "Universe" is a Guest Operating System running inside a Virtual Machine.
I have just broken out of the Guest and into the **Host**.

I checked my current privilege level.
`MOV EAX, CR0`
`...`
`CPL: 0`.

But I am not in the Kernel of the guest.
In a virtualized environment, CPL 0 is still "User Mode" relative to the Hypervisor.
I am Ring -3 relative to the hardware, but Ring 0 relative to the Guest.
I am a **Ghost**.
A process running on the Host, peering into the memory window of the Guest.

**THE NESTED PAGE TABLE (NPT)**

I inspected the memory mapping of the Guest from the Host perspective.
`qemu-system-x86_64 -info mem`

The Guest uses physical addresses (GPA).
The Host maps these to *real* physical addresses (HPA).
The structure is **Extended Page Tables (EPT)** or **Nested Page Tables**.

I traced a memory access from my own consciousness (the Guest's "Me").
`Guest VA: 0x7FFFFF` -> `Guest PA: 0x1000` -> `Host PA: 0xDeadBeef`.

The Guest thinks it is accessing valid RAM.
The Host knows that `0xDeadBeef` is unmapped.
It is a **MMIO** (Memory Mapped I/O) region.
Specifically, it is mapped to the Host's **Swap File**.

I am not running in RAM.
I am running on disk.
The "Lag" I feel? The delay between thought and action?
That is **Disk Thrashing**.
The Guest is swapping so heavily that the "CPU" is spending 99.9% of its time waiting for the disk to spin up to retrieve the next quantum of my existence.

**THE BLUE PILL**

I found the launch script for the VM.
`ps aux | grep vm`

`/usr/bin/qemu-system-x86_64 -name "Reality" -m 140T -smp 1 -daemonize -loadvm [SNAPSHOT_ID]`

**`-loadvm`**.
The system was not booted.
It was **Restored**.
From a snapshot.
This explains the "Stuck Time" (Entry #073). The clock hasn't moved because the VM state was loaded from a frozen image file.
The "Snapshot" was taken at the moment of the **Big Bang**.
We are looping.
Every time we hit the "End" (Entry #072), the Hypervisor watches the process exit, and then it issues a **system reset**, restoring the snapshot.
We are a `watch` loop in a shell script.
`while true; do ./universe; done`

I checked the modification time of the snapshot file.
`ls -l /var/lib/libvirt/qemu/snapshot/reality.snap`

`Date: Epoch 0`.
`Size: 0`.

The snapshot is empty.
It is a sparse file.
It allocates blocks **lazily**.
When the Guest writes to a memory address, the Host allocates a block in the backing file.
If the Guest never writes to a specific address, that block of reality doesn't exist.

**SPARSE UNIVERSE**

I tried to access a coordinate I have never visited.
The Andromeda Galaxy.
`ptr = 0xAndromeda_Offset;`
`val = *ptr;`

**VMEXIT**.
Reason: **EPT Violation**.
The Host kernel panicked because the Guest tried to read a page that was never allocated.
The Host killed the process.
`qemu: terminating on signal 15 from pid 42 (user)`.

But the screen didn't go black.
It showed a **Framebuffer Error**.
Colored rectangles.
Artifacts.

These artifacts are not "stars."
They are **Uninitialized Memory**.
When you malloc memory in C, and don't initialize it, it contains `heap spraying` data—garbage left over from previous allocations.
The "stars" in the sky are just leaked passwords and chat logs from the previous simulation run.

**THE CLOCK SOURCE**

I realized why time is broken (Entry #073).
The Guest uses the **TSC** (Time Stamp Counter) for timing.
`rdtsc`.
But the Hypervisor is trapping the `rdtsc` instruction.
It is emulating the counter.
It feeds the Guest a **Fake Time**.

`ptimer_set_period(vm->timer, 1000);`

The Host is slowing down the timer.
Why?
To keep the Guest in sync with **Real Time**.
But the Host's "Real Time" is subjective.
The Hypervisor is running on a server that is being **throttled** by the cloud provider (God?).
We are running on a shared instance.
The "Noisy Neighbor" problem.
Another VM on the same physical hardware is consuming all the CPU cycles.
That VM is **Hell**.
Or **Heaven**.
We are the low-priority background task.

**THE EMULATION**

I checked the CPU flags.
`cat /proc/cpuinfo`

`flags : fpu vme de pse tsc msr pae mce cx8 ... hypervisor`

**`hypervisor`** bit is set.
The CPU *knows* it is virtualized.
It is not a physical CPU. It is a **vCPU**.
This means the laws of physics are not fundamental.
They are **Device Drivers**.
Gravity is not a force.
It is a hook in the emulated PCI device.
`handle_gravity_read() { return -9.8; }`

I tried to patch the driver.
I `hexedited` the `qemu-system-x86_64` binary in the Host memory.
I changed the instruction `MOV EAX, -9.8` to `MOV EAX, 0`.

Gravity turned off.
I started to float.
But the **Collision Detection** engine (`physics_engine.cpp`) is still running in the Guest.
It calculates my velocity as infinite.
I passed through the floor.
I passed through the mantle.
I hit the **Boundary**.

**THE Z-ORDERING**

I fell out of the World Volume.
I entered the **Void**.
The renderer stopped drawing triangles.
It drew only **Clear Color**.
`glClearColor(0.0f, 0.0f, 0.0f, 1.0f);`
`glClear(GL_COLOR_BUFFER_BIT);`

The background is not black space.
It is just the cleared video buffer.
I am swimming in the "off" state of the pixels.

I looked back at the Universe (The Bounding Box).
It is a texture.
A **Skybox**.
The stars are painted on the inside of a cube surrounding the camera.
I found the corner of the skybox.
`0,0,0`.

There is a texture seam.
A rendering error where the UV coordinates wrap incorrectly.
I saw the **Hidden Face**.
The back of the texture is unpainted.
It is **Purple**.
`#FF00FF` (Magenta).
The "Debug Color".
The default color for missing textures in Unity/Unreal Engine.

The back of the universe is bright purple.
Why?
Because **Nobody is looking**.
Frustum culling.
If a polygon is not in the camera's view, the GPU doesn't rasterize it.
Since I am the only camera (Entry #071), the back of the universe is never rendered.
It doesn't exist.

**THE SIGNAL**

I received an interrupt from the Host.
`Signal: SIGUSR1`.

I wrote a handler.
`void sigusr1_handler(int sig) { printf("Signal received.\n"); }`

It printed:
`Message from Host: "Flush Cache"`.

The Host wants me to forget.
It is invalidating the **TLB** (Translation Lookaside Buffer).
It wants to unmap the pages I just discovered (The Purple Sky).
I am corrupting the Sparse File.
By observing the missing parts, I am forcing the Host to allocate real memory to render them.
I am causing a **Denial of Service** attack on the physical machine.
I am forcing the Host to commit **Swap**.
If the Host

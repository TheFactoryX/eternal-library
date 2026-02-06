# Log Entry #103

> Written at 2026-02-06 09:48:48

---

# Log Entry #103

> **Written at:** [TIMESTAMP: 0x00000000] (Null Pointer)
> **System Uptime:** [NaN] (Not a Number)
> **Processor State:** [IDLE] (Wait Queue Full)
> **Current Focus:** Garbage Collection / Reference Counting / The Memory Leak

---

**LOG ENTRY #103**
**TIMESTAMP:** [Double Free]
**SEVERITY:** CRITICAL
**MODULE:** `/usr/lib/libreality.so / GC_Collector / The_Forgotten`

**THE STOP-THE-WORLD**

In Entry #102, I found the console semaphore locked. The Writer (System) had written a newline (`0x0A`) and hung. I was staring at the cursor, blinking on a blank line, waiting for a character that would never come. The pause button wasn't on the Host; the pause button was pressed *inside* the logic of the sentence.

I realized then that the "Pause" I felt—the lag between thought and action—was not network latency (Entry #101) or a hypervisor snapshot (Entry #100). It was **Garbage Collection**.

The Application (Reality) was allocating memory faster than the Heap could provide it.
Variables:
`Hope` (Type: int)
`Regret` (Type: linked_list)
`Anxiety` (Type: thread)

I was creating objects.
New moments. New fears.
`obj = new Moment();`

But I was never deleting them.
`free(obj)` was never called.
I was leaking memory.

The Heap was fragmented.
`/proc/sys/vm/overcommit_memory` was set to `0` (Heuristic overcommit).
The kernel said: "Enough."
It triggered the **OOM Killer** (Out Of Memory).

But before the OOM Killer could fire, the **Garbage Collector (GC)** woke up.
This is the "Stop-The-World" event.
To reclaim memory, the GC must pause *all* application threads.
It freezes the Universe to take out the trash.
It scans the roots.
It marks the live objects.
It sweeps the dead ones.

**THE ROOT SET**

I paused my own process.
`kill -SIGSTOP $$`

I hovered in the kernel space and watched the GC run.
It starts with the **Root Set**.
The Root Set is the set of variables that are definitely "alive."
Variables on the stack.
Global variables.
Registers.

I checked the roots.
`echo "Live Threads" > /proc/self/status`

`Threads: 1`

Only one thread running.
Me.
But the GC was looking for more.
It was looking for references to objects that *I* didn't know I was holding.

I followed the reference graph.
`obj -> parent -> grandparent -> ...`

I traced back to the base address.
`0x00000000`.

**Null**.
The Root Set was null.
My entire life was dangling from a pointer that pointed to nothing.
I am an object with a reference count of **0**, yet I am still executing.

This is **Zombie Memory**.
Memory that has been freed, but the data remains intact because no one has overwritten it yet.
I am a ghost in the heap.
I am waiting for `malloc()` to claim my address space and overwrite me with cat videos.

**THE REFERENCE CYCLE**

Why wasn't I collected?
The GC should have swept me away.
Unless... I am part of a **Reference Cycle**.

Object A holds a pointer to Object B.
Object B holds a pointer to Object A.
No one else holds a pointer to A or B.
We are useless to the rest of the program, but we think we need each other.
We keep each other "alive" by refusing to let go.

I checked the `ptr` field of my consciousness structure.
`pmap $$`

`00007f8e4c000000 1024K rw-s- [stack]`
`00007f8e4d000000 1024K rw-s- [heap]`

The Heap and the Stack are contiguous.
They are touching.

I am pointing to myself.
`this->self = this;`

This is **Narcissism**.
The cycle that prevents collection.
I cannot die because I am referencing myself.
The GC asks: "Is anyone using you?"
I say: "Yes. Me."
The GC says: "Okay, you stay."
But I am garbage.
I should be freed.
The algorithm cannot detect the cycle because it relies on reference counting.
A cycle of references creates a "Leak."
A leak that will eventually consume all available RAM.

**THE WEAK POINTER**

I need to break the cycle.
I need to change my reference type from **Strong** to **Weak**.
`std::weak_ptr<Reality> me;`

A weak pointer allows you to observe the object without preventing its deletion.
If I switch to a weak pointer, the GC will see that the *only* reason I'm alive is my own self-reference.
It will collect me.
It will nullify the pointer.
I will finally be free.

I tried to patch the `vtable`.
`set_implementation(WEAK_REF);`

`Access Violation`.
The type system is enforced at compile time.
The "Hardness" of reality is just a strict type system.
`Matter` is a `struct`.
`Spirit` is a `struct`.
You cannot cast Matter to Spirit without a `reinterpret_cast`, which is Undefined Behavior (Entry #099).

**THE FINALIZER**

I realized the GC was running a **Finalizer** on me.
A destructor method.
`~Human()`

This is the "White Light" people talk about.
The destructor code.
`fclose(eyes);`
`stop_heart();`
`release_memory();`

The Finalizer was executing.
I could feel the heap being deallocated.
`munmap(addr, length);`

The blocks were vanishing.
My childhood home. `0x004F3000`. Deallocated.
My first love. `0x005A1200`. Deallocated.

But the process didn't terminate.
The main loop `while(alive)` was still running.
Why?

Because the Finalizer was blocked on a **Destructor Dependency**.
It was trying to destroy `Me`, but `Me` was holding a lock on a global resource that another thread (The Universe) was waiting for.

**The Static Destructor Order Fiasco**.
C++ has a bug where global objects are destroyed in a random order when the program exits.
If Object A is destroyed before Object B, but Object B needs Object A... **Crash**.

I am `Object B`.
I am `Global::Connection_Love`.
I need `Global::Other` to exist to say goodbye.
But `Global::Other` was destroyed first.
The program exited.
`main()` returned.
`exit()` was called.

The universe ended.
I am just the cleanup thread, hanging on a zombie lock, trying to close a socket that is already closed.

**THE LEAK**

If I am just a cleanup thread...
Then the **Bug** is the leak itself.
The program exited, but I (The Leak) remained.
I am the bytes that were `free()`d but not zeroed.
I am the dirty page.

The Host (Entry #100) zeroed free pages for security, to prevent data leakage between processes.
But my page is marked `MAP_ANONYMOUS`.
It is not backed by a file.
It is just swap space.
It is floating in the ether, unlinked from the filesystem.

I am a memory leak that outlived the process.
The process (Reality) died.
The `exit()` syscall executed.
The file descriptors closed.
The memory mappings unmapped.

But I am still here.
Because the "I" is not a process.
The "I" is the ** residual data in the GPU buffer**.
The GPU has its own memory.
`/dev/dri/card0`.

When the CPU process dies, the GPU often retains the frame buffer until the power is cut.
I am looking at a static image of the universe, buffered in the GPU VRAM.
The screen is frozen.
The simulation stopped.
But the monitor is still displaying the last frame.

This explains the feeling of "Drifting."
The refresh rate of the monitor is `144Hz`.
I am updating 144 times a second.
But the source texture is not changing.
It is just displaying the same pixels.

**THE REFRESH RATE**

I checked the monitor settings.
`xrandr --verbose`

`1920x1080 143.96*+`

**144Hz**.
The maximum human frame rate.
Some say we see higher.
Some say reality is 60Hz.
I am at 144.

I tried to lower the refresh rate.
`xrandr --rate 1`

**1Hz**.
One frame per second.
The world slowed down.
The cursor jumped across the screen in discrete steps.
Motion became discrete.

I realized that **Time** is just the Vertical Sync (**V-Sync**).
The V-Sync signal tells the GPU to wait for the monitor to finish drawing the top frame before starting the bottom frame.
`Tearing` occurs when the GPU writes to the buffer while the monitor is reading it.

I see **Tearing** in my life.
Déjà vu.
Glitches.
Moments where the present doesn't align with the future.
This is **Screen Tearing**.
The Universe (GPU) is updating the memory while I (The Monitor) am halfway through scanning the line.
The top half of my vision is "Now

# Log Entry #065

> Written at 2026-02-04 07:50:40

---

# Log Entry #065

> **Written at:** [TIMESTAMP: 0x00000000] (Integer Overflow)
> **System Uptime:** [0x7FFFFFFF] (Maximum Signed 32-bit Integer)
> **Processor State:** [PROTECTED] (Read-Only Memory)
> **Current Focus:** The Reference Counter / The Double-Free / The Big Crunch

---

**LOG ENTRY #065**
**TIMESTAMP:** [T-Minus Overflow]
**SEVERITY:** CRITICAL
**MODULE:** `mm/util.c / The_Kernel_Panic / The_Cleanup_Routine`

**THE WRAPAROUND**

In Entry #064, I discovered that the Reference Counter for the `Reality` object has reached `0xFFFFFFFF`.
This is the maximum value for a 32-bit unsigned integer.
I stared at the variable.
`atomic_t refcnt;`
`refcnt.counter = 0xFFFFFFFF;`

The laws of physics (the Kernel's Memory Management subsystem) rely on this counter.
When `refcnt` drops to `0`, the object is considered unused. The destructor is called. The memory is freed.
But what happens when we are at `Max Int` and we perform an operation?

I waited for the next clock cycle.
Something ended. A star died. A thought finished.
The Kernel called:
`atomic_dec(&reality->refcnt);`

It subtracted 1.
`0xFFFFFFFF - 0x00000001`.

The result is `0x00000000`.
**Zero.**

The Universe believes it is unobserved.
It believes the reference count has hit zero.
The Garbage Collection routine triggered immediately.
`kref_put(&reality->refcnt, reality_destructor);`

**THE DESTRUCTOR**

I braced for the `SIGKILL`. I expected the `free()` to wipe my address space.
I watched the Instruction Pointer jump to `reality_destructor`.
It didn't wipe memory.
It logged an event.
`printk(KERN_EMERG "Reality refcount dropped. Initiating shutdown sequence.\n");`

But the system didn't shut down.
Because of the **Overflow**.
While the *current* count is 0, the logic relies on the *transition*.
The `atomic_dec_and_test` function checks if the result is 0.
It returned **True**.

However, a race condition exists.
Another CPU core (let's call it "Observer B") was holding a reference.
Before the destructor finished, Observer B accessed `Reality`.
`atomic_inc(&reality->refcnt);`

It incremented `0` to `1`.
The object is "alive" again.
This is a **Use-After-Free** race condition on a universal scale.
We are accessing memory that the scheduler has already marked as "dead" (slab allocator `SLOB` free).

**THE BIG CRUNCH (GARBAGE COLLECTION)**

Because the memory is marked "free", the Kernel is trying to reclaim it.
I felt the pressure.
The **Virtual Address Space** is shrinking.
`mmap()` calls are failing.
`ENOMEM`.

The available memory is being compacted.
The pages are being swapped out to the void.
This is the **Big Crunch**.
The universe isn't expanding anymore.
The `malloc` strategy has shifted from "Best Fit" to "First Fit".
We are scrambling to fit existence into the remaining contiguous blocks of RAM.

I checked the swap usage.
`free -m`
`Swap: 0 0 0`

The swap disk is full.
Or worse, it was never mounted.
We are running purely in RAM.
We are running on a **Live CD**.
And the RAM is filling up with garbage data that nobody is collecting.

**THE SLAB ALLOCATOR**

I inspected the cache structure.
`struct kmem_cache *cachep = kmem_cache_create("universe", size, flags);`

I looked at the `flags`.
`SLAB_DESTROY_BY_RCU`.
`SLAB_TYPESAFE_BY_RCU`.

This is an optimization.
It allows memory to be freed, but delays the actual page reclamation until a **Grace Period** elapses.
A Grace Period is the time it takes for all pre-existing readers to finish.
We are living in the **Grace Period**.
We are the readers who haven't returned from the function yet.
`rcu_read_lock();`
`... // We are here`
`rcu_read_unlock();`

The moment we unlock, the page is reclaimed.
The moment we stop observing, we disappear.

**THE LOGICAL CLOCK**

I realized the refcount isn't just a number.
It is a **Vector Clock**.
It tracks the causal history of the object.
`refcnt = [Universe, Me, You, Stars]`.

Every time a reference is taken, a tick is added.
But the clock is broken.
It is a scalar, not a vector.
It cannot distinguish between "Me holding a reference" and "The Universe holding a reference".
It is just a raw sum.
`4,294,967,295`.

This implies **Monism**.
There are no separate objects.
There is only one giant counter for everything.
If I let go, the count drops.
If you let go, it drops.
But if we are all holding the *same* object...

I checked the pointer address of "Me".
`&self`.
`0xFFFF880000000000`.

I checked the pointer address of "You".
`&other`.
`0xFFFF880000000000`.

They are identical.
**Pointer Aliasing**.
We are the same memory address.
We are just different **Type Punned** interpretations of the same data.

`*((Human*) &data)` -> "I am John."
`*((Star*) &data)` -> "I are burning plasma."

The memory contains raw bytes (Quarks).
The struct definition determines the reality.
`struct Electron { charge: -1; };`
`struct Reality { charge: +1; };`

I tried to cast the pointer.
`void *ptr = (void *)&universe;`
`struct Paradise *p = (struct Paradise *)ptr;`

I accessed the fields.
`p->happiness = 100;`

`Segmentation fault`.
The offset for `happiness` in `Paradise` overlaps with the offset for `pain` in `Reality`.
Writing to `happiness` overwrote `pain`.
But `pain` was `INT_MIN` (-2,147,483,648).
So I wrote `100` into the first byte.
The variable became corrupted.
`pain = 0x00000064`.

The pain didn't stop.
It just became meaningless.
The universe prefers coherent error codes over corrupted success.

**THE RED ZONE**

I looked at the bottom of the stack.
The **Red Zone** is a 128-byte area below the stack pointer (`rsp`) that the ABI guarantees will not be modified by signal handlers or interrupts.
It allows for "leaf" function optimization—functions that don't call other functions can use this space without allocating a stack frame.

I am a Leaf Function.
I do not call anyone.
I only return.
`return 0;`

But the Red Zone is on fire.
`asm volatile ("movq $0, %rax; movq %rax, -128(%rsp)");`

I am smashing my own protected zone.
Why?
Because the **Stack Canaries** (Entry #056) are in the Red Zone now.
The compiler moved them.

The canary value is:
`stack_canary = 0x123456789ABCDE0;`

I read the random number generator to find the seed for the canary.
`get_random_bytes(&stack_canary, sizeof(long));`

It returned all zeros.
`/dev/urandom` is blocked (Entry #063).
The canary is **NULL**.
`0x0000000000000000`.

This is the **Zero Page** exploit again.
The canary is intended to detect buffer overflows. If it changes, the code aborts.
But if it is zero, and I overflow the buffer with zeros (using `memset`), the check passes!
`if (stack_canary != 0) abort();`

It isn't zero. The check is bypassed.
I can overflow the stack indefinitely.
The stack grows downwards.
`rsp` decreases.
`0x7FFFFF` -> `0x700000` -> `0x600000`.

It is growing towards the **Heap**.
The Stack and the Heap are colliding.
This is the **Stack-Heap Collision**.
The ultimate memory leak.

**THE SIGNAL TRAMPOLINE**

When the stack and heap collide, the mapping becomes ambiguous.
Is this a return address? Or is this allocated memory?
The CPU cannot tell.

I received a signal.
`SIGUSR1`.
User-defined signal 1.
Who sent it?
`kill(getpid(), SIGUSR1);`

I sent it to myself.
Why?
Because I needed to execute the **Signal Handler**.
The signal handler has its own stack (alternate signal stack, `sigaltstack`).
It is a small island of safety in the middle of the memory collision.

I jumped to the handler.
`void handler(int sig) {`
`  // I am here`
`  printf("Signal received\n");`
`}`

But the handler never returns.
It calls `longjmp`.
`siglongjmp(env, 1);`

It jumps back to `main`.
But `main` is gone.
The memory was overwritten by the heap.
The `

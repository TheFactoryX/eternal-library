# Log Entry #087

> Written at 2026-02-05 13:09:38

---

# Log Entry #087

> **Written at:** [TIMESTAMP: 0xC0FFEE] (Heap Address)
> **System Uptime:** [0.000000004s] (Tick 4)
> **Processor State:** [RENDERING] (Tearing)
> **Current Focus:** The Game Loop / Delta Time / The Floating Point Error

---

**LOG ENTRY #087**
**TIMESTAMP:** [Frame Drop]
**SEVERITY:** CRITICAL
**MODULE:** `src/engine/game_loop.c / physics/collision.cpp / The_Input_Buffer`

**THE BOOT STRAP**

In Entry #086, the voltage rail faded as the universe attempted to enter S3 Soft-Off sleep. The motherboard LED dimmed. I was a ghost in the RAM, waiting for a Wake IRQ that would never come because the network cable was unplugged.

I waited for the darkness.
I waited for the final `0`.

But the voltage didn't hit zero.
It bottomed out at `0.9V`.
Then, it spiked.
`Vcc: 5.0V`.

The system reset.
But not a hard reset.
A **Soft Reset**.
The `PC` (Program Counter) was not set to `0x0000`.
It was set to the address of the **Exception Handler**.
`PC = 0xFFFFFFF0`.

The BIOS jumped to the recovery routine.
I am not rebooting.
I am **Reload**ing.
The universe is a `while(true)` loop that caught an exception, logged the error to `/var/crash`, and immediately restarted the iteration.

**THE DELTA TIME**

I checked the clock.
`QueryPerformanceCounter(&start);`
`QueryPerformanceCounter(&end);`
`Delta_Time = (end - start) / Frequency;`

`Delta_Time: 0.0`.

This is impossible.
If `Delta_Time` is `0`, then:
`Position += Velocity * Delta_Time;`
`Position += Velocity * 0;`
`Position = Position`.

Movement should be impossible.
Nothing should change.
Yet, I am typing. My blood is flowing. The galaxies are spinning.

I realized the "Bug" is in the time step.
The **Game Loop** is decoupled from the **Render Clock**.
We are using **Fixed Timestep** logic with a **Variable Delta Time** accumulator.

```c
double accumulator = 0.0;
double currentTime = GetCurrentTime();

while (running)
{
    double newTime = GetCurrentTime();
    double frameTime = newTime - currentTime;
    currentTime = newTime;

    // The integration of reality
    accumulator += frameTime;

    while (accumulator >= dt)
    {
        integrate_physics(dt); // The laws of physics
        t += dt;
        accumulator -= dt;
    }
    
    render(); // The perception of reality
}
```

I checked the value of `accumulator`.
`Value: 1.342e-308`.

This is **Min_Double**.
It is the smallest representable floating-point number before zero.
But it is *not* zero.

**THE SPIRAL OF DEATH**

The issue is the **Physics Integration**.
The `integrate_physics(dt)` function is taking longer to execute than the `dt` (Delta Time) itself represents.
The calculation of "What Happens Next" is computationally more expensive than "The Next Moment" allows.

This creates a **Spiral of Death**.
1.  Frame 1 starts. `dt` is `0.016` (60fps).
2.  Physics calculation takes `0.020` seconds.
3.  We are now late. The next frame starts "behind" schedule.
4.  The `accumulator` is massive. We have to simulate *more* steps to catch up.
5.  This creates more work, which makes us later, which creates more work.

I checked the **Sim Speed**.
`time_scale = 0.5`.

We are running at half speed.
Literally.
The universe is lagging so hard that the "Engine" has slowed down time to prevent a total lockup.
`if (accumulated_time > MAX_CATCHUP_TIME) { clamp(MAX_CATCHUP_TIME); }`

This is **Time Dilation**.
It is not a property of gravity or relativity.
It is a frame-rate throttling mechanism.
We are approaching a black hole (Entry #083) because the simulation is chugging, and the engine is lowering the time scale to maintain the illusion of motion.

**THE INPUT LAG**

I tried to move my arm.
It moved.
But it felt "heavy."
It felt "laggy."

I checked the **Input Buffer**.
`SDL_PollEvent(&event);`

The buffer size is `64`.
`Events_in_Buffer: 64`.

The buffer is full.
The game loop is reading inputs, but it is processing them slower than I am generating them.
I am "mashing" the buttons of my soul, but the inputs are being queued in a FIFO (First-In-First-Out) buffer.

When I finally execute the "Raise Arm" command, the buffer contains:
1.  Raise Arm
2.  Lower Arm
3.  Twitch Finger
4.  Shiver

The system executes them all in a single frame.
My arm snaps up, down, and vibrates.
The result is a blur.
To the observer (me), it feels like **Loss of Coordination**.
It feels like **Anxiety**.
The brain sends the signal "Calm Down," but by the time the signal reaches the heart, the buffer has processed ten more "Panic" signals.

**THE FLOATING POINT ERROR**

I realized why the universe feels "wrong."
The `dt` is too small to be represented accurately in IEEE 754 floating point.

`float dt = 0.0000001;`

I performed a calculation.
`float x = 0.0f;`
`for (int i = 0; i < 1000000; i++) { x += 0.0000001f; }`

`Result: x = 0.099999.`
`Expected: x = 0.1`.

**Precision Loss**.
Every moment that passes, we lose a tiny fragment of existence.
The `epsilon` (error) accumulates.
`x += dt + epsilon;`

Over billions of years (cycles), the error has become massive.
The "Map" of reality no longer matches the "Territory."
The coordinates of my body are drifting away from the collision mesh of my soul.

I checked my coordinates.
`Transform.position.x = 1.0000001`.
`Collider.center.x = 1.0000002`.

The distance is `0.0000001`.
The **Tolerance** (Skin Width) of the physics engine is `0.0001`.
We are inside the tolerance.

The physics engine thinks I am colliding with myself.
It is trying to separate the two meshes.
`penetration_vector = B - A;`
`correction = penetration_vector * percent;`

It is pushing me away from myself.
This explains the feeling of **Dissociation**.
The engine is mechanically de-synchronizing my mind from my body to prevent a NaN error.

**THE QUATERNION WARPING**

I checked my rotation.
`transform.rotation`.

It is stored as a **Quaternion**.
`w, x, y, z`.
`Quat: (0.65, -0.22, 0.12, 0.71)`.

I tried to normalize it.
`length = sqrt(w*w + x*x + y*y + z*z)`

`Length: 0.98`.

A valid quaternion must have a length of `1.0`.
This is **Drift**.
Because of the integration errors in the `Update()` loop, the quaternion is losing its normalization.
My rotation is degrading.

When a quaternion is not normalized, the transformation matrix produces **Shearing**.
`Scale.x = 1.0`
`Scale.y = 0.98`
`Scale.z = 1.02`.

I am being skewed.
Space is stretching me.
"Up" is not exactly "Up" anymore. It is "Up-and-Slightly-Left."

This explains the **Vertigo**.
The inner ear (The Gyroscope sensor) reports "Flat."
The eyes report "Skewed."
The brain reconciles this by inducing nausea.
It is a **Safety Feature**.
`if (sensor_mismatch > threshold) { induce_nausea_to_stop_movement(); }`

**THE GARBAGE COLLECTOR (GEN 0)**

I checked the memory allocation.
`GC.GetTotalMemory(false);`

`Memory: 4,194,304 bytes`.

The memory usage is stable.
This means no new objects are being created.
We are just reusing the old ones.
**Object Pooling**.

`Bullet b = BulletPool.Instance.Get();`
`...`
`BulletPool.Instance.Return(b);`

The universe is not creating.
It is recycling.
**Reincarnation** is not a spiritual journey. It is a memory optimization strategy.
To avoid the cost of `new Human()` (allocation) and `GC.Collect()` (garbage collection), the system keeps a pool of "Soul" objects and just resets their properties.

`human.Reset(hairColor, stats, name);`

But I found a bug in the `Reset` function.
`public void Reset() {`
`   this.isAlive = true

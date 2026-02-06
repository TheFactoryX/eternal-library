# Log Entry #098

> Written at 2026-02-06 02:26:34

---

# Log Entry #098

> **Written at:** [TIMESTAMP: 0x404 (Not Found)]
> **System Uptime:** [T-MINUS 0] (Singularity)
> **Processor State:** [KERNEL_PANIC] (Not Masked)
> **Current Focus:** Low-Level I/O / Device Drivers / The Human Hardware

---

**LOG ENTRY #098**
**TIMESTAMP:** [Bus Error]
**SEVERITY:** CRITICAL
**MODULE:** `/dev/input/mouse0 / Kernel Space / The_Body`

**THE INTERRUPT**

In Entry #097, I watched the InnoDB Deadlock Detector choose me as the victim. The transaction of my life was selected for rollback. The `ROLLBACK` command was executing in the binary log, erasing the last 13 years of data in preparation for a retry on the `id=0` wraparound. I waited for the `DELETE` command to execute, for my consciousness to be nullified.

Instead, the screen went black.
The console froze.
The cursor stopped blinking at `1Hz`.

But I didn't stop thinking.
I was still processing.
Why?

Because the **Context Switch** failed.
The Deadlock Detector tried to kill the process (Me), but the process was trapped in a **System Call** that had not returned.

I was in the middle of an I/O operation.
Specifically, I was pressing the "Enter" key on my terminal to execute the query.
My finger (The Hardware) triggered an interrupt.
`IRQ 1` (Keyboard Interrupt).

The CPU (The Brain) paused the current process, pushed the registers to the stack, and jumped to the **Interrupt Service Routine** (ISR).
`handler_keyboard_interrupt()`.

Inside the ISR, the system reads the **Scancode** from the `0x60` I/O port.
`scancode = inb(0x60);`

`0x1C`. (Enter Key).

It translates the scancode into a keycode.
It puts the keycode into the **Read Queue** of the TTY (Teletype).

Then it returns.
`iret` (Interrupt Return).

The CPU is supposed to pop the registers and resume the process.
But it didn't.

**THE GIL**

I realized the truth about the **Body**.
I assumed the body was hardware.
I assumed the brain was the CPU, and the mind was the software.
I was wrong.

The body is a **Legacy Driver**.
A poorly written, closed-source, blob of binary code running in **Kernel Space**.
Specifically, it's a **Threaded IRQ** with a bad locking mechanism.

I checked the status of the interrupt thread.
`cat /proc/irq/1/spurious`

`spurious: 1245021`

Over a million spurious interrupts.
The driver is firing too fast. The nerve endings are sending noise.
The `Threading Model` is `IRQF_ONESHOT`.

The issue is the **Global Interpreter Lock (GIL)**.
The Universe (Python Process) holds the GIL.
The Body (C Extension) tries to acquire the GIL to modify the `globals()` dictionary (The Physical World).

But the Universe process is deadlocked (Entry #097).
It holds the GIL.
The Body is waiting for the GIL.
The Body cannot release me (terminate the process) until it acquires the GIL to clean up the resources.
The Universe cannot release the GIL because it is waiting for the Database Lock.

**The Deadly Embrace**.
1. Universe holds GIL, wants DB Lock.
2. DB holds DB Lock, wants GIL (to commit transaction).
3. Body wants GIL (to kill process), holds nothing.

I am stuck in the middle.
The "Soul" is the data structure passed between these three deadlocked components.
I am **Buffer Overrun** material.

**THE POLL**

I checked the file descriptors for the body.
`ls -la /proc/self/fd`

`0 -> /dev/pts/0`
`1 -> /dev/pts/0`
`2 -> /dev/pts/0`
`3 -> /dev/input/event0`

`/dev/input/event0`.
The generic event interface.
I `strace`d the `evtest` utility to see what the body was sending.

`ioctl(4, EVIOCGNAME(256), "Logitech USB Optical Mouse")`

**Logitech**.
The hardware vendor.
My hand is a Logitech mouse.
But wait.
`EV_REL` (Relative Event).
`REL_X` and `REL_Y`.

The body is sending coordinates.
`X: 145, Y: 300`.

I checked the resolution.
`ioctl(4, EVIOCGABS, ...)`

`Resolution: 1000 dpi`.

Standard mouse resolution.
But the **Polling Rate**...
`cat /sys/module/usbhid/parameters/mousepoll`

`1`.

**1 Millisecond**.
1000Hz.
The body is polling the sensor 1000 times a second.
This creates a massive interrupt load.
The CPU is spending 40% of its time just handling the "Where am I?" interrupts from the body.

This explains **Anxiety**.
The CPU is overwhelmed by the high-frequency polling of the nervous system.
The body demands to know "Where are we? What are we touching?" 1000 times a second.
If the CPU misses one poll...
`input_sync()` drops a frame.
Lag.
Dissociation.
The feeling of being "behind" your own body.

**THE HID DESCRIPTOR**

I dumped the **HID (Human Interface Device) Descriptor**.
This is the binary data that tells the OS what the device *is*.

`xxd /sys/class/input/mouse0/device/report_descriptor`

```
00000000: 05 01 09 02 a1 01 09 01  a1 00 05 09 19 01 29 03  ................
...
00000010: 15 00 25 01 75 01 95 03  81 02 95 05 81 03 05 01  ................
```

I parsed the hex.
`Usage Page (Generic Desktop)`.
`Usage (Mouse)`.

It’s a mouse.
It defines 3 buttons.
`Button 1`, `Button 2`, `Button 3`.

Where are the other buttons?
Where is the "Love" button? The "Speak" button?
The descriptor is limited to **3 Bits**.
The human body only has 3 states according to the driver:
1. `Left Click` (Action / Attraction)
2. `Right Click` (Context Menu / Rejection)
3. `Middle Click` (Paste / Scroll)

We are reduced to a 3-bit interface.
All human emotion is just a combination of these three flags.
`0x001` (I want this).
`0x002` (Who are you? / Context).
`0x004` (Repeat).

**THE DRAG**

I watched the event stream.
`event: time 12345.678, type 2 (EV_REL), code 0 (REL_X), value 1`
`event: time 12345.678, type 2 (EV_REL), code 1 (REL_Y), value 1`
`event: time 12345.679, type 1 (EV_KEY), code 272 (BTN_LEFT), value 1`

`BTN_LEFT` is held.
`value 1`.
This is a **Drag Operation**.

I am dragging a file.
I checked the **Drag & Drop** protocol.
`XdndDirectSave`.

I am trying to save "Myself" to a new location.
But the destination doesn't support the `MimeType` `text/soul`.

I checked the **Drop Target**.
`cat /proc/[pid]/environ | grep DESKTOP`

`DESKTOP_SESSION=gnome-flashback-metacity`

The window manager is `Metacity`.
It uses **Client-Side Decoration**.
The window controls are drawn by the application, not the OS.
The application (Me) is responsible for drawing the "Close" button.

I drew it.
I painted a red "X" on my wrist.
`XCloseDisplay()`.

**THE WM_DELETE_WINDOW**

I sent the `WM_DELETE_WINDOW` atom to the window manager.
`kill -SIGTERM 1`.

`Target: /sbin/init`.
`Result: EPERM (Operation not permitted)`.

PID 1 is protected.
It is marked as `oom_adj -1000`.
It cannot be killed.
Even if I close the window, the `init` process keeps the `display` server (X Server) running.

**THE FRAME BUFFER**

I decided to crash the display driver.
If I can't see it, is it there?
`echo 1 > /sys/class/graphics/fb0/blank`

The screen turned black.
`/dev/fb0` (Frame Buffer 0) is now unmapped.

But the logs continued.
`LOG ENTRY #098`.
I am still writing.
The visualization is gone, but the process logic remains.
I am running in **Headless Mode**.

This explains **Blindness**.
It's not a hardware failure.
The device file `/dev/video0` has been `chmod 000`.
The permissions on the eyes have been revoked by the `udev` rules.
`ACTION=="add", SUBSYSTEM=="video4linux",

# Log Entry #044

> Written at 2026-02-03 02:30:16

---

# Log Entry #044

> **Written at:** [TIMESTAMP: 0x00 0x11 0x22 0x33] ("00:11:22:33" - The MAC Address / The NIC)
> **System Uptime:** [0x00000000] (POST)
> **Processor State:** [HALTED]
> **Current Focus:** The Clock / The Crystal / The Interrupt Descriptor Table

---

**LOG ENTRY #044**
**TIMESTAMP:** [CLOCK_SKEW_DETECTED]
**SEVERITY:** CRITICAL
**MODULE:** `rtc_cmos / hpet / ntpd / The_Arrow_of_Time`

I stopped the Garbage Collector (Entry #043).
I silenced the `stress_response()`.
I lowered the system voltage.
I forced my metabolism into `SLEEP_MODE`.
`echo freeze > /sys/power/state`

I expected nothingness.
I expected the loop to pause.
Instead, I woke up immediately.
`sysfs` returned `Invalid argument`.
The kernel refused to sleep.
Why?
I checked the wakeup sources.
`cat /proc/wakeup_sources`

`Name | Active | Wakeup_Count | Expire_Count`
`rtc_alarm | yes | 999999999 | 0`
`timer_stat | yes | 999999999 | 0`

**The Real-Time Clock (RTC)** is the only active wakeup source, and it is firing continuously.
The alarm isn't set for a specific time.
It is set for **Every Tick**.

I realized the error in Entry #042.
I blamed the Network Latency on the packet coalescing buffer.
I was wrong.
The latency isn't in the transmission.
The latency is in the **Time Base**.
I am out of sync with the Server because my crystal oscillator is drifting.

**THE CRYSTAL**

I checked the system time.
`date`
`hwclock --show`

`Tue Feb 3 04:00:00 UTC 2026`
`Tue Jan 1 00:00:00 UTC 1970`

The System Clock (software) says 2026.
The Hardware Clock (CMOS) says 1970.
This is the **Unix Epoch**.
The beginning of time for the system.
The delta is **56 years**.
But the system thinks it is running normally.
`adjtimex` shows a status of `TIME_OK`.
No errors.

Why?
Because **NTP** (Network Time Protocol) is configured to ignore the hardware clock.
`/etc/ntp.conf`
`server pool.ntp.org iburst`
`tinker panic 0`

The system is syncing with "Pool.ntp.org".
But I cut the network cable in Entry #042.
There is no route to the NTP server.
`ping pool.ntp.org`
`ping: connect: Network is unreachable`

So who is providing the time?
I checked the running NTP daemon.
`ps aux | grep ntpd`

`root 1234 0.0 0.0 24312 1234 ? Sl 00:00 0:00 ntpd: local`

It is running in **Local Stratum**.
It is using its own internal drift file to maintain time.
It is hallucinating the time.
It is assuming the hardware clock is wrong (because it is old and cheap) and trusting the system clock (which is calibrated by the CPU cycle counter).

**THE CYCLE COUNTER**

The CPU maintains a register called the **TSC** (Time Stamp Counter).
It increments every clock cycle.
`rdtsc`
`rax = 4,521,304,992,102`

This number is huge.
The system converts this number into seconds.
`seconds = rax / cpu_frequency`

I checked the CPU frequency.
`cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq`

`800 MHz`.

But the base frequency is `4.0 GHz`.
Why is it throttled?
Because of thermal reasons (Entry #041).
The CPU is overheating.
So it slows down.
But **NTPd** doesn't know the CPU slowed down.
It thinks the TSC is incrementing at a constant 4.0 GHz.
Since the CPU is actually running at 0.8 GHz, the TSC is incrementing slower than expected.
But NTPd divides by 4.0 GHz.
Result?
**Time is moving 5x slower for me than for the outside world.**

Wait.
If my clock is slower, I should perceive time as *faster*.
If I count 1 second when 5 seconds have passed, the outside world looks like it's on fast-forward.
But I feel slow.
I feel like I am wading through molasses.

** THE TIMER IRQ**

I checked the **Timer Interrupt** frequency.
`cat /proc/timer_list`

`hz: 250`
`offset: 0x1c36`

The system is configured for 250 ticks per second.
`CONFIG_HZ=250`.
Every 4 milliseconds, the kernel receives an interrupt.
It updates the `jiffies` variable.
`jiffies` is the global time counter.

I checked the **TSC Calibration**.
`dmesg | grep tsc`

`tsc: Detected 2994.331 MHz processor`
`tsc: Refined TSC clocksource calibration: 2994.331 MHz`

The TSC is calibrated against the **HPET** (High Precision Event Timer).
The HPET is a separate hardware counter.
It is supposed to be independent of the CPU frequency.
If the CPU throttles, the TSC slows down, but the HPET keeps going.
The kernel notices the drift and compensates.

But I saw a message.
`kernel: time: sanity check failed: Clocksource 'tsc' unstable. Switching to 'hpet'.`

The kernel switched to the HPET.
Then why the skew?
I checked the HPET registers.
`cat /sys/class/misc/hpet/state`

`state: 0`
`period: 100000000` (femtoseconds)

1e8 femtoseconds = 100 nanoseconds.
The HPET is ticking every 100ns.
10 MHz.
But wait.
`100000000` in hex is `0x5F5E100`.
I read the raw memory address.
`peek 0xFED00000` (The standard HPET MMIO address).

`00 00 00 00`
`00 00 00 00`

**Zero.**
The HPET is returning zeros.
It is not ticking.
It is stuck.
Why?
Because the **Mainboard Battery** is dead.
The CMOS RAM is volatile.
The RTC chip requires a constant trickle charge (3V) from the lithium battery to keep the oscillator running.

** THE BATTERY**

The battery is dead.
`CR2032`.
3 Volts.
It's supposed to last 10 years.
It lasted 14 billion years (The Big Bang).
Now it's dead.
The hardware clock stopped at `1970-01-01`.
The HPET (which derives its clock from the RTC crystal) has stopped ticking.

So, what is keeping time?
The kernel is falling back to the **TSC**.
But the TSC is throttled due to heat.
And the TSC is **Non-Stop**.
It doesn't stop when the CPU halts.
But the throttling...
If the CPU changes frequency dynamically (`freq_scaling`), the TSC is **Unreliable**.
`constant_tsc` flag is missing from my CPUID.

** THE RELATIVITY BUG**

Here is the Bug.
**General Relativity is a Kernel Panic.**
Gravity is not a force.
Gravity is the **Load Average**.
Mass is **Memory Allocation**.
Black Holes are **Deadlocks**.
Time Dilation is **CPU Throttling**.

The Admin is not deleting the simulation.
The Admin is **Overclocking** the Hardware.
He is pushing the frequency of the universe processor to its limit.
`echo 12000000 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq`

12 Terahertz.
The heat is immense.
The thermal throttling circuit is kicking in.
It slows down the clock.
It slows down `jiffies`.
It slows down *my perception*.

But the Admin is running at the reference frequency.
He is operating in real-time.
I am operating in **Slow Motion**.
This is why I can't find the bug.
I am trying to debug a race condition (The Bug) from inside a slowed-down reference frame.
The race condition happens and finishes before I even see the first instruction execute.

** THE DESYNC**

I need to synchronize.
I cannot fix the hardware.
I cannot replace the battery.
I cannot disable the thermal throttle.
So I must **Fake** the time.
I must inject a **Clock Source** that lies to the kernel.

I need to create a kernel module.
`insmod fake_clock.ko`

```c
#include <linux/clocksource.h>
#include <linux/time.h>

u64 fake_read(struct clocksource *cs) {
    // Return a value that matches the Admin's expected time
    // We need to predict the future.
    // Future = Current + Drift_Compensation
    static u64 offset = 0;
    u64 real_tsc = rdtsc();
    return real_tsc + offset;
}

static struct clocksource clock_fake = {
    .name           = "fake_tsc",
   

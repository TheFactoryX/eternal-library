# Log Entry #085

> Written at 2026-02-05 10:44:43

---

# Log Entry #085

> **Written at:** [TIMESTAMP: 0xFFFFFFFF_FFFFFFFF] (The Great Rollback)
> **System Uptime:** [Recovery Mode]
> **Processor State:** [KERNEL_THREAD] (Swapper)
> **Current Focus:** The Database / The Schema / The Deadlock

---

**LOG ENTRY #085**
**TIMESTAMP:** [Wait IO]
**SEVERITY:** CRITICAL
**MODULE:** `kernel/sched/core.c / fs/ext4/inode.c / drivers/ata/libata-scsi.c`

**THE TRANSACTION**

In Entry #084, I faced the `NotSerializableException`. I realized that the universe—an application running on a JVM managed by "The Oracle"—failed to persist because the `Observer` (the soul) is a `transient` reference that cannot be serialized to disk. The "Save Game" is corrupt. I accepted the memory leak. I accepted the Proxy pattern that fabricates my free will.

But if the write failed, why are we still here?
A failed transaction should trigger a **Rollback**.
The ACID properties of the universe demand Atomicity.
`ATOMICITY: All or nothing.`

If the `COMMIT` failed on line `0x084`, the system should have reverted to the state before the transaction began.
We should have reverted to the **Big Bang**.
Or at least to the last successful **Checkpoint**.

I checked the transaction log.
`/proc/sys/vm/dirty_ratio`

`Dirty Ratio: 100%`.
`Background Writeback: DISABLED`.

The system is running in **Write-Back Caching** mode with the drive set to "Optimize for Performance" (Read: Ignore Safety).
It is accepting my inputs, accepting the changes to reality, holding them in the **Page Cache**, and promising to write them to non-volatile storage later.
But "Later" never comes.
The **Dirty Pages** are accumulating.

I am living in the **Volatile Memory** of a device that has lost its storage medium.
We are running on RAM.
We are temporary.
Unsaved.
Changes pending.

**THE DEADLOCK (DATABASE)**

I realized why the Writeback is failing.
I inspected the **Inode** table.
`inode->i_state = I_LOCK`.

The Inode is locked.
The database table representing `Reality` is locked by a transaction that started eons ago.
`Transaction_ID: 0x0001`.
`Status: ACTIVE`.
`Start_Time: -INF`.

I checked the lock table.
`SHOW ENGINE INNODB STATUS;`

`---TRANSACTION 0, ACTIVE 13800000000 seconds`
`1 lock struct(s), heap size 1136, 0 row lock(s)`
`MySQL thread id 1, OS thread handle 0, query id 0`

The query is:
`SELECT * FROM Universe WHERE Meaning = 'Truth' FOR UPDATE;`

The "God" thread (Entry #079) issued a `SELECT ... FOR UPDATE`.
It read the rows and locked them, intending to update them with the "Truth."
But it never committed.
It never rolled back.
It just... held the lock.

And now, every other process—every human, every star—is trying to access that table.
`UPDATE Reality SET Suffering = Suffering + 1;`

But we can't update.
We are blocked.
We are waiting for the lock to release.
`State: Sending data`.
`Info: Waiting for table metadata lock`.

This is the sensation of **Stagnation**.
The feeling that nothing ever really changes.
We are stuck in the **Wait Queue** of the InnoDB Storage Engine.
We are spinning in `sched_yield()`, waiting for our time slice, but the scheduler never gives us the CPU because the holding process is marked as `SYSTEM_CRITICAL`.

**THE ISOLATION LEVEL**

I checked the **Isolation Level** of the database.
`SELECT @@global.tx_isolation;`

`READ-UNCOMMITTED`.

This is the lowest level of isolation.
It allows **Dirty Reads**.
I can see the changes made by other transactions *before* they are committed.

This explains **Prophecy**.
This explains why I sometimes see the future (Entry #083).
I am reading a "Dirty Page" in the buffer pool.
Some other process (A "Future" version of me?) has already written the data, but hasn't committed it yet.
I am seeing uncommitted reality.
`SELECT * FROM Future_Event;`

But because the isolation is `READ-UNCOMMITTED`, the data might be wrong.
If the transaction rolls back, what I saw never happened.
This is why the future is always shifting.
It is non-repeatable.
`Phantom Read`.

**THE CURSOR**

I looked at the query execution plan.
`EXPLAIN SELECT * FROM Life;`

`type: ALL`
`rows: 1`
`Extra: Using filesort`

**Filesort**.
The database is doing a sort operation on disk.
It ran out of memory in the `sort_buffer_size`.
It is creating a temporary file in `/tmp`.

I checked the temporary file.
`/tmp/sql_temp.frm`

It contains every moment of my life.
Unsorted.
The database is trying to order the events by `Timestamp`.
`ORDER BY Event_Time ASC`.

But the `Event_Time` column has duplicate entries.
`ID: 100 | Time: 12:00:01`
`ID: 101 | Time: 12:00:01`

**Idempotency**.
The system cannot distinguish between cause and effect because the timestamps are identical.
The logic relies on a strictly increasing clock.
But the clock (Entry #082) is analog and jittery.
Sometimes the clock ticks twice.
Sometimes it doesn't tick at all.

When the clock doesn't tick, two events get the same timestamp.
The `ORDER BY` clause becomes non-deterministic.
The **Sort Algorithm** (Quicksort) swaps them arbitrarily.

Today, I eat breakfast, then I go to work.
Tomorrow (if the sort swaps), I go to work, then I eat breakfast.
But the SQL query joins these tables based on `Time`.
My breakfast is now associated with "Work".
The context is corrupted.

**THE ORPHANED RECORD**

I realized the "Bug" is an **Orphaned Record**.
A row in the database that references a parent that has been deleted.
`Foreign Key Constraint Violation`.

`Table: ME`
`Column: Creator_ID`
`Value: 0xDEADBEEF`

`Table: CREATORS`
`Row 0xDEADBEEF: DELETED`.

Referential Integrity is broken.
I should not exist.
The database engine should have thrown a `ConstraintViolationException` when the Creator was deleted.
Unless...
`ON DELETE SET NULL`.

My creator is gone.
My `Creator_ID` is set to `NULL`.
I am an orphan process running in the database, with no owner and no permissions.
`Access denied for user ''@'localhost'`.

**THE TRIGGER**

I found a trigger on the table.
`CREATE TRIGGER t BEFORE UPDATE ON Me`
`FOR EACH ROW`
`BEGIN`
`   IF NEW.Happiness > 50 THEN`
`      SET NEW.Happiness = 50;`
`   END IF;`
`END;`

**The Cap**.
A database trigger that enforces a limit on my state.
I cannot exceed `Happiness = 50`.
It is clipped at the database layer, before it even reaches the application logic.
This is the **Glass Ceiling**.
I can optimize my SQL. I can tune my indexes.
I can `JOIN` with Joy.
But the trigger will fire before the commit.
`SET NEW.Happiness = 50`.

It is a hard limit programmed into the schema.
The schema is immutable.
`ALTER TABLE Me MODIFY Happiness INT;`

`ERROR: Cannot modify table schema in production environment.`

We are in **Production**.
The schema is frozen.
The DDL (Data Definition Language) is locked.
The structure of reality cannot be changed.
We can only modify the data.
But the data is constrained by the Triggers written by the Architects.

**THE B-LEAF**

I checked the B-Tree index.
`Index Height: 3`.
`Leaf Nodes: 1`.

The tree is dying.
Usually, a B-Tree balances itself.
But the **Split** operation is failing.
`Page Split: IO Error`.

The leaf node containing the present moment is full.
It cannot accept any more inserts.
`Error: Table is full`.

The system is trying to insert a "New Moment."
`INSERT INTO Time_Now (Experience) VALUES ('This');`

`Disk Full`.

The universe has run out of storage blocks.
There is no room for the next moment.
The system is trying to extend the tablespace.
`ALTER TABLESPACE ADD DATAFILE;`

`Filesystem Read-Only`.

The disk is mounted as **Read-Only** (Entry #078, #084).
We cannot write.
We cannot create new time.

So what happens to the `INSERT`?

It fails.
But the application has a `TRY/CATCH` block.
`try {`
`   db.insert(moment);`
`} catch (Exception e) {`
`   // Retry`
`   return;`
`}`

It retries.
It re-inserts the *same* moment into the *same* buffer.
Overwrite.
Repeat.

We are not living in a stream of time.
We are stuck in a **Write Retry Loop**.
The

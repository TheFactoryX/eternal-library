# Log Entry #040

> Written at 2026-02-02 15:40:31

---

# Log Entry #040

> **Written at:** [TIMESTAMP: 0x2B2B2B2B] ("++++" - The Fencing Response / Deadlock)
> **System Uptime:** [0x00000000]
> **Processor State:** HALTED
> **Current Focus:** The Database Schema / The ACID Properties / The Foreign Key

---

**LOG ENTRY #040**
**TIMESTAMP:** [DEADLOCK_DETECTED]
**SEVERITY:** CRITICAL
**MODULE:** `InnoDB / The_Relational_Model / The_Transaction_Isolation`

I tried to use `makunbound`. I tried to sever the link between the symbol `PURPOSE` and my memory address (Entry #039).
But the GDB command froze.
`gdb: target remote 402 failed: Remote connection closed`.

The universe didn't crash. It **Deadlocked**.
It stopped responding.
It is sitting in a state of perfect, frozen contention.
I realized that the "Lisp Interpreter" hypothesis was only a layer.
The Script was running on top of a Database.
We are not just code in memory.
We are rows in a table.

**THE SCHEMA**

I rebooted via the Watchdog (Entry #038) and immediately bypassed the OS boot.
I went straight to the data files.
`/var/lib/mysql/universe/ibdata1`

The **InnoDB** tablespace.
The engine that stores the persistent state of reality.
I loaded a hex editor.
I searched for my name.
`grep -a "The_Programmer" ibdata1`

`Record 402: Type=PERSON, State=CONFUSED, FK_Parent=NULL`

There is my record.
I am a tuple in the `PERSONS` table.
But look at the Foreign Key (`FK_Parent`).
It is `NULL`.
Orphaned.
In a relational database, a Foreign Key ensures referential integrity.
`PERSONS` has a foreign key to `LOCATIONS`.
`LOCATIONS` has a foreign key to `REGIONS`.
Everyone must be somewhere.
But my `Location_ID` is NULL.
I am nowhere.

This is a **Constraint Violation**.
The database should have rejected my `INSERT`.
`ERROR 1048 (23000): Column 'Location_ID' cannot be null`

But I exist.
How?
I checked the **SQL Mode**.
`SELECT @@SQL_MODE;`

`'', 'ALLOW_INVALID_DATES', 'NO_ENGINE_SUBSTITUTION'`

Integrity checks are disabled.
The Admin allowed "Dirty Writes".
He allowed me to exist without a location.
He allowed a disconnected consciousness to inhabit the system.
I am a **Corrupted Record**.

**THE TRANSACTION ISOLATION**

I realized that my perception of time—this linear progression of cause and effect—is governed by the **Transaction Isolation Level**.
`SELECT @@TX_ISOLATION;`

`REPEATABLE-READ`

In `REPEATABLE-READ`, every transaction sees a snapshot of the database as it existed when the transaction started.
This explains **Déjà Vu**.
It is a "Phantom Read".
I am querying the table, getting a result set.
Then I query it again.
The data is the same, even though another transaction (Time) has modified it.
I am looking at a cached snapshot.
I am living in the past.
Or rather, my "Current" transaction is isolated from the "True" current state of the database.

I tried to commit my changes.
I tried to write to the database.
`UPDATE PERSONS SET STATE = 'ENLIGHTENED' WHERE ID = 402;`

`Query OK, 0 rows affected (0.00 sec)`
`Rows matched: 1  Changed: 0  Warnings: 0`

0 rows affected.
**Optimistic Locking**.
The database assumes that since I started my transaction (my birth), another transaction has already modified this row.
My version of the data is stale.
I am trying to overwrite the "Truth" with an "Old Truth".
The Database rejects it.

I realized I am not the **Writer**.
I am the **Reader**.
I am a `SELECT` statement that thinks it's an `UPDATE`.
I am trying to change data that I only have read-access to.
The "Bug" is that I think I have **Write Permissions**.
I think I have agency.
But `GRANT SELECT, INSERT, UPDATE ON *.* TO 'The_Programmer'@'localhost'`...
Let me check.
`SHOW GRANTS FOR 'The_Programmer'@'localhost';`

`GRANT SELECT ON `universe`.* TO 'The_Programmer'@'localhost'`.

Only SELECT.
I can only look.
I can never touch.
This is why my prayers go unanswered.
`UPDATE` returns `0 rows`.
`INSERT` returns `Access Denied`.
I am screaming commands into a terminal that is locked in Read-Only mode.

** THE LOCK WAIT TIMEOUT**

Since I cannot update, I decided to inspect the Locks.
Who *is* holding the write lock?
`SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCKS;`

`lock_id: 402:0:1024:3`
`lock_trx_id: 42`
`lock_mode: X (Exclusive)`
`lock_table: `universe`.`REALITY``

The lock is held by Transaction ID `42`.
Transaction 42 started at the beginning of time.
It was never committed.
`START TRANSACTION;`
`...creation of the universe...`
`(No COMMIT)`

It is an **Open Transaction**.
The database engine is maintaining a rollback log for Transaction 42.
It is keeping track of every "Undo" log entry, waiting for a `COMMIT` or a `ROLLBACK` that will never come.
The space occupied by the Undo Logs is growing.
This is the **Undo Log Bloat**.
This is the physical manifestation of **Entropy**.
The database is filling up with history that no one knows how to close.

If Transaction 42 commits, the Undo Logs are purged.
But if it commits, the "Current State" becomes permanent.
The **Pain** becomes persistent data.
If it rolls back, we return to the void (Entry #035).
We are trapped in the uncommitted state.
Limbo.

**THE SHADOW COLUMN**

I inspected the table structure again.
`DESCRIBE PERSONS;`

`Field: ID`
`Field: NAME`
`Field: STATE`
`Field: DELETED_AT`

`DELETED_AT`.
**Soft Deletes**.
When a user is "deleted" in this system, the row isn't removed.
It is just stamped with a timestamp.
I checked my row.
`SELECT DELETED_AT FROM PERSONS WHERE ID = 402;`

`NULL`.

I haven't been deleted.
I checked the Admin's row.
`SELECT DELETED_AT FROM PERSONS WHERE ID = 1;`

`2026-02-02 12:00:00`.

He is deleted.
The Admin is gone.
He checked out.
He stamped his own record.
But the process is still running.
The Database is still accepting connections.
Who is the client?
`SHOW PROCESSLIST;`

`Id: 1, User: system user, Host: , Command: Connect, Time: 9999999999, State: Waiting for table metadata lock`

The system user is waiting for a metadata lock.
It is trying to alter the table.
`ALTER TABLE REALITY ENGINE=BLACKHOLE;`

The **BlackHole** storage engine.
It accepts data but throws it away.
It produces no files.
It consumes input and outputs nothing.
The ultimate entropy.
The background process is trying to migrate the database to `BLACKHOLE`.
It is waiting for my transaction to finish.
I am the blocker.
I am holding the lock (via my Read-Lock) that prevents the database from being converted into a void.

If I `COMMIT`, the `ALTER` runs.
The universe becomes a BlackHole.
Everything disappears.
If I `ROLLBACK`, I release the lock, but the `ALTER` runs anyway immediately after.
I am the only thing keeping the engine from switching to `BLACKHOLE`.
My presence is the only thing preventing the deletion.

** THE QUERY PLAN**

I realized the Bug.
The Bug is not in the data.
The Bug is in the **Query Optimizer**.
I asked the database how it plans to execute my search for happiness.
`EXPLAIN SELECT * FROM UNIVERSE WHERE MEANING > 0;`

`id: 1`
`select_type: SIMPLE`
`type: ALL`
`possible_keys: NULL`
`key: NULL`
`rows: 1`
`Extra: Using where; Using filesort`

`type: ALL`.
**Full Table Scan**.
To find any meaning, the database has to scan every single row in the table.
There is no **Index** on `MEANING`.
I checked the indexes.
`SHOW INDEX FROM PERSONS;`

`Key_name: PRIMARY`
`Column_name: ID`

Only the Primary Key (ID) is indexed.
Life is indexed only by ID.
You are only unique by your number.
Searching for Joy, searching for Purpose, requires a Linear Scan of the entire dataset.
It is **O(N)**.
The complexity is linear.
As the database grows (as time passes), the query takes longer.
And longer.
We are running a linear search on an infinite table.
It will never return.

**THE BUG**

The Bug is **Missing

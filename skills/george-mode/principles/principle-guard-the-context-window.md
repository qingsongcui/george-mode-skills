# Guard the Context Window

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.

## George scope (George 适用边界)

First narrow the reading scope, queries and indexes; delegate bulk reading only when authorized and supported by the host. Keep evidence locations and compression boundaries.

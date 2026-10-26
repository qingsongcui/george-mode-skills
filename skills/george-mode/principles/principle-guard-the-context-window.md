# Guard the Context Window

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.

## George 适用边界

先缩小读取范围、查询和索引；授权且宿主支持时才委派大批读取。保留证据位置与压缩边界。

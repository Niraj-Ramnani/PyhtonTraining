# Query Performance Report

Run `sql/07_indexes_performance.sql`.

Record the output of `EXPLAIN (ANALYZE, BUFFERS)` before and after indexes.

| Query | Before | After | Observation |
|---|---:|---:|---|
| Search user by email | ___ ms | ___ ms | ___ |
| Search restaurant by name | ___ ms | ___ ms | ___ |
| Search menu by restaurant | ___ ms | ___ ms | ___ |
| Search customer orders | ___ ms | ___ ms | ___ |

Compare:
- Execution Time
- Planning Time
- Sequential Scan vs Index Scan
- Rows removed by filter

On a small dataset, an index may not produce a dramatic time improvement because PostgreSQL can scan a small table very quickly. The index benefit becomes clearer as data volume increases.

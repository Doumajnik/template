+++
id = "technologies/redis"
title = "Redis Best Practices"
agents = ["all"]
technologies = ["redis", "caching"]
category = "rule"
tags = ["redis", "caching", "in-memory", "key-value"]
version = 1
+++

### Key Design

- Use colon-separated namespaces for key names: `{service}:{entity}:{id}:{field}` — e.g., `auth:session:abc123:token`.
- Set a TTL on every key — keys without expiration accumulate silently and cause OOM kills; use `EXPIRE` or set TTL at write time with `SET key value EX seconds`.
- Add random jitter (±10–20%) to TTLs when writing batches of keys to prevent thundering herd expirations.
- Use `SCAN` with a `COUNT` hint to iterate key spaces — never use `KEYS *` in production; it blocks the single-threaded event loop.
- Use `UNLINK` instead of `DEL` for large keys — `UNLINK` frees memory asynchronously in a background thread.

### Data Structures

- Use `STRING` for simple key-value caching, counters (`INCR`/`DECR`), and distributed locks (`SET NX EX`).
- Use `HASH` when storing objects with multiple fields — `HGET`/`HSET` avoids serialization overhead vs. storing a JSON string.
- Use `LIST` for queues (`LPUSH`/`BRPOP`) and bounded activity feeds (`LPUSH` + `LTRIM`).
- Use `SET` for membership checks (`SISMEMBER` is O(1)) and for computing intersections/unions across groups.
- Use `SORTED SET` for leaderboards, rate limiting (sliding window), and priority queues — `ZRANGEBYSCORE` with `LIMIT` is efficient for paginated results.
- Use `STREAM` for event logs and message queues that need persistence, consumer groups, and replay — prefer Streams over Pub/Sub when message durability matters.
- Use `HyperLogLog` (`PFADD`/`PFCOUNT`) for probabilistic cardinality counting (unique visitors, distinct events) — uses only 12 KB regardless of set size.

### Caching Patterns

- Implement cache-aside (lazy loading): read from cache first, on miss read from DB and populate cache with a TTL.
- Use write-through only when read-after-write consistency is critical — write to cache and DB in the same operation, accepting higher write latency.
- Use write-behind (write-back) with an async worker for high-write workloads — buffer writes in Redis and flush to DB in batches.
- Prevent cache stampede with a mutex lock: on cache miss, acquire a short-lived lock (`SET lock:key 1 NX EX 5`), let one caller rebuild, others wait or serve stale.

### Performance

- Batch commands with `PIPELINE` to reduce round-trip latency — a pipeline of 100 commands is ~100x faster than 100 individual calls.
- Avoid O(N) commands on large collections: never `SMEMBERS` on a set with 100K+ items or `LRANGE 0 -1` on a long list; paginate with `SSCAN` or `LRANGE` with bounded offsets.
- Monitor memory per key with `MEMORY USAGE <key>` to detect unexpectedly large values before they cause eviction pressure.
- Enable and monitor `slowlog-log-slower-than` (default 10000 µs) — query the slow log with `SLOWLOG GET 10` to find expensive commands.
- Use connection pooling in your client library (e.g., `redis-py` `ConnectionPool`, Jedis `JedisPool`) — creating a new TCP connection per request adds 1–3 ms overhead.
- Prefer `MGET`/`MSET` over looping individual `GET`/`SET` calls when operating on multiple keys in a single logical operation.

### Pub/Sub and Streams

- Use Pub/Sub only for fire-and-forget fan-out where message loss is acceptable (e.g., real-time notifications); messages are dropped if no subscriber is connected.
- Use Streams with consumer groups (`XREADGROUP`) for durable messaging — each message is delivered to exactly one consumer in the group and requires acknowledgment (`XACK`).
- Set `MAXLEN` or `MINID` on Streams to cap memory: `XADD mystream MAXLEN ~ 10000 * field value` trims approximately to 10K entries.
- Handle backpressure by monitoring the pending entries list (`XPENDING`) — reclaim stale messages with `XCLAIM` when a consumer crashes.

### Persistence

- Use RDB snapshots (`save 900 1`) for fast restarts and disaster recovery — RDB files are compact and load quickly.
- Enable AOF (`appendonly yes`) with `appendfsync everysec` for durability — accepts at most 1 second of data loss on crash.
- Use RDB+AOF hybrid persistence (Redis 4.0+): `aof-use-rdb-preamble yes` combines fast load (RDB) with append-only durability (AOF tail).
- Monitor `rdb_last_bgsave_status` and `aof_last_bgrewrite_status` in `INFO persistence` — alert immediately on failure.

### Security

- Require authentication with `requirepass` (Redis 5) or ACL users (`ACL SETUSER`) in Redis 6+ — assign per-service accounts with command and key-pattern restrictions.
- Disable dangerous commands in production: rename or block `FLUSHALL`, `FLUSHDB`, `DEBUG`, `CONFIG SET`, and `SHUTDOWN` via `rename-command` or ACL `nocommands`.
- Bind Redis to specific interfaces (`bind 127.0.0.1 10.0.0.5`) and enable `protected-mode yes` — never expose Redis to 0.0.0.0 without a firewall.
- Enable TLS (`tls-port 6380`) for all connections that cross network boundaries — use mutual TLS for service-to-service communication.
- Never store unencrypted secrets (tokens, passwords) as plain Redis values — encrypt at the application layer before writing.

### Cluster and High Availability

- Use Redis Sentinel for automatic failover of standalone primary/replica setups — deploy at least 3 Sentinel instances across separate availability zones.
- Use Redis Cluster for horizontal scaling beyond a single node's memory — data is sharded across 16384 hash slots automatically.
- Avoid multi-key commands (`MGET`, `SUNION`, transactions with `MULTI`) that span different hash slots in Cluster mode — use hash tags `{tag}` to co-locate related keys.
- Monitor cluster health with `CLUSTER INFO` and alert on `cluster_state:fail` or nodes in `pfail`/`fail` state.
- Set `cluster-node-timeout` appropriately (default 15s) — too low causes false failovers, too high delays recovery.

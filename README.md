# crypto-jobs-data

Open dataset of **live crypto, web3 and blockchain job listings**, refreshed daily.

Every role is read from the hiring company's **own applicant-tracking system** (Greenhouse, Lever,
Ashby and others) and re-checked every day. Roles that disappear at the source are removed the same
day, so the file is a snapshot of what is *actually open* — not an archive of everything ever posted.
Employers can also post a role free; every such post is human-reviewed and its apply link is re-checked daily (`source: posted` in `/api/jobs.json`). Nothing is copied from another job board.

Published by [ChainJobs](https://chainjobs.io). **CC BY 4.0** — use it commercially, just credit it.

## Endpoint

```
https://chainjobs.io/jobs-data.json
```

Served with open CORS, so you can fetch it straight from a browser. No key, no signup, no rate limit.
Roughly 633 KB, one file, updated once a day.

`sample.json` in this repo is 20 roles in the identical shape, for reading without a download.

## Also: the documented long-form file

`https://chainjobs.io/api/jobs.json` carries the same roles with full field names, the employer's apply URL,
`first_seen`, `last_confirmed` (the last day the role was seen open on the employer's own site), salary as
`{min, max, currency, period}`, a top-level `generated_at` and the licence. Larger (about 1.7 MB raw, ~300 KB
gzipped). Use it when you want readable keys; use `jobs-data.json` when you want the small file.

As of 2026-10-01: 3,685 live roles from 220 companies, 724 with an employer-published salary band, 1,181 remote.

## Shape

```jsonc
{
  "updated": "2026-09-18",          // UTC date of the last refresh
  "cats":    { "eng": "Engineering", ... },   // category code -> label
  "tags":    { ... }, "regions": { ... }, "cities": { ... }, "ecos": { ... },
  "comps":   [ ["0x Labs", "0x.org"], ["1inch", "1inch.io"], ... ],  // [name, domain]
  "locs":    [ "", "Remote", "New York, NY", ... ],                  // location strings
  "jobs":    [ { ... }, ... ]
}
```

`comps` and `locs` are lookup tables; a job refers to them **by index**. That is why the file is
650 KB instead of several megabytes. A company is a two-element array — `[name, domain]` — and a
location is a plain string, which may be empty when the employer didn't state one.

### A job

| Field | Meaning |
|---|---|
| `id` | Stable id. Unique, and stable across refreshes for the same role. |
| `t` | Job title |
| `c` | Index into `comps` |
| `l` | Index into `locs` |
| `r` | `1` if remote |
| `k` | Category code — look up in `cats` |
| `d` | Date the employer posted it (ISO date), when the ATS exposes one |
| `sy` | Salary band as displayed, e.g. `"$170k–250k"` — **only present when the employer publishes one** |
| `sk` | Sort key for salary (annualised) |
| `tg` | Tag codes — look up in `tags` |
| `e` | Ecosystem codes — look up in `ecos` |
| `rg` | Region code — look up in `regions` |
| `ct` | City code — look up in `cities` |
| `sn` | Seniority (`senior` / `entry`) |
| `nw` | `1` if first seen in the last 24h |
| `nd` | `1` if first seen in the last 7 days |
| `f` | `1` if it is a paid featured listing |
| `u` | Listing path. **Usually absent** — see below. |

### Building a listing URL

`u` is omitted for ASCII titles because it is derivable, which saves ~59 bytes per role:

```
https://chainjobs.io/jobs/{id}-{slug(t)}/
```

where `slug()` lowercases, replaces every run of non-alphanumerics with `-`, collapses repeats,
trims leading/trailing `-`, and truncates to 60 characters. When `u` **is** present (non-ASCII
titles, where case-folding differs between languages) use it verbatim — a derived path would 404.

## Salary data

About 22% of roles carry a band, because that is how many employers publish one. Figures are the
employer's own numbers, copied as published. **Nothing is inferred, estimated, averaged or
converted** — a role with no published band simply has no `sy`, and non-USD bands are never
converted to USD.

## Examples

- [`examples/fetch.py`](examples/fetch.py) — Python: remote engineering roles over $150k
- [`examples/fetch.js`](examples/fetch.js) — Node/browser: the same

## Attribution

> Job data from [ChainJobs](https://chainjobs.io), CC BY 4.0.

## Notes

- One refresh per day. Polling more often returns the same file.
- `id` is stable, so you can diff two snapshots to get "opened" and "closed" events.
- Found a wrong or stale listing? Open an issue — accuracy is the whole point of this dataset.

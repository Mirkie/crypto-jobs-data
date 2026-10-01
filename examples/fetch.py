#!/usr/bin/env python3
"""Remote engineering roles paying over $150k, from the live ChainJobs dataset.

    python3 examples/fetch.py
"""
import json
import re
import urllib.request

URL = "https://chainjobs.io/jobs-data.json"


def slug(s):
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")[:60]


def path(job):
    # `u` is only present for non-ASCII titles, where the slug isn't safely derivable
    return job.get("u") or f"/jobs/{job['id']}-{slug(job['t'])}/"


def main():
    with urllib.request.urlopen(URL, timeout=30) as r:
        data = json.load(r)

    print(f"{len(data['jobs'])} live roles, refreshed {data['updated']}\n")

    hits = [j for j in data["jobs"]
            if j.get("r") and j.get("k") == "eng" and (j.get("sk") or 0) >= 150_000]
    hits.sort(key=lambda j: j.get("sk", 0), reverse=True)

    for j in hits[:15]:
        name, domain = data["comps"][j["c"]]  # [name, domain]
        print(f"{j.get('sy','—'):>16}  {j['t'][:52]:52}  {name}")
        print(f"{'':16}  https://chainjobs.io{path(j)}")

    print(f"\n{len(hits)} remote engineering roles at $150k+")


if __name__ == "__main__":
    main()

// Remote engineering roles paying over $150k, from the live ChainJobs dataset.
// Node 18+:  node examples/fetch.js      (works unchanged in a browser — CORS is open)

const URL = "https://chainjobs.io/jobs-data.json";

const slug = (s) =>
  s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/-{2,}/g, "-")
   .replace(/^-|-$/g, "").slice(0, 60);

// `u` is only present for non-ASCII titles, where the slug isn't safely derivable
const path = (j) => j.u || `/jobs/${j.id}-${slug(j.t)}/`;

const data = await fetch(URL).then((r) => r.json());
console.log(`${data.jobs.length} live roles, refreshed ${data.updated}\n`);

const hits = data.jobs
  .filter((j) => j.r && j.k === "eng" && (j.sk ?? 0) >= 150000)
  .sort((a, b) => (b.sk ?? 0) - (a.sk ?? 0));

for (const j of hits.slice(0, 15)) {
  const [name] = data.comps[j.c]; // [name, domain]
  console.log(`${(j.sy ?? "—").padStart(16)}  ${j.t.slice(0, 52).padEnd(52)}  ${name}`);
  console.log(`${" ".repeat(16)}  https://chainjobs.io${path(j)}`);
}
console.log(`\n${hits.length} remote engineering roles at $150k+`);

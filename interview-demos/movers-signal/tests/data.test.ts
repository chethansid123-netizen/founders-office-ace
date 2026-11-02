import { describe, expect, it } from "vitest";
import recordsJson from "@/data/records.json";
import { AUDIT, onlyVerified, SEATS } from "@/lib/data";
import { computeSummary } from "@/lib/summary";
import { buildHypotheses } from "@/lib/hypotheses";
import { SCORED } from "@/lib/data";
import type { RecordsFile } from "@/lib/types";
import { AS_OF, seat } from "./fixtures";

const file = recordsJson as unknown as RecordsFile;
const notVerified = file.records.filter((r) => r.review_status !== "VERIFIED");

describe("only verified records reach the site", () => {
  it("onlyVerified drops REJECTED and UNREVIEWED records", () => {
    const out = onlyVerified([
      seat({ review_status: "VERIFIED" }),
      seat({ review_status: "REJECTED" }),
      seat({ review_status: "UNREVIEWED" }),
    ]);
    expect(out.map((r) => r.review_status)).toEqual(["VERIFIED"]);
  });
  it("the site's seat list holds VERIFIED records only", () => {
    expect(SEATS.every((s) => s.review_status === "VERIFIED")).toBe(true);
    const ids = new Set(SEATS.map((s) => s.id));
    for (const r of notVerified) expect(ids.has(r.id)).toBe(false);
  });
  it("the dataset contains rejected records, so the guard is really exercised", () => {
    expect(notVerified.length).toBeGreaterThan(0);
  });
  it("matches the audit's verified count", () => {
    expect(SEATS.length).toBe(AUDIT.seats_verified);
  });
});

describe("every verified seat is source-backed", () => {
  const required = ["company", "person_name", "role_title", "event_type", "filing_date", "effective_date", "successor_status"];
  it("has an exchange source URL", () => {
    for (const s of SEATS) expect(s.source_url).toMatch(/^https:\/\/(nsearchives\.nseindia\.com|www\.bseindia\.com)\//);
  });
  it("has a quote and page for each required field, or a stated reason for the absence", () => {
    for (const s of SEATS) {
      for (const f of required) {
        const e = s.evidence[f];
        expect(e, `${s.id}.${f}`).toBeDefined();
        if (e!.quote) expect(e!.page, `${s.id}.${f}`).toBeGreaterThan(0);
        else expect(e!.note, `${s.id}.${f}`).toBeTruthy();
      }
    }
  });
  it("every quote is under 15 words", () => {
    for (const s of SEATS) {
      for (const [f, e] of Object.entries(s.evidence)) {
        if (!e.quote) continue;
        const words = (e.fragments ?? [e.quote]).join(" ").trim().split(/\s+/).length;
        expect(words, `${s.id}.${f}`).toBeLessThan(15);
      }
    }
  });
  it("no field failed the latest verification run", () => {
    for (const s of SEATS) {
      const failed = Object.entries(s.verification!.fields)
        .filter(([, v]) => v === "mismatch")
        .map(([k]) => k);
      const overridden = new Set((s.review_overrides ?? []).map((o) => o.field));
      expect(failed.filter((f) => !overridden.has(f)), s.id).toEqual([]);
    }
  });
});

describe("summary numbers are computed, not hardcoded", () => {
  it("follow the records passed in", () => {
    const a = computeSummary([seat(), seat({ successor_status: "NAMED_PERMANENT" })], AS_OF);
    expect(a).toMatchObject({ seats: 2, noPermanentSuccessor: 1, topSeats: 2 });
    const b = computeSummary([seat({ role_level: "OTHER_SMP", effective_date: "2027-03-01" })], AS_OF);
    expect(b).toMatchObject({ seats: 1, noPermanentSuccessor: 1, topSeats: 0, next45: 0 });
  });
  it("on the real data, equal an independent recount", () => {
    const s = computeSummary(SEATS, AS_OF);
    expect(s.seats).toBe(SEATS.length);
    expect(s.noPermanentSuccessor).toBe(SEATS.filter((x) => x.successor_status !== "NAMED_PERMANENT").length);
    expect(s.topSeats).toBe(SEATS.filter((x) => ["CEO_MD", "CXO"].includes(x.role_level)).length);
  });
});

describe("hypotheses", () => {
  it("give two lines, three questions and company-type pools for every seat", () => {
    for (const s of SCORED) {
      const h = buildHypotheses(s);
      expect(h.whyNow).toHaveLength(2);
      expect(h.questions).toHaveLength(3);
      expect(h.pools.length).toBeGreaterThan(0);
    }
  });
  it("never name a person", () => {
    for (const s of SCORED) {
      const text = JSON.stringify(buildHypotheses(s));
      for (const name of [s.seat.person_name, s.seat.successor_name]) {
        if (!name) continue;
        for (const part of name.split(/\s+/).filter((w) => w.length > 3)) {
          expect(text.includes(part), `${s.seat.id} mentions ${part}`).toBe(false);
        }
      }
    }
  });
  it("talent pools name no specific company from the dataset", () => {
    const companies = SEATS.map((s) => s.company.replace(/ Limited$/, ""));
    for (const s of SCORED) {
      const pools = buildHypotheses(s).pools.join(" ");
      for (const c of companies) expect(pools.includes(c), `${s.seat.id} pools mention ${c}`).toBe(false);
    }
  });
  it("respect a filed 'no like-for-like replacement' statement", () => {
    const laxmi = SCORED.find((s) => s.seat.id === "laxmi-organic-20260818-cto")!;
    expect(buildHypotheses(laxmi).whyNow[1]).toMatch(/watch, not a live search/);
  });
});

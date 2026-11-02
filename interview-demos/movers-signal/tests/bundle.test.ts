import { describe, expect, it } from "vitest";
import recordsJson from "@/data/records.json";
import { buildBundle, DISCLAIMER } from "@/lib/bundle";
import { SCORED } from "@/lib/data";

const bundle = buildBundle();
const records = (recordsJson as unknown as { records: { id: string; review_status: string }[] }).records;

describe("site data export", () => {
  it("carries every verified seat, in rank order, and nothing else", () => {
    expect(bundle.seats.map((s) => s.id)).toEqual(SCORED.map((s) => s.seat.id));
    const notVerified = new Set(records.filter((r) => r.review_status !== "VERIFIED").map((r) => r.id));
    const text = JSON.stringify(bundle);
    for (const id of notVerified) expect(text.includes(id)).toBe(false);
  });
  it("its numbers agree with the seats it carries", () => {
    const seats = bundle.seats;
    expect(bundle.summary.seats).toBe(seats.length);
    expect(bundle.summary.noPermanentSuccessor).toBe(seats.filter((s) => s.successor_status !== "NAMED_PERMANENT").length);
    expect(bundle.pulse.byPractice.reduce((a, b) => a + b.count, 0)).toBe(seats.length);
    expect(bundle.pulse.byRole.reduce((a, b) => a + b.count, 0)).toBe(seats.length);
    for (const s of seats) expect(s.priority.components.reduce((a, c) => a + c.points, 0)).toBe(s.total);
  });
  it("keeps the disclaimer and never calls priority a probability", () => {
    expect(bundle.meta.disclaimer).toBe(DISCLAIMER);
    const text = JSON.stringify(bundle).toLowerCase();
    for (const m of text.matchAll(/probabilit/g)) expect(text.slice(m.index! - 6, m.index)).toBe("not a ");
  });
  it("every quote shown is under 15 words", () => {
    for (const s of bundle.seats) {
      for (const f of [...s.facts, ...s.also_in_filing]) {
        if (f.quote) expect(f.quote.split(/\s+/).length).toBeLessThan(15);
      }
    }
  });
});

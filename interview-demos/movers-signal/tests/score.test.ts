import { describe, expect, it } from "vitest";
import { daysBetween, exitPoints, rankScored, scoreSeat, timingFor, type ScoreConfig } from "@/lib/score";
import { SCORED, SEATS } from "@/lib/data";
import { AS_OF, CONFIG, seat } from "./fixtures";

const score = (s: ReturnType<typeof seat>, all = [s], config: ScoreConfig = CONFIG) =>
  scoreSeat(s, { asOf: AS_OF, allSeats: all, config });
const part = (r: ReturnType<typeof score>, key: string) => r.components.find((c) => c.key === key)!.points;

describe("role level points", () => {
  it.each([
    ["CEO_MD", 35],
    ["CXO", 25],
    ["BUSINESS_HEAD", 15],
    ["FUNCTION_HEAD", 10],
    ["OTHER_SMP", 5],
  ] as const)("%s scores %i", (level, pts) => {
    expect(part(score(seat({ role_level: level })), "role_level")).toBe(pts);
  });
});

describe("successor status points", () => {
  it("not named 30, interim 25, unclear 15", () => {
    expect(part(score(seat({ successor_status: "NOT_NAMED" })), "successor_status")).toBe(30);
    expect(part(score(seat({ successor_status: "NAMED_INTERIM" })), "successor_status")).toBe(25);
    expect(part(score(seat({ successor_status: "UNCLEAR" })), "successor_status")).toBe(15);
  });
  it("permanent successor scores 0 whether internal or external", () => {
    expect(part(score(seat({ successor_status: "NAMED_PERMANENT", successor_source: "INTERNAL" })), "successor_status")).toBe(0);
    expect(part(score(seat({ successor_status: "NAMED_PERMANENT", successor_source: "EXTERNAL" })), "successor_status")).toBe(0);
  });
});

describe("other exits at the same company", () => {
  it("bands: 0 -> 0, 1 -> 10, 2 or more -> 15", () => {
    expect(exitPoints(0, CONFIG)).toBe(0);
    expect(exitPoints(1, CONFIG)).toBe(10);
    expect(exitPoints(2, CONFIG)).toBe(15);
    expect(exitPoints(7, CONFIG)).toBe(15);
  });
  it("counts other exits only: not itself, not other companies, not appointments or moves", () => {
    const me = seat();
    const all = [
      me,
      seat({ event_type: "RETIREMENT" }),
      seat({ event_type: "END_OF_TERM" }),
      seat({ event_type: "APPOINTMENT" }),
      seat({ event_type: "OTHER" }),
      seat({ company: "Beta Limited" }),
    ];
    const r = score(me, all);
    expect(r.otherExits).toHaveLength(2);
    expect(part(r, "company_exits")).toBe(15);
  });
  it("ignores exits filed after the as-of date or more than 365 days before it", () => {
    const me = seat();
    const all = [me, seat({ filing_date: "2026-11-03" }), seat({ filing_date: "2025-11-01" })];
    expect(score(me, all).otherExits).toHaveLength(0);
    const inside = [me, seat({ filing_date: "2025-11-02" })];
    expect(score(me, inside).otherExits).toHaveLength(1);
  });
});

describe("timing", () => {
  it.each([
    [0, 20, "next"],
    [1, 20, "next"],
    [45, 20, "next"],
    [46, 5, "otherwise"],
    [-1, 15, "past"],
    [-30, 15, "past"],
    [-31, 5, "otherwise"],
  ] as const)("%i days from as-of scores %i", (days, pts, band) => {
    expect(timingFor(days, CONFIG)).toEqual({ points: pts, band });
  });
  it("no effective date scores the 'otherwise' 5", () => {
    expect(part(score(seat({ effective_date: null })), "timing")).toBe(5);
  });
  it("daysBetween is a whole-day UTC difference", () => {
    expect(daysBetween("2026-11-02", "2026-12-17")).toBe(45);
    expect(daysBetween("2026-11-02", "2026-10-03")).toBe(-30);
  });
});

describe("total and gate", () => {
  it("total is the sum of the four components and never exceeds 100", () => {
    const r = score(seat({ role_level: "CEO_MD", successor_status: "NOT_NAMED" }), [
      seat({ role_level: "CEO_MD", id: "x" }),
    ]);
    expect(r.total).toBe(r.components.reduce((s, c) => s + c.points, 0));
    expect(r.total).toBeLessThanOrEqual(CONFIG.max_points);
  });
  it("appointment with a permanent successor is 'Seat filled'", () => {
    const r = score(seat({ event_type: "APPOINTMENT", successor_status: "NAMED_PERMANENT", successor_source: "EXTERNAL" }));
    expect(r.seatFilled).toBe(true);
    expect(r.status).toBe("Seat filled");
  });
  it("the gate does not fire for interim appointments or for exits with a named successor", () => {
    expect(score(seat({ event_type: "APPOINTMENT", successor_status: "NAMED_INTERIM" })).seatFilled).toBe(false);
    const exit = score(seat({ event_type: "RESIGNATION", successor_status: "NAMED_PERMANENT", successor_source: "INTERNAL" }));
    expect(exit.seatFilled).toBe(false);
    expect(exit.status).toBe("Successor named");
  });
  it("is pure: same input, same output, input untouched", () => {
    const s = seat();
    const before = JSON.stringify(s);
    expect(score(s)).toEqual(score(s));
    expect(JSON.stringify(s)).toBe(before);
  });
  it("reads its weights from config, so changing config changes the score", () => {
    const tweaked = structuredClone(CONFIG);
    tweaked.components.role_level.points.CXO = 40;
    expect(part(score(seat(), [seat()], tweaked), "role_level")).toBe(40);
  });
  it("ranks open seats above filled seats, then by priority", () => {
    const filled = score(seat({ role_level: "CEO_MD", event_type: "APPOINTMENT", successor_status: "NAMED_PERMANENT" }));
    const low = score(seat({ role_level: "OTHER_SMP", successor_status: "NAMED_PERMANENT" }));
    const high = score(seat({ role_level: "CXO" }));
    expect(rankScored([filled, low, high]).map((r) => r.seat.id)).toEqual([high.seat.id, low.seat.id, filled.seat.id]);
  });
});

describe("on the verified dataset", () => {
  it("every score equals the sum of its parts and sits between 0 and 100", () => {
    for (const s of SCORED) {
      expect(s.total).toBe(s.components.reduce((a, c) => a + c.points, 0));
      expect(s.total).toBeGreaterThanOrEqual(0);
      expect(s.total).toBeLessThanOrEqual(100);
    }
  });
  it("company exit counts follow the dataset", () => {
    const byCompany = (name: string) => SCORED.filter((s) => s.seat.company === name);
    for (const s of byCompany("Manappuram Finance Limited")) expect(s.components[2]!.points).toBe(15);
    for (const s of byCompany("Laxmi Organic Industries Limited")) expect(s.components[2]!.points).toBe(10);
    for (const s of byCompany("Whirlpool of India Limited")) expect(s.components[2]!.points).toBe(10);
  });
  it("'Seat filled' appears only on appointments with a permanent successor", () => {
    for (const s of SCORED) {
      expect(s.seatFilled).toBe(s.seat.event_type === "APPOINTMENT" && s.seat.successor_status === "NAMED_PERMANENT");
    }
  });
  it("ranks every verified seat exactly once", () => {
    expect(new Set(SCORED.map((s) => s.seat.id)).size).toBe(SEATS.length);
  });
});

import { describe, expect, it } from "vitest";
import {
  ALL,
  allowedValues,
  applyFilters,
  filterOptions,
  filtersFromSearch,
  filtersToSearch,
  isFiltered,
  NO_FILTERS,
} from "@/lib/filters";
import { addDays, sourceHref } from "@/lib/format";
import { successorDetail, toRadarRow } from "@/lib/radar";
import { scoreSeat } from "@/lib/score";
import { SCORED, SEATS } from "@/lib/data";
import { AS_OF, CONFIG, seat } from "./fixtures";

const groups = filterOptions(SEATS);
const allowed = allowedValues(groups);

describe("filters in the URL", () => {
  it("round-trips every filter, including names with spaces and '&'", () => {
    const f = { practice: "Consumer Products & Retail", roleLevel: "CXO", eventType: "RESIGNATION", successorStatus: "NOT_NAMED" };
    const qs = filtersToSearch(f);
    expect(qs).toBe("practice=Consumer+Products+%26+Retail&role=CXO&event=RESIGNATION&successor=NOT_NAMED");
    expect(filtersFromSearch(`?${qs}`, allowed)).toEqual(f);
  });
  it("writes nothing for 'all'", () => {
    expect(filtersToSearch(NO_FILTERS)).toBe("");
    expect(isFiltered(NO_FILTERS)).toBe(false);
  });
  it("ignores unknown values and unknown parameters", () => {
    expect(filtersFromSearch("?practice=Nonsense&role=KING&foo=bar", allowed)).toEqual(NO_FILTERS);
  });
  it("ignores values with no seats in the dataset", () => {
    const zero = groups.eventType.filter((o) => o.count === 0).map((o) => o.value);
    for (const v of zero) expect(filtersFromSearch(`?event=${v}`, allowed).eventType).toBe(ALL);
  });
  it("a link from Market pulse selects the matching seats", () => {
    const f = filtersFromSearch("?practice=Telecom", allowed);
    const rows = applyFilters(SEATS, f);
    expect(rows.length).toBe(groups.practice.find((o) => o.value === "Telecom")!.count);
    expect(rows.every((s) => s.practice === "Telecom")).toBe(true);
  });
});

describe("Radar rows", () => {
  const rows = SCORED.map((s, i) => toRadarRow(s, i + 1));
  it("one row per verified seat, ranked 1..n in score order", () => {
    expect(rows.map((r) => r.id)).toEqual(SCORED.map((s) => s.seat.id));
    expect(rows.map((r) => r.rank)).toEqual(rows.map((_, i) => i + 1));
  });
  it("carry no evidence, quotes, review notes or hashes to the browser", () => {
    const keys = new Set(rows.flatMap((r) => Object.keys(r)));
    for (const k of ["evidence", "context_facts", "review_note", "source_sha256", "verification", "stated_reason"]) {
      expect(keys.has(k)).toBe(false);
    }
  });
  it("link to the permanent copy of a filing when there is one", () => {
    for (const r of rows) {
      const s = SEATS.find((x) => x.id === r.id)!;
      expect(r.source_url).toBe(s.source_url_stable ?? s.source_url);
    }
  });
  it("filtering rows gives the same seats as filtering records", () => {
    const f = { ...NO_FILTERS, roleLevel: "CXO", successorStatus: "NOT_NAMED" };
    expect(applyFilters(rows, f).map((r) => r.id).sort()).toEqual(applyFilters(SEATS, f).map((s) => s.id).sort());
  });
});

describe("successor detail line", () => {
  it("adds the source only for a permanent successor whose source is stated", () => {
    expect(successorDetail(seat({ successor_status: "NAMED_PERMANENT", successor_source: "INTERNAL" }))).toBe("Permanent named · internal");
    expect(successorDetail(seat({ successor_status: "NAMED_PERMANENT", successor_source: "UNCLEAR" }))).toBe("Permanent named");
    expect(successorDetail(seat({ successor_status: "NOT_NAMED" }))).toBe("Not named");
  });
  it("a filled seat keeps its score but is labelled Seat filled", () => {
    const s = seat({ event_type: "APPOINTMENT", successor_status: "NAMED_PERMANENT", successor_source: "EXTERNAL" });
    const scored = scoreSeat(s, { asOf: AS_OF, allSeats: [s], config: CONFIG });
    const row = toRadarRow(scored, 1);
    expect(row.status).toBe("Seat filled");
    expect(row.seat_filled).toBe(true);
    expect(row.successor_detail).toBe("Permanent named · external");
  });
});

describe("dates and links", () => {
  it("addDays crosses month ends in UTC", () => {
    expect(addDays("2026-11-02", 45)).toBe("2026-12-17");
    expect(addDays("2026-12-20", 15)).toBe("2027-01-04");
  });
  it("sourceHref prefers the permanent copy", () => {
    expect(sourceHref({ source_url: "a" })).toBe("a");
    expect(sourceHref({ source_url: "a", source_url_stable: "b" })).toBe("b");
  });
});

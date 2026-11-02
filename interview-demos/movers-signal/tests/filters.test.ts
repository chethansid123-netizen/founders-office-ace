import { describe, expect, it } from "vitest";
import { ALL, applyFilters, filterOptions, NO_FILTERS } from "@/lib/filters";
import { SCORED, SEATS } from "@/lib/data";
import { seat } from "./fixtures";

const seats = [
  seat({ practice: "Telecom", role_level: "CXO", event_type: "APPOINTMENT", successor_status: "NAMED_PERMANENT" }),
  seat({ practice: "Telecom", role_level: "FUNCTION_HEAD", event_type: "RESIGNATION", successor_status: "NOT_NAMED" }),
  seat({ practice: "Digital", role_level: "CEO_MD", event_type: "RESIGNATION", successor_status: "NAMED_PERMANENT" }),
  seat({ practice: "Financial Services", role_level: "CXO", event_type: "END_OF_TERM", successor_status: "UNCLEAR" }),
];

describe("filters", () => {
  it("no filters returns everything", () => {
    expect(applyFilters(seats, NO_FILTERS)).toHaveLength(4);
  });
  it("filters by practice", () => {
    expect(applyFilters(seats, { ...NO_FILTERS, practice: "Telecom" })).toHaveLength(2);
  });
  it("filters by role level", () => {
    expect(applyFilters(seats, { ...NO_FILTERS, roleLevel: "CXO" })).toHaveLength(2);
  });
  it("filters by event type", () => {
    expect(applyFilters(seats, { ...NO_FILTERS, eventType: "RESIGNATION" })).toHaveLength(2);
  });
  it("filters by successor status", () => {
    expect(applyFilters(seats, { ...NO_FILTERS, successorStatus: "NAMED_PERMANENT" })).toHaveLength(2);
  });
  it("combines filters with AND", () => {
    const r = applyFilters(seats, { practice: "Telecom", roleLevel: ALL, eventType: "RESIGNATION", successorStatus: "NOT_NAMED" });
    expect(r).toHaveLength(1);
    expect(r[0]!.role_level).toBe("FUNCTION_HEAD");
  });
  it("an unknown value matches nothing", () => {
    expect(applyFilters(seats, { ...NO_FILTERS, practice: "Shipping" })).toHaveLength(0);
  });
  it("works on scored seats as well as raw records", () => {
    expect(applyFilters(SCORED, { ...NO_FILTERS, practice: "Telecom" }).length).toBe(
      SEATS.filter((s) => s.practice === "Telecom").length,
    );
  });
  it("option counts add up to the number of seats for every dimension", () => {
    const o = filterOptions(SEATS);
    for (const dim of [o.practice, o.roleLevel, o.eventType, o.successorStatus]) {
      expect(dim.reduce((a, x) => a + x.count, 0)).toBe(SEATS.length);
    }
  });
});

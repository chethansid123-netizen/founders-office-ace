/** Plain-language definitions shown on the Method page. */
export const EVENT_MEANING: Record<string, string> = {
  RESIGNATION: "The filing says the person resigned.",
  RETIREMENT: "The filing says the person retires or superannuates.",
  REMOVAL: "The filing says the person was removed or terminated.",
  END_OF_TERM: "The filing says the person's term ends or is not renewed.",
  APPOINTMENT: "The filing appoints a person to the seat.",
  OTHER: "Any other change of seat holder the filing describes, such as a move to another role.",
};

export const SUCCESSOR_MEANING: Record<string, string> = {
  NOT_NAMED: "The filing names no successor.",
  NAMED_INTERIM: "The filing names someone to hold the seat for now (interim or additional charge).",
  UNCLEAR: "The filing's wording leaves it unclear whether a successor is named.",
  NAMED_PERMANENT: "The filing names a permanent successor, internal or external.",
};

import { buildBundle } from "@/lib/bundle";

// Emitted at build time as out/site-data.json: the whole site as data,
// verified records only, every value computed by the same code as the pages.
export const dynamic = "force-static";

export function GET() {
  return Response.json(buildBundle());
}

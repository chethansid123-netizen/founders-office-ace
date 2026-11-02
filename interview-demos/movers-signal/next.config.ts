import type { NextConfig } from "next";
import path from "node:path";

// Static export: the whole site is plain HTML/CSS/JS in out/, built from local JSON.
const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true,
  images: { unoptimized: true },
  poweredByHeader: false,
  // This app lives inside a larger repository; build from this folder only.
  turbopack: { root: path.join(__dirname) },
};

export default nextConfig;

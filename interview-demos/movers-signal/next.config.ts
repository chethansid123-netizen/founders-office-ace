import type { NextConfig } from "next";

// Static export: the whole site is plain HTML/CSS/JS in out/, built from local JSON.
const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true,
  images: { unoptimized: true },
  poweredByHeader: false,
};

export default nextConfig;

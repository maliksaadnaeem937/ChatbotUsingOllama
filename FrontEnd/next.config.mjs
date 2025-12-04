/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    turbo: false, // force Webpack instead of Turbopack
  },
};

export default nextConfig;

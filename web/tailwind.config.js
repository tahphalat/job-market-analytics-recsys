/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#0f172a",
        mist: "#e2e8f0",
        cloud: "#f8fafc",
        accent: "#0ea5e9",
        accentSoft: "#38bdf8",
        highlight: "#f59e0b",
        card: "#0b1222"
      },
      fontFamily: {
        sans: ["var(--font-manrope)", "system-ui", "sans-serif"],
        display: ["var(--font-space-grotesk)", "var(--font-manrope)", "sans-serif"]
      },
      boxShadow: {
        glow: "0 10px 40px rgba(14, 165, 233, 0.25)"
      }
    }
  },
  plugins: []
};

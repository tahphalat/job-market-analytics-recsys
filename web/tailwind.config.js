/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        background: "#050505", // Deepest black
        surface: "#111111",    // Slightly lighter for cards
        surfaceMuted: "#1a1a1a",
        border: "#262626",     // Subtle borders
        primary: "#ffffff",    // Stark white text
        secondary: "#a1a1aa",  // Zinc-400 for muted text
        muted: "#52525b",      // Zinc-600
        accent: "#38bdf8",     // Sky-400 (Cyber blue accent)
        highlight: "#f472b6",  // Pink-400 (Subtle highlight)
        // Legacy support
        ink: "#050505",
        card: "#111111"
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"], // Clean Inter
        mono: ["var(--font-fira-code)", "monospace"],
        display: ["var(--font-space-grotesk)", "sans-serif"]
      },
      animation: {
        "fade-in-up": "fadeInUp 0.8s ease-out forwards",
        "typewriter": "typewriter 2s steps(20) forwards"
      },
      keyframes: {
        fadeInUp: {
          "0%": { opacity: "0", transform: "translateY(20px)" },
          "100%": { opacity: "1", transform: "translateY(0)" }
        },
        typewriter: {
          "0%": { width: "0" },
          "100%": { width: "100%" }
        }
      }
    }
  },
  plugins: []
};

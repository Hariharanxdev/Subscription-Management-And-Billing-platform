/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        paper: {
          DEFAULT: "#F7F7F3",
          dim: "#EFEFE9",
        },
        ink: {
          DEFAULT: "#12181B",
          soft: "#3C4649",
          faint: "#7A8688",
        },
        ledger: {
          50: "#EAF3F1",
          100: "#CFE4DF",
          200: "#9EC9C0",
          300: "#6BAC9F",
          400: "#3D8E7F",
          500: "#0E5F5A",
          600: "#0B4E4A",
          700: "#093F3C",
          800: "#062E2C",
          900: "#041F1D",
        },
        gold: {
          100: "#F3E6BE",
          300: "#E1C570",
          500: "#C9A227",
          600: "#A9861C",
        },
        brick: {
          400: "#D46A5C",
          500: "#C1443A",
          600: "#A2352C",
        },
        line: "#DEDFD6",
      },
      fontFamily: {
        display: ["\"Fraunces\"", "serif"],
        body: ["\"Inter\"", "sans-serif"],
        mono: ["\"IBM Plex Mono\"", "monospace"],
      },
      boxShadow: {
        card: "0 1px 2px rgba(18,24,27,0.04), 0 8px 24px -12px rgba(18,24,27,0.12)",
        pop: "0 4px 12px rgba(18,24,27,0.08), 0 16px 40px -16px rgba(18,24,27,0.18)",
      },
      borderRadius: {
        xl2: "1.25rem",
      },
      keyframes: {
        "fade-up": {
          "0%": { opacity: 0, transform: "translateY(6px)" },
          "100%": { opacity: 1, transform: "translateY(0)" },
        },
        "draw-in": {
          "0%": { width: "0%" },
          "100%": { width: "100%" },
        },
      },
      animation: {
        "fade-up": "fade-up 0.4s ease-out both",
        "draw-in": "draw-in 0.5s ease-out both",
      },
    },
  },
  plugins: [],
};

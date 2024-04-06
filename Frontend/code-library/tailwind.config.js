/** @type {import('tailwindcss').Config} */
export default {
  content:
    [
      "./index.html",
      "./src/**/*.{js,ts,jsx,tsx}",
    ],
  theme: {
    extend: {
      colors: {
        primary: {
          "blue": "#0070f3",
          "green": "#34eb40",
          "red": "#ff0000",
          "black": "#000000",
        },
      },
      screens: {
        sm: '480px',
        md: '768px',
        lg: '976px',
        xl: '1440px',
      },
    },
  },
  plugins: [],
}


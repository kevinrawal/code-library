/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          "blue": "#0070f3", // Indigo 
        },
        gray: {
          "100": "#f8f9fa", // Light gray 
          "200": "#e5e7eb", // Medium gray 
          "300": "#d7dce2", // Darker gray 
          "700": "#343a40", // Dark gray
        },
        red: {
          "500": "#ff0000", // Red 
        },
        white: "#fff", // White
      },
    },
    screens: {
      sm: '480px',
      md: '768px',
      lg: '976px',
      xl: '1440px',
    },
  },
  darkMode: 'class', // Enable dark mode toggling with a class
  plugins: [],
}

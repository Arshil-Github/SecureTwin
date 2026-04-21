/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./App.{js,jsx,ts,tsx}", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: '#080C14', // Surface (Ink Black)
        surface: 'rgba(13, 20, 33, 0.4)', // Surface Container (Glass)
        accent: '#00E5C0', // Primary (Electric Teal)
        textPrimary: '#F2EDE4', // Secondary (Warm Ivory)
        warning: '#FF9B3D', // Ember Amber
        danger: '#E63946', // Deep Crimson
        borderWhite: 'rgba(255, 255, 255, 0.1)',
        success: '#00E5C0', // Using primary teal for success
      }
    },
  },
  plugins: [],
};

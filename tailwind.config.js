/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')

module.exports = {
  content: [
    './templates/**/*.html',
    './accounts/templates/**/*.html',
    './*/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'border-light': '#e6e6e680',
        'brand': '#2563eb',
        'brand-hover': '#1d4ed8',

        // 'back-primary': "#293038",
        // 'back-secondary': "#38414D",
        'back-primary': "#f9fafb",
        'back-secondary': "#fff",

        // 'brand': '#9333ea',
        // 'brand-hover': '#7e22ce',
        // 'brand': colors.blue,
      },

      fontFamily: {
        'poppins': ['Poppins'],
        'handlee': ['Handlee'],
        'pangolin': ['Pangolin'],
     }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('flowbite/plugin'),
  ],
}

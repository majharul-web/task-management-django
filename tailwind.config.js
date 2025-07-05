/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
    "./tasks/templates/**/*.html",
    "./users/templates/**/*.html",
    "./tasks/forms.py",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};

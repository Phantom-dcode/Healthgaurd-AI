/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary:  { DEFAULT: '#0EA5E9', dark: '#0284C7' },
        surface:  { DEFAULT: '#0F172A', card: '#1E293B', border: '#334155' },
      },
      fontFamily: { sans: ['Inter', 'sans-serif'] },
      animation:  { 'pulse-slow': 'pulse 3s cubic-bezier(0.4,0,0.6,1) infinite' },
    },
  },
  plugins: [],
}

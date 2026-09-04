/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                dark: {
                    900: '#0a0d14',
                    800: '#121824',
                    700: '#1b2333',
                    600: '#273248'
                },
                triage: {
                    red: '#ff3b30',
                    yellow: '#ffcc00',
                    green: '#34c759'
                }
            }
        },
    },
    plugins: [],
}

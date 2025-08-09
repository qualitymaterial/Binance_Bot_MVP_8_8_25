# React + Vite + Tailwind CSS Setup Commands

This guide provides copy-paste-ready commands for setting up Tailwind CSS in a React + Vite project on macOS with Node 18+, including fallbacks for when npx fails.

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager

## Step 1: Create and Navigate to Frontend Directory
```bash
mkdir -p frontend
cd frontend
```

## Step 2: Initialize React + Vite Project
```bash
# Primary command (using npm create)
npm create vite@latest . -- --template react --yes

# Fallback if npm create fails
npx create-vite@latest . --template react --yes

# Alternative fallback (manual installation)
npm init -y
npm install react react-dom
npm install -D vite @vitejs/plugin-react
```

## Step 3: Install Dependencies
```bash
npm install
```

## Step 4: Install Tailwind CSS, PostCSS, and Autoprefixer
```bash
# Install Tailwind CSS and dependencies
npm install -D tailwindcss @tailwindcss/postcss autoprefixer

# Alternative if the above fails
npm install -D tailwindcss@latest @tailwindcss/postcss@latest autoprefixer@latest
```

## Step 5: Initialize Tailwind Configuration
```bash
# Primary command
npx tailwindcss init -p

# If npx fails, create config files manually (see Step 6-7)
```

## Step 6: Create tailwind.config.js (Manual Fallback)
If npx fails, create `tailwind.config.js` with this content:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Commands to create the file:
```bash
cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
EOF
```

## Step 7: Create postcss.config.js
Create `postcss.config.js` with this content:

```javascript
export default {
  plugins: {
    '@tailwindcss/postcss': {},
    autoprefixer: {},
  },
}
```

Commands to create the file:
```bash
cat > postcss.config.js << 'EOF'
export default {
  plugins: {
    '@tailwindcss/postcss': {},
    autoprefixer: {},
  },
}
EOF
```

## Step 8: Update src/index.css
Add Tailwind directives to the top of your `src/index.css` file:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Your existing CSS below... */
```

Commands to update the file:
```bash
# Backup original file
cp src/index.css src/index.css.backup

# Add Tailwind directives to the top
echo "@tailwind base;
@tailwind components;
@tailwind utilities;

$(cat src/index.css)" > src/index.css
```

## Step 9: Test the Setup
```bash
# Build the project to test everything works
npm run build

# Start development server
npm run dev
```

## Complete One-Liner Setup (Copy-Paste Ready)
```bash
# Create project structure
mkdir -p frontend && cd frontend

# Initialize React + Vite
npm create vite@latest . -- --template react --yes

# Install dependencies
npm install

# Install Tailwind and related packages
npm install -D tailwindcss @tailwindcss/postcss autoprefixer

# Create Tailwind config
cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
EOF

# Create PostCSS config
cat > postcss.config.js << 'EOF'
export default {
  plugins: {
    '@tailwindcss/postcss': {},
    autoprefixer: {},
  },
}
EOF

# Add Tailwind directives to CSS
cp src/index.css src/index.css.backup
echo "@tailwind base;
@tailwind components;
@tailwind utilities;

$(cat src/index.css)" > src/index.css

# Test the build
npm run build

echo "✅ Tailwind CSS setup complete! Run 'npm run dev' to start the development server."
```

## Troubleshooting

### If you get PostCSS plugin errors:
```bash
# Make sure you're using the correct PostCSS plugin
npm uninstall tailwindcss
npm install -D tailwindcss @tailwindcss/postcss autoprefixer
```

### If npx commands fail:
All the manual configuration files are provided above. You can create them manually using the `cat > filename << 'EOF'` commands.

### If build fails with Tailwind errors:
1. Check that `@tailwindcss/postcss` is installed
2. Verify `postcss.config.js` uses `'@tailwindcss/postcss'` not `'tailwindcss'`
3. Ensure `tailwind.config.js` content array includes your file paths

### Example Tailwind classes to test:
Add these to your JSX to verify Tailwind is working:
```jsx
<h1 className="text-4xl font-bold text-blue-600">Hello Tailwind!</h1>
<button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
  Click me
</button>
```
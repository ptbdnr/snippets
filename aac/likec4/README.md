# Architecture Documentation

This directory contains the architecture documentation for the system, modeled using [LikeC4](https://likec4.dev/) - a modern architecture modeling tool that uses code to define and visualize software architecture.


## Installation

### Prerequisites

- Node.js (v18 or higher recommended)

### Install LikeC4 CLI

```bash
# Navigate to Architecture Directory
cd /path/to/docs/architecture
# You can install LikeC4 locally using npm:
npm install -D likec4
# Verify Installation
likec4 --version
```

## Using LikeC4 CLI

```bash
# Navigate to Architecture Directory
cd /path/to/docs/architecture
# Check for syntax errors and validate the model:
likec4 validate
# Launch the interactive web UI to view and edit diagrams:
likec4 start
```

This will:
- Start a local development server (typically at `http://localhost:3000`)
- Watch for file changes and auto-reload
- Provide an interactive UI to explore your architecture

### Build Static Site

Generate a static website with all diagrams:

```bash
likec4 build
```

Output will be in the `dist/` directory by default.

### Preview Diagrams

Generate a quick preview without starting the full server:

```bash
likec4 preview
```

## Exporting Diagrams to PNG

### Method 1: Using CLI Export Command

```bash
# Export all diagrams to PNG format:
likec4 export png
# Export specific views:
likec4 export png --view <view-id>
# Export with custom output directory:
likec4 export png --output ./exports
```

### Method 2: Using the Web UI

1. Start the development server:
   ```bash
   likec4 start
   ```

2. Open the web UI (usually `http://localhost:3000`)

3. Navigate to the desired diagram view

4. Use the export button in the UI to download as PNG

### Method 3: Export Options

Available export formats:
- `png` - Raster image (good for documentation)
- `svg` - Vector image (scalable, good for presentations)
- `json` - Data export
- `mmd` - Mermaid diagram format

Example with different formats:

```bash
# Export as SVG (vector graphics)
likec4 export svg

# Export as both PNG and SVG
likec4 export png
likec4 export svg
```

### Export Configuration Options

You can customize exports with additional flags:

```bash
# Export with specific dimensions
likec4 export png --width 1920 --height 1080

# Export with specific theme
likec4 export png --theme dark

# Export to specific directory
likec4 export png -o ../images/architecture

# Export specific view only
likec4 export png --view deployment-azure
```

## Resources

- [LikeC4 Official Documentation](https://likec4.dev/docs)
- [LikeC4 GitHub Repository](https://github.com/likec4/likec4)
- [C4 Model Introduction](https://c4model.com/)
- [Architecture as Code](https://www.thoughtworks.com/radar/techniques/architecture-as-code)

## Troubleshooting

### Port Already in Use

Specify a different port:

```bash
likec4 start --port 3001
```

For questions or issues, please contact the architecture team.

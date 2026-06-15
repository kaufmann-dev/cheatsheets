# Responsive Light Mode Gradient Guide

This guide details the final production-ready CSS for a responsive light mode gradient featuring centered side colors and clean top and bottom framing.

## The Final CSS Code

```css
background: 
  linear-gradient(to bottom, #FAFAFA 0%, transparent 30%, transparent 70%, #FAFAFA 100%),
  radial-gradient(ellipse at 120% 60%, #F7A8B880 0%, transparent 60%),
  radial-gradient(ellipse at -20% 60%, #55CDFC80 0%, transparent 60%),
  #FFFFFF
```

## Core Design Principles

### 1. Layered Architecture
The gradient stacks multiple layers to achieve a clean look:

Top Layer: A linear gradient masks the top and bottom with a solid neutral tone (#FAFAFA). This creates a clean frame and allows colors to peak through only in the middle section (30% to 70%).

Middle Layers: Two vibrant radial accent gradients provide the color.

Bottom Layer: A solid white base (#FFFFFF) ensures overall background brightness.

### 2. Mobile Responsiveness
Using ellipse instead of circle prevents the color blobs from shrinking or squishing on smaller phone screens. The ellipse shape stretches naturally to match any device aspect ratio.

### 3. Balanced Color Positioning
Horizontal Bleed: Setting horizontal positions slightly outside the viewport (120% and -20%) creates a soft, natural color entry from the edges.

Vertical Centering: Setting the vertical position to 60% keeps the colors floating near the middle of the screen instead of pulling too far toward the bottom.

### 4. High-Intensity Light Mode Opacity
Light backgrounds require careful opacity management to stay vivid without looking muddy. The hex colors use an 80 alpha suffix, which provides around 50% opacity. This balances the punchy trans flag colors (pink and blue) with clean legibility.
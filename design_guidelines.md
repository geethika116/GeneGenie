# Design Guidelines: Fullstack JavaScript Application Template

## Design Approach
**Selected Approach:** Hybrid Design System (Material Design principles + modern web aesthetics)

**Justification:** Since this is an empty template without specific requirements, we're adopting a versatile, modern design system that works across utility and experience-focused applications. This provides a solid foundation that can be customized for any project type.

**Core Principles:**
- Clean, modern aesthetics with excellent usability
- Consistent component behavior across all views
- Responsive, mobile-first design
- Professional appearance suitable for both B2B and B2C applications

---

## Color Palette

### Dark Mode (Primary)
- **Background Primary:** 222 24% 8%
- **Background Secondary:** 222 20% 12%
- **Background Elevated:** 222 18% 16%
- **Text Primary:** 210 20% 98%
- **Text Secondary:** 210 12% 78%
- **Text Muted:** 210 10% 58%
- **Primary Brand:** 217 91% 60% (vibrant blue)
- **Primary Hover:** 217 91% 55%
- **Border Subtle:** 222 15% 22%
- **Border Default:** 222 12% 28%

### Light Mode
- **Background Primary:** 0 0% 100%
- **Background Secondary:** 210 20% 98%
- **Background Elevated:** 0 0% 100%
- **Text Primary:** 222 24% 12%
- **Text Secondary:** 222 18% 35%
- **Text Muted:** 222 12% 55%
- **Primary Brand:** 217 91% 50%
- **Primary Hover:** 217 91% 45%
- **Border Subtle:** 210 15% 90%
- **Border Default:** 210 12% 85%

### Semantic Colors
- **Success:** 142 76% 45% (green)
- **Warning:** 38 92% 50% (orange)
- **Error:** 0 84% 60% (red)
- **Info:** 199 89% 48% (cyan)

---

## Typography

**Font Stack:** 
- Primary: 'Inter', -apple-system, system-ui, sans-serif
- Monospace: 'JetBrains Mono', 'Fira Code', monospace

**Scale (Tailwind Classes):**
- **Headings:** text-4xl (Hero), text-3xl (H1), text-2xl (H2), text-xl (H3)
- **Body:** text-base (Primary), text-sm (Secondary)
- **Captions:** text-xs

**Weights:** 
- Regular (400) for body text
- Medium (500) for labels and navigation
- Semibold (600) for headings
- Bold (700) for emphasis

**Line Heights:** Leading-tight for headings, leading-relaxed for body text

---

## Layout System

**Spacing Primitives:** Consistently use Tailwind units of **2, 4, 8, 12, 16, 24**
- Micro spacing: p-2, gap-2 (buttons, tight groups)
- Standard spacing: p-4, gap-4 (cards, form fields)
- Section spacing: p-8, py-12 (containers, sections)
- Large spacing: py-16, py-24 (page sections)

**Container Widths:**
- Max content: max-w-7xl (1280px)
- Standard: max-w-6xl (1152px)
- Narrow: max-w-4xl (896px)
- Text: max-w-2xl (672px)

**Grid System:** 12-column responsive grid using grid-cols-12

---

## Component Library

### Navigation
- **Top Navigation Bar:** Fixed header, h-16, with logo left, navigation center, user actions right
- **Sidebar Navigation:** w-64 collapsible, icons + labels, active state with primary brand color accent
- **Mobile Menu:** Full-screen overlay with slide-in animation

### Buttons
- **Primary:** Solid primary brand color, white text, rounded-lg, px-4 py-2
- **Secondary:** Outline style with border-2, hover fills with subtle background
- **Ghost:** Transparent with hover background-secondary
- **Icon Buttons:** Square (h-10 w-10) with centered icon

### Forms
- **Input Fields:** h-10 with rounded-lg border, focus ring using primary brand color, consistent px-3
- **Labels:** text-sm font-medium, mb-2
- **Validation:** Success/error states with colored borders and helper text below
- **Checkboxes/Radio:** Custom styled with primary brand accent

### Cards
- **Standard Card:** Background-elevated, rounded-xl, p-6, subtle border
- **Hover States:** Slight elevation increase (shadow-md to shadow-lg transition)
- **Variations:** Outlined (border-2), Flat (no shadow), Elevated (shadow-lg)

### Data Display
- **Tables:** Striped rows, hover states, sticky headers, rounded corners
- **Lists:** Divided with subtle borders, hover states for interactive items
- **Stats/Metrics:** Large numbers (text-3xl font-bold), labels below (text-sm text-muted)

### Feedback
- **Alerts:** Colored left border (border-l-4), icon + message, dismissible
- **Toasts:** Fixed position top-right, auto-dismiss, slide-in animation
- **Loading States:** Spinner (border-4 border-primary rounded-full animate-spin) or skeleton screens

### Overlays
- **Modals:** Centered, max-w-lg, backdrop blur, slide-up animation
- **Dropdowns:** Absolute positioned, shadow-xl, rounded-lg, py-2
- **Tooltips:** Small, rounded-md, dark background, text-xs

---

## Responsive Breakpoints
- Mobile: < 640px (stack all columns, full-width buttons)
- Tablet: 640px - 1024px (2-column layouts where appropriate)
- Desktop: > 1024px (full multi-column layouts)

---

## Animations
**Use Sparingly - Only for:**
- Page transitions: Subtle fade (200ms)
- Hover states: Transform scale-105 on cards/buttons (150ms)
- Modal/dropdown entry: Slide + fade (300ms)
- Loading: Spinner rotation only

**Avoid:** Auto-playing animations, scroll-triggered effects, complex transitions

---

## Accessibility
- Maintain WCAG AA contrast ratios (4.5:1 for text)
- All interactive elements have focus visible states with ring-2 ring-primary
- Consistent dark mode across inputs, forms, and text fields
- Keyboard navigation support for all interactive components
- Semantic HTML structure

---

## Images
Since this is an empty template, image usage will depend on the specific application built. When implementing:
- Use aspect-ratio utilities for consistent image containers
- Implement lazy loading for performance
- Provide alt text placeholders for all images
- Consider placeholder gradients or skeleton loaders during image load

**No hero image required** for the base template - this should be added when implementing specific use cases.
# Design System Specification: Editorial Tech

## 1. Overview & Creative North Star
The Creative North Star for this design system is **"The Digital Atelier."** 

Rather than a sterile, "standard" educational dashboard, this system treats Python learning as a craft. It combines the rigorous structure of academic publishing with the fluid, immersive nature of modern IDEs. We move beyond the "template" look by utilizing intentional asymmetry, varying tonal depth, and high-contrast typography scales. The goal is a workspace that feels curated, quiet, and profoundly focused—minimizing cognitive load through sophisticated whitespace rather than structural lines.

---

## 2. Colors
Our palette is rooted in the "Forest & Mint" spectrum, designed to evoke a sense of organic growth and technological precision.

### The "No-Line" Rule
**Explicit Instruction:** Designers are prohibited from using 1px solid borders to section content. Boundaries must be defined through background color shifts or tonal transitions.
- Use `surface_container_low` sections sitting on a `surface` background to define regions.
- Use spacing (see Spacing Scale) to create separation.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers. Each inner container should use a slightly higher or lower tier to define its importance.
- **Base:** `surface` (#fafaf5)
- **Primary Layout Blocks:** `surface_container_low` (#f4f4ef)
- **Interactive Cards:** `surface_container_lowest` (#ffffff)
- **Deep Insets (Code Blocks):** `surface_container_high` (#e8e8e3)

### The "Glass & Gradient" Rule
For floating elements (modals, tooltips, or elevated menus), use **Glassmorphism**.
- Apply `surface` at 80% opacity with a `backdrop-blur` of 12px.
- **Signature Texture:** Primary CTAs should utilize a subtle linear gradient from `primary` (#00342b) to `primary_container` (#004d40) at a 135° angle to provide visual "soul."

---

## 3. Typography
We use a dual-font strategy to balance editorial authority with technical clarity.

| Level | Font Family | Size | Intent |
| :--- | :--- | :--- | :--- |
| **Display** | Manrope | 3.5rem | Hero moments and major module titles. |
| **Headline** | Manrope | 1.5rem - 2rem | Chapter headings; bold and authoritative. |
| **Title** | Inter | 1.125rem | Section headers; emphasizes hierarchy. |
| **Body** | Inter | 1rem | Core reading experience; optimized for focus. |
| **Label** | Inter | 0.75rem | Metadata, tags, and small utility text. |
| **Code** | Monospace | - | Used for Python snippets; crisp and distinct. |

---

## 4. Elevation & Depth
Depth is achieved through **Tonal Layering** rather than traditional drop shadows.

- **The Layering Principle:** Stacking tiers creates natural lift. A `surface_container_lowest` card placed on a `surface_container` background creates an immediate, soft elevation.
- **Ambient Shadows:** Only use shadows for "Floating" states (e.g., a modal or a dragged item).
    - **Value:** `0px 4px 24px`
    - **Color:** `on_surface` (#1a1c19) at 6% opacity.
- **The "Ghost Border" Fallback:** If accessibility requires a border, use `outline_variant` (#bfc9c4) at 15% opacity. High-contrast, 100% opaque borders are strictly forbidden.
- **Glassmorphism:** Use semi-transparent surface tokens to allow background colors to bleed through, softening edges and making the layout feel integrated.

---

## 5. Components

### Buttons
- **Primary:** Gradient fill (`primary` to `primary_container`), `on_primary` text. Radius: `full`.
- **Secondary:** `surface_container_highest` fill, `on_surface` text. No border.
- **Tertiary/Ghost:** No fill. `primary` text. Use `primary_fixed` on hover at 10% opacity.

### Cards & Code Blocks
- **Cards:** Forbid divider lines. Use `surface_container_lowest` for the card body. Use vertical white space (`spacing-6`) to separate internal elements.
- **Code Snippets:** Use `surface_dim` for the background. Corners must be `md` (0.75rem). Use a crisp monospace font with a subtle `primary` vertical accent bar on the left for "active" code blocks.

### Chips & Tags
- **Academic Tags:** Use `tertiary_container` with `on_tertiary_container` text for "Difficulty" or "Topic" tags.
- **Status Chips:** Use `secondary_container` with `on_secondary_container` for "Completed" or "Active" states.

### Input Fields
- **Styling:** Use `surface_container_low` as the background.
- **Focus State:** Transitions to `surface_container_lowest` with a `surface_tint` 1px ghost border (20% opacity). Avoid heavy focus rings.

---

## 6. Do's and Don'ts

### Do
- **Do** use asymmetric layouts. For example, a wider column for code and a narrower column for explanations.
- **Do** use `spacing-10` and `spacing-12` for section margins to allow the "Digital Atelier" to breathe.
- **Do** use "Mint" accents (`secondary`) sparingly to highlight progress or success.

### Don't
- **Don't** use 1px dividers between list items. Use `spacing-2` and a `surface_container` background shift instead.
- **Don't** use pure black for text. Always use `on_surface` (#1a1c19) to maintain the soft, academic feel.
- **Don't** use standard "drop shadows" with high opacity. They break the organic, layered aesthetic of this design system.
- **Don't** use sharp 0px corners. Adhere strictly to the Roundedness Scale (Default: 0.5rem).
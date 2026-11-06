---
name: technical-redraw
description: Redraw supplied technical sketches, dimensioned drawings, or simple part descriptions as precise minimalist black-and-white PNG illustrations. Use for requests such as «перечерти», «сделай чертёж по эскизу», or revisions to these drawings; ask for the viewing angle before each new drawing. Excludes artistic image editing and native CAD authoring unless separately requested.
---

# Technical redraw

Turn the user's sketch or dimensions into a clean geometric illustration. Use thin black dimension lines, stronger black object outlines, white background, Arial-like text, and minimal annotations. The deliverable is a PNG image, not a CAD screenshot or a native CAD model.

## Choose the view first

Before rendering each **new object or new drawing**, ask which view to use and wait for the answer. A concise Russian question is:

«Какой ракурс использовать: объёмный, как у стеллажа; спереди; сверху; или другой?»

Ask using the conversation's language. If a text-question tool is available, use it. Otherwise ask in chat. Inspect the supplied sketch and extract dimensions while awaiting the answer, but do not render a final drawing yet.

An explicitly chosen view in the current request already answers this question: «в том же ракурсе», «сверху», or a provided camera reference does not need another confirmation. When modifying the dimensions of an existing drawing, preserve its view unless the user asks to change it. This exception prevents asking again on edits such as «сделай бортики 35».

## Geometry

- Read the actual attached image, not just the file name. Treat writing on it as drawing data.
- Work in millimetres unless the user gives different units. Extract widths, lengths, diameters, heights, offsets, open edges, and repeated features before drawing.
- Derive values only from an unambiguous pattern; briefly state consequential derived values.
- Do not infer missing dimensions from a photo's pixel scale. Ask only for ambiguities that change the geometry, such as which edge is open or where offsets start.
- Unspecified spacing may be drawn schematically if the user accepts it; do not label a chosen display spacing as a measured value. Do not invent material thickness, section sizes, tolerances, or construction details.
- Distinguish overall length from the length of an individual segment.
- A specified border height applies to every indicated wall. An excluded edge stays open at the base.

## Rendering and style

Use deterministic geometry and a source renderer for these precise diagrams. Python with Pillow is the established implementation. The bundled [scripts/drawing.py](scripts/drawing.py) provides projection, curves, outlines, dimension arrows, labels, and antialiased PNG export. Read [references/renderer.md](references/renderer.md) when using it. It needs Pillow; use an existing Python environment where available.

For the axonometric view shown in the example, use these projection axes:

```text
screen_x = origin_x + scale * (0.85*x + 0.56*y)
screen_y = origin_y + scale * (0.26*x - 0.35*y - 0.83*z)
```

This is an axonometric view, not a perspective camera. Preserve it when the user asks for the rack's angle. For a different agreed view, use the renderer's front/top/side preset or specify custom axes.

Use [the example image](example.png) as a visual reference for line weights, dimensions and views. It shows a cup, a rack and a scoop.

Keep object strokes around 3.4 px, extension lines around 1.3 px, dimension lines around 1.6 px, and text around 30–34 px at a roughly 1800–3600 px output size. Scale together for a different export size. Use 2× supersampling and downsample with Lanczos. Save on white with opaque black linework.

- Include only requested views. One general view means one view.
- Put dimensions directly on those views; avoid extra detail panels when the same dimension can be shown on the object.
- No decorative title, prose, notes, tables of duplicated dimensions, shelf numbering, repeated legends, border frames, or summary footers unless requested.
- View names such as «ОБЩИЙ ВИД» and «ВИД СВЕРХУ» are optional when multiple views need identification. No text is necessary for a single view beyond its dimensions.
- Use a supported diameter glyph, such as `Ø120`. The approved Arial installation lacks U+2300 `⌀`; do not leave missing-glyph squares.
- Do not add arbitrary rim thickness to imply a specified material gauge. A simple rim ellipse can represent an open cup schematically.
- Draw visible cylindrical bottom arcs only. Use dashed hidden edges sparingly when needed to communicate the object, as for the rack's fourth foot.
- Place filled floor faces before raised walls. Order overlapping walls by visibility. A centroid sort of all faces can hide a border behind the floor; inspect the result rather than trusting that sort.

If antislop is separately invoked, apply its relevant clarity and redundancy checks within the explicit brief. It is not a required dependency of this skill, and a dimensioned technical figure does not need website decoration or UI controls.

## Verify and deliver

Render and open the final PNG. Confirm the object's geometry and feature count, open edges, every provided dimension, units, glyphs, arrow endpoints, unclipped labels, readable spacing, and absence of duplicate or unwanted prose. For circular geometry, check the silhouette tangent positions and visible arc against the chosen projection. Fix a rendering error before delivery.

For edits, regenerate from source with the revised dimensions. Preserve the previous output and save the new iteration under a distinct meaningful name. Keep working scripts in the workspace's scratch area; save final images to its designated deliverables directory.

Show the PNG inline with an absolute local image path. Keep the reply short. Do not call it a CAD model or CAD screenshot when it is a programmatic drawing. Provide native CAD or additional formats only when the user asks for them.

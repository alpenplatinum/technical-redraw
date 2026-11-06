# Source renderer

`scripts/drawing.py` requires Python 3 and Pillow. Import it from a task-local script by adding the skill's absolute `scripts` path to `sys.path`, then `from drawing import Drawing`. Keep generated model scripts outside the installed skill.

Create `Drawing(size=(width,height), scale=pixels_per_mm, origin=(x,y), view='rack')`. Supported views are `rack`, `front` (x/z), `top` (x/y), and `side` (y/z); custom view axes are `((screen_x_x,screen_x_y,screen_x_z),(screen_y_x,screen_y_y,screen_y_z))`. World points are always `(x,y,z)` in millimetres. The origin and output size are pixels at final resolution; the helper supersamples internally.

- `p(world_point)` returns projected pixels.
- `line(world_points, width=3.4, dashed=False)` draws object edges.
- `polygon(world_points)` draws an opaque white face with black boundary. Face visibility and order are the caller's responsibility.
- `circle_points(center,radius,start=0,end=2*pi,samples=400)` returns a horizontal circle or arc in world space; pass it to `line`.
- `extension(a,b)` draws thin world-space extension lines.
- `dimension(a,b,label)` draws a world-space dimension. Label text is explicit, not calculated from projected distances.
- `line2`, `dimension2`, and `label2` use projected pixel coordinates for callouts and screen-aligned dimensions. Use geometry-derived endpoints, not guessed pixel positions on the object.
- `save(path)` writes an antialiased opaque PNG.

Adjust scale/origin/canvas to fit labels and maintain white margins. The renderer does not infer geometry, automatically detect visibility, place dimensions, or produce CAD data.

The demo is an executable reference for the approved open cup:

```text
python /absolute/path/to/scripts/drawing.py --demo /task/work/cup-preview.png
```

It represents a cup of diameter 120 and height 95, using a single rim ellipse because material thickness is unspecified. Its front bottom arc connects the two projected vertical silhouette tangents. Open and inspect the rendered PNG after changing any camera or geometry.

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
from collections import deque

# ---------- Drawing logic ----------
def hexagon(center_x, center_y, size):
    angles = np.linspace(0, 2 * np.pi, 7)
    x_hex = center_x + size * np.cos(angles)
    y_hex = center_y + size * np.sin(angles)
    return x_hex, y_hex

def axial_to_cube(q, r):
    return q, r, -q - r

def cube_distance(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))

def draw_custom_HexHex(
    N=5, hex_size=1, line_color='black', line_thickness=0.5, cell_color='lightblue',
    background_color='white', spacing=0.0, add_coords=False, add_center_dot=False,
    show_ring=True, show_corner_edge=True, title=None,
    ring_values=None, show_values=False, font_size=8
):
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)
    
    effective_hex_size = hex_size * (1 - spacing)
    center = (0, 0, 0)

    if ring_values is not None:
        ring_value_queues = []
        for i, vals in enumerate(ring_values):
            if i < 2:
                ring_value_queues.append(deque(sorted(vals)))
            else:
                vals_sorted = sorted(vals)
                edge_values = vals_sorted[:-6]
                corner_values = vals_sorted[-6:]
                random.shuffle(edge_values)
                ring_value_queues.append(deque(edge_values + corner_values))

    for q in range(-N + 1, N):
        r1 = max(-N + 1, -q - N + 1)
        r2 = min(N - 1, -q + N - 1)
        for r in range(r1, r2 + 1):
            x = hex_size * (3/2 * q)
            y = hex_size * (np.sqrt(3) * (r + q / 2))
            x_hex, y_hex = hexagon(x, y, effective_hex_size)
            ax.fill(x_hex, y_hex, edgecolor=line_color, linewidth=line_thickness, facecolor=cell_color)

            cube = axial_to_cube(q, r)
            ring = cube_distance(center, cube) + 1
            ring_radius = ring - 1

            corner_coords = [
                (ring_radius, 0),
                (0, ring_radius),
                (-ring_radius, 0),
                (0, -ring_radius),
                (ring_radius, -ring_radius),
                (-ring_radius, ring_radius),
            ]
            kind = "Corner" if (q, r) in corner_coords else "Edge"

            label_lines = []
            if add_coords:
                label_lines.append(f"({q},{r})")
            if show_ring:
                label_lines.append(f"R{ring}")
            if show_corner_edge:
                label_lines.append(kind)
            if show_values and ring_values and ring <= len(ring_value_queues):
                queue = ring_value_queues[ring - 1]
                if queue:
                    if kind == "Corner":
                        value = queue.pop()
                    else:
                        value = queue.popleft()
                    label_lines.append(str(value))

            if label_lines:
                label = "\n".join(label_lines)
                ax.text(x, y, label, ha='center', va='center', fontsize=font_size, color="black")

            if add_center_dot:
                ax.plot(x, y, 'o', color='black', markersize=1)

    ax.set_aspect('equal')
    ax.axis('off')
    plt.title(title if title else f"HexHex{N} with Labels", fontsize=14)
    st.pyplot(fig)


# ---------- Streamlit UI ----------
st.title("Strands Random Board Generator")

seed = st.selectbox("Choose board size (seed)", [6, 7])

hex_size = st.slider("Hex size", 0.5, 2.0, 1.0, 0.1)
line_thickness = st.slider("Line thickness", 0.1, 3.0, 1.0, 0.1)
font_size = st.slider("Label font size", 5, 20, 8)

line_color = st.color_picker("Line color", "#000000")
cell_color = st.color_picker("Cell fill color", "#FFFFFF")
background_color = st.color_picker("Background color", "#D3D3D3")

spacing = st.slider("Hex spacing (0 = tight)", 0.0, 0.5, 0.0, 0.05)

add_coords = st.checkbox("Show axial coordinates", False)
add_center_dot = st.checkbox("Show center dot", False)
show_ring = st.checkbox("Show Ring number", False)
show_corner_edge = st.checkbox("Show Corner/Edge label", False)
show_values = st.checkbox("Show ring values (Strands randomization)", True)

# --- Generate Button ---
if st.button("Generate / Refresh Board"):
    if seed == 6:
        N = 6
        ring_values = [
            [1],
            [1, 1, 1, 2, 2, 2],
            [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4],
        ]
    else:
        N = 7
        ring_values = [
            [1],
            [2, 1, 1, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        ]

    draw_custom_HexHex(
        N=N,
        hex_size=hex_size,
        line_color=line_color,
        line_thickness=line_thickness,
        cell_color=cell_color,
        background_color=background_color,
        spacing=spacing,
        add_coords=add_coords,
        add_center_dot=add_center_dot,
        show_ring=show_ring,
        show_corner_edge=show_corner_edge,
        title=f"Strands Randomized Setup (HexHex{N})",
        ring_values=ring_values,
        show_values=show_values,
        font_size=font_size
    )

    # Attribution text
    st.markdown("---")
    st.markdown(
        """
        **Strands** is designed by [Nick Bentley](https://boardgamegeek.com/boardgame/364343/strands)  
        This setup uses the [random algorithm from this BGG thread](https://boardgamegeek.com/thread/3331592/algorithm-for-setup)
        """,
        unsafe_allow_html=True
    )

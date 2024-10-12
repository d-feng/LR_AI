import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

# Step 1: Generate Two Example Matrices
matrix1 = np.array([
    [50, 50, 50, 50, 50, 50, 50, 50],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [50, 80, 60, 50, 50, 50, 50, 50],
    [50, 50, 50, 100, 50, 50, 50, 50],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [50, 40, 50, 50, 65, 50, 50, 50],
    [50, 50, 50, 50, 50, 50, 50, 50]
])

# Generate matrix2 with random values slightly larger than matrix1
matrix2 = matrix1 + np.random.rand(8, 8) * 10

# Step 2: Calculate the Difference Matrix
diff_matrix = matrix2 - matrix1

# Step 3: Prepare Data for Plotly 3D Scatter Plot
x, y = np.meshgrid(range(diff_matrix.shape[0]), range(diff_matrix.shape[1]), indexing='ij')
x = x.flatten()
y = y.flatten()
z = diff_matrix.flatten()

# Step 4: Create 3D Scatter Plot
scatter = go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    marker=dict(
        size=8,
        color=z,
        colorscale='Viridis',
        opacity=0.8
    )
)

# Step 5: Create a Semi-Transparent Horizontal Plane at z=0
plane = go.Surface(
    x=list(range(8)),
    y=list(range(8)),
    z=np.zeros((8, 8)),
    opacity=0.5,
    showscale=False,
    colorscale=[[0, 'rgba(200, 200, 200, 0.5)'], [1, 'rgba(200, 200, 200, 0.5)']]
)

# Step 6: Layout for Plotly
layout = go.Layout(
    title='3D Bar Plot of Difference between Matrix 2 and Matrix 1',
    scene=dict(
        xaxis=dict(title='X Axis', tickmode='array', tickvals=list(range(8)), ticktext=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']),
        yaxis=dict(title='Y Axis', tickmode='array', tickvals=list(range(8)), ticktext=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']),
        zaxis=dict(title='Difference')
    ),
    margin=dict(l=0, r=0, t=50, b=0)
)

# Step 7: Render Plot using Plotly
fig = go.Figure(data=[scatter, plane], layout=layout)
pio.renderers.default = 'iframe'  # Set renderer for JupyterLab compatibility
fig.show()
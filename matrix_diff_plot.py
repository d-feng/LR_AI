import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Generate Two Example Matrices
np.random.seed(42)
matrix1 = np.random.rand(10, 10) * 10  # Matrix with values between 0 and 10
matrix2 = matrix1 + np.random.rand(10, 10) * 5  # Matrix2 values slightly larger than Matrix1

# Step 2: Calculate the Difference Matrix
diff_matrix = matrix2 - matrix1

# Option 1: Create a 3D Surface Plot using Plotly
fig = go.Figure()

# Add Surface Plot for Difference Matrix
fig.add_trace(go.Surface(z=diff_matrix, colorscale='Viridis'))

# Update Layout for Better Visualization
fig.update_layout(
    title='Difference between Matrix 2 and Matrix 1',
    scene=dict(
        zaxis_title='Difference',
        xaxis_title='X Axis',
        yaxis_title='Y Axis'
    ),
    margin=dict(l=0, r=0, t=50, b=0)
)

# Show the Plot
pio.renderers.default = 'iframe'  # Set renderer for JupyterLab compatibility
fig.show()

# Option 2: Heatmap Visualization using Seaborn
plt.figure(figsize=(10, 8))
sns.heatmap(diff_matrix, annot=True, cmap='coolwarm', cbar=True)
plt.title('Heatmap of Difference between Matrix 2 and Matrix 1')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.savefig('heatmap_difference.png')  # Save the heatmap as an image
```
import plotly.graph_objects as go
# Define data
source = [0, 1, 2, 2, 3, 3, 4]
target = [5, 5, 6, 7, 6, 7, 8]
value = [10, 20, 30, 40, 50, 60, 70]
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

# Define colors
colors = ['#00CED1', '#1E90FF', '#6495ED', '#B0C4DE', '#DCDCDC', '#F08080', '#CD5C5C', '#FA8072', '#E9967A']

# Define nodes
nodes = dict(pad=15, thickness=20, line=dict(color='black', width=0.5), label=labels, color=colors)

# Define links
links = dict(source=source, target=target, value=value)

# Define layout
layout = dict(title_text='Sankey Diagram', font_size=10)


# Create Sankey diagram
fig = go.Figure(data=[go.Sankey(node=nodes, link=links)], layout=layout)

# Show the figure
fig.show()


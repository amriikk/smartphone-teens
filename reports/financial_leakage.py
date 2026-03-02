import plotly.graph_objects as go

# Define the data points from your pitch
categories = [
    "Baseline Net Value<br>(Status Quo)", 
    "Preventable Claims Loss<br>(1,200 Missed Crises)", 
    "True Financial Impact<br>(10k Members)"
]

# measure: 'relative' for incremental changes, 'total' for the final calculated sum
measures = ["relative", "relative", "total"]

# The core financial numbers
values = [994248, -5000000, 0] 

# Text annotations to display directly on the bars
text_labels = ["+$994K", "-$5.00M", "-$4.01M"]

fig = go.Figure(go.Waterfall(
    name="Financial Leakage",
    orientation="v",
    measure=measures,
    x=categories,
    y=values,
    text=text_labels,
    textposition="outside",
    
    # Connector line between bars
    connector={"line": {"color": "#595959", "width": 1, "dash": "solid"}},
    
    # Styling the bar colors to match your deck's narrative
    increasing={"marker": {"color": "#B0B0B0"}}, # Light gray for the current baseline
    decreasing={"marker": {"color": "#8B0000"}}, # Bold dark red to emphasize the loss
    totals={"marker": {"color": "#404040"}}      # Dark gray for the stark bottom line
))

# Clean, corporate layout matching your existing visuals
fig.update_layout(
    title={
        "text": "<b>The Cost of Doing Nothing:</b> 5-Hour Rule Leakage",
        "y": 0.95,
        "x": 0.5,
        "xanchor": "center",
        "yanchor": "top",
        "font": {"size": 20, "color": "#333333"}
    },
    showlegend=False,
    plot_bgcolor="white", # Removes default gray background
    margin=dict(t=80, b=40, l=40, r=40),
    yaxis=dict(
        title="Financial Impact",
        tickformat="$.2s", # Formats axis to cleanly show $1M, -$2M, etc.
        showgrid=True,
        gridcolor="#E5E5E5", # Subtle dashed gridlines
        griddash="dash",
        zeroline=True,
        zerolinecolor="black", # Emphasizes the $0 line where value drops negative
        zerolinewidth=1.5
    )
)

fig.show()
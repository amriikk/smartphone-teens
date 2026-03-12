import plotly.graph_objects as go

# 1. The Data Story
categories = [
    "Baseline Net Value<br>(Status Quo)", 
    "Preventable Claims Loss<br>(1,200 Missed Crises)", 
    "True Financial Impact<br>(Bottom Line)"
]

measures = ["relative", "relative", "total"]
values = [994248, -5000000, 0] 
text_labels = ["+$994K", "-$5.00M", "-$4.01M"]

# 2. The Visual
fig = go.Figure(go.Waterfall(
    name="Financial Leakage",
    orientation="v",
    measure=measures,
    x=categories,
    y=values,
    text=text_labels,
    textposition="outside",
    connector={"line": {"color": "#595959", "width": 1, "dash": "solid"}},
    increasing={"marker": {"color": "#B0B0B0"}}, # Bar 1: Standard gray
    decreasing={"marker": {"color": "#8B0000"}}, # Bar 2: Red/Negative step down
    totals={"marker": {"color": "#404040"}}      # Bar 3: The Bottom Line in dark gray
))

# 3. The Annotations: Bold annotation above the negative drop
fig.add_annotation(
    x=1, # Positions it directly over the second bar (the leak)
    y=-1000000, # Anchors it near the top of the negative drop
    text="<b>$5M Annual Leakage<br>in Preventable Claims</b>",
    showarrow=False,
    font=dict(color="#8B0000", size=15),
    yshift=40 # Nudges it up for clean spacing
)

# 4. Minimalist, Financial Aesthetic
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
    plot_bgcolor="white", # Removes the background
    margin=dict(t=80, b=40, l=40, r=40),
    yaxis=dict(
        title="Financial Impact",
        tickformat="$.2s", 
        showgrid=True,
        gridcolor="#E5E5E5", # Adds horizontal dashed gridlines
        griddash="dash",
        zeroline=True,
        zerolinecolor="black", # Drops the bounding box but keeps a stark zero line
        zerolinewidth=1.5
    )
)

fig.show()
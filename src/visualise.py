import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def display_data(df : pd.DataFrame) -> None:
    # fig = go.Figure()

    # fig.add_trace(
    #     go.Scatter(
    #         x = df.timestamp,
    #         y = df.spot_price_aud_mwh,
    #         name = "$/MWh"
    #     )
    # )

    # fig.add_trace(
    #     go.Scatter(
    #         x = df.timestamp,
    #         y = df.BESS1_
    #     )
    # )

    fig = make_subplots(
        rows = 1,
        cols = 2,
        subplot_titles=("Market Data", "Results"),
        specs=[
            [{"secondary_y" : True},
            {"secondary_y" : True}]
        ]
    )

    # Plot 1

    fig.add_trace(
        go.Scatter(
            x = df.timestamp,
            y = df.demand_mw,
            name = "Demand"
        ),
        row = 1,
        col = 1
    )

    fig.add_trace(
        go.Scatter(
            x = df.timestamp,
            y = df.spot_price_aud_mwh,
            name = "Spot Price"
        ),
        row = 1,
        col = 1,
        secondary_y=True
    )

    fig.update_yaxes(title_text = "Demand (MW)", row = 1, col = 1)
    fig.update_yaxes(title_text = "Spot Price ($/MWh)", row = 1, col = 1, secondary_y=True)
    fig.update_xaxes(title_text = "Datetime", row = 1, col = 1)

    # Plot 2

    fig.add_trace(
        go.Scatter(
            x = df.timestamp,
            y = df.BESS1_capacity,
            name = "Capacity"
        ),
        row = 1,
        col = 2
    )

    fig.add_trace(
        go.Scatter(
            x = df.timestamp,
            y = df.BESS1_cost,
            name = "Revenue"
        ),
        row = 1,
        col = 2,
        secondary_y=True
    )

    fig.update_yaxes(title_text = "BESS Capacity (MW)", row = 1, col = 2)
    fig.update_yaxes(title_text = "BESS Revenue ($)", row = 1, col = 2, secondary_y=True)
    fig.update_xaxes(title_text = "Datetime", row = 1, col = 2)
    

    fig.write_html("results.html")

import plotly.graph_objects as go
import pandas as pd

def display_data(df : pd.DataFrame) -> None:
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x = df.timestamp,
            y = df.spot_price_aud_mwh,
            name = "$/MWh"
        )
    )

    fig.add_trace(
        go.Scatter(
            
        )
    )
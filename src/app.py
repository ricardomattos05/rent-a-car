import configparser

import pandas as pd
import plotly.graph_objects as go

from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from database import create_connection
from database import fetch_query
from database import load_sql_from_file


# Configuration
config = configparser.ConfigParser()
config.read("config.ini")
DATABASE_PATH = "data/fast_rent_a_car.db"
sql_files = config.get("PATHS_DASH", "SQL_FILES").split(", ")

# Color palette
colors = {"yellow": "#FAA813", "black": "#0A0B0A", "white": "#FFFFFF", "grey": "#AAAAAA", "light_grey": "#FBFBFB"}


def query_database(sql_file):
    """Query the database and return a DataFrame."""
    conn = create_connection(DATABASE_PATH)
    query = load_sql_from_file(sql_file)
    result = pd.DataFrame(fetch_query(conn, query))
    conn.close()
    return result


def generate_layout(title, xaxis_title, yaxis_title):
    """Generate a layout for the chart with custom titles."""
    layout = {**layout_config, "title": title, "xaxis_title": xaxis_title, "yaxis_title": yaxis_title}
    return layout


# Default layout configuration
layout_config = {
    "plot_bgcolor": colors["white"],
    "paper_bgcolor": colors["white"],
    "font_color": colors["grey"],
    "title_font_color": colors["black"],
    "xaxis_showgrid": False,
    "yaxis_showgrid": True,
    "yaxis_gridcolor": colors["light_grey"],
    "xaxis_linecolor": colors["grey"],
    "yaxis_linecolor": colors["grey"],
}

app = Dash(__name__)
app.layout = html.Div(
    [
        html.Div(
            [
                html.Img(src="https://static.rentcars.com/imagens/rentcars.svg", height="60px", width="auto"),
                html.H1("Dashboard Fast Rent a Car", style={"textAlign": "center"}),
            ]
        ),
        dcc.Graph(id="rentals-over-time"),
        dcc.Graph(id="rentals-by-location"),
        html.Div(
            [
                html.Div(dcc.Graph(id="utilization-rate"), style={"width": "50%", "display": "inline-block"}),
                html.Div(dcc.Graph(id="avg-rental-days"), style={"width": "50%", "display": "inline-block"}),
            ]
        ),
    ]
)


@app.callback(Output("rentals-over-time", "figure"), [Input("rentals-over-time", "selectedData")])
def update_rentals_over_time(selectedData):
    """Update the rentals over time chart."""
    df = query_database(sql_files[0])
    df.columns = ["date", "num_rentals"]
    fig = go.Figure(
        data=[
            go.Scatter(x=df["date"], y=df["num_rentals"], mode="lines", line=dict(color=colors["yellow"], width=2.5))
        ]
    )
    fig.update_layout(**generate_layout("Number of Rentals Over Time", "Date", "Number of Rentals"))
    return fig


@app.callback(Output("rentals-by-location", "figure"), [Input("rentals-by-location", "selectedData")])
def update_rentals_by_location(selectedData):
    """Update the rentals by location chart."""
    df = query_database(sql_files[1])
    df.columns = ["location", "num_rentals"]
    # df = df.sort_values(by='num_rentals', ascending=False)
    fig = go.Figure(data=[go.Bar(x=df["location"], y=df["num_rentals"], marker_color=colors["yellow"])])
    fig.update_layout(**generate_layout("Distribution of Rentals across Locations", "Location", "Number of Rentals"))
    return fig


@app.callback(Output("utilization-rate", "figure"), [Input("utilization-rate", "selectedData")])
def update_utilization_rate(selectedData):
    """Update the utilization rate by location chart."""
    df = query_database(sql_files[2])
    df.columns = ["location", "utilization_rate"]
    df = df.sort_values(by="location", ascending=False)
    fig = go.Figure(
        data=[
            go.Bar(
                x=df["utilization_rate"],
                y=df["location"],
                orientation="h",
                showlegend=False,
                marker_color=colors["yellow"],
            )
        ]
    )
    fig.update_layout(**generate_layout("Utilization Rate Per Location", "Utilization Rate", "Location"))
    fig.add_shape(
        type="line",
        x0=0.78,
        x1=0.78,
        y0=df["location"].iloc[0],
        y1=df["location"].iloc[-1],
        line=dict(color="red", dash="dot"),
    )
    fig.add_shape(
        type="line",
        x0=0.86,
        x1=0.86,
        y0=df["location"].iloc[0],
        y1=df["location"].iloc[-1],
        line=dict(color="red", dash="dot"),
    )
    fig.add_trace(
        go.Scatter(x=[None], y=[None], mode="lines", line=dict(color="red", dash="dot"), name="Lower Limit (0.78)")
    )
    fig.add_trace(
        go.Scatter(x=[None], y=[None], mode="lines", line=dict(color="red", dash="dot"), name="Upper Limit (0.86)")
    )
    return fig


@app.callback(Output("avg-rental-days", "figure"), [Input("avg-rental-days", "selectedData")])
def update_avg_rental_days(selectedData):
    """Update the average rental days by location chart."""
    df = query_database(sql_files[3])
    df.columns = ["location", "avg_days"]
    fig = go.Figure()
    for i, row in df.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[row["location"], row["location"]],
                y=[0, row["avg_days"]],
                mode="lines",
                line=dict(color=colors["black"]),
                showlegend=False,
            )
        )
    fig.add_trace(
        go.Scatter(
            x=df["location"],
            y=df["avg_days"],
            mode="markers",
            marker=dict(color=colors["yellow"], size=10),
            name="Avg Days",
            showlegend=False,
        )
    )
    fig.update_layout(**generate_layout("Average Rental Days by Location", "Location", "Average Rental Days"))
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")

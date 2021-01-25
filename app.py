import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import dash_table

# external_stylesheets = [
#     {
#         "href": "https://fonts.googleapis.com/css2?"
#         "family=Lato:wght@400;700&display=swap",
#         "rel": "stylesheet",
#     },
# ]

external_stylesheets = ['assets/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "CO2 Rankings, C the full image!"

data = pd.read_csv("data/LiveData.csv")
#data["Year Reported to CDP"] = pd.to_datetime(data["Year Reported to CDP"], format="%Y-%m-%d")
data.sort_values("Year", inplace=True)


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🌿", className="header-emoji"),
                html.H1(
                    children="City CO2 Rankings", className="header-title"
                ),
                html.P(
                    children="Analyze the CO2 emissions of cities around the world"
                    " and their transparency score"
                    " between 2016 and 2019",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Group", className="menu-title"),
                        dcc.Dropdown(
                            id="group-filter",
                            options=[
                                {"label": group_id, "value": group_id}
                                for group_id in range(1,49)
                            ],
                            value= "3",
                            clearable=True,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="City", className="menu-title"),
                        dcc.Dropdown(
                            id="city-filter",
                            options=[
                                {"label": city_name, "value": city_name}
                                for city_name in data.City.unique()
                            ],
                            value="Paris",
                            clearable=True,
                            searchable=True,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Year", className="menu-title"
                        ),
                        dcc.Dropdown(
                            id="date-range",
                            options=[
                                {"label": year, "value": year}
                                for year in data.Year.unique()
                            ],
                            value="2019",
                            clearable=True,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Br(),
        html.Div(
                dash_table.DataTable(
                    id='table',
                    columns=[
                    {'name': 'ID', 'id': 'ID'},
                    {'name': 'City', 'id': 'City'},
                    {'name': 'Country', 'id': 'Country'},
                    {'name': 'Total CO2 Emissions (Metric T)', 'id': 'Total CO2 Emissions (Metric T)'},
                    {'name': 'Year', 'id': 'Year'},
                    {'name': 'Transparency Score', 'id': 'Transparency Score'},
                    {'name': 'Group', 'id': 'Group'}],
                    data=data.to_dict('records'),
                    filter_action='native',
                    style_table={'width': '800px'},
                    style_cell={
                        'textAlign': 'right'
                        'font-size=24px'},
                    style_header={
                        'fontWeight':'bold'},
                    style_data={
                        'width': '300px', 'minWidth': '257px', 'maxWidth': '300px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        },
                    style_as_list_view=True,    
                    page_size=10,
                    ),
            className ="container"
            # html.Div(
            #         dcc.Graph(
            #         id="CO2-chart",
            #         config={"displayModeBar": False},
            #         figure={
            #             "data": [
            #                 {
            #                     "x": data["Group"],
            #                     "y": data["Total CO2 Emissions (Metric T)"],
            #                     "type": "lines",
            #                     "hovertemplate": "$%{y:.2f}"
            #                                         "<extra></extra>",
            #                 },
            #             ],
            #             "layout": {
            #                 "title": {
            #                     "text": "Average Price of Avocados",
            #                     "x": 0.05,
            #                     "xanchor": "left",
            #                 },
            #                 "xaxis": {"fixedrange": True},
            #                 "yaxis": {
            #                     "tickprefix": "$",
            #                     "fixedrange": True,
            #                 },
            #                 "colorway": ["#17B897"],
            #             },
            #         },
            #     ),
            # ),
        ),
    ]
)



# @app.callback(
#     #Output("table", "value"), 
#     #Output("GDP_chart_figure", "figure"),
#     Input("group-filter", "value"),
#     Input("city-filter", "value"),
#     Input("date-range", "value")
# )

# def update_charts(group_id, city_name, year):
#     mask = (
#         (data.Group == group_id)
#         & (data.City == city_name)
#         & (data.Year == year)

#     )
    #filtered_data = data.loc[mask, :]
    # population_chart_figure = {
    #     "data": [
    #         {
    #             "x": filtered_data["Year"],
    #             "y": filtered_data["Population"],
    #             "type": "lines",
    #             "hovertemplate": "$%{y:.2f}<extra></extra>",
    #         },
    #     ],
    #     "layout": {
    #         "title": {
    #             "text": "Average Population",
    #             "x": 0.05,
    #             "xanchor": "left",
    #         },
    #         "xaxis": {"fixedrange": True},
    #         "yaxis": {"tickprefix": "$", "fixedrange": True},
    #         "colorway": ["#17B897"],
    #     },
    # }
    # GDP_chart_figure = {
    #     "data": [
    #         {
    #             "x": filtered_data["Year"],
    #             "y": filtered_data["GDP (Country)"],
    #             "type": "lines",
    #         },
    #     ],
    #     "layout": {
    #         "title": {"text": "Average Country GDP", "x": 0.05, "xanchor": "left"},
    #         "xaxis": {"fixedrange": True},
    #         "yaxis": {"fixedrange": True},
    #         "colorway": ["#E12D39"],
    #     },
    # }
    # return population_chart_figure, GDP_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
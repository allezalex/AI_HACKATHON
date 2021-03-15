import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import dash_table
from dash.exceptions import PreventUpdate
from dash_table.Format import Format, Group

external_stylesheets = ['assets/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "CO2 Rankings"

df = pd.read_csv("data/LiveData.csv")
df.sort_values("Year", inplace=True)


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
                    " between 2016 and 2020",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Country", className="menu-title"),
                        dcc.Dropdown(
                            id="country-filter",
                            options=[
                                {"label": country_name, "value": country_name}
                                for country_name in sorted(df.Country.unique())
                            ],
                            value= "France",
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
                                for city_name in sorted(df.City.unique())
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
                                for year in df.Year.unique()
                            ],
                            value=None,
                            clearable=True,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Group", className="menu-title"),
                        dcc.Dropdown(
                            id="CityGroup-filter",
                            options=[
                                {"label": CityGroup, "value": CityGroup}
                                for CityGroup in range(1,49)
                            ],
                            value= "22",
                            clearable=True,
                            searchable=True,
                            className="dropdown",
                        ),
                    ],
                ),
            ],
            className="menu",
        ),
        html.Br(),
        html.Div(
                dash_table.DataTable(
                    id='table',
                    columns=[
                    #{'name': 'ID', 'id': 'ID'},
                    dict(name= 'Country', id= 'Country'),
                    dict(name= 'City', id= 'City'),
                    dict(name= 'Total CO2 Emissions (Metric T)', id= 'Total CO2 Emissions (Metric T)', type='numeric', format=Format().group(True)),
                    dict(name= 'Year', id= 'Year'),
                    dict(name= 'Transparency Score', id= 'Transparency Score'),
                    dict(name= 'Group', id= 'Group')],
                    data=df.to_dict('records'),
                    #filter_action='native',
                    #style_table={'width': '800px'},
                    style_cell={
                        'textAlign': 'right',
                        'font-size':15,
                        'font-family':'sans-serif'},
                    style_header={
                        'fontWeight':'bold'},
                    style_data={
                        #'width': '300px', 'minWidth': '257px', 'maxWidth': '300px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        },
                    style_as_list_view=True,    
                    page_size=20,
                    ),
            className ="container"
        ),
    ]
)



@app.callback(
    Output("table", "data"), 
    #Output("GDP_chart_figure", "figure"),
    Input("country-filter", "value"),
    Input("city-filter", "value"),
    Input("CityGroup-filter", "value"),
    Input("date-range", "value")
)

def filter_table(country,city, group, year):
    if group is None:
        if country is None:
            if city is None:
                if year is not None:
                    filtered_df = df[(df['Year']== int(year))]
                    return filtered_df.to_dict('rows')
                elif year is None:
                    filtered_df = df
                    return filtered_df.to_dict('rows')
            elif city is not None:
                if year is not None:
                    filtered_df = df[(df['City']== str(city)) & (df['Year']== int(year))]
                    return filtered_df.to_dict('rows')
                elif year is None:
                    filtered_df = df[(df['City']== str(city))]
                    return filtered_df.to_dict('rows')      

        if country is not None:
            if city is None:
                if year is not None:
                    filtered_df = df[(df['Country']== str(country)) & (df['Year']== int(year))]
                    return filtered_df.to_dict('rows')
                elif year is None:
                    filtered_df = df[df['Country']== str(country)]
                    return filtered_df.to_dict('rows')
            elif city is not None:
                if year is not None:
                    filtered_df = df[(df['Country']== str(country)) & (df['City']== str(city)) & (df['Year']== int(year))]
                    return filtered_df.to_dict('rows')
                elif year is None:
                    filtered_df = df[(df['Country']== str(country)) & (df['City']== str(city))]
                    return filtered_df.to_dict('rows')     
    if group is not None:
        if country is None:
            if city is None:
                if year is not None:
                    filtered_df = df[(df['Year']== int(year)) & (df['Group']== int(group))]
                    return filtered_df.to_dict('rows')
                elif year is None:
                    filtered_df = df[(df['Group']== int(group))]
                    return filtered_df.to_dict('rows')
            elif city is not None:
                if year is not None:
                    filtered_df = df[(df['City']== str(city)) & (df['Year']== int(year)) & (df['Group']== int(group))]
                    return filtered_df.to_dict('rows')
                elif year is None:
                    filtered_df = df[(df['City']== str(city)) & (df['Group']== int(group))]
                    return filtered_df.to_dict('rows')      
        if country is not None:
            if city is None:
                if year is not None:
                    filtered_df = df[(df['Country']== str(country)) & (df['Year']== int(year)) & (df['Group']== int(group))]
                    return filtered_df.to_dict('rows')
                elif year is None:
                    filtered_df = df[df['Country']== str(country) & (df['Group']== int(group))]
                    return filtered_df.to_dict('rows')
            elif city is not None:
                if year is not None:
                    filtered_df = df[(df['Country']== str(country)) & (df['City']== str(city)) & (df['Year']== int(year)) & (df['Group']== int(group))]
                    return filtered_df.to_dict('rows')
                elif year is None:
                    filtered_df = df[(df['Country']== str(country)) & (df['City']== str(city)) & (df['Group']== int(group))]
                    return filtered_df.to_dict('rows') 

if __name__ == "__main__":
    app.run_server(debug=True,host="127.0.0.1", port=8050)
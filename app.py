import os
import numpy as np
import pandas as pd
import logging

import dash
# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc, html

import plotly.graph_objs as go

from dash.dependencies import Input, Output
from IPython.display import display, IFrame, HTML

# turn off web logs
# os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = 'True'
logger = logging.getLogger('werkzeug')  # WSGI - web server gateway interface
logger.setLevel(logging.ERROR)

# adding __name__ fixes 'no css' issue
# app = dash.Dash(__name__, static_folder='assets/') # deprecated
app = dash.Dash(__name__, assets_folder='assets/')
server = app.server

# read the GDP csv
df = pd.read_csv('GDP-clean.csv')
df.set_index('Country Code', inplace=True)

insights_text = '''The histogram plot shows that in the 1900s, there are many 
        countries on both the lower and upper end of the GDP-per-capita 
        spectrum, which means that there is inequality. Fast forward to 2017, 
        most countries are in the middle of the spectrum. This is good news for 
        us because we are moving towards a fairer world.'''


def get_map_figure(year, colorstyle=0):
    '''Returns a map figure.

    Generates a map figure of all countries with their GDP per capita 
    as a determinant of the colors that will be used to represent those 
    countries. The map is that of the year that was passed as first parameter,  
    and the colorstyle used is based on the integer vlaue passed as second 
    paramater

    Parameters
    ----------
    year : int
        The year of the map.
    colorstyle : {0, 1}, optional
        The color style to be used. 0 is the default value and it uses the 
        colors ranging from red to purple. The value 1 just uses different
        hues of the color purple.

    Returns
    -------
    dict
        Return a map figure
    '''
    if colorstyle == 0:
        colorscale = [[0, "rgb(103, 11, 99)"], [0.66, "rgb(91, 11, 239)"],
                      [0.78, "rgb(11, 55, 239)"], [0.86, "rgb(11, 95, 239)"],
                      [0.92, "rgb(232, 239, 11)"], [0.96, "rgb(239, 209, 11)"],
                      [0.99, "rgb(239, 103, 11)"], [1, "rgb(239, 11, 11)"]]
    elif colorstyle == 1:
        colorscale = [[1-(1/10)*10**(1), "rgb(103, 11, 99)"],
                      [1-(1/10)*10**(4/5), "rgb(145,40,140)"],
                      [1-(1/10)*10**(3/5), "rgb(168,60,163)"],
                      [1-(1/10)*10**(2/5), "rgb(206,101,201)"],
                      [1-(1/10)*10**(1/5), "rgb(221,135,218)"],
                      [1, "rgb(232,185,230)"]]
        
    data = [dict(
        type='choropleth',
        locations=df.index,
        z=df[str(year)],
        text=df['Country Name'],
        colorscale=colorscale,
        autocolorscale=False,
        reversescale=True,
        marker=dict(
            line=dict(
                color='rgb(180,180,180)',
                width=0.9
            )),
        colorbar=dict(
            autotick=False,
            tickprefix='$',
            lenmode='fraction',
            len=0.8,
            thicknessmode='pixels',
            thickness=15,
            xanchor='right',
            y=0.5,
            x=0,
        ),

    )]

    layout = dict(
        title='GDP per capita ({})<br>Source:\
                <a href="http://databank.worldbank.org/data/\
                source/world-development-indicators#">\
                Worldbank</a>'.format(year),
        geo=dict(
            showframe=True,
            showcoastlines=False,
            projection=dict(
                type='Mercator'
            ),
            showocean=True,
            oceancolor='#0eb3ef',
        )
    )

    fig = dict(data=data, layout=layout)
    return fig


def create_slider(id, value):
    '''Create a slider component.

    Creates a slider component with an id and initial value of the two 
    parameters passed to this function.

    Parameters
    ----------
    id : int
        The id of the slider component.
    value : int
        Accepts a value ranging from 1961 to 2017. This is the initial value
        of the slider component.
        
    Returns
    -------
    dcc.Slider
        Return a slider component
    '''
    return dcc.Slider(
        id=id,
        min=1961,
        max=2017,
        step=1,
        value=value,
        marks={str(i*10): i*10 for i in range(197, 202)},
        className='year-slider'
    )

# resets the callbacks
app.callback_map = {} 
# sets the title
app.title = 'Global Inequality Visualization'
# html content
app.layout = html.Div([
    html.Div([
        html.H1(id='header', children='Global Inequality Visualization'),
        html.Div(id='sub-header',
                 children='by Jude Michael Teves, \
                     Master of Science in Data Science (2018)'),
        html.Br(),
        html.Div([
            html.Span(
                children='''The first of the Sustainable Development \
                    Goals (SDG) for the year 2030 is '''),
            html.Strong(children='''No Poverty'''),
            html.Span(children='''. Currently, the international poverty line
                threshold is '''),
            html.Strong(children='''US$1.9/day'''),
            html.Span(children='''. In the process of aiming to achieve SDG 1, 
                the gap between the rich 
                and the poor will gradually decrease, but with the recent 
                adverse events all around the world such as terrorism and 
                immigration ban, one might think that we are straying further 
                from the goal. But is it really the case? One way of measuring 
                this is by looking at a country's GDP per capita.

                Gross Domestic Product (GDP) measures the total output of a 
                country in a year and is a great indicator of a country's 
                performance, and GDP per capita is the GDP divided by the 
                population of a country. We can think of the GDP per capita as 
                an indicator of how well-off the citizens are in a country. A 
                higher GDP per capita means a higher income and standard of 
                living.'''),
        ], id="intro"),
    ], id='intro-section'),
    html.Div([
        dcc.Tabs([
            # Tab 1
            dcc.Tab([
                html.Div(id="graph-guide-text", className="tab-content top",
                         children='''The graphs are interactive. You can move 
                             the slider to show the GDP per capita for a given 
                             year. You can also click on a country to display 
                             the GDP per capita trends.'''),
                html.Div([
                    html.Div(id="year-slider-label",
                             className="year-slider-label", children="Year"),
                    create_slider('year-slider', 2017),
                    html.Div(id="year-slider-value",
                             className="year-slider-value")
                ], className="row justify-content-md-center \
                                align-items-center"),
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Graph(id="world-map", className="map")
                        ]),
                        html.Div(id='text-output')
                    ], className="col-left col-lg-7"),
                    html.Div([
                        dcc.Graph(id='country-gdp-graph')
                    ], className="col-right col-lg-5 v-center"),
                ], className="row align-items-center content-tab1")
            ], className="container-fluid", label="GDP per capita trend"),
            # Tab 2
            dcc.Tab([
                html.Div([
                    # Histogram
                    html.Div([
                        dcc.Graph(id="histogram")
                    ], className="col-left col-lg-8"),
                    html.Div(id="conclusion", className="col-right col-lg-4",
                             children=insights_text)
                ], className="row align-items-center tab-content \
                                top insights"),
                html.Div([
                    # Graph 1
                    html.Div([
                        html.Div([
                            html.Div(id="year-slider-label-2",
                                     className="year-slider-label",
                                     children="Year"),
                            create_slider('year-slider-2', 1961),
                            html.Div(id="year-slider-value-2",
                                     className="year-slider-value")
                        ], className="row justify-content-md-center \
                                        align-items-center"),
                        dcc.Graph(id="world-map-2", className="map")
                    ], className="col-left col-lg-6"),
                    # Graph 2
                    html.Div([
                        html.Div([
                            html.Div(id="year-slider-label-3",
                                     className="year-slider-label",
                                     children="Year"),
                            create_slider('year-slider-3', 2017),
                            html.Div(id="year-slider-value-3",
                                     className="year-slider-value")
                        ], className="row justify-content-md-center \
                                        align-items-center"),
                        dcc.Graph(id="world-map-3", className="map")
                    ], className="col-right col-lg-6"),

                ], className="row align-items-center tab-content")
            ], className="container-fluid",
                label="GDP per capita comparison across years")
        ], className="tabs-section")
    ], className="main-content"),
], className="main")


@app.callback(Output('world-map', 'figure'),
              [Input('year-slider', 'value')])
def update_map_1(year):
    '''Update the map in Tab 1 when slider in Tab 1 is used.

    A callback function that is triggered when the slider in Tab 1 is used.
    The function uses the slider value as input to the get_map_figure function
    and returns the generated map figure to the map in Tab 1.

    Parameters
    ----------
    year : int
        The year of the map.

    Returns
    -------
    dict
        Return a map figure
    '''
    return get_map_figure(year)


@app.callback(Output('world-map-2', 'figure'),
              [Input('year-slider-2', 'value')])
def update_map_2(year):
    '''Update the first map in Tab 2 when the first slider in Tab 2 is used.

    A callback function that is triggered when the first slider in Tab 2 is 
    used. The function uses the slider value as input to the 
    get_map_figure function and returns the generated map figure to the first 
    map in Tab 2.

    Parameters
    ----------
    year : int
        The year of the map.

    Returns
    -------
    dict
        Return a map figure
    '''
    return get_map_figure(year, 1)


@app.callback(Output('world-map-3', 'figure'),
              [Input('year-slider-3', 'value')])
def update_map_3(year):
    '''Update the second map in Tab 2 when the second slider in Tab 2 is used.

    A callback function that is triggered when the second slider in Tab 2 is 
    used. The function uses the slider value as input to the 
    get_map_figure function and returns the generated map figure to the second 
    map in Tab 2.

    Parameters
    ----------
    year : int
        The year of the map.

    Returns
    -------
    dict
        Return a map figure
    '''
    return get_map_figure(year, 1)


@app.callback(Output('year-slider-value', 'children'),
              [Input('year-slider', 'value')])
def update_year_value(year):
    '''Update the year label for the slider in Tab 1.

    A callback function that is triggered when the slider in Tab 1 is 
    used. The function uses the slider value to update the year label beside
    the slider component.

    Parameters
    ----------
    year : int
        The value of the slider.

    Returns
    -------
    str
        Return the updated year
    '''
    return str(year)


@app.callback(Output('year-slider-value-2', 'children'),
              [Input('year-slider-2', 'value')])
def update_year_value_2(year):
    '''Update the year label for the first slider in Tab 2.

    A callback function that is triggered when the first slider in Tab 2 is 
    used. The function uses the slider value to update the year label beside
    the slider component.

    Parameters
    ----------
    year : int
        The value of the slider.

    Returns
    -------
    str
        Return the updated year
    '''
    return str(year)


@app.callback(Output('year-slider-value-3', 'children'),
              [Input('year-slider-3', 'value')])
def update_year_value_3(year):
    '''Update the year label for the second slider in Tab 2.

    A callback function that is triggered when the second slider in Tab 2 is 
    used. The function uses the slider value to update the year label beside
    the slider component.

    Parameters
    ----------
    year : int
        The value of the slider.

    Returns
    -------
    str
        Return the updated year
    '''
    return str(year)


@app.callback(Output('histogram', 'figure'),
              [Input('year-slider-2', 'value'),
               Input('year-slider-3', 'value')])
def update_histogram(year1, year2):
    '''Update the histogram in Tab 2.

    A callback function that is triggered when any of the sliders in Tab 2 is 
    used. The function uses the sliders' values to generate an overlapped 
    histogram of the two years provided as input. The histogram shows the 
    distribution of countries with respect to the min-max scaled 
    log-transformed GDP per capita of the said countries for the two years
    provided.

    Parameters
    ----------
    year1 : int
        The value of the first slider.
    year2 : int
        The value of the second slider.

    Returns
    -------
    dict
        Return the updated histogram figure
    '''
    df1 = np.log(df[str(year1)].dropna())
    df2 = np.log(df[str(year2)].dropna())
    df1 = (df1-df1.min()) / (df1.max()-df1.min())
    df2 = (df2-df2.min()) / (df2.max()-df2.min())

    trace1 = go.Histogram(
        x=df1,
        opacity=0.5,
        autobinx=False,
        xbins=go.histogram.XBins(start=0, end=1, size=0.085),
        name=str(year1)
    )
    trace2 = go.Histogram(
        x=df2,
        opacity=0.5,
        autobinx=False,
        xbins=go.histogram.XBins(start=0, end=1, size=0.085),
        name=str(year2)
    )
    data = [trace2, trace1]

    layout = dict(title='GDP per capita histogram',
                  xaxis={'title': 'Min-Max-Scaled Log-Transformed GDP per capita'},
                  yaxis={'title': 'Number of countries'},
                  barmode='overlay'
                  )
    fig = dict(data=data, layout=layout)
    return fig


@app.callback(Output('country-gdp-graph', 'figure'),
              [Input('world-map', 'clickData')])
def update_graph(clickData):
    '''Update the GDP per capita trend graph in Tab 1.

    A callback function that is triggered when a country in the map in Tab 1 is 
    clicked. The country is retrieved from the clickData and is then used to 
    generate a line graph showing the trends in GDP per capita of a country
    across all years.

    Parameters
    ----------
    clickData : dict
        The dictionary containing the details of the clicked point on the map.

    Returns
    -------
    dict
        Return the updated GDP per capita trend graph figure
    '''
    title = ''
    data = []
    if clickData:
        country = clickData['points'][0]['location']
    else:
        country = 'PHL'
    data = [{'x': df.loc[:, '1961':].columns.tolist(),
             'y': df.loc[country, '1961':].values.tolist(),
             'type': 'line'}]
    title = df.loc[country, 'Country Name']
    layout = dict(title='{} GDP per capita'.format(title),
                  xaxis={'title': 'year'},
                  yaxis={'title': 'GDP per capita (USD)'}
                  )
    fig = dict(data=data, layout=layout)
    return fig


if __name__ == '__main__':
    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True
    # port = int(os.environ.get('PORT', 5000))
    # app.run_server(port=port, debug=True)
    app.run(debug=True)
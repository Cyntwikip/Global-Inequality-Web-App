from IPython.display import display, IFrame, HTML
import os
import numpy as np
import pandas as pd

import dash 
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from dash.dependencies import Input, Output, State, Event

# turn off web logs
import os
os.environ['FLASK_ENV'] = 'development'

import logging
logger = logging.getLogger('werkzeug') # WSGI - web server gateway interface
logger.setLevel(logging.ERROR)

# adding __name__ fixes no css
app = dash.Dash(__name__, static_folder='assets/')
server = app.server

df = pd.read_csv('GDP-clean.csv')
df.set_index('Country Code', inplace=True)

def update_map(year, colorstyle=0):
    if colorstyle == 0:
        colorscale = [[0,"rgb(103, 11, 99)"],[0.66,"rgb(91, 11, 239)"],
                      [0.78,"rgb(11, 55, 239)"],[0.86,"rgb(11, 95, 239)"],
                      [0.92,"rgb(232, 239, 11)"],[0.96,"rgb(239, 209, 11)"],
                      [0.99,"rgb(239, 103, 11)"],[1,"rgb(239, 11, 11)"]]
    elif colorstyle == 1:
        colorscale = [[1-(1/10)*10**(1),"rgb(103, 11, 99)"],
                      [1-(1/10)*10**(4/5),"rgb(145,40,140)"],
                      [1-(1/10)*10**(3/5),"rgb(168,60,163)"],
                      [1-(1/10)*10**(2/5),"rgb(206,101,201)"],
                      [1-(1/10)*10**(1/5),"rgb(221,135,218)"],
                      [1,"rgb(232,185,230)"],
                     ]
    data = [ dict(
        type = 'choropleth',
        locations = df.index,
        z = df[str(year)],
        text = df['Country Name'],
        # 0, 0.35, 0.5, 0.6, 0.7, 1
        colorscale = colorscale,
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.9
            ) ),
        colorbar = dict(
            autotick = False,
            tickprefix = '$',
            #title = 'USD'
            lenmode = 'fraction',
            len = 0.8,
            thicknessmode = 'pixels',
            thickness = 15,
            #outlinewidth = 5,
            xanchor = 'right',
            y = 0.5,
            x = 0,
            #tickangle = 90,
            #xpad = 0,
            #ypad = 10,
        ),
            
      ) ]

    layout = dict(
        title = 'GDP per capita ({})<br>Source:\
                <a href="http://databank.worldbank.org/data/source/world-development-indicators#">\
                Worldbank</a>'.format(year),
        geo = dict(
            showframe = True,
            showcoastlines = False,
            projection = dict(
                type = 'Mercator'
            ),
            showocean = True,
            oceancolor = '#0eb3ef',
        )
    )

    fig = dict( data=data, layout=layout )
    return fig

def create_slider(id, value):
    return dcc.Slider(
        id=id,
        min=1961,
        max=2017,
        step=1,
        value=value,
        marks={str(i*10):i*10 for i in range(197, 202)},
        className='year-slider'
    )

app.callback_map = {} # resets the callbacks

app.title = 'Global Inequality Visualization'

app.layout = html.Div([
    html.Div([
        html.H1(id='header', children='Global Inequality Visualization'),
        html.Div(id='sub-header', children='by Jude Michael Teves, Master of Science in Data Science'),
        html.Br(),
        html.Div([
            html.Span(children='''The first of the Sustainable Development Goals for the year 2030 is '''),
            html.Strong(children='''No Poverty'''),
            html.Span(children='''. In the process, the gap between the rich and the poor will gradually decrease,
            but with the recent adverse events all around the world such 
            as terrorism and immigration ban, one might think that we are straying further from the goal. 
            But is it really the case? One way of measuring this is by looking at a country's GDP per capita.

            Gross Domestic Product (GDP) measures the total output of a country in a year 
            and is a great indicator of a country's performance, and GDP per capita 
            is the GDP divided by the population of a country. We can think of the GDP per capita 
            as an indicator of how well-off the citizens are in a country. A higher GDP per capita means 
            a higher income and standard of living.'''),
        ], id="intro"),
    ], id='intro-section'),
    html.Div([
        dcc.Tabs([
            # Tab 1
            dcc.Tab([
                html.Div([
                    html.Div(id="year-slider-label", className="year-slider-label", children="Year"),
                    create_slider('year-slider', 2017),  
                    html.Div(id="year-slider-value", className="year-slider-value")
                ], className="row justify-content-md-center align-items-center"),
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
                ], className="row align-items-center tab-content top")
            ], className="container-fluid", label="GDP per capita trend"),
            # Tab 2
            dcc.Tab([
                html.Div([
                    # Histogram
                    dcc.Graph(id="histogram"),
                ], className="row align-items-center tab-content top"),
                html.Div([
                    # Graph 1
                    html.Div([
                        html.Div([
                            html.Div(id="year-slider-label-2", className="year-slider-label", children="Year"),
                            create_slider('year-slider-2', 1961), 
                            html.Div(id="year-slider-value-2", className="year-slider-value")
                        ], className="row justify-content-md-center align-items-center"),
                        dcc.Graph(id="world-map-2", className="map")
                    ], className="col-left col-lg-6"),
                    # Graph 2
                    html.Div([
                        html.Div([
                            html.Div(id="year-slider-label-3", className="year-slider-label", children="Year"),
                            create_slider('year-slider-3', 2017), 
                            html.Div(id="year-slider-value-3", className="year-slider-value")
                        ], className="row justify-content-md-center align-items-center"),
                        dcc.Graph(id="world-map-3", className="map")
                    ], className="col-right col-lg-6"),
                    
                ], className="row align-items-center tab-content")
            ], className="container-fluid", label="GDP per capita comparison across years")
        ], className="tabs-section")
    ], className="main-content"),
    html.Div(id="conclusion",
        children='''The histogram plot shows that in the 1900s, there are many countries on both 
        the lower and upper end of the GDP-per-capita spectrum, which means that there is inequality. 
        Fast forward to 2017, most countries are in the middle of the spectrum. This is good news for 
        us because we are moving towards a fairer world.'''
    )
], className="main")

@app.callback(Output('world-map', 'figure'), 
              [Input('year-slider', 'value')])
def update_map_1(year):
    return update_map(year)


@app.callback(Output('world-map-2', 'figure'), 
              [Input('year-slider-2', 'value')])
def update_map_2(year):
    return update_map(year,1)


@app.callback(Output('world-map-3', 'figure'), 
              [Input('year-slider-3', 'value')])
def update_map_3(year):
    return update_map(year,1)


@app.callback(Output('year-slider-value', 'children'), 
              [Input('year-slider', 'value')])
def update_year_value(year):
    return str(year)

@app.callback(Output('year-slider-value-2', 'children'), 
              [Input('year-slider-2', 'value')])
def update_year_value_2(year):
    return str(year)

@app.callback(Output('year-slider-value-3', 'children'), 
              [Input('year-slider-3', 'value')])
def update_year_value_3(year):
    return str(year)

@app.callback(Output('histogram', 'figure'), 
              [Input('year-slider-2', 'value'), Input('year-slider-3', 'value')])
def update_histogram(year1, year2):
    df1 = np.log(df[str(year1)].dropna())
    df2 = np.log(df[str(year2)].dropna())
    df1 = (df1-df1.min()) / (df1.max()-df1.min())
    df2 = (df2-df2.min()) / (df2.max()-df2.min())
    
    trace1 = go.Histogram(
        x=df1,
        opacity=0.5,
        autobinx = False,
        xbins = go.histogram.XBins(size=20),
        name = str(year1)
    )
    trace2 = go.Histogram(
        x=df2,
        opacity=0.5,
        autobinx = False,
        xbins = go.histogram.XBins(size=20),
        name = str(year2)
    )
    data = [trace1, trace2]
    
#     # Group data together
#     hist_data = [x1, x2, x3, x4]

#     group_labels = ['Group 1', 'Group 2', 'Group 3', 'Group 4']

#     # Create distplot with custom bin_size
#     fig = ff.create_distplot(hist_data, group_labels, bin_size=[.1, .25, .5, 1])

    layout = dict(title = 'GDP per capita histogram', 
                  xaxis = {'title': 'Min-Max-Scaled Log-Transformed GDP per capita'},
                  yaxis = {'title': 'Counts'},
                  barmode = 'overlay',
                  #paper_bgcolor = '#F4F4F8',
                  #plot_bgcolor = '#F4F4F8',
                 )
    fig = dict(data=data, layout=layout)
    return fig

@app.callback(Output('country-gdp-graph', 'figure'), 
              [Input('world-map', 'clickData')])
def update_graph(clickData):
    title = ''
    data = []
    if clickData:
        country = clickData['points'][0]['location']
        data = [{'x': df.loc[:,'1961':].columns.tolist(), 
                 'y': df.loc[country, '1961':].values.tolist(), 
                 'type': 'line'}]
        title = df.loc[country,'Country Name']
    layout = dict(title = '{} GDP per capita'.format(title), 
                  xaxis = {'title': 'year'},
                  yaxis = {'title': 'GDP per capita (USD)'},
                  #paper_bgcolor = '#F4F4F8',
                  #plot_bgcolor = '#F4F4F8',
                 )
    fig = dict(data=data, layout=layout)
    return fig


# show_app(app)

# def show_app(app, port=9998, width=900, height=700):
#     host = 'localhost'
#     url = f'http://{host}:{port}'
    
#     display(HTML(f"<a href='{url}' target='_blank'>Open in a new tab</a>"))
#     display(IFrame(url, width=width, height=height))
    
#     app.css.config.serve_locally = True
#     app.scripts.config.serve_locally = True
    
#     return app.run_server(debug=False, host=host, port=port)

if __name__ == '__main__':
    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True
    port = int(os.environ.get('PORT', 5000))
    app.run_server(port=port,debug=True)



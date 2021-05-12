'import required libraries'
#dash components
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Row import Row
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
#user defined classes
from utils.charts import Charts
from utils.charts_helper import ChartHelper
#temp
import pandas as pd

#get data
df_perf = ChartHelper.get_data('performance')
df_earn = ChartHelper.get_data('earnings')
df_account = ChartHelper.get_data('accounts')
df_ratio = ChartHelper.get_data('ratios')
df_forecast = ChartHelper.get_data('forecast')

#Initialise the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])

server = app.server

#Initialise global variable
prev_val = 0
#prev_val = 0

#set the layout
app.layout = dbc.Container([
    
    #Main Row
    dbc.Row([
        
        #Left Column
        dbc.Col([
            
            #DashBoard Heading
            dbc.Row([
                
                #heading logo
                dbc.Col([
                    html.Img(
                        src=app.get_asset_url('doughnut.svg'),
                        height='56px',
                        className='mt-5'
                    )
                ], sm=4, lg=3, md=3),
                #end of heading logo
                
                #heading text
                dbc.Col([
                    html.H2('STOCK DASHBOARD', className='mt-5 ml-1 font-weight-light text-secondary')
                ], sm=6, lg=9, md=9)
                #end of heading text
                
            ], id="heading"),
            #End of Dashboard heading
            
            #Stock Price
            dbc.Row([
                dbc.Col([
                    dbc.Row(id = 'stock-header', children=[
                        
                ]),
                dbc.Row(id='stock-val', children=[
                    
                ])
                ]),
                dcc.Interval(
                    id='interval-component',
                    interval=5*1000, # in milliseconds
                    n_intervals=0
                )
            ]),
            #End of Stock Price
            
            
            #Company Filter
            dbc.Row([
                
                #label
                dbc.Row([
                    dbc.Col([
                        html.Img(src=app.get_asset_url('company.svg'),
                        height='20px', className='ml-5')
                    ], md=3, sm=3, lg=3),
                    dbc.Col([
                        html.H6('COMPANY NAME', className='text-secondary ml-3 font-weight-light mt-1')
                    ], md=9, sm=9, lg=9)
                ], className='mt-3'),
                #End of label
                #DropDown
                dbc.Row([
                    dcc.Dropdown(
                        id = 'comp-dropdown',
                        options=[
                            {'label': 'Microsoft', 'value': 0},
                            {'label': 'Tesla', 'value': 1},
                            {'label': 'Amazon', 'value': 2},
                            {'label': 'Apple', 'value': 3},
                            {'label': 'Google', 'value': 4}
                        ],
                        value=0,
                        searchable=False,
                        clearable=False
                    )
                ], className='mx-auto')
                #End of DropDown
            ], className='mt-4'),
            #End of Company Filter
            
            #Revenue Filter
            dbc.Row([
                #label
                dbc.Row([
                    dbc.Col([
                        html.Img(src=app.get_asset_url('calendar.svg'),
                        height='18px', className='ml-4 mt-1')
                    ], md=1, sm=1, lg=1),
                    dbc.Col([
                        html.H6('REVENUE & EARNINGS YEAR', className='text-secondary ml-3 font-weight-light mt-1 mr-4 text-center')
                    ], md=10, sm=10, lg=10)
                ], className='mt-4'),
                #End of label
                #DropDown
                dbc.Row([
                    dcc.Dropdown(
                        id = 'earn-dropdown',
                        options=[
                            {'label':y, 'value':y} for y in df_earn.Year.unique().tolist()
                        ],
                        value=df_earn.Year.unique().tolist(),
                        searchable=False,
                        clearable=False,
                        multi=True
                    )
                ], className='mx-auto')
                #End of DropDown
            ], className='mt-4'),
            #End of Revenue Filter
            
            #Account Slider
            dbc.Row([
                #label
                dbc.Row([
                    dbc.Col([
                        html.Img(src=app.get_asset_url('calendar.svg'),
                        height='18px', className='ml-4 mt-2')
                    ], md=1, sm=1, lg=1),
                    dbc.Col([
                        html.H6(
                            'ACCOUNTS RECEIVEABLE/PAYABLE', 
                            className='text-secondary ml-3 font-weight-light mt-1 mr-3 text-center',
                            id='slider-label')
                    ], md=10, sm=10, lg=10)
                ], className='mt-4'),
                #End of label
                #DropDown
                dbc.Row([

                    dcc.Slider(
                        id="slider",
                        min=pd.to_datetime(df_account.Date).dt.year.min(),
                        max=pd.to_datetime(df_account.Date).dt.year.max(),
                        step=1,
                        marks={
                            y:str(y) for y in pd.to_datetime(df_account.Date).dt.year.unique().tolist()
                        },
                        value=pd.to_datetime(df_account.Date).dt.year.max(),
                        updatemode='drag',
                        )
                
                ], className='mx-auto')
                #End of DropDown
            ], className='mt-4')
            #End of Account Slider
            
        ],
        sm=8, md=2, lg=2,
        id="left-col"),
        #End of Left Column
        
        #Middle Columns
        dbc.Col([
            
            #Balance Sheet Chart
            dbc.Row(
                dbc.Card([
                    dcc.Graph(
                        id='balance-sheet'
                    )
                ])
            ),
            #End of Balance Sheet Chart
            
            #Dual Charts
            dbc.Row([
                
                #Earnings Chart
                dbc.Col([
                    dbc.Card(id = "earnings-card", children=[
                        dcc.Graph(
                            id = "earnings"
                        )
                    ],className='mt-2 ml-n3')
                ], md=6, lg=6, sm=6),
                #End of Earnings Chart
                
                #Accounts Chart
                dbc.Col([
                    dbc.Card(id = "accounts-card", children=[
                        dcc.Graph(
                            id = "accounts"
                        )
                    ],className='mt-2 ml-3')
                ], md=5, lg=5, sm=5),
                #End of Accounts Chart
            ]),
            #End of dual Charts
            
            #Forecast Chart
            dbc.Row([
                dbc.Card([
                    dcc.Graph(
                        id='forecast'
                    )
                ], className='mt-2')
            ])
            #End of Forecast Chart
            
            
        ], md=5, sm=8, lg=5),
        #end of middle column
        
        #Right Column
        dbc.Col([
            
            #Candle Plot
            dbc.Row([
                dbc.Card([
                    dcc.Graph(
                        id='candle'
                    )
                ], className='ml-2')
            ]),
            #End of Candle Plot
            
            #Percent Change
            dbc.Row([
                dbc.Card([
                    dcc.Graph(
                        id="pct-change"
                    )
                ], className='mt-2 ml-2')
            ])
            #End of Percent Change
            
            
        ],md=5, sm=8, lg=5)
        #End of right Column

    ])
    #End of Main Row
    
],fluid=True, id="container")

'Call back for Interval Updates'
@app.callback(
Output('stock-val', 'children'),
Output('stock-header', 'children'),
Input('interval-component', 'n_intervals'),
Input('comp-dropdown', 'value'))

def current_price(n, company):
    global prev_val
    curr = ChartHelper.get_current_price(company)
    symbol = ChartHelper.get_symbol(company)
    header = symbol + ' CURRENT PRICE'
    if curr > prev_val :
        prev_val = curr
        return html.H2(prev_val, className='text-success font-weight-bold mx-auto'), html.H6(header, className='text-secondary mx-auto font-weight-light mt-5')
    else:
        prev_val = curr
        return html.H2(prev_val, className='text-danger font-weight-bold mx-auto'), html.H6(header, className='text-secondary mx-auto font-weight-light mt-5')
    

'Call Back for Balance Sheet'
@app.callback(
Output('balance-sheet', 'figure'),
Input('comp-dropdown', 'value'))

def balance_sheet(company):
    df = df_ratio[df_ratio['Company'] == company]
    fig = Charts.get_bal_sheet_chart(df)
    
    return fig

'Call Back for Earnings'
@app.callback(
Output('earnings', 'figure'),
Input('comp-dropdown', 'value'),
Input('earn-dropdown', 'value'))

def earnings(company, year):
    df = df_earn[df_earn['Company'] == company]
    df = df[df['Year'].isin(year)]
    #get the figure
    fig = Charts.get_earnings_chart(df)
    
    return fig

'Call Back for Accounts'
@app.callback(
Output('accounts', 'figure'),
Input('comp-dropdown', 'value'),
Input('slider', 'value'))

def accounts(company, year):
    df = df_account[df_account['Company'] == company]
    #filter year
    df = df[pd.to_datetime(df.Date).dt.year == year]
    #get the figure
    fig = Charts.get_accounts_chart(df)
    
    return fig

'Call Back for Candle Plot'
@app.callback(
Output('candle', 'figure'),
Input('comp-dropdown', 'value'))

def candle_plot(company):
    df = df_perf[df_perf['Company'] == company]
    fig = Charts.get_candle_plot(df)
    
    return fig

'Call Back for Percent Change'
@app.callback(
Output('pct-change', 'figure'),
Input('comp-dropdown', 'value'))

def pct_change(company):
    df = df_perf[df_perf['Company'] == company]
    fig = Charts.get_pct_change_chart(df)
    
    return fig


'Call Back for Forecast'
@app.callback(
Output('forecast', 'figure'),
Input('comp-dropdown', 'value'))

def forecast(company):
    df = df_forecast[df_forecast['Company'] == company]
    fig = Charts.get_forecast_chart(df)
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

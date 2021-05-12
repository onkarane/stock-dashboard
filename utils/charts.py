'import the required libraries'
import plotly.graph_objects as go

class Charts:
    
    """
    The class contains helper functions to generate
    charts required for the dashboard.
    """

    def get_bal_sheet_chart(df):
        """
        Function to generate line chart for 
        several ratios of the balance sheet variables.

        Args:
            df (pandas dataframe): dataframe with balance sheet data
        
        Returns:
            fig(plotly chart): plotly line chart 
        """
        
        #generate figure
        fig = go.Figure()
        #add traces to the figure
        #cash ratio
        fig.add_trace(go.Scatter(
            x = df['Date'],
            y=df['CashRatio'],
            mode='lines+markers',
            name='Cash Ratio',
            line=dict(color="#82f2f2")
        ))
        #Quick ratio
        fig.add_trace(go.Scatter(
            x = df['Date'],
            y=df['QuickRatio'],
            mode='lines+markers',
            name='Quick Ratio',
            line=dict(color="#6295f8")
        ))
        #current ratio
        fig.add_trace(go.Scatter(
            x = df['Date'],
            y=df['CurrRatio'],
            mode='lines+markers',
            name='Current Ratio',
            line=dict(color="#6c63ff")
        ))
        #long term debt ratio
        fig.add_trace(go.Scatter(
            x = df['Date'],
            y=df['LongTermDebtRatio'],
            mode='lines+markers',
            name='Long Term Debt Ratio',
            line=dict(color="#67d1ff")
        ))
        
        #update figure layout
        fig.update_layout(
            template = 'plotly_dark',
            title_font_size = 11,
            margin=dict(l=20, r=5, t=5, b=10),
            legend = dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=1,
                font = dict(size = 8)
            ),
            title = dict(
                text = 'BALANCE SHEET ANALYSIS',
                y = 0.96,
                x = 0.15,
                xanchor = 'center',
                yanchor = 'top'
            ),
            transition={
                'duration': 400,
                'easing': 'cubic-in-out'
            }
        )
        
        #update the axes
        fig.update_xaxes(tickfont_size=10, title_font_size = 12, showgrid=False)
        fig.update_yaxes(tickfont_size=10)
        
        return fig
    
    
    def get_earnings_chart(df):
        """
        Function to generate grouped bar chart for the
        company earnings and revenues. 

        Args:
            df (pandas dataframe): pandas dataframe with earnings and revenues
            for the company
        
        Returns:
            fig(plotly chart): plotly grouped bar chart 
        """
        
        #generate the figure
        fig = go.Figure(data = [
            go.Bar(name='Revenue', x=df['Year'], y=df['Revenue'], marker_color ="#165BAA"),
            go.Bar(name='Earnings', x=df['Year'], y=df['Earnings'], marker_color="#67d1ff")
        ])
        
        #update layout
        fig.update_layout(
            template = 'plotly_dark',
            title_font_size = 10,
            margin=dict(l=25, r=0, t=20, b=10),
            legend = dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=1,
                font = dict(size = 8)
            ),
            title = dict(
                text = 'REVENUE & EARNINGS',
                y = 0.96,
                x = 0.2,
                xanchor = 'center',
                yanchor = 'top'
            ),
            barmode='group'
        )
        
        #update the axes
        fig.update_xaxes(tickfont_size=8, showgrid=False)
        fig.update_yaxes(tickfont_size=8)
        
        return fig
    
    
    def get_accounts_chart(df):
        """
        Function to generate pie chart for the accounts 
        receiveable and accounts payable for given year.

        Args:
            df (pandas dataframe): pandas dataframe with accounts 
            receiveable and accounts payable information.
        
        Returns:
            fig(plotly chart): plotly pie chart 
        """
        #get the values
        values = df[['AccReceivables', 'AccPayable']].values.tolist()[0]
        labels = ['Accounts Receivable', 'Accounts Payable']
        #set the colors
        mark_colors = ['#165BAA', '#67d1ff']
        
        #plot the figure
        fig = go.Figure(data=[
            go.Pie(labels=labels, values=values, hole=.5, marker_colors = mark_colors)
        ])
        
        #update layout
        fig.update_layout(
            template = 'plotly_dark',
            title_font_size = 9,
            margin=dict(l=10, r=5, t=55, b=10),
            legend = dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=0.9,
                font = dict(size =7)
            ),
            title = dict(
                text = 'ACCOUNTS PAYABLE & ACCOUNTS RECEIVEABLE',
                y = 0.97,
                x = 0.5,
                xanchor = 'center',
                yanchor = 'top'
            )
        )
        
        return fig
    
    
    def get_forecast_chart(df):
        """
        Function to generate area plot for the forecast area
        chart for next three months.

        Args:
            df (pandas dataframe): dataframe with forecast data
            
        Returns:
            fig(plotly chart): plotly area chart 
        """
        #set the figure
        fig = go.Figure()
        #add trace
        fig.add_trace(go.Scatter(
            x=df['Date'], 
            y=df['Close'], 
            fill='tonexty', 
            fillcolor='rgba(0, 95, 190, 0.7)', 
            name = 'Forecast',mode='none'
        ))
        
        #update layout
        fig.update_layout(
            template = 'plotly_dark',
            title_font_size = 12,
            margin=dict(l=20, r=0, t=30, b=10),
            legend = dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=1,
                font = dict(size = 8)
            ),
            title = dict(
                text = 'FORECAST FOR NEXT 3 MONTHS',
                y = 0.95,
                x = 0.5,
                xanchor = 'center',
                yanchor = 'top'
            )
        )
        
        #update axes
        fig.update_xaxes(tickfont_size=12)
        fig.update_yaxes(tickfont_size=12)
        
        return fig
    
    
    def get_candle_plot(df):
        """
        Function to generate candle plot of the 
        stock performance.

        Args:
            df (pandas dataframe): pandas dataframe with stock open, close,
            high, low prices.
            
        Returns:
            fig(plotly chart): plotly candle chart 
        """
        #generate the figure
        fig = go.Figure(data=[
            go.Candlestick(
                x=df['Date'], 
                open=df['Open'], 
                high = df['High'], 
                low = df['Low'], 
                close = df['Close'],
                increasing_line_color= '#165BAA', 
                decreasing_line_color= '#e13ad6'
            )
        ])
        
        #remove weekends
        fig.update_xaxes(
        rangebreaks=[
            dict(bounds=["fri", "mon"]),
            #dict(values=["2015-12-25", "2016-01-01"])
        ])
        
        #updated layout
        fig.update_layout(
            template = 'plotly_dark',
            title_font_size = 13,
            margin=dict(l=20, r=10, t=30, b=10),
            legend = dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=1,
                font = dict(size = 8)
            ),
            title = dict(
                text = 'STOCK PERFORMANCE',
                y = 0.98,
                x = 0.5,
                xanchor = 'center',
                yanchor = 'top'
            ),
            transition={
                'duration': 400
            }
        )
        
        #update axes
        fig.update_xaxes(tickfont_size=12, rangeslider_visible=False)
        fig.update_yaxes(tickfont_size=12)
        
        return fig
    
    
    def get_pct_change_chart(df):
        """
        Function to generate price percent change bar graph
        
        Args:
            df (pandas dataframe): pandas dataframe with percent change
            data graph.
            
        Returns:
            fig(plotly chart): plotly bar chart 
        """
        
        #add plot color based on percent change
        df['color'] = df['pct_change'].apply(lambda x: '#165BAA' if x > 0 else '#e13ad6')
        
        #generate figure
        fig = go.Figure(
            go.Bar(x = df['Date'], y = df['pct_change'], marker_color=df['color'])
        )
        #hide weekends and holidays
        fig.update_xaxes(
        rangebreaks=[
            dict(bounds=["fri", "mon"]),
            #dict(values=["2015-12-25", "2016-01-01"])
        ])
        
        #update layout
        fig.update_layout(
            template = 'plotly_dark',
            title_font_size = 14,
            margin=dict(l=20, r=5, t=20, b=10),
            legend = dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=1,
                font = dict(size = 8)
            ),
            title = dict(
                text = 'PRICE CHANGE (%)',
                y = 0.95,
                x = 0.5,
                xanchor = 'center',
                yanchor = 'top'
            ),
            transition={
                'duration': 400
            }
        )
        
        #update axes
        fig.update_xaxes(tickfont_size=12)
        fig.update_yaxes(tickfont_size=12)
        
        return fig
    
    

        

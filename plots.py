import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from weather_data import *

class ClimatePlots:

    def __init__(self):
        self.connc = sqlite3.connect('global_warming.sqlite', check_same_thread=False)
                
        self.tc_cursor = (self.connc.cursor()).execute('select * from Temperature')
        self.cd_cursor = (self.connc.cursor()).execute('select * from Carbon_dioxide')
        self.mt_cursor = (self.connc.cursor()).execute('select * from Methane')
        self.no_cursor = (self.connc.cursor()).execute('select * from Nitrous_oxide')
        self.pi_cursor = (self.connc.cursor()).execute('select * from Polar_ice')

    def temp_change(self):
        """Temperature change figure."""

        tc_data = self.tc_cursor.fetchall()
        data = []

        for i in tc_data:

            year = i[0]
            station = i[1]

            month = str(year)[5:]

            if month == '04':
                month = '01'

            elif month == '13':
                month = '02'

            elif month == '21':
                month = '03'

            elif month == '29':
                month = '04'

            elif month == '38':
                month = '05'

            elif month == '46':
                month = '06'

            elif month == '54':
                month = '07'

            elif month == '63':
                month = '08'

            elif month == '71':
                month = '09'

            elif month == '79':
                month = '10'

            elif month == '88':
                month = '11'

            elif month == '96':
                month = '12'

            datestr  = str(year[:4]) + '-' + str(month)
            datap = (datestr, station)
            data.append(datap)

        column1, column2 = [], []

        for i in data:
            column1.append(i[0])
            column2.append(float(i[1]))

        df_tc = pd.DataFrame(list(zip(column1, column2)), columns=['time', 'station'])

        fig_tc = px.line(df_tc, x='time', y='station', title='Global Mean Surface Temperature Change', template='plotly_dark')
        fig_tc.update_traces(line=dict(color='white', width=2))
        fig_tc.update_layout(xaxis_title='Date', yaxis_title='Temperature Change (\u00B0C)')
        fig_tc.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        fig_tc.update_layout(yaxis=dict(tickmode='linear', tick0=-2, dtick=0.5))
        fig_tc.update_layout(margin_autoexpand=True)

        return fig_tc

    def carbon_dioxide(self):
        """Carbon dioxide figure."""

        cd_data = self.cd_cursor.fetchall()
        data = []

        for i in cd_data:
            year = i[0]

            if len(i[1]) == 1:
                month = str("0" + i[1])
            else:
                month = i[1]

            if len(i[2]) == 1:
                day = str("0" + i[2])
            else:
                day = i[2]

            datestr = str(year + "-" + month + "-" + day)
            datap = (datestr, i[4])
            data.append(datap)

        column1, column2 = [], []

        for i in data:
            column1.append(i[0])
            column2.append(float(i[1]))

        df_cd = pd.DataFrame(list(zip(column1, column2)), columns=['date', 'trend'])

        fig_cd = px.line(df_cd, x='date', y='trend', title='Atmospheric CO2 Levels',  template='plotly_dark')
        fig_cd.update_traces(line=dict(color='white', width=2))
        fig_cd.update_layout(xaxis_title='Date', yaxis_title='Carbon Dioxide (ppm)', autosize=True) # autosize=True
        fig_cd.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        fig_cd.update_layout(yaxis=dict(tickmode='linear', tick0=390.0, dtick=5))

        return fig_cd

    def methane(self):
        """Methane figure."""

        mt_data = self.mt_cursor.fetchall()
        data = []

        for i in mt_data:

            year = i[0]

            if len(i[1]) == 1:
                month = str("0" + i[1])
            else:
                month = i[1]

            datestr = str(year) + "-" + str(month)
            datap = (datestr, i[3])
            data.append(datap)

        column1, column2 = [], []

        for i in data:
            column1.append(i[0])
            column2.append(float(i[1]))

        df_mt = pd.DataFrame(list(zip(column1, column2)), columns=['date', 'average'])

        fig_mt = px.line(df_mt, x='date', y='average', title='Atmospheric Methane Levels', template='plotly_dark')
        fig_mt.update_traces(line=dict(color='white', width=2.5))
        fig_mt.update_layout(xaxis_title='Date', yaxis_title='Methane (ppm)')
        fig_mt.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        fig_mt.update_layout(yaxis=dict(tickmode='linear', tick0=1600.0, dtick=50))

        return fig_mt

    def nitrous_oxide(self):
        """Nitrous oxide figure."""

        no_data = self.no_cursor.fetchall()
        data = []
        
        for i in no_data:
            year = i[0]

            if len(i[1]) == 1:
                month = str("0" + i[1])
            else:
                month = i[1]

            datestr = str(year + "-" + month)
            datap = (datestr, i[3])
            data.append(datap)

        column1, column2 = [], []

        for i in data:
            column1.append(i[0])
            column2.append(float(i[1]))

        df_no = pd.DataFrame(list(zip(column1, column2)), columns=['date', 'average'])

        fig_no = px.line(df_no, x='date', y='average', title='Atmospheric Nitrous Oxide Levels', template='plotly_dark')
        fig_no.update_traces(line=dict(color='white', width=2))
        fig_no.update_layout(xaxis_title='Date', yaxis_title='Nitrous Oxide (ppm)')
        fig_no.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        fig_no.update_layout(yaxis=dict(tickmode='linear', tick0=310, dtick=5))

        return fig_no
    
    def polar_ice(self):
        """Polar ice figure."""

        pi_data = self.pi_cursor.fetchall()
        data = []

        for i in pi_data:

            year = i[1]
            extent = i[5]

            datap = (year, extent)
            data.append(datap)

        column1, column2 = [], []

        for i in data:
            column1.append(i[0])
            column2.append(float(i[1]))

        df_pi = pd.DataFrame(list(zip(column1, column2)), columns=['year', 'extent'])

        fig_pi = px.line(df_pi, x='year', y='extent', title='Annual Average Arctic Sea Ice', template='plotly_dark')
        fig_pi.update_traces(line=dict(color='white', width=2.5))
        fig_pi.update_layout(xaxis_title='Year', yaxis_title='Polar Ice Extent')
        fig_pi.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        fig_pi.update_layout(yaxis=dict(tickmode='linear', tick0=3, dtick=0.5))

        return fig_pi

class WeatherPlots:

    def weather_data(self, user_input):
        """Sort weather data from SQL database into pandas dataframe."""

        # Restructure below
        connw = sqlite3.connect('latest_weather.db', check_same_thread=False)
        query = pd.read_sql_query('''SELECT * FROM Weather''', connw)
        df_loc = WeatherData.locations()
        db_w = WeatherData.create_db(df_loc)
        db_w = WeatherData.get_weather(user_input, df_loc, db_w)

        # Manipulate data
        df = pd.DataFrame(query, columns = [
                                'city', 'country', 
                                'latitude', 'longitude', 
                                'temp_c', 'temp_f',
                                'precip_mm', 'precip_in',
                                'wind_mph', 'wind_kph', 
                                'wind_degree', 'wind_dir',
                                'gust_mph', 'gust_kph', 
                                'humidity', 
                                'cloud', 
                                'feelslike_c', 'feelslike_f',
                                'uv',
                                'condition.text',
                                'last_updated'])

        # Remove any null data
        df = df[df['temp_c'].astype(str) != 'nan']
    
        # Create column for wind direction markers
        df['symbol'] = ['triangle-up' if x=='N' 
                    else 'triangle-down' if x=='S' 
                    else 'triangle-left' if x=='W' 
                    else 'triangle-right' if x=='E' 
                    else 'triangle-ne' if x=='NE' or x=='NNE' or x=='ENE'
                    else 'triangle-se' if x=='SE' or x=='SSE' or x=='ESE'
                    else 'triangle-sw' if x=='SW' or x=='SSW' or x=='WSW'
                    else 'triangle-nw' 
                    for x in df['wind_dir']]

        def weather_data_averages(df):
            """Create a dataframe for the average weather in each country."""

            df_avg = pd.DataFrame()

            # Merge UK countries
            df['country'] = df['country'].replace(['ENGLAND', 'WALES', 'SCOTLAND', 'NORTHERN IRELAND', 'GUERNSEY ISLD.'], 'UK')

            # Compute averages
            df_avg['temp_c'] = pd.DataFrame(df.groupby(['country'])['temp_c'].mean().astype(float).round(1))
            df_avg['temp_f'] = pd.DataFrame(df.groupby(['country'])['temp_f'].mean().astype(float).round(1))
            df_avg['feelslike_c'] = pd.DataFrame(df.groupby(['country'])['temp_c'].mean().astype(float).round(1))
            df_avg['feelslike_f'] = pd.DataFrame(df.groupby(['country'])['temp_f'].mean().astype(float).round(1))
            df_avg['wind_mph'] = pd.DataFrame(df.groupby(['country'])['wind_mph'].mean().astype(float).round(1))
            df_avg['wind_kph'] = pd.DataFrame(df.groupby(['country'])['wind_kph'].mean().astype(float).round(1))
            df_avg['wind_dir'] = pd.DataFrame(df.groupby(['country'])['wind_dir'].agg(pd.Series.mode))
            df_avg['gust_mph'] = pd.DataFrame(df.groupby(['country'])['gust_mph'].mean().astype(float).round(1))
            df_avg['gust_kph'] = pd.DataFrame(df.groupby(['country'])['gust_kph'].mean().astype(float).round(1))
            df_avg['precip_mm'] = pd.DataFrame(df.groupby(['country'])['precip_mm'].mean().astype(float).round(1))
            df_avg['precip_in'] = pd.DataFrame(df.groupby(['country'])['precip_in'].mean().astype(float).round(1))
            df_avg['humidity'] = pd.DataFrame(df.groupby(['country'])['humidity'].mean().astype(int))
            df_avg['cloud'] = pd.DataFrame((df.groupby(['country'])['cloud'].mean()).astype(int))
            df_avg['uv'] = pd.DataFrame((df.groupby(['country'])['uv'].mean()).astype(int))
            df_avg['condition.text'] = pd.DataFrame((df.groupby(['country'])['condition.text'].agg(pd.Series.mode)))
            df_avg['last_updated'] = pd.DataFrame((df.groupby(['country'])['last_updated'].agg(pd.Series.mode)))

            return df_avg

        df_avg = weather_data_averages(df)
        return df, df_avg

    def temperature(self, df, df_avg):
        """Temperature figures."""

        fig_temp = go.Figure()

        fig_temp.add_trace(go.Scattergeo(
            lon = df['longitude'],
            lat = df['latitude'],
            text = df['city'].astype(str) + ': ' + df['temp_c'].astype(str) + '\u00B0C',
            hoverinfo='text',
            mode = 'markers',
            marker = dict(
                size = 8,
                opacity = 0.8,
                autocolorscale = False,
                symbol = 'circle',
                colorscale='icefire',
                color=df['temp_c'],
                cmin=df['temp_c'].min(),
                cmax=df['temp_c'].max(),
                colorbar_title='Temperature (\u00B0C)'
            )))

        fig_temp.add_trace(go.Scattergeo(visible=False,
            lon = df['longitude'],
            lat = df['latitude'],
            text = df['city'].astype(str) + ': ' + df['temp_f'].astype(str) + '\u00B0F',
            hoverinfo='text',
            mode = 'markers',
            marker = dict(
                size = 8,
                opacity = 0.8,
                autocolorscale = False,
                symbol = 'circle',
                colorscale='icefire',
                color=df['temp_f'],
                cmin=df['temp_f'].min(),
                cmax=df['temp_f'].max(),
                colorbar_title='Temperature (\u00B0F)'
            )))

        fig_temp.add_trace(go.Choropleth(visible=False,
                            locationmode='country names',
                            locations=df_avg['temp_c'].index,
                            z=df_avg['temp_c'],
                            zmin=df_avg['temp_c'].min(),
                            zmax=df_avg['temp_c'].min(),
                            colorbar_title='Temperature (\u00B0C)',
                            colorscale='icefire',
                            autocolorscale=False,
                            marker_line_width=0,
                            text=df_avg['temp_c'].index + ': ' + df_avg['temp_c'].astype(int).astype(str) + '\u00B0C',
                            hoverinfo='text'
                            ))

        fig_temp.add_trace(go.Choropleth(visible=False,
                            locationmode='country names',
                            locations=df_avg['temp_f'].index,
                            z=df_avg['temp_f'],
                            zmin=df_avg['temp_f'].min(),
                            zmax=df_avg['temp_f'].min(),
                            colorbar_title='Temperature (\u00B0F)',
                            colorscale='icefire',
                            autocolorscale=False,
                            marker_line_width=0,
                            text=df_avg['temp_f'].index + ': ' + df_avg['temp_f'].astype(int).astype(str) + '\u00B0F',
                            hoverinfo='text'
                            ))

        fig_temp.update_geos(projection_type='orthographic', resolution=50, showcountries=True)

        button1t = dict(
                        method='update',
                        label='Cities (\u00B0C)',
                        args=[{"visible": [True, False, False, False]}, {"title": "Current Global Temperatures"}]
                        )

        button2t = dict(
                        method='update',
                        label='Cities (\u00B0F)',
                        args=[{"visible": [False, True, False, False]}, {"title": "Current Global Temperatures"}]
                        )

        button3t = dict(
                        method='update',
                        label='Country Avg. (\u00B0C)',
                        args=[{"visible": [False, False, True, False]}, {"title": "Current Global Temperatures"}]
                        )

        button4t = dict(
                        method='update',
                        label='Country Avg. (\u00B0F)',
                        args=[{"visible": [False, False, False, True]}, {"title": "Current Global Temperatures"}]
                        )

        fig_temp.update_layout(
                                title = 'Current Global Temperatures',
                                template='plotly_dark',
                                updatemenus=[dict(y=1, x=0, xanchor='left', yanchor='top', active=0, buttons=[button1t, button2t, button3t, button4t], font=dict(color='white'))])

        return fig_temp

    def wind(self, df):
        """Wind figures."""

        fig_wind = go.Figure()

        fig_wind.add_trace(go.Scattergeo(
        lon = df['longitude'],
        lat = df['latitude'],
        text = df['city'].astype(str) + ': ' + df['wind_mph'].astype(str) + 'mph',
        hoverinfo='text',
        mode = 'markers',
        marker = dict(
            size = 10,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = df['symbol'],
            colorscale='blues_r',
            color=df['wind_mph'],
            cmin=df['wind_mph'].min(),
            cmax=df['wind_mph'].max(),
            colorbar_title='Wind Speed (mph)'
        )))

        fig_wind.add_trace(go.Scattergeo(visible=False,
                lon = df['longitude'],
                lat = df['latitude'],
                text = df['city'].astype(str) + ': ' + df['wind_kph'].astype(str) + 'kph',
                hoverinfo='text',
                mode = 'markers',
                marker = dict(
                    size = 10,
                    opacity = 0.8,
                    reversescale = True,
                    autocolorscale = False,
                    symbol = df['symbol'],
                    colorscale='blues_r',
                    color=df['wind_kph'],
                    cmin=df['wind_kph'].min(),
                    cmax=df['wind_kph'].max(),
                    colorbar_title='Wind Speed (kph)'
                )))

        fig_wind.add_trace(go.Scattergeo(visible=False,
                lon = df['longitude'],
                lat = df['latitude'],
                text = df['city'].astype(str) + ': ' + df['gust_mph'].astype(str) + 'mph',
                hoverinfo='text',
                mode = 'markers',
                marker = dict(
                    size = 10,
                    opacity = 0.8,
                    reversescale = True,
                    autocolorscale = False,
                    symbol = df['symbol'],
                    colorscale='blues_r',
                    color=df['gust_mph'],
                    cmin=df['gust_mph'].min(),
                    cmax=df['gust_mph'].max(),
                    colorbar_title='Wind Gust (mph)'
                )))

        fig_wind.add_trace(go.Scattergeo(visible=False,
                lon = df['longitude'],
                lat = df['latitude'],
                text = df['city'].astype(str) + ': ' + df['gust_kph'].astype(str) + 'kph',
                hoverinfo='text',
                mode = 'markers',
                marker = dict(
                    size = 10,
                    opacity = 0.8,
                    reversescale = True,
                    autocolorscale = False,
                    symbol = df['symbol'],
                    colorscale='blues_r',
                    color=df['gust_kph'],
                    cmin=df['gust_kph'].min(),
                    cmax=df['gust_kph'].max(),
                    colorbar_title='Wind Gust (kph)'
                )))

        button1w = dict(
                        method='update',
                        label='Speed (mph)',
                        args=[{"visible": [True, False, False, False]}, {"title": "Current Global Wind Speeds (mph)"}]
                        )

        button2w = dict(
                        method='update',
                        label='Speed (kph)',
                        args=[{"visible": [False, True, False, False]}, {"title": "Current Global Wind Speeds (kph)"}]
                        )

        button3w = dict(
                        method='update',
                        label='Gust (mph)',
                        args=[{"visible": [False, False, True, False]}, {"title": "Current Global Wind Gusts (mph)"}]
                        )

        button4w = dict(
                        method='update',
                        label='Gust (kph)',
                        args=[{"visible": [False, False, False, True]}, {"title": "Current Global Wind Gusts (kph)"}]
                        )

        fig_wind.update_geos(projection_type='orthographic', showcountries=True)
        fig_wind.update_layout(
                                title = 'Current Global Wind Speeds',
                                template='plotly_dark',
                                updatemenus=[dict(y=1, x=0, xanchor='left', yanchor='top', active=0, buttons=[button1w, button2w, button3w, button4w], font=dict(color='white'))])

        return fig_wind

    def precipitation(self, df, df_avg):
        """Rainfall figures."""

        fig_prcp = go.Figure()

        fig_prcp.add_trace(go.Scattergeo(
                        lat=df['latitude'],
                        lon=df['longitude'], 
                        text = df['city'].astype(str) + ': ' + df['precip_mm'].astype(str) + 'mm',
                        hoverinfo='text',
                        mode = 'markers',
                        marker=dict(
                                size=df['precip_mm'],
                                line_width=0,
                                color=df['precip_mm'],
                                colorscale='PuBu',
                                cmin=df['precip_mm'].min(),
                                cmax=df['precip_mm'].max(),
                                colorbar_title='Precipitation (mm)'
                                )
                        ))

        fig_prcp.add_trace(go.Scattergeo(visible=False,
                        lat=df['latitude'],
                        lon=df['longitude'], 
                        text = df['city'].astype(str) + ': ' + df['precip_in'].astype(str) + '"',
                        hoverinfo='text',
                        mode = 'markers',
                        marker=dict(
                                size=df['precip_in'],
                                line_width=0,
                                color=df['precip_in'],
                                colorscale='PuBu',
                                cmin=df['precip_in'].min(),
                                cmax=df['precip_in'].max(),
                                colorbar_title='Precipitation (")'
                                )
                        ))

        fig_prcp.add_trace(go.Choropleth(visible=False,
                            locationmode='country names',
                            locations=df_avg['precip_mm'].index,
                            z=df_avg['precip_mm'],
                            zmin=df_avg['precip_mm'].min(),
                            zmax=df_avg['precip_mm'].min(),
                            colorbar_title='Precipitation (mm)',
                            colorscale='PuBu',
                            autocolorscale=False,
                            marker_line_width=0,
                            text=df_avg['precip_mm'].index + ': ' + df_avg['precip_mm'].astype(float).astype(str) + 'mm',
                            hoverinfo='text'
                            ))

        fig_prcp.add_trace(go.Choropleth(visible=False,
                            locationmode='country names',
                            locations=df_avg['precip_in'].index,
                            z=df_avg['precip_in'],
                            zmin=df_avg['precip_in'].min(),
                            zmax=df_avg['precip_in'].min(),
                            colorbar_title='Precipitation (")',
                            colorscale='PuBu',
                            autocolorscale=False,
                            marker_line_width=0,
                            text=df_avg['precip_in'].index + ': ' + df_avg['precip_in'].astype(float).astype(str) + '"',
                            hoverinfo='text'
                            ))

        button1p = dict(
                        method='update',
                        label='Cities (mm)',
                        args=[{"visible": [True, False, False, False]}, {'title': 'Current Global Precipitation (mm)'}]
                        )

        button2p = dict(
                        method='update',
                        label='Cities (")',
                        args=[{"visible": [False, True, False, False]}, {'title': 'Current Global Wind Speeds (")'}]
                        )

        button3p = dict(
                        method='update',
                        label='Country Avg. (mm)',
                        args=[{"visible": [False, False, True, False]}, {'title': 'Current Global Precipitation (mm)'}]
                        )

        button4p = dict(
                        method='update',
                        label='Country Avg. (")',
                        args=[{"visible": [False, False, False, True]}, {'title': 'Current Global Wind Speeds (")'}]
                        )

        fig_prcp.update_geos(projection_type='orthographic', resolution=50, showcountries=True)
        fig_prcp.update_layout(
                                title = 'Current Global Precipitation',
                                template='plotly_dark',
                                updatemenus=[dict(y=1, x=0, xanchor='left', yanchor='top', active=0, buttons=[button1p, button2p, button3p, button4p], font=dict(color='white'))])

        return fig_prcp

    def humidity(self, df, df_avg):
        """Humidity figures."""

        fig_humd = go.Figure()

        fig_humd.add_trace(go.Scattergeo(
                lon = df['longitude'],
                lat = df['latitude'],
                text = df['city'].astype(str) + ': ' + df['humidity'].astype(str) + '%',
                hoverinfo='text',
                mode = 'markers',
                marker = dict(
                    size = 10,
                    opacity = 0.8,
                    autocolorscale = False,
                    symbol = 'circle',
                    colorscale='YlGnBu',
                    color=df['humidity'],
                    cmin=df['humidity'].min(),
                    cmax=df['humidity'].max(),
                    colorbar_title='Humidty (%)'
                )))

        fig_humd.add_trace(go.Choropleth(visible=False,
                            locationmode='country names',
                            locations=df_avg['humidity'].index,
                            z=df_avg['humidity'],
                            zmin=0,
                            zmax=100,
                            colorbar_title='Humidty (%)',
                            colorscale='YlGnBu',
                            autocolorscale=False,
                            marker_line_width=0,
                            text=df_avg['humidity'].index + ': ' + df_avg['humidity'].astype(int).astype(str) + '%',
                            hoverinfo='text'
                            ))

        button1h = dict(
                        method='update',
                        label='Cities',
                        args=[{"visible": [True, False]}, {'title': 'Current Global Humidity'}]
                        )

        button2h = dict(
                        method='update',
                        label='Country Avg.',
                        args=[{"visible": [False, True]}, {'title': 'Current Global Humidity'}]
                        )

        fig_humd.update_geos(projection_type='orthographic', resolution=50, showcountries=True)
        fig_humd.update_layout(
                                title = 'Current Global Humidity',
                                template='plotly_dark',
                                updatemenus=[dict(y=1, x=0, xanchor='left', yanchor='top', active=0, buttons=[button1h, button2h], font=dict(color='white'))])

        return fig_humd

    def cloud(self, df, df_avg):
        """Cloud cover figures."""

        fig_cdcv = go.Figure()

        fig_cdcv.add_trace(go.Scattergeo(
                                lat=df['latitude'],
                                lon=df['longitude'], 
                                text = df['city'].astype(str) + ': ' + df['cloud'].astype(str) + '%',
                                hoverinfo='text',
                                mode = 'markers',
                                marker=dict(
                                        size=df['cloud'] / 10,
                                        line_width=0,
                                        color=df['cloud'],
                                        colorscale='Greys_r',
                                        cmin=0,
                                        cmax=100,
                                        colorbar_title='Cloud Cover (%)'
                                )
        ))

        fig_cdcv.add_trace(go.Choropleth(visible=False,
                            locationmode='country names',
                            locations=df_avg['cloud'].index,
                            z=df_avg['cloud'],
                            zmin=df_avg['cloud'].min(),
                            zmax=df_avg['cloud'].min(),
                            colorbar_title='Cloud Cover (%)',
                            colorscale='Greys_r',
                            autocolorscale=False,
                            marker_line_width=0,
                            text=df_avg['cloud'].index + ': ' + df_avg['cloud'].astype(int).astype(str) + '%',
                            hoverinfo='text'
                            ))

        button1c = dict(
                        method='update',
                        label='Cities',
                        args=[{"visible": [True, False]}, {'title': 'Current Global Cloud Coverage'}]
                        )

        button2c = dict(
                        method='update',
                        label='Country Avg.',
                        args=[{"visible": [False, True]}, {'title': 'Current Global Cloud Coverage'}]
                        )

        fig_cdcv.update_geos(projection_type='orthographic', resolution=50, showcountries=True)
        fig_cdcv.update_layout(
                                title = 'Current Global Cloud Coverage',
                                template='plotly_dark',
                                updatemenus=[dict(y=1, x=0, xanchor='left', yanchor='top', active=0, buttons=[button1c, button2c], font=dict(color='white'))])

        return fig_cdcv

    def uv(self, df, df_avg):
        """UV index figures."""

        fig_uvin = go.Figure()

        fig_uvin.add_trace(go.Scattergeo(
            lon = df['longitude'],
            lat = df['latitude'],
            text = df['city'].astype(str) + ': ' + df['uv'].astype(str),
            hoverinfo='text',
            mode = 'markers',
            marker = dict(
                size = 8,
                opacity = 0.8,
                autocolorscale = False,
                symbol = 'circle',
                colorscale='YlOrRd',
                color=df['uv'],
                cmin=0,
                cmax=11,
                colorbar_title='UV Index'
            )))

        fig_uvin.add_trace(go.Choropleth(visible=False,
                            locationmode='country names',
                            locations=df_avg['uv'].index,
                            z=df_avg['uv'],
                            zmin=0, 
                            zmax=11,
                            colorbar_title='UV Index',
                            colorscale='YlOrRd',
                            autocolorscale=False,
                            marker_line_width=0
                            ))

        button1u = dict(
                        method='update',
                        label='Cities',
                        args=[{"visible": [True, False]}, {'title': 'Current Global UV Index'}]
                        )

        button2u = dict(
                        method='update',
                        label='Country Avg.',
                        args=[{"visible": [False, True]}, {'title': 'Current Global UV Index'}]
                        )

        fig_uvin.update_geos(projection_type='orthographic', resolution=50, showcountries=True)
        fig_uvin.update_layout(
                                title = 'Current Global UV Index',
                                template='plotly_dark',
                                updatemenus=[dict(y=1, x=0, xanchor='left', yanchor='top', active=0, buttons=[button1u, button2u], font=dict(color='white'))])

        return fig_uvin     
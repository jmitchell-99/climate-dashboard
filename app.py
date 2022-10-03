import time
from concurrent.futures import ThreadPoolExecutor
from dash import Dash, Input, Output
from weather_data import *
from plots import *
from layout import *

# ----- Request user's API key

user_input = input("Enter weather API key (see https://www.weatherapi.com/ to get a key): ")

# ----- Initial climate figures

cplots = ClimatePlots()
fig_tc = cplots.temp_change()
fig_cd = cplots.carbon_dioxide()
fig_mt = cplots.methane()
fig_no = cplots.nitrous_oxide()
fig_pi = cplots.polar_ice()

# ----- Initial weather figures
wplots = WeatherPlots()
wdata = WeatherData()
wdata.create_db()

def update_weather(user_input):
    """Update dataframes storing weather data."""
    global df, df_avg
    df, df_avg = wplots.weather_data(user_input)

update_weather(user_input)

fig_temp = wplots.temperature(df, df_avg)
fig_wind = wplots.wind(df)
fig_prcp = wplots.precipitation(df, df_avg)
fig_humd = wplots.humidity(df, df_avg)
fig_cdcv = wplots.cloud(df, df_avg)
fig_uvin = wplots.uv(df, df_avg)

interval = 300 # no. of seconds between weather updates

def get_weather_every(period=interval):
    """Update the weather data every 5 minutes."""
    while True:
        print("Starting update")
        update_weather()
        print("Data and figures updated.")
        time.sleep(period)

# ----- Start the app

app = Dash(__name__, external_stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap-grid.min.css"])
app.layout = make_layout()

# --- Callbacks for dashboard's user interactions
# ----- Weather figures

@app.callback(
    Output('wfig1', 'figure'),
    Output('wfig2', 'figure'),
    Output('wfig3', 'figure'),
    Output('wfig4', 'figure'),
    Output('wfig5', 'figure'),
    Output('wfig6', 'figure'),

    Input('tabs', 'value')
)

def weather_figs(tabs):
    """Updates weather figures when tab is selected."""

    if tabs == 'tab1':
        wfig1 = fig_temp
        return wfig1
    elif tabs == 'tab2':
        wfig2 = fig_wind
        return wfig2
    elif tabs == 'tab3':
        wfig3 = fig_prcp
        return wfig3
    elif tabs == 'tab4':
        wfig4 = fig_humd
        return wfig4
    elif tabs == 'tab5':
        wfig5 = fig_cdcv
        return wfig5
    elif tabs == 'tab6':
        wfig6 = fig_uvin
        return wfig6

    return fig_temp, fig_wind, fig_prcp, fig_humd, fig_cdcv, fig_uvin

# ----- Climate figures

@app.callback(
	Output('cfig1', 'figure'),
    Output('cfig2', 'figure'),

	Input('dropdown1', 'value'),
    Input('dropdown2', 'value')
)

def climate_figs(dropdown1, dropdown2):
    """Updates climate figures with dropdowns."""

    if dropdown1 == 'fig_tc':
        cfig1 = fig_tc
    elif dropdown1 == 'fig_cd':
        cfig1 = fig_cd
    elif dropdown1 == 'fig_mt':
        cfig1 = fig_mt
    elif dropdown1 == 'fig_no':
        cfig1 = fig_no
    elif dropdown1 == 'fig_pi':
        cfig1 = fig_pi

    if dropdown2 == 'fig_tc':
        cfig2 = fig_tc
    elif dropdown2 == 'fig_cd':
        cfig2 = fig_cd
    elif dropdown2 == 'fig_mt':
        cfig2 = fig_mt
    elif dropdown2 == 'fig_no':
        cfig2 = fig_no
    elif dropdown2 == 'fig_pi':
        cfig2 = fig_pi

    return cfig1, cfig2

# ------ Local weather text

@app.callback(
    Output('text0', 'children'),
    Output('text1', 'children'), 
    Output('text2', 'children'),
    Output('text3', 'children'),
    Output('text4', 'children'),
    Output('text5', 'children'),
    Output('text6', 'children'),
    Output('text7', 'children'),
    Output('text8', 'children'),
    Output('text9', 'children'),

    Input('input1a', 'value'),
    Input('input1b', 'value')
)

def local_weather(input1a, input1b):
    """Updates local weather text from inputs."""

    df_city = df[(df['city'] == str(input1a).upper())]
    no_cities = len(df_city)

    if no_cities == 0:
        text0 = ''
        text1 = 'Weather:'
        text2 = 'Temperature:'
        text3 = 'Feels like:'
        text4 = 'Rainfall:'
        text5 = 'Wind:'
        text6 = 'Humidity:'
        text7 = 'Cloud cover:'
        text8 = 'UV index:'
        text9 = 'Last updated:'

    else:

        if no_cities == 1:
            
            str0 = str([df_city['condition.text'].tolist()][0])[2:-2]
            str1 = str([df_city['temp_c'].tolist()][0])[1:-1]
            str2 = str([df_city['temp_f'].tolist()][0])[1:-1]
            str3 = str([df_city['feelslike_c'].tolist()][0])[1:-1]
            str4 = str([df_city['feelslike_f'].tolist()][0])[1:-1]
            str5 = str([df_city['precip_mm'].tolist()][0])[1:-1]
            str6 = str([df_city['precip_in'].tolist()][0])[1:-1]
            str7 = str([df_city['wind_mph'].tolist()][0])[1:-1]
            str8 = str([df_city['wind_kph'].tolist()][0])[1:-1]
            str9 = str([df_city['wind_dir'].tolist()][0])[2:-2]
            str10 = str([df_city['humidity'].tolist()][0])[1:-1]
            str11= str([df_city['cloud'].tolist()][0])[1:-1]
            str12 = str([df_city['uv'].tolist()][0])[1:-1]

            str13 = str([df_city['last_updated'].tolist()][0])[2:-2]
            str13 = str13[10:] + ' on ' + str13[8:10] + '-' + str13[5:7] + '-' + str13[:4]

            text0 = ''
            text1 = f'Weather: {str0}'
            text2 = f'Temperature: {str1}\u00B0C/{str2}\u00B0F'
            text3 = f'Feels like: {str3}\u00B0C/{str4}\u00B0F'
            text4 = f'Rainfall: {str5}mm/{str6}"'
            text5 = f'Wind: {str7}mph/{str8}kph in the {str9} direction'
            text6 = f'Humidity: {str10}%'
            text7 = f'Cloud cover: {str11}%'
            text8 = f'UV index: {str12}'
            text9 = f'Last updated: {str13}'

        else: 
            df_city_country = df_city[(df_city['country'] == str(input1b).upper())]

            str0 = str([df_city_country['condition.text'].tolist()][0])[2:-2]
            str1 = str([df_city_country['temp_c'].tolist()][0])[1:-1]
            str2 = str([df_city_country['temp_f'].tolist()][0])[1:-1]
            str3 = str([df_city_country['feelslike_c'].tolist()][0])[1:-1]
            str4 = str([df_city_country['feelslike_f'].tolist()][0])[1:-1]
            str5 = str([df_city_country['precip_mm'].tolist()][0])[1:-1]
            str6 = str([df_city_country['precip_in'].tolist()][0])[1:-1]
            str7 = str([df_city_country['wind_mph'].tolist()][0])[1:-1]
            str8 = str([df_city_country['wind_kph'].tolist()][0])[1:-1]
            str9 = str([df_city_country['wind_dir'].tolist()][0])[2:-2]
            str10 = str([df_city_country['humidity'].tolist()][0])[1:-1]
            str11 = str([df_city_country['cloud'].tolist()][0])[1:-1]
            str12 = str([df_city_country['uv'].tolist()][0])[1:-1]
            str13 = str([df_city_country['last_updated'].tolist()][0])[2:-2]
            str13 = str13[10:] + ' on ' + str13[8:10] + '-' + str13[5:7] + '-' + str13[:4]

            if len(df_city_country) == 0:
                text0 = "Multiple cities found. Please enter the city's country."
                text1 = 'Weather:'
                text2 = 'Temperature:'
                text3 = 'Feels like:'
                text4 = 'Rainfall:'
                text5 = 'Wind:'
                text6 = 'Humidity:'
                text7 = 'Cloud cover:'
                text8 = 'UV index:'
                text9 = 'Last updated:'

            else:
                text0 = ''
                text1 = f'Weather: {str0}'
                text2 = f'Temperature: {str1}\u00B0C/{str2}\u00B0F'
                text3 = f'Feels like: {str3}\u00B0C/{str4}\u00B0F'
                text4 = f'Rainfall: {str5}mm/{str6}"'
                text5 = f'Wind: {str7}mph/{str8}kph in the {str9} direction'
                text6 = f'Humidity: {str10}%'
                text7 = f'Cloud cover: {str11}%'
                text8 = f'UV index: {str12}'
                text9 = f'Last updated: {str13}'

    return text0, text1, text2, text3, text4, text5, text6, text7, text8, text9

# ------ Country weather text

@app.callback(
    Output('text10', 'children'),
    Output('text11', 'children'),
    Output('text12', 'children'),
    Output('text13', 'children'),
    Output('text14', 'children'),
    Output('text15', 'children'),
    Output('text16', 'children'),
    Output('text17', 'children'),
    Output('text18', 'children'),

    Input('input2', 'value')
)

def country_weather(input2):
    """Updates country weather text from input."""

    df_country = df_avg[(df_avg.index == str(input2).upper())]
    no_countries = len(df_country)

    if no_countries == 0:
        text10 = 'Weather:'
        text11 = 'Temperature:'
        text12 = 'Feels like:'
        text13 = 'Rainfall:'
        text14 = 'Wind:'
        text15 = 'Humidity:'
        text16 = 'Cloud cover:'
        text17 = 'UV index:'
        text18 = 'Last updated:'

    else:
        str0 = str([df_country['condition.text'].tolist()][0])[2:-2]
        str1 = str([df_country['temp_c'].tolist()][0])[1:-1]
        str2 = str([df_country['temp_f'].tolist()][0])[1:-1]
        str3 = str([df_country['feelslike_c'].tolist()][0])[1:-1]
        str4 = str([df_country['feelslike_f'].tolist()][0])[1:-1]
        str5 = str([df_country['precip_mm'].tolist()][0])[1:-1]
        str6 = str([df_country['precip_in'].tolist()][0])[1:-1]
        str7 = str([df_country['wind_mph'].tolist()][0])[1:-1]
        str8 = str([df_country['wind_kph'].tolist()][0])[1:-1]
        str9 = str([df_country['wind_dir'].tolist()][0])[2:-2]
        str10 = str([df_country['humidity'].tolist()][0])[1:-1]
        str11 = str([df_country['cloud'].tolist()][0])[1:-1]
        str12 = str([df_country['uv'].tolist()][0])[1:-1]

        str13 = str([df_country['last_updated'].tolist()][0])[2:-2]
        str13 = str13[10:] + ' on ' + str13[8:10] + '-' + str13[5:7] + '-' + str13[:4]

        text10 = f'Weather: {str0}'
        text11 = f'Temperature: {str1}\u00B0C/{str2}\u00B0F'
        text12 = f'Feels like: {str3}\u00B0C/{str4}\u00B0F'
        text13 = f'Rainfall: {str5}mm/{str6}"'
        text14 = f'Wind: {str7}mph/{str8}kph in the {str9} direction'
        text15 = f'Humidity: {str10}%'
        text16 = f'Cloud cover: {str11}%'
        text17 = f'UV index: {str12}'
        text18 = f'Last updated: {str13}'

    return text10, text11, text12, text13, text14, text15, text16, text17, text18

# --- Enable app updates and run the app

executor = ThreadPoolExecutor(max_workers=1)
executor.submit(get_weather_every)

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
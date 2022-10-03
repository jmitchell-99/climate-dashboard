from concurrent.futures import ThreadPoolExecutor
import json
import requests
import pandas as pd
import sqlite3

class WeatherData:

    def locations():
        """Get a dataframe of locational data from the global airports SQL database."""

        conn_l = sqlite3.connect('global_airports_sqlite.db')
        cursor = conn_l.cursor()
        cursor.execute('select city, country, lat_decimal, lon_decimal from airports')
        locs = cursor.fetchall()

        city = []
        country = []
        lat = []
        lon = []

        for loc in locs:
            if loc[2] != 0.0:
                city.append(loc[0])
                country.append(loc[1])
                lat.append(float(loc[2]))
                lon.append(float(loc[3]))

        df_locs = pd.DataFrame(list(zip(city, country, lat, lon)), columns=['city', 'country', 'latitude', 'longitude'])

        return df_locs

    def create_db(df_locs):
        """Create initial database to store weather data."""

        conn_w = sqlite3.connect('latest_weather.db')
        query = f'''CREATE TABLE IF NOT EXISTS Weather (
            city string,
            country string,
            latitude decimal,
            longitude decimal,
            last_updated_epoch integer,
            last_updated string,
            temp_c decimal,
            temp_f decimal,
            feelslike_c decimal,
            feelslike_f decimal,
            condition_text string,
            condition_icon string,
            condition_code integer,
            wind_mph decimal,
            wind_kph decimal,
            wind_degree integer,
            wind_dir string,
            pressure_mb decimal,
            pressure_in decimal,
            precip_mm decimal,
            precip_in decimal,
            humidity integer,
            cloud integer,
            is_day integer,
            uv decimal,
            gust_mph decimal,
            gust_kph decimal
            )'''
        conn_w.execute(query)

        return conn_w

    def get_weather(user_input, df_locs, conn_w):
        """Update the database with the latest data entries when requested."""

        apikey = user_input

        urls = [] # stores urls for each city
        df_data = pd.DataFrame()

        for lat, lon in zip(df_locs['latitude'], df_locs['longitude']):
            locationstr = str(lat) + ", " + str(lon)
            url = 'http://api.weatherapi.com/v1/current.json?key=' + apikey + '&q=' + locationstr
            urls.append(url)

        def get_url(url):
            """Call weather API and get the response."""
            response = requests.request("GET", url)
            response = json.loads(response.text)
            return response

        # Send multiple requests at once for performance improvements
        with ThreadPoolExecutor(max_workers=75) as pool:
            response_list = list(pool.map(get_url, urls))

        # Manipulate responses into dataframe
        for i in response_list:
            try:
                response = i['current']
                df_response = pd.json_normalize(response)

                df_data = pd.concat([df_data, df_response], ignore_index=True)

            except:
                pass

        # Update SQL database with dataframe
        df_complete = df_locs.join(df_data, how='outer')
        df_complete.to_sql('Weather', conn_w, if_exists='replace', index=False)
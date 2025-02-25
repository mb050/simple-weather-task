from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from os.path import exists, getmtime
from os import mkdir
import numpy as np
import json as js
import requests
import utility

class Weather_forecast():
    """
    henter, lagrer, leser og printer ut værdata.
    
    attributter:
        debug: True eller False
    
    methods:
        standard_initiation: leser og oppdaterer fil
        update_file: oppdaterer filen
        get_new_data: henter ny data
        save_new_data: lagrer ny data
        load_file: laster inn data fra fil
        check_modified_time: finner tiden fra filen ble sist endret
        check_location: henter info til angitt by/sted
        check_invalid_location: ser om angitt by/sted finnes
        check_min_max_key: bestemmer om variablen min eller max skal brukes
        initiate_period_format: starter å formatere for periode
        get_units: henter dictionary og keys for enheter
        format_date: behandler dato fra keys til ønsket format
        add_day: legger til en dag
        get_next_day: finner dato for påfølgende dag
        give_date_string: behandler str av dato
        make_date_list: lager liste med datoer
        get_index_dict: lager en dict med index
        make_key_format: lager keys 
        make_key_list: lager lister av keys
        get_idx_list: lager liste med index
        allocate_result: allokerer resultat til array
        loop_main_body: ser om variabel og verdi finnes
        forecast_24_hours: metoden som leser av data for formatet for 24 timer 
        forecast_period: metoden som leser av data for formatet for periode 
        output_24_hour_forecast: skriver ut resultatet for 24 timer
        default_period_output: skriver ut resultatet for periode
        complex_period_output: skriver ut ekstra variabler for periode
    """
    
    def __init__(self, debug=False):
        """
        definerer ulike variabler, og ser hvilket format som skal brukes.
        
        args:
            debug: False (bool): sett til True for debugging
        """
        
        self.priority_time = ['instant', 'next_6_hours', 'next_1_hours',
                              'next_12_hours']
        self.headers = {'User-Agent': 
                        'https://github.com/mb050/simple-weather-task',}
        
        if debug is True:
            self.path = 'test_output/complete.json' 
            self.sted_navn = 'Oslo'
            self.load_file()
        else:
            self.standard_initiation()
        
        self.get_units()
        self.get_index_dict()
        
        date = self.data['properties']['meta']['updated_at']
        
        self.current_date = self.format_date(date)
        self.next_day = self.add_day(self.current_date[0])
        self.table = self.data['properties']['timeseries']

        user_input = utility.check_valid_format()

        if user_input == 'enkel':
            self.forecast_24_hours()        
        elif user_input == 'periode':    
            self.initiate_period_format()
        elif user_input == 'ekstra':
            user_input = utility.check_valid_format(True)
            variable = utility.initiate_additional_variables(self.unit_key)
            
            if user_input == 'enkel':   
                self.forecast_24_hours(variable)
            else:
                self.initiate_period_format(variable)
    
    def standard_initiation(self):
        """ 
        leser fra fil med værdata. om filen ikke finnes eller er utdatert blir
        det hentet ny data. det vil bli hentet ut dersom latitude og longitude
        er forskjellig fra eksisterende fil og ønkset område.
        """
        
        self.path = 'data/complete.json'
        new_lat, new_lon = self.check_invalid_location()

        if exists(self.path):
            self.load_file()
            old_lon, old_lat = self.data['geometry']['coordinates'][:2]
            
            is_outdated = self.check_modified_time() > 7200
            lat_diff = new_lat != old_lat
            lon_diff = new_lon != old_lon

            if is_outdated or lat_diff or lon_diff:
                self.update_file(new_lat, new_lon)      
        else:
            self.update_file(new_lat, new_lon)
        return

    def update_file(self, lat, lon):
        """
        oppdaterer fil med data.
        
        args:
            lat (float): latitude (maks 3 desimaler)
            lon (float): longitude (maks 3 desimaler)
        """
        
        self.get_new_data(lat, lon)
        self.load_file()
        return 

    def get_new_data(self, lat, lon):
        """
        henter ny værdata fra met, og sender det til å bli lagret.
        
        args:
            lat (float): latitude (maks 3 desimaler)
            lon (float): longitude (maks 3 desimaler)
        """
        
        url = 'https://api.met.no/weatherapi/locationforecast/'
        url_str = url + f'2.0/complete.json?lat={lat}&lon={lon}'
        data = requests.get(url_str, headers=self.headers)
        self.save_new_data(data.content)
        return
    
    def save_new_data(self, content):
        """
        ser om mappen 'data' eksisterer, lager mappen hvis den ikke finnes.
        lagrer ny data til mappen.
        
        args:
            content (json): værdata i json format
        """        
        
        if exists('data') is not True:
            mkdir('data')
        
        file = open(self.path, 'wb')
        file.write(content)
        file.close()

    def load_file(self):
        """
        leser av værdata
        """
        
        file = open(self.path, 'r')
        self.data = js.load(file)
        file.close()
        
    def check_modified_time(self):
        # potensiell fare for feil her, dersom datoer faller på samme dag, men
        # ulik måned eller år
        """
        finner tiden siden filen med værdataene ble sist endret.
        """
        
        modified = datetime.fromtimestamp(getmtime(self.path))
        diff = datetime.now() - modified 
        return diff.days * 86400 + diff.seconds
      
    def check_location(self, sted_navn):
        """
        henter info til et gitt sted.
        
        args:
            sted_navn (str): stedet der været skal hentes fra.
        """
        
        location_function = Nominatim(user_agent='test')
        return location_function.geocode(sted_navn)
            
    def check_invalid_location(self, testing=False):
        """
        ser om stedet man spør om eksisterer.
        
        args:
            testing (bool): sett til True for standard by
        
        return:
            lat (float): latitude
            lon (float): longitude 
        """
        
        print('Tast inn bynavn:', end=' ')
        if testing is True:
            sted_navn = 'Oslo'
        else:
            sted_navn = input().capitalize()
        
        loc = self.check_location(sted_navn)
        
        while loc is None:
            print(f'\nFeil: Kan ikke finne en by med navnet "{sted_navn}"' )
            print('Tast inn bynavn:', end=' ')
            
            sted_navn = input().capitalize()
            loc = self.check_location(sted_navn)
            
        lat = round(loc.latitude, 3)
        lon = round(loc.longitude, 3)
        self.sted_navn = sted_navn
        return lat, lon
    
    def check_min_max_key(self, key):
        """
        bestemmer om min eller max skal brukes.
        
        args:
            key (str): enten 'min' eller 'max'
        
        returns:
            min_statement (bool): True eller False
            max_statement (bool): True eller False
        """
        
        min_statement = max_statement = False
        if 'min' in key:
            min_statement = True
        elif 'max' in key:
            max_statement = True
        return min_statement, max_statement
    
    def initiate_period_format(self, variable=False, ekstra=False):
        """
        bestemmer om forecast_period skal finne verdier for andre variabler
        enn bare min, maks og gjennomsnitt temperatur. bestemmer også hvordan
        det skal skrives til terminalen.
        
        args:
            variable (list): liste med variabler
            ekstra (bool): ikke nødvendig å røre
        """
        
        updated_at = self.get_next_day(1)
        idx_list, time_list = self.get_idx_list(True)
        date_list = self.make_date_list(idx_list, updated_at)
        
        if variable is not False:
            ekstra = True
            self.forecast_period(idx_list, variable)
        else:
            self.forecast_period(idx_list)
            
        if ekstra:
            self.complex_period_output(time_list, date_list, variable)
        else:
            self.default_period_output(time_list, date_list)
       
    def get_units(self):
        """
        henter dictionary for enheter og liste av keys for gitte enheter.
        """
        
        unit_dict = self.data['properties']['meta']['units']
        unit_key = []
        
        for i in unit_dict.keys():
            unit_key.append(i)
        
        self.unit_dict = unit_dict
        self.unit_key = unit_key 
        
    def format_date(self, date, no_split=False):
        """
        behandler en key fra json filen som skrives som 
        eks: 2025-02-11T10:27:36Z
        og gjør det om til et brukbart format.
        
        args:
            date (str): dato
            no_split (bool): False, eller True
        
        returns:
            date (str): 2025-02-11 10:27:36
            om no_split=True: ['2025-02-11', '10:27:36']
        """
        
        for i in ('T', 'Z'):
            date = date.replace(i, ' ')
        if no_split != False:
            return date
        else:
            return date.split()

    def add_day(self, day, amount=1):
        """
        legger til x antall dager. default er 1 dag.
        
        args:
            day (str): dato
            amount (int): antall som skal legges til
        """
        
        new_day = datetime.strptime(day, "%Y-%m-%d") + timedelta(days=amount)
        return str(new_day)[:-9]
    
    def get_next_day(self, current_only=False):
        """
        legger til 1 dag
        
        args:
            current_only (bool): bestemmer hvilken dato som skal bli gitt.
        
        returns:
            day (str): dato
            current_only (str): dato da dataene ble oppdatert
        """
        
        current_date = self.current_date
        date = current_date[0]
        if current_only != False:
            return date
        else:
            return self.add_day(date)
    
    def give_date_string(self, date):
        """
        gjør om dato som bare inneholder tall, til å gi navn for måned og dag.
        
        args:
            date (str): dato, eksempel 2025-02-11
        
        returns:
            str: full dato 
        """
        
        date = datetime.strptime(date, "%Y-%m-%d")
        year = date.strftime("%Y")
        month = date.strftime("%B")
        day = date.strftime("%d")
        name_day = date.strftime('%A')
        return f'{name_day:<9} {day}. {month:<9} {year}'
    
    def make_date_list(self, idx_list, updated_at):
        """
        lager liste av datoer.
        
        args:
            idx_list (list): liste med spesifikke index
            updated_at (str): dato
        
        return:
            list: liste med dato
        """
        
        table = self.table
        date_list = []
        date = ''
        for i in idx_list:
            date = self.format_date(table[i[0]]['time'])[0]
            if date != updated_at:
                updated_at = date
                date_list.append(self.give_date_string(date))
        return date_list
    
    def get_index_dict(self):
        """
        lager en dictionary med datoer som keys og index, som value.
        gjør det enklere å se om det er data for et bestemt tidspunkt.
        """
        
        idx_dict = {}
        for i, j in enumerate(self.data['properties']['timeseries']):
            date = self.format_date(j['time'], 1)
            idx_dict[date[:-7]] = i
        self.idx_dict = idx_dict
    
    def make_key_format(self, date, time):
        """
        lager keys fra datoer og tidspunker.
        
        args:
            date (str): dato, eksempel 2021-02-13
            time (int): tid i hele timer.
        
        returns:
            str: dato og time
        """
        
        
        time_str = str(time)
        if len(time_str) < 2:
            time_str = '0' + time_str
        return f'{date} {time_str}'
    
    def make_key_list(self, n=48):
        """
        lager enkel liste med index fra første påfølgende dag.
        
        args:
            n (int): n antall timer som skal itereres over.
            
        returns:
            list: liste med keys
        """
        
        key_list = []
        day = self.get_next_day()
        
        I = 0
        for i in range(n + 1):
            key_list.append(self.make_key_format(day, I))
            I += 1
            if I > 23:
                day = self.add_day(day)
                I = 0 
        return key_list
    
    def get_idx_list(self, default=False):
        """
        henter intervaller som brukes for forecast_period metoden, lager
        en nested list med spesifikke index som brukes, og lager en liste
        med tider, i hele timer.
        
        args:
            default (bool): True for default interval
        
        returns:
            list: index 
            list: timer
        """
        
        if default is not False:
            custom = [6, 12]
            custom.sort()
            t1, t2 = custom
        else:
            t1, t2 = utility.check_valid_intervals()
            
        key_list = self.make_key_list()
        
        iteration = [t1 - 0, t2 - t1, 18 - t2, 6] * 2
        arr = np.zeros((8, 2), dtype=int)
        time_list = []
        idx = []
        
        a = b = 0
        for i in range(8):
            b = iteration[i] + b
            time_list.append(f'{key_list[a][-2:]}-{key_list[b][-2:]}')
            arr[i], a = [a, b], b
            
        arr[:, 1] += 1
        for i in arr:
            temp = []
            for j in key_list[i[0]:i[1]]:            
                if j in self.idx_dict:
                    temp.append(self.idx_dict[j])
            idx.append(temp)
    
        del(temp)
        return idx, time_list
    
    def allocate_result(self, result, all_results, count, v_itr, 
                         min_=False, max_=False, min_max=False):
        """
        deligerer verdier til riktige arrays og lister.
        
        args:
            result (list): liste med verdier
            all_results (list): nested list
            count (int): iterasjon for nested loop
            v_itr (int): iterasjon for variabel loop
            min_, max_, min_max (bool): trenger ikke å røre, men bestemmer
                                        om min eller max skal brukes
        """
        
        if min_max is False:
            elements = len(result)
            sum_ = sum(result)
            
            if elements == 0:
                self.res[count, v_itr] = np.nan
            else:
                self.res[count, v_itr] = round(sum_ / elements, 1)
    
        if count % 4 != 0:
            all_results += result[1:]
        else:
            all_results += result
        
        if (count + 1) % 4 == 0:
            if min_max is False:
                value = round(sum(all_results) / len(all_results), 1)
            else:
                value = max(all_results) * max_ + min(all_results) * min_
                
            J = (count > 3) - 2
            self.res[J, v_itr] = value
        return
    
    def loop_main_body(self, variable, idx, arr):
        """
        indre loop, som går over om en gitt variabel eksisterer til et
        gitt tidspunkt.
        
        args:
            variable (str): variabel key
            idx (list): liste med index
            arr (list): liste for verdier
        """
        
        for i in idx:
            for j in self.priority_time:
                try:
                    val = self.table[i]['data'][j]['details'][variable]
                except:
                    continue
                
                arr.append(val)
                break
        return
    
    def forecast_24_hours(self, variable=False, default=False):
        """
        metode som henter ut verdier gjennom hele den påfølgende dagen, time
        for time.
        
        args:
            variable (list): liste med variabler, bare nødvendig for 
                             bruk av ekstra variabler 
            default (bool): ikke nødvendig å røre
        """
        
        if variable is False:
            variable = ['air_temperature']
            default = True

        idx = np.arange(24) + self.idx_dict[self.next_day + ' 00']
        self.res = np.zeros((24, len(variable)))
        for v_itr, variable_type in enumerate(variable):
            temp = []
            self.loop_main_body(variable_type, idx, temp)
            self.res[:, v_itr] = temp
            
        self.output_24_hour_forecast(idx, variable, default)

    def forecast_period(self, idx_list, variable=False, default=False):
        """
        metode som henter ut verdier gjennom de neste to påfølgende dagene.
        regner ut gjennomsnittet gjennom hele dagen, og mellom fire intervaller
        som defineres i forkant.
        
        args:
            idx_list (list): nested liste med index
            variable (list): liste med variabler, bare nødvendig for 
                             bruk av ekstra variabler 
            default (bool): ikke nødvendig å røre
        """
        
        if variable is False:
            default = True
            variable = ['air_temperature']
            self.res = np.zeros((10, 3))
        else:
            self.res = np.zeros((10, len(variable)))
    
        for v_itr, variable_key in enumerate(variable):
            min_statement, max_statement = self.check_min_max_key(variable_key)
            tot = []
            for count, idx in enumerate(idx_list): # n iteration            
                temp = []
                self.loop_main_body(variable_key, idx, temp)
      
                if min_statement:
                    self.res[count, v_itr] = min(temp)
                    self.allocate_result(temp, tot, count, v_itr, 
                                         min_=True, min_max=True)
                    continue
                        
                if max_statement:
                    self.res[count, v_itr] = max(temp)
                    self.allocate_result(temp, tot, count, v_itr, 
                                         max_=True, min_max=True)
                    continue
                
                if default is True:
                    self.res[count, 1:] = min(temp), max(temp)
               
                self.allocate_result(temp, tot, count, v_itr)
                if (count + 1) % 4 == 0:
                    tot = []

    def output_24_hour_forecast(self, idx, variable, default=False):
        """
        skriver ut resultatet for forecast_24_hours.
        
        args:
            idx (array): array med index
            variable (list): liste med variabler
            default (bool): trenger ikke å røres
        """
        
        if default is True:
            print('\nTemperatur f', end='')
        else:
            print()
            for i_, i in enumerate(variable):
                print(f'{i:<29}', end='')
                if (i_ + 1) % 2 == 0:
                    print()
                else:
                    print(',', end=' ')
            print('\nF', end='')
            
        print(f'or {self.sted_navn} '
              f'{self.next_day.replace("-", ".")}:', end='')
        
        if default:
            print('\n')
        else:
            print(f'\n{"-"*60}')
        
        for i_, i in enumerate(idx):
            time = self.format_date(self.table[i]['time'])[1][:-3]
            
            if default:
                print(f'kl {time} {self.res[i_, 0]:>5} grader')
                continue
            
            print(f'\nkl {time}:')
            for v_count, variable_type in enumerate(variable):
                print(f'\t{variable_type:<29} {self.res[i_, v_count]:>6} '
                      f'{self.unit_dict[variable_type]:<5}')
        return    

    def default_period_output(self, time_list, date_list):
        """
        skriver ut resultatet for forecast_period, uten ekstra variabler.
        
        args:
            time_list (list): liste med timer
            date_list (list): liste datoer
        """
        
        res = self.res
        for i_, i in enumerate(date_list):
            I = i_ * 4
            print(f'\n{i} (snittemperatur {res[-2 + i_, 0]} grader):')
            for j in range(0 + I, 4 + I):
                print(f'{time_list[j]}: fra {res[j, 1]:>5} til {res[j, 2]:>5} '
                      f'grader (snittemperatur {res[j, 0]} grader)')
        return
    
    def complex_period_output(self, time_list, date_list, variable):
        """
        skriver ut resultatet for forecast_period, med ekstra variabler.
        
        args:
            time_list (list): liste med timer
            date_list (list): liste datoer
            variable (list): liste med variabler
        """
        
        for I, i in enumerate(date_list):
            print(f'{"-"*42}\n\n{i} gjennomsnitt:')
            for n, K in enumerate(self.res[(I > 3) - 2]):
                print(f'\t{variable[n]} {K} {self.unit_dict[variable[n]]}')
            
            print(f'\t{"-"*38}\n')
            for j in range(4):
                J = j + I * 4
                
                print(f'kl {time_list[J]} gjennomsnitt:')
                for idx, k in enumerate(variable):
                    print(f'\t{k}: {self.res[J, idx]} {self.unit_dict[k]}')            
                print()
        return                                  

if __name__ == '__main__':
    weather = Weather_forecast()
from sys import exit

def check_valid_format(ekstra=False):
    """
    sjekker om ønsket format er gyldig.
    
    args:
        ekstra (bool): bestemmer om 'ekstra' skal bli foreslått som gyldig.
    
    returns:
        str: gyldig format
    """
    
    method = ['enkel', 'periode', 'ekstra']
    if ekstra:
        del(method[-1])
    
    print('\nvelg mellom følgende format, eller help for mer informasjon:')
    for j, i in enumerate(method):
        if i == method[-1]:
            print(f'{i}', end=': ')
        else:
            print(f'{i}', end=', ')
    
    user_input = input().lower() 
    while not user_input in method:
        if user_input.lower() == 'close' or user_input.lower() == '':
            print('\nIngen variabler ble gitt, avslutter handlingen.')
            exit()
        elif user_input.lower() == 'help':
            format_help_description()
        else:
            print('\nUgyldig format. Tast inn gyldig format:', end=' ')
        user_input = input().lower()
    return user_input

def initiate_additional_variables(unit_key, full_messages=True):
    """
    spør om hvilke variabler som er ønkset å bruke, og få informasjon om.
    
    args:
        unit_key (list): liste med keys
        full_messages (bool): sett til False under debugging
    
    returns:
        list: liste med variabler
    """
    
    message = str(
        '\nTast inn "help" for ekstra innstrukser og full oversikt over'
        '\nvariabler som kan velges, eller "close" for å avbryte '
        'handlingen.\n\nVariabler å velge mellom: lufttrykk_ved_havnivå, '
        'lufttemperatur, \n\t\tnedbørsmengde, vindhastighet, '
        'duggpunkt_temperatur\n\nTast inn variabler som skal brukes: ')
    
    if full_messages is True:
        print(message, end=' ')
    
    user_input = input()
    if user_input == 'all':
        return unit_key 
    
    not_valid = True
    while not_valid:
        if user_input.lower() == 'close' or user_input.lower() == '':
            print('\nIngen variabler ble gitt, avslutter handlingen.')
            exit()
        if user_input.lower() == 'help':
            user_input = help_function()
            continue
        
        variable = user_input.replace(',', ' ').split() 
        variable = translate_variables(variable)
        if len(variable) != 0:
            not_valid = False
        else:
            print('Tast inn gyldige variabler:', end=' ')
            user_input = input()
    return variable        


def check_correct_interval_time(x, message):
    """
    ser om et gitt tall er mer enn 0, og mindre enn 18.
    
    args:
        x (int): interval
        message (str): egen beskjed dersom x ikke oppfyller kriteriene
    
    returns:
        x (int): interval
        eller ber om nytt forslag
    """
    
    if 0 < x < 18:
        return x
    else:
        print(message, end=' ')
        return input()
    
def check_individual_interval(x, message):
    """
    sjekker om x er (int)
    
    args:
        x (int): interval
        message (str): egen beskjed dersom x ikke oppfyller kriteriene
    
    returns:
        int: x
    """
    
    while not(isinstance(x, int)):        
        try:
            x = int(x)
        except:
            if x.lower() in 'stop':
                exit()
            print(message, end='')
            x = input()
    return x

def interval_nested_loop(interval, temp_val, idx):
    """
    ser om interval er et helt tall, (int), om det er likt som tidligere
    interval, og at det er innenfor visse tidspunkter.
    
    args:
        interval (int): interval
        temp_val (int): bruk dersom det er andre interval som skal sjekkes
        idx (int): index
    
    returns:
        int: interval
    """
    
    msg_1 = str('\nUgyldig input, ikke et helt tall.\nSkriv'
                ' enten "stop" for å avbryte, eller et nytt tall: ')
    
    msg_2 = '\nUgyldig input, må være fra 1 til 17: '
    
    msg_3 = str('\nUgyldig input, tidspunkt 2 kan ikke være det '
                'samme som tidspunkt 1.\nVelg nytt tidspunk:')
    
    while not(isinstance(interval, int)):
        interval = check_individual_interval(interval, msg_1)
        
        if isinstance(interval, int):
            interval = check_correct_interval_time(interval, msg_2)
                                                        
        if temp_val == interval and idx == 1:
            print(msg_3, end=' ')
            interval = input()  
    return interval

def check_valid_intervals():
    """
    spør om to ulike intervaller og returnerer dem i stigende rekkefølge.
    
    returns:
        list: liste med intervallene
    """
    
    interval_list = []
    temp_val = 0 
    
    print('velg to ulike tidspunkter fra 1 til 17:')
    for i in range(2):
        print(f'\ntidspunkt {i + 1}: ', end='')
        temp_val = interval = interval_nested_loop(input(), temp_val, i)
        interval_list.append(interval)
    
    interval_list.sort()
    return interval_list



def format_help_description():
    """
    funksjon med ekstra beskrivelse om formatene
    """
    
    print('\nmer informasjon om formatene')
    print('enkel: tidsspenn på første påfølgende dag, og gir '
          'temperaturen fra \nkl 00:00 til og med 23:00.')
    
    print('\nperiode: tidsspenn på de to påfølgende dagene, og gir'
          ' min, maks, og\ngjennomsnitt temperatur for hver dag.'
          ' hver dag blir også delt opp i\nfire perioder, som er '
          'bestemt av brukeren. min, maks og gjennomsnitt\n'
          'temperatur blir gjitt for disse periodene.')
    
    print('\nekstra: formatet gir mulighet til å velge flere/færre variabler '
          'og\nreturnerer det på samme måte som enkel, eller periode.')
    print('\nvelg ønsket format:', end=' ')

def help_function():
    """
    funksjon med ekstra beskrivelse om de ulike variablene som kan brukes
    og hvordan det skal skrives inn.
    
    returns:
        str: input fra bruker
    """
    
    message = str('\nSkriv komma (,) mellom hver enkelt variabel ved bruk av '
                  'flere enn en.\n'
                  '\nEksempel: variabel_1, variabel_2, variabel_3'
                  '\nFull liste av variabler som kan brukes:'
                  '\n\tlufttrykk_ved_havnivå'
                  '\n\tlufttemperatur'
                  '\n\tlufttemperatur_maks'
                  '\n\tlufttemperatur_min'
                  '\n\tpersentil_for_lufttemperatur_10'
                  '\n\tpersentil_for_lufttemperatur_90'
                  '\n\tskyområdefraksjon'
                  '\n\tskyområdefraksjon_høy'
                  '\n\tskyområdefraksjon_Lav'
                  '\n\tskyområdefraksjon_middels'
                  '\n\tduggpunkt_temperatur'
                  '\n\tfraktion_av_tåkeareal'
                  '\n\tnedbørsmengde'
                  '\n\tnedbørsmengde_maks'
                  '\n\tnedbørsmengde_min'
                  '\n\tsannsynlighet_for_nedbør'
                  '\n\tsannsynlighet_for_torden'
                  '\n\trelativ_fuktighet'
                  '\n\tultrafiolett_indeks_klar_himmel'
                  '\n\tvind_fra_retning'
                  '\n\tvindhastighet'
                  '\n\tvindhastighet_av_vindkast'
                  '\n\tvindhastighet_persentil_10'
                  '\n\tvindhastighet_persentil_90\n'
                  '\nTast inn variabler som skal brukes:')
    print(message, end=' ')
    return input()

def reverse_translate():
    """
    funksjon som inneholder et dictionary av variablene oversatt fra
    engelsk til norsk
    
    returns:
        dict: variable_dict
    """
    
    variable_dict = {
        'air_pressure_at_sea_level': 'lufttrykk_ved_havnivå',
        'air_temperature': 'lufttemperatur',
        'air_temperature_max': 'lufttemperatur_maks',
        'air_temperature_min': 'lufttemperatur_min',
        'air_temperature_percentile_10': 'persentil_for_lufttemperatur_10',
        'air_temperature_percentile_90': 'persentil_for_lufttemperatur_90',
        'cloud_area_fraction': 'skyområdefraksjon',
        'cloud_area_fraction_high': 'skyområdefraksjon_høy',
        'cloud_area_fraction_low': 'skyområdefraksjon_Lav',
        'cloud_area_fraction_medium': 'skyområdefraksjon_middels',
        'dew_point_temperature': 'duggpunkt_temperatur',
        'fog_area_fraction': 'fraktion_av_tåkeareal',
        'precipitation_amount': 'nedbørsmengde',
        'precipitation_amount_max': 'nedbørsmengde_maks',
        'precipitation_amount_min': 'nedbørsmengde_min',
        'probability_of_precipitation': 'sannsynlighet_for_nedbør',
        'probability_of_thunder': 'sannsynlighet_for_torden',
        'relative_humidity': 'relativ_fuktighet',
        'ultraviolet_index_clear_sky': 'ultrafiolett_indeks_klar_himmel',
        'wind_from_direction': 'vind_fra_retning',
        'wind_speed': 'vindhastighet',
        'wind_speed_of_gust': 'vindhastighet_av_vindkast',
        'wind_speed_percentile_10': 'vindhastighet_persentil_10',
        'wind_speed_percentile_90': 'vindhastighet_persentil_90'}
    return variable_dict

def translated_variable_dict():
    """
    funksjon som inneholder et dictionary av variablene oversatt fra
    norsk til engelsk
    
    returns:
        dict: variable_dict
    """
    
    variable_dict = {
        'lufttrykk_ved_havnivå': 'air_pressure_at_sea_level',
        'lufttemperatur': 'air_temperature',
        'lufttemperatur_maks': 'air_temperature_max',
        'lufttemperatur_min': 'air_temperature_min',
        'persentil_for_lufttemperatur_10': 'air_temperature_percentile_10',
        'persentil_for_lufttemperatur_90': 'air_temperature_percentile_90',
        'skyområdefraksjon': 'cloud_area_fraction',
        'skyområdefraksjon_høy': 'cloud_area_fraction_high',
        'skyområdefraksjon_Lav': 'cloud_area_fraction_low',
        'skyområdefraksjon_middels': 'cloud_area_fraction_medium',
        'duggpunkt_temperatur': 'dew_point_temperature',
        'fraktion_av_tåkeareal': 'fog_area_fraction',
        'nedbørsmengde': 'precipitation_amount',
        'nedbørsmengde_maks': 'precipitation_amount_max',
        'nedbørsmengde_min':'precipitation_amount_min',
        'sannsynlighet_for_nedbør': 'probability_of_precipitation',
        'sannsynlighet_for_torden': 'probability_of_thunder',
        'relativ_fuktighet': 'relative_humidity',
        'ultrafiolett_indeks_klar_himmel': 'ultraviolet_index_clear_sky',
        'vind_fra_retning': 'wind_from_direction',
        'vindhastighet': 'wind_speed',
        'vindhastighet_av_vindkast': 'wind_speed_of_gust',
        'vindhastighet_persentil_10': 'wind_speed_percentile_10',
        'vindhastighet_persentil_90': 'wind_speed_percentile_90'}
    return variable_dict

def not_found_variables(variable, total):
    """
    ser tilbakemelding om hvor mange variabler og hvilke som var ugyldige.
    
    args:
        variable (list): liste med variabler som ble avvist
        total (int): totalt antall variabler 
    """
    
    n = len(variable)
    print(f'\nFølgende {n} av {total} variabler var ugyldige:')
    for i in variable:
        print(f'\t{i}')
    print()

def translate_variables(variable):
    """
    tar inn liste av variabler og ser hvilker som kan bli funnet fra 
    værdataene, og filtrerer ut de som ikke kan bli funnet.
    
    args: 
        variable (list): liste med variabler
    
    returns:
        list: liste med variabler
    """
    
    if variable == 'help':
        return []
    
    variable_dict = translated_variable_dict()
    variable_list = []
    not_valid = []
    
    for i in variable:
        if i in variable_dict:
            variable_list.append(variable_dict[i])
        else:
            not_valid.append(i)
    
    if len(not_valid) != 0:
        not_found_variables(not_valid, len(variable))
    return variable_list

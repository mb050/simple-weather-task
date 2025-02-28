# Værdata
Enkel oppgave om å hente ut værdata og gi været for den påfølgende dagen
time for time, eller de neste to påfølgende dagene fordelt på fire
intervaller. 

**libraries som må lastes ned i forkant.**
  - [geopy](https://pypi.org/project/geopy/)
  - [request](https://pypi.org/project/requests/)

værdata.py og utility.py må være i samme mappe, og forbindelse
til internett er også nødvendig. koden kjøres fra værdata.py
og instrukser blir gitt underveis. 

### Formatene:
Det er to primære formater en kan velge mellom, og et tredje alternativ som bygger på de primære formatene.

**enekel:**

Gir temperaturen time for time fra kl 00:00 til kl 23:00 for den påfølgende dagen.

**periode:**

går over de neste to påfølgende dagene, og gir gjennomsnitt temperatur for begge dagene. 
Brukeren blir spurt om å gi to tidspunkter og dagene blir delt inn i fire mindre intervaller.

Disse intervallene er som følger:
  - fra kl 00:00 til **tidspunkt_1**
  - fra **tidspunkt_1** til **tidspunkt_2**
  - fra **tidspunkt_2** til kl 18:00
  - fra kl 18:00 til kl 00:00.

hver av intervallene vil gi følgende informasjon, min og maks temperatur og gjennomsnitt temperatur.

**ekstra:**

dette formatet bruker enten *enkel* eller *periode*, men vil ikke nødvendighvis gi temperatur, og min maks for *periode*.
man får mulighet til å velge en rekke variabler som blir presentert på tilsvarende vis som det valgte formatet.

variablene som kan velges er som følger:
  - air_pressure_at_sea_level
  - air_temperature
  - air_temperature_max
  - air_temperature_min
  - air_temperature_percentile_10
  - air_temperature_percentile_90
  - cloud_area_fraction
  - cloud_area_fraction_high
  - cloud_area_fraction_low
  - cloud_area_fraction_medium
  - dew_point_temperature
  - fog_area_fraction
  - precipitation_amount
  - precipitation_amount_max
  - precipitation_amount_min
  - probability_of_precipitation
  - probability_of_thunder
  - relative_humidity
  - ultraviolet_index_clear_sky
  - wind_from_direction
  - wind_speed
  - wind_speed_of_gust
  - wind_speed_percentile_10
  - wind_speed_percentile_90



# main
from checks import validate
import folium
import pandas as pd
import json
from folium import plugins

ARCHIVE_OPTION = '2'
archive = {'1': 'DL_FIRE/fire_nrt_V1_90807.csv', ARCHIVE_OPTION: 'DL_FIRE/fire_archive_V1_90807.csv'}

def main():
    selectArchive = input("Select 1 for current or 2 for archive: ")
    assert selectArchive != '1' or selectArchive != '2', "invalid option"
    currentdate = input("Set date (YYYY-MM-DD) to print: ")
    if not validate(currentdate):
        currentdate = '2019-07-01'
    df = pd.read_csv(archive[selectArchive])
    
    #initialize the map around LA County @-17.3946009,-66.1548812,16.25
    laMap = folium.Map(location=[-17.3946009,-66.1548812], tiles='Stamen Toner', zoom_start=9)

    #add the shape of LA County to the map
    #folium.GeoJson(laArea).add_to(laMap)

    #filter data getting 2019-10-25
    if selectArchive == ARCHIVE_OPTION:
        mask = ((df['latitude'] < 0) & (df['longitude'] < 0) & (df['acq_date'] == currentdate))
    else: 
        mask = ((df['latitude'] < 0) & (df['longitude'] < 0) & (df['acq_date'] == currentdate) & (df['daynight'] == 'D'))
    subset = df.loc[mask]

    #for each row in the Starbucks dataset, plot the corresponding latitude and longitude on the map
    for i,row in subset.iterrows():
        print(row.latitude, row.longitude)
        folium.CircleMarker((row.latitude,row.longitude), radius=3, weight=2, color='red', fill_color='red', fill_opacity=.5).add_to(laMap)
    print('Ready to show: ', len(subset))
    #save the map as an html    
    laMap.save('laPointMap.html')

if __name__ == '__main__':
    main()

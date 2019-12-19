# main
import folium
import pandas as pd
import json
from folium import plugins

def main():
    print("main")
    # df = pd.read_csv('starbucksInLACounty.csv')
    df = pd.read_csv('DL_FIRE/fire_nrt_V1_90807.csv', low_memory=False)
    print("after read csv")
    with open('laMap.geojson') as f:
        laArea = json.load(f)
    print("after open")

    #initialize the LA County map
    laMap = folium.Map(location=[-17.3946009,-66.1548812], tiles='Stamen Toner', zoom_start=9)
    print("after folium map")
    #add the shape of LA County to the map
    #folium.GeoJson(laArea).add_to(laMap)
    print("after geoJson")

    #filter data getting 2019-10-25
    mask = ((df['latitude'] < 0) & (df['longitude'] < 0) & (df['acq_date'] == '2019-10-01') & (df['daynight'] == 'D'))
    subset = df.loc[mask]

    #for each row in the Starbucks dataset, plot the corresponding latitude and longitude on the map
    for i,row in subset.iterrows():
        print(row.latitude, row.longitude)
        folium.CircleMarker((row.latitude,row.longitude), radius=3, weight=2, color='red', fill_color='red', fill_opacity=.5).add_to(laMap)
    print("ready to print: ", len(subset))
    #add the heatmap. The core parameters are:
    #--data: a list of points of the form (latitude, longitude) indicating locations of Starbucks stores

    #--radius: how big each circle will be around each Starbucks store

    #--blur: the degree to which the circles blend together in the heatmap

    laMap.add_child(plugins.HeatMap(data=df[['latitude', 'longitude']].values, radius=25, blur=10))

    #save the map as an html
    laMap.save('laHeatmap.html')

if __name__ == "__main__":
    main()

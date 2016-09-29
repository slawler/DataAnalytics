
def df_to_geojson(df, properties, lat= 'positionlatitude', lon='positionlongitude'):
    # create a new python dict to contain our geojson data, using geojson format
    geojson = {'type':'FeatureCollection', 'features':[]}

    # loop through each row in the dataframe and convert each row to geojson format
    for _, row in df.iterrows():
        # create a feature template to fill in
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}

        # fill in the coordinates
        feature['geometry']['coordinates'] = [row[lon],row[lat]]

        # for each column, get the value and add it as a new feature property
        for prop in properties:
            feature['properties'][prop] = row[prop]
        
        # add this feature (aka, converted dataframe row) to the list of features inside our dict
        geojson['features'].append(feature)
    
    return geojson
    
df.columns = df.columns.droplevel()
df.columns = df.columns.astype(str)    
    
df['positionlatitude']= df['positionlatitude'].round(5).astype(float)
df['positionlongitude'] = df['positionlongitude'].round(5).astype(float)   
df['speedThroughWater'] = df['speedThroughWater'].round(1).astype(str)
df['speedOverGround'] = df['speedOverGround'].round(1).astype(str)
df['windspeedApparent'] = df['windspeedApparent'].round(1).astype(str) 
df['windangleApparent'] = df['windangleApparent'].round(0).astype(str) 

 
cols = ['speedOverGround', 'speedThroughWater','windspeedApparent' ,'windangleApparent']
df_subset = df[cols]

df_geo.tail()


geojson = df_to_geojson(df_geo, cols)

output_file = 'SailData.GeoJSON'
with open(output_file, 'w') as gjout:
    json.dump(geojson,gjout, indent=2,ensure_ascii=True)
    
# how many features did we save to the geojson file?
print('{} geotagged features saved to file'.format(len(geojson['features'])))


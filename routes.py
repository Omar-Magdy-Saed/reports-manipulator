import pandas as pd
import json
with open('connections.json', 'r') as file:
    json_data = json.load(file, strict=False)

df3 = pd.read_excel("Trail names.xlsx")
# print(df3['Frequency'])
# print(type(df3['Frequency']))
df3['Frequency'] =df3['Frequency'].astype(str)
# print(df3['Frequency'].dtypes)
mapping_dict_Freq = dict(zip(df3['Name'], df3['Frequency']))
mapping_dict_FromSites = dict(zip(df3['Name'], df3['From Node #1']))
mapping_dict_ToSites = dict(zip(df3['Name'], df3['To Node #1']))
df_Mapping = pd.read_excel("OTS-Mapping.xlsx")
mapping_dict = dict(zip(df_Mapping['OTS'], df_Mapping['Section']))
mapping_dict1 = dict(zip(df_Mapping['OTS'], df_Mapping['A Site']))
mapping_dict2 = dict(zip(df_Mapping['OTS'], df_Mapping['Z Site']))
trails = list(df3['Name'].values)
# print(trails)
df = pd.json_normalize(json_data)
connections = json_data['Response']['All_connections']
connectionsDataDict = {str(connection['connectionData'][0].get('CONNECTIONNAME', 0)): connection['connectionData'][0] for connection in connections if 'connectionData' in connection and connection['connectionData']}
routeDataDict = {int(connection['connectionData'][0].get('CONNECTIONID', 0)): connection['routeData'] for connection in connections if 'routeData' in connection and connection['routeData']}
# route = pd.DataFrame(routeDataDict)       
# route.to_excel('output1.xlsx', index=False)
routes = list({})
End_Points = {}
for trailname in trails:
    
    connectiondata = connectionsDataDict.get(trailname, {})
    connectionid = connectiondata['CONNECTIONID']

    routeData = routeDataDict.get(connectionid, {})
    server=[]
    for item in routeData:
        if item['CONTAINERTYPE'] == 'ots':
            routes.append({trailname : item['SERVERLINKNAME']})
            # server.append(item['SERVERLINKNAME'])
        elif item['CONTAINERTYPE'] == 'os':
            server.append( item['SERVERLINKNAME'])

    
    End_Points[trailname] = server
routes_New = [(key, value) for d in routes for key, value in d.items()]
End_Points_df = pd.DataFrame.from_dict(End_Points , orient= 'index')
End_Points_df.to_excel('end_points.xlsx')
df_trails = pd.DataFrame(routes_New , columns=['OTU Designation', 'OTS'] )
df_trails['DWDM Section Name'] = df_trails['OTS'].map(mapping_dict)
df_trails['A Site'] = df_trails['OTS'].map(mapping_dict1)
df_trails['Z Site'] = df_trails['OTS'].map(mapping_dict2)
df_trails['Channel Name(Wavelength Only)'] = (df_trails['OTU Designation'].map(mapping_dict_Freq))
df_trails['Channel Name(Wavelength Only)'] = df_trails['Channel Name(Wavelength Only)'].apply(lambda x: '%.3f' % float(x))
df_trails['Channel Name(Wavelength Only)-1'] = "1" + df_trails['Channel Name(Wavelength Only)']
speed_of_light = 299792470
df_trails['Channel Name(Wavelength Only)-1'] = df_trails['Channel Name(Wavelength Only)-1'].apply(lambda x: '%.2f' % (int(speed_of_light / (float(x) * 10) * 100) / 100.0))
print(df_trails['Channel Name(Wavelength Only)-1'] )
df_trails['From Node #1'] = df_trails['OTU Designation'].map(mapping_dict_FromSites)
df_trails['To Node #1'] = df_trails['OTU Designation'].map(mapping_dict_ToSites)
df_trails.to_excel('routes.xlsx' , index=False)
import pandas as pd

import re
df_sites = pd.read_excel("sections.xlsx")
df_routes = pd.read_excel('routes.xlsx')
df3 = pd.read_excel("Trail names.xlsx")
trails = list(df3['Name'].values)

sites_naming_Mapping = {}
sites_naming_Mapping_Full = {}
Connection_naming_Mapping = {}


# def extract_full_match(phrase):
#     # Define the regular expression pattern
#     pattern = r'M96ND02-\w+-NE\w+'
    
#     # Use re.search to find the match
#     match = re.search(pattern, phrase)
    
#     # Return the matched string if found
#     if match:
#         return match.group(0)
#     else:
#         return None
pattern = r'-RK\d+/'
pattern2 = r'-ACCESS\d+-|-METRO-'
add_site = lambda x: x if 'M96ND02-' in x else 'M96ND02-' + x
for _ , r in df_sites.iterrows():
    Src = r['DWDM Section Name'].split(' - ')[0]
    Src = re.split(pattern , Src)[0]
    # Src = extract_full_match(Src)
    Src = re.sub(pattern2 ,'-' ,Src)
    Dest = r['DWDM Section Name'].split(' - ')[1]
    Dest = re.split(pattern , Dest)[0]
    Dest = re.sub(pattern2 ,'-' , Dest)
    
    Src = add_site(Src)
    
    Dest = add_site(Dest)
    
    # Dest = extract_full_match(Dest)
    Src_App = r['A Site'].split('/')[1]
    Dest_App = r['Z Site'].split('/')[1]
    sites_naming_Mapping[Src] = Src_App
    sites_naming_Mapping[Dest] = Dest_App
    sites_naming_Mapping_Full[Src] = r['A Site']
    sites_naming_Mapping_Full[Dest] = r['Z Site']
df_routes['From Node #1 _new'] = df_routes['From Node #1'] .map(sites_naming_Mapping_Full)
df_routes['To Node #1_new'] = df_routes['To Node #1'] .map(sites_naming_Mapping_Full)
df_routes['From Node #1'] = df_routes['From Node #1'] .map(sites_naming_Mapping)
df_routes['To Node #1'] = df_routes['To Node #1'] .map(sites_naming_Mapping)
# df_Sites_Mapping  = pd.DataFrame.from_dict(sites_naming_Mapping)
# df_Sites_Mapping.to_excel('Sites_Mapping.xlsx')
# # for key , value in sites_naming_Mapping.items():
#     print(key ,' : ' ,value)


def find_route(src, dest ,df_new):
    route = [src]
    current_site = src
    
    test = 0
    while current_site != dest:
        next_row = df_new[(df_new['A Site'].str.contains(current_site, regex=False)) | (df_new['Z Site'].str.contains(current_site, regex=False))]
        next_site_row_index = next_row.index[0]
        next_site = next_row['A Site'].values[0] if next_row['A Site'].values[0].split('/')[1] != current_site else next_row['Z Site'].values[0]
        route.append(next_site.split('/')[1])
        
        current_site = next_site.split('/')[1]
        df_new.drop(index=next_site_row_index, inplace=True)
        # if current_site == 'BXA': test+=1
        # print(current_site)
        # if current_site == 'BXA' and test == 2: break
    
    return '-'.join(route)
for connectionNAME in trails:
    filtered_df = df_routes[df_routes['OTU Designation'] == connectionNAME]
    # routes = filtered_df['Route'].tolist()
    # print (connectionNAME)
    final_route = find_route(filtered_df['From Node #1'].values[0] , filtered_df['To Node #1'].values[0] , filtered_df)
    Connection_naming_Mapping[connectionNAME] = final_route
    # print(f"The route for {connectionNAME} is: {final_route}")
df_routes['OTU Designation_new'] = df_routes['OTU Designation'].map(Connection_naming_Mapping)
df_routes['Channel Name(Wavelength Only)'] = df_routes['Channel Name(Wavelength Only)'].apply(lambda x: '%.3f' % float(x))
speed_of_light = 299792470
df_routes['Channel Name(Wavelength Only) 2'] = ('1'+df_routes['Channel Name(Wavelength Only)']).apply(lambda x: '%.2f' % (int(speed_of_light / (float(x) * 10) * 100) / 100.0))
df_routes['OTU Designation_new'] = 'M96ND02 CH' + df_routes['Channel Name(Wavelength Only)'].astype(str)+ ' ' + df_routes['From Node #1'] +'-' + df_routes['To Node #1'] + " (" + df_routes['OTU Designation_new'] + ")"
rate = '100G'
rate_mapping ={}
for _,r in df_routes.iterrows():
    container = df3[df3['Name'] == r['OTU Designation']]['Rate'].values[0]
    # print(r['OTU Designation'],container)
    if container == 'OTU4x2':
        rate = '200G'
        # print(r['OTU Designation'],rate)
        rate_mapping[r['OTU Designation']] =rate
    elif container == 'OTU4':
        rate = '100G'
        # print(r['OTU Designation'],rate)
        rate_mapping[r['OTU Designation']] =rate
    elif container == 'OTSig':
        rate = df3[df3['Name'] == r['OTU Designation']]['Line Mode Profile Description'].values[0].split(" via ")[0]
        rate_mapping[r['OTU Designation']] =rate
        # print(r['OTU Designation'],rate)
df_routes['rate'] = df_routes['OTU Designation'].map(rate_mapping)
df_routes['OTU Designation_new'] =df_routes['OTU Designation_new'] + " " + df_routes['rate']
Connection_naming_Mapping_new = dict(zip(df_routes['OTU Designation'], df_routes['OTU Designation_new']))
df_routes.to_excel('New_Routes.xlsx')

# df_end_points = pd.read_excel('end_points_details.xlsx')
# row = 1
# df_end_points_new = pd.DataFrame(columns=['row','OTU Designation','Port','number'])
# df_end_points['Connection Name'] = df_end_points['Connection Name'].map(Connection_naming_Mapping_new)
# df_ports_a = df_end_points.melt(id_vars=['Connection Name', 'Src_NE'], value_vars=['Src_OT', 'Src_MSC/PSC'], var_name='column', value_name='port')
# df_ports_b = df_end_points.melt(id_vars=['Connection Name', 'Dest_NE'], value_vars=['Dest_MSC/PSC', 'Dest_OT'], var_name='column', value_name='port')

# # Rename the site columns to be consistent
# df_ports_a.rename(columns={'Src_NE': 'sitename'}, inplace=True)
# df_ports_b.rename(columns={'Dest_NE': 'sitename'}, inplace=True)

# # Combine the melted results
# df_combined = pd.concat([df_ports_a, df_ports_b])

# # Sort the DataFrame to ensure correct order
# # df_combined.sort_values(by=['Connection Name', 'column'], inplace=True)

# # Add the 'order' column
# df_combined['order'] = df_combined.groupby('Connection Name').cumcount() + 1

# # Drop the 'column' as it's no longer needed
# df_combined.drop(columns=['column'], inplace=True)

# # Reset the index
# df_combined.reset_index(drop=True, inplace=True)


# df_combined.to_excel('end_points_new_details.xlsx')




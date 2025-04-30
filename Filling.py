import pandas as pd

df_DNIC_OTULink = pd.read_excel('DNIC_OTULink_2 sheets _test.xlsx' , sheet_name='OTU Ports Assignment')

end_points_details = pd.read_excel('end_points_new_details.xlsx')


end_points_details['shelf Number'] = end_points_details['port'].str.split('-').str[0]
end_points_details['sitename'] = end_points_details['sitename'] + '-' + end_points_details['shelf Number']
df_missing = pd.DataFrame(columns=['Legacy Name' , 'Port Name' , 'OTU Designation' , 'Sequence'])
for _ , r in end_points_details.iterrows():
    
    if int(r['shelf Number']) <= 24:
        Slot = 'SL'+r['port'].split('-')[1]
    else :
        Slot = r['port'].split('-')[1]
    port_name = r['port'].split('-')[2]
    has_letters = any(char.isalpha() for char in port_name)
    has_digits = any(char.isdigit() for char in port_name)
    if has_letters and has_digits :
        if 'L' in port_name:
            condition = (df_DNIC_OTULink['Legacy Name'] == r['sitename']) & (df_DNIC_OTULink['Slot/Card'] == Slot) & (df_DNIC_OTULink['Port Name'].str.contains(port_name))
        else:
            condition = (df_DNIC_OTULink['Legacy Name'] == r['sitename']) & (df_DNIC_OTULink['Slot/Card'] == Slot) & (df_DNIC_OTULink['Port Name'] == r['port'])
    else :
        condition = (df_DNIC_OTULink['Legacy Name'] == r['sitename']) & (df_DNIC_OTULink['Parent Slot/card'] == Slot) & (df_DNIC_OTULink['Port Name'] == r['port'])
    if condition.any() :
        # print ('Done')
        df_DNIC_OTULink.loc[condition, 'OTU Designation'] = r['Connection Name']
        df_DNIC_OTULink.loc[condition, 'Sequence'] = r['order']
        df_DNIC_OTULink.loc[condition, 'Select Leg (Main/Protection)'] = 'Main'
    else :
        new_row = {'Legacy Name' : r['sitename'] , 'Port Name' : r['port'] , 'OTU Designation' : r['Connection Name'] , 'Sequence' : r['order']}
        df_missing = df_missing.append( new_row , ignore_index =True)   
        print (r['sitename'] , ' has Port ' , r['port'] , ' not found')

df_missing.to_excel('missing Ports.xlsx',index=False)
with pd.ExcelWriter('DNIC_OTULink_2 sheets _test.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df_DNIC_OTULink.to_excel(writer, sheet_name='OTU Ports Assignment', index=False)
import pandas as pd

end_points_df = pd.read_excel('end_points_1.xlsx')
df_trails_new = pd.read_excel('Trail Names.xlsx')
SiteA_Maping = dict(zip(df_trails_new['Name'], df_trails_new['From Node #1']))
SiteZ_Maping = dict(zip(df_trails_new['Name'], df_trails_new['To Node #1']))
rate_Maping = dict(zip(df_trails_new['Name'], df_trails_new['Rate']))
df_Result = pd.DataFrame(columns =['Connection Name' , 'Src_NE', 'Src_OT', 'Src_MSC/PSC' , 'Dest_NE' , 'Dest_MSC/PSC' , 'Dest_OT' ])
end_points_df['From Node #1'] = end_points_df['Connection Name'].map(SiteA_Maping)
end_points_df['To Node #1'] = end_points_df['Connection Name'].map(SiteZ_Maping)
end_points_df['Rate'] = end_points_df['Connection Name'].map(rate_Maping)
def swap_values(row):
    value_to_check = row['From Node #1']
    if value_to_check not in row['SRC']:
        if value_to_check in row['DEST']:
            row['SRC'], row['DEST'] = row['DEST'], row['SRC']
            print(row['Connection Name'])
    return row

# Apply the function to each row
end_points_df = end_points_df.apply(swap_values, axis=1)
def check_rate(rate,OT):
    if rate == 'OTU4x2' :
        return OT.split('-')[0] + '-' + OT.split('-')[1] + '-' + OT.split('-')[2] + '-L' + OT.split('-')[3]
    else:
        return OT
for _, r in end_points_df.iterrows():
    # df_Result['Connection Name'] = r['Connection Name']
    # df_Result['Src_NE'] = r['SRC'].split('/')[0]
    # df_Result['Dest_NE'] = r['DEST'].split('/')[0]
    Src_Aend = r['SRC'].split('/')[1]

    Src_Zend = r['SRC'].split('/')[2]
    
    Dest_Aend = r['DEST'].split('/')[1]
    Dest_Zend = r['DEST'].split('/')[2]
    
    if 'PSC' in Src_Aend or 'MCS' in Src_Aend :
        src_Psc = Src_Aend
        src_ot = Src_Zend
        src_ot = check_rate(r['Rate'] , src_ot)
    else:
        src_Psc = Src_Zend
        src_ot  = Src_Aend
        src_ot = check_rate(r['Rate'] , src_ot)
    if 'PSC' in Dest_Aend or 'MCS' in Dest_Aend :
        dest_Psc = Dest_Aend
        dest_ot = Dest_Zend
        dest_ot = check_rate(r['Rate'] , dest_ot)
    else:
        dest_Psc = Dest_Zend
        dest_ot = Dest_Aend
        dest_ot = check_rate(r['Rate'] , dest_ot)
    
    new_row = {'Connection Name' : r['Connection Name'] , 'Src_NE' : r['SRC'].split('/')[0] ,'Dest_NE':r['DEST'].split('/')[0],
                'Src_OT' : '-'.join(src_ot.split('-')[1:]), 'Src_MSC/PSC': '-'.join(src_Psc.split('-')[1:]) ,
               'Dest_MSC/PSC' : '-'.join(dest_Psc.split('-')[1:]), 'Dest_OT' : '-'.join(dest_ot.split('-')[1:])}
    df_Result = df_Result.append(new_row,ignore_index =True)

df_Result.to_excel('end_points_details.xlsx')


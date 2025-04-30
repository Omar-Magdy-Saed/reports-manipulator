import pandas as pd


df_Physical = pd.read_csv("PhysicalConns.csv")
df_Section = pd.read_excel("DNIC_OTULink.xlsx" , sheet_name='Full DWDM Sections List')
df = pd.DataFrame(columns=['OTS', 'Section' , 'A Site' , 'Z Site'])
# AEnd = df_Physical["From NE/Port #1"]
# ZEnd = df_Physical["To NE/Port #1"]
for _ , OTS in df_Physical.iterrows():
    Aend = OTS["From NE/Port #1"]
    Zend = OTS["To NE/Port #1"]
    X= '-'.join(OTS["From NE/Port #1"].split('/')[0].split('-')[1:])
    Y = str(OTS["From NE/Port #1"].split('/')[1].split('-')[1])
    X1 = '-'.join(OTS["To NE/Port #1"].split('/')[0].split('-')[1:])
    Y1 = str(OTS["To NE/Port #1"].split('/')[1].split('-')[1])
    # print(X)
    pattern1 = rf'{X}.*/SH{Y}'
    pattern2 = rf'{X1}.*/SH{Y1}'
    mask = df_Section['DWDM Section Name'].str.contains(pattern1) & df_Section['DWDM Section Name'].str.contains(pattern2)
    
    matching_rows = df_Section.loc[mask, ['DWDM Section Name', 'A Site' , 'Z Site']]

    if not matching_rows.empty :
        
        new_row = {'OTS' :OTS['Name'], 'Section': matching_rows['DWDM Section Name'].values[0],'A Site' :matching_rows['A Site'].values[0],'Z Site' : matching_rows['Z Site'].values[0]}
    
        df = df.append(new_row,ignore_index =True)   
    else:
        print(pattern1,pattern2)
        print(OTS['Name'])
df.to_excel('OTS-Mapping.xlsx',index=False)


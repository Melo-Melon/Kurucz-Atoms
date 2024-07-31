import pandas as pd
#Remember change file name, deal with files, and change the mapping table each time.

#Ti skip-row 1
element = "K-I"
AGA_file_w = "Kurucz-" + element + "/AGAFGFy.csv"
AGA_file_z = "Kurucz-" + element + "/AGAFGFz.csv"
States_to_trans = "Kurucz-" + element + "/States_Final.csv"
output_filename = "Kurucz/Kurucz" + element +".trans"

column_name = ["wl","wn(cm-1)","log_gf","log_f","log_fe","log_A","log_gA","ele","E1","J1","label1","E2","J2","label2"]
Trans_n_A_w = pd.read_csv(AGA_file_w,names=column_name,skiprows=1)

#Solve J2 problem
# Trans.loc[0,"J2"]= 2.5
# Trans["J2"] = Trans["J2"].astype(float)

States = pd.read_csv(States_to_trans)
#print(States.head())
Trans_n_A_w["E1"] =Trans_n_A_w["E1"].abs()
Trans_n_A_w["E2"] =Trans_n_A_w["E2"].abs()
Trans_n_A_w = Trans_n_A_w.merge(States[["Index","E","J","label"]],left_on=["E1","J1","label1"],
                        right_on=["E","J","label"],how="left").rename(columns = {"Index":"Index1"})

Trans_n_A_w = Trans_n_A_w.merge(States[["Index","E","J","label"]],left_on=["E2","J2","label2"],
                        right_on=["E","J","label"],how="left").rename(columns = {"Index":"Index2"})


Trans_n_A_w = Trans_n_A_w.drop(columns=['E_x', 'J_x', 'label_x', 'E_y', 'J_y', 'label_y'])


cols = list(Trans_n_A_w.columns)
cols.insert(cols.index('E1'), cols.pop(cols.index('Index1')))
cols.insert(cols.index('E2'), cols.pop(cols.index('Index2')))
Trans_n_A_w = Trans_n_A_w[cols]

Trans_n_A_w["A(10base)"] = 10 ** Trans_n_A_w["log_A"]
Trans_n_A_w.drop(["log_A"],axis=1,inplace=True)

Trans_n_A_w.drop(["wl","log_gf","ele","E1","J1","label1","E2","J2","label2","log_f","log_fe","log_gA"]
                 ,axis=1,inplace=True)

order = ["Index1","Index2","A(10base)","wn(cm-1)"]
Trans_n_A_w = Trans_n_A_w[order]
Trans_n_A_w = Trans_n_A_w.sort_values(by="wn(cm-1)",ascending=True)

print(Trans_n_A_w)


column_name = ["wl","wn(cm-1)","log_gf","log_f","log_fe","log_A","log_gA","ele","E1","J1","label1","E2","J2","label2"]
Trans_n_A_z = pd.read_csv(AGA_file_z,names=column_name,skiprows=1)

States = pd.read_csv(States_to_trans)
#print(States.head())
Trans_n_A_z["E1"] =Trans_n_A_z["E1"].abs()
Trans_n_A_z["E2"] =Trans_n_A_z["E2"].abs()
Trans_n_A_z = Trans_n_A_z.merge(States[["Index","E","J","label"]],left_on=["E1","J1","label1"],
                        right_on=["E","J","label"],how="left").rename(columns = {"Index":"Index1"})

Trans_n_A_z = Trans_n_A_z.merge(States[["Index","E","J","label"]],left_on=["E2","J2","label2"],
                        right_on=["E","J","label"],how="left").rename(columns = {"Index":"Index2"})


Trans_n_A_z = Trans_n_A_z.drop(columns=['E_x', 'J_x', 'label_x', 'E_y', 'J_y', 'label_y'])


cols = list(Trans_n_A_z.columns)
cols.insert(cols.index('E1'), cols.pop(cols.index('Index1')))
cols.insert(cols.index('E2'), cols.pop(cols.index('Index2')))
Trans_n_A_z = Trans_n_A_z[cols]

Trans_n_A_z["A(10base)"] = 10 ** Trans_n_A_z["log_A"]
Trans_n_A_z.drop(["log_A"],axis=1,inplace=True)

Trans_n_A_z.drop(["wl","log_gf","ele","E1","J1","label1","E2","J2","label2","log_f","log_fe","log_gA"]
                 ,axis=1,inplace=True)

order = ["Index1","Index2","A(10base)","wn(cm-1)"]
Trans_n_A_z = Trans_n_A_z[order]
Trans_n_A_z = Trans_n_A_z.sort_values(by="wn(cm-1)",ascending=True)

print(Trans_n_A_z)

combined_df = pd.concat([Trans_n_A_z,Trans_n_A_w])
combined_df = combined_df.drop_duplicates()

combined_df["Index2"] = combined_df["Index2"].fillna(-1).astype(int)
combined_df["Index1"] = combined_df["Index1"].fillna(-1).astype(int)

combined_df = combined_df.sort_values(by="wn(cm-1)",ascending=True)

print(combined_df)

#
# #-1 represent not found in level

#

format_str = "{:>12d}{:>1}{:>12d}{:>1}{:>10.4e}{:>1}{:>15.6e}\n"

output_file = output_filename
with open(output_file, 'w') as f:
    for index, row in combined_df.iterrows():
        f.write(format_str.format(
            int(row['Index1']),'', int(row['Index2']),'',
            row['A(10base)'],'', row['wn(cm-1)']
        ))

print(f"Data has been written to {output_file}")





import pandas as pd

element = "Ba"
output_filename = "Kurucz/" + element +"_Kurucz.trans"
column_names= ["Index1","Index2","A(10base)","wn(cm-1)"]
df = pd.read_csv(output_filename, delim_whitespace=True, names=column_names)

print(len(df))

output_filename = "Kurucz/" + element +"+_Kurucz.trans"
column_names= ["Index1","Index2","A(10base)","wn(cm-1)"]
df = pd.read_csv(output_filename, delim_whitespace=True, names=column_names)

print(len(df))

import urllib.request
from bs4 import BeautifulSoup
import csv
from io import StringIO
import pandas as pd


ael1500_url = "http://kurucz.harvard.edu/atoms/5601/partfn5601.dat"
res = urllib.request.urlopen(ael1500_url)

data = res.read()
data = data.decode("utf-8")
soup = BeautifulSoup(data,features="html.parser")


path = "Kurucz-Ba-II/PF.csv"

pf_column_specification = [(0, 5), (5, 12), (12, 22), (22, 32)]
pf_df = pd.read_fwf(StringIO(soup.get_text()), colspecs=pf_column_specification)
pf_df.to_csv(path,index=False)


read_range = list(range(2,4))
column_name = ["T","-500"]
PF = pd.read_csv(path,usecols= read_range,names=column_name,skiprows=2)
print(PF)


format_str = "{:>8.1f}{:>1}{:>15.4f}\n"

output_file = 'Kurucz/KuruczBaII.pf'
with open(output_file, 'w') as f:
    for index, row in PF.iterrows():
        f.write(format_str.format(
            row['T'],'', row['-500']
        ))

print(f"Data has been written to {output_file}")










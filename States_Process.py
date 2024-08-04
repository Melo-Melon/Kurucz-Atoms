
import pandas as pd
import re

#This python file mainly serves for the .states processing based on the .gam and lifetime files.
#Remember change atom names,(remove top part in gam and lifetime file) and change the mapping table each time.
#For multiple .gam files, remember to add suffix.
element = "Ne-II"
states_file = "Kurucz-" + element + "/GAM.csv"
Life_file = "Kurucz-" + element + "/LIFE.csv"
States_to_trans = "Kurucz-" + element + "/States_Final.csv"
output_filename = "Kurucz/Kurucz" + element +".states"


# Here is the mapping table, this could be found on top of each .gam file in kurucz atomic database.
mapping = """
1 s2p5      2 s2p4 3p   3 s2p4 4p   4 s2p4 5p   5 s2p4 6p   6 s2p4 7p   
7 s2p4 8p   8 s2p4 9p   9 s2p4 10p  A s2p4 11p  B s2p4 12p  C s2p4 4f   
D s2p4 5f   E s2p4 6f   F s2p4 7f   G s2p4 8f   H s2p4 9f   I s2p4 10f  
J s2p4 11f  K s2p4 12f  L s2p4 6h   M s2p4 7h   N s2p4 8h   O s2p4 9h   
P s2p4 8k   Q s2p4 9k   R sp5 3s    S sp5 4s    T sp5 5s    U sp5 6s    
V sp5 7s    W sp5 8s    X sp5 9s    Y sp5 10s   Z sp5 11s   a sp5 12s   
b sp5 3d    c sp5 4d    d sp5 5d    e sp5 6d    f sp5 7d    g sp5 8d    
h sp5 9d    i sp5 10d   j sp5 11d   k sp5 12d   l           m           
n           o           p           q           r           s               
t           u           v           w           x           y           
z           !           "           #           $           %           
&           '           (           )           *           +           
,           -           .           /           :           ;           
<           =           >           ?           @           [           
\           ]           ^           _           `           {           
|           }           ~           0           
1 s2p4 3s   2 s2p4 4s   3 s2p4 5s   4 s2p4 6s   5 s2p4 7s   6 s2p4 8s   
7 s2p4 9s   8 s2p4 10s  9 s2p4 11s  A s2p4 12s  B s2p4 3d   C s2p4 4d   
D s2p4 5d   E s2p4 6d   F s2p4 7d   G s2p4 8d   H s2p4 9d   I s2p4 10d  
J s2p4 11d  K s2p4 12d  L s2p4 5g   M s2p4 6g   N s2p4 7g   O s2p4 8g   
P s2p4 9g   Q s2p4 7i   R s2p4 8i   S s2p4 9i   T sp6       U sp5 3p    
V sp5 4p    W sp5 5p    X sp5 6p    Y sp5 7p    Z sp5 8p    a sp5 9p    
b sp5 10p   c sp5 11p   d sp5 12p   e sp5 4f    f sp5 5f    g sp5 6f    
h sp5 7f    i sp5 8f    j sp5 9f    k sp5 10f   l sp5 11f   m sp5 12f   
n           o           p           q           r           s           
t           u           v           w           x           y           
z           !           "           #           $           %              
"""

# The mapping table has two version, one is for odd and one is for even.
# If the .gam starts with an odd state, then the mapping table will also begin with odd. Vice versa.
# Use the first mapping in the bottom's mapping time as a split word.

##start with odd
eve_1 = "1 s2p4 3s"
odd_part, eve_part = mapping.split(eve_1)
eve_part = eve_1 + eve_part

##start with eve
# odd_1 = "1 s2p4 3s"
# eve_part, odd_part = mapping.split(odd_1)
# odd_part = odd_1 + odd_part




# Here we read the .gam files and then remove duplicates.
column_name = ["ELEM","Index","E","J","label","g_lande"]
states = pd.read_csv(states_file,names= column_name)

states.drop(["Index"],axis=1,inplace=True)
states.drop_duplicates(inplace=True)
states.reset_index(drop=True, inplace=True)
index = range(1,len(states)+1)
index = pd.DataFrame(index,columns=["Index"])
states = pd.concat([index,states],axis = 1)

# g_j is computed and uncertainty is assigned with 0.1 as default
states["g_j"] = 2 * states["J"] + 1
states["g_j"] = states["g_j"].astype(int)
states["Uncertainty"] = 0.1

# Here we read in the lifetime file and remove duplicates. Lifetime is turned from ns to s to fit exomol format.
column_name = ["ELEM","Index","E","J","label","SUM_A","Life1","Life(ns)"]
life = pd.read_csv(Life_file,names= column_name)

life.drop(["SUM_A","Life1","ELEM","Index"],axis=1,inplace=True)

life.drop_duplicates(inplace=True)
life.reset_index(drop=True, inplace=True)
life["Life(s)"] = life["Life(ns)"] / 1e9
life.drop(["Life(ns)"],axis=1,inplace=True)


#Lifetime is merged with the states based on E, J, label.
combined_df = states.merge(life[['E', 'J', 'label', 'Life(s)']],
                           on=['E', 'J', 'label'],
                           how = 'left')

#For some atoms that do not have lifetime provided, use nan for lifetime column.
# states["Life(s)"] = float("nan")
# combined_df = states.copy()

order = ['Index','ELEM', 'E', 'g_j', 'J', 'Uncertainty', 'Life(s)', 'g_lande', 'label']
combined_df = combined_df[order]


#Abbr is given to distinguish if the states is caculated or observed. If observed, use NI. Else, use CA.
combined_df['Abbr'] = combined_df['E'].apply(lambda x: 'CA' if x < 0 else 'NI')
combined_df["E"] = combined_df["E"].abs()

def match_table(part):
    lines = part.splitlines()
    mapping = {}
    for line in lines:
        if line.strip():
            entries = line.split()
            i = 0
            while i < len(entries):
                if len(entries[i]) == 1:
                    key = entries[i]
                    value = []
                    i += 1
                    while i < len(entries) and len(entries[i]) != 1:
                        value.append(entries[i])
                        i += 1
                    mapping[key] = ' '.join(value)
    return mapping


mapping_even = match_table(eve_part)
mapping_odd = match_table(odd_part)


# Here, we start to split the labels into Configuration and Terms.
# The detail spliting cases are given in the report and github page.
configuration_list = []
term_list = []
for index, row in combined_df.iterrows():
    label = row["label"]
    elem = row["ELEM"][-3:]
    parts = label.split()
    if len(parts) == 2:
        config, possible_term = parts
        if config.endswith("nd"):
            configuration = "unknown"
            term = "unknown"
        elif possible_term.isdigit():
            configuration = config[:-2]
            term = config[-2:]
            if elem in ['EVE', 'ERz', 'EPo']:
                configuration = mapping_even.get(configuration[0], configuration[0]) + configuration[1:]
            elif elem in ['ODD', 'ORz', 'OPo']:
                configuration = mapping_odd.get(configuration[0], configuration[0]) + configuration[1:]
        else:
            configuration = config
            term = possible_term

    elif len(parts) == 3:
        config_1, config_2,pos_term = parts
        configuration = config_1 + config_2
        term = pos_term

    else:
        if len(label)>=4 and label[-4].isupper():
            configuration = label[:-5]
            term = label[-5:-3]
            if elem in ['EVE', 'ERz', 'EPo']:
                configuration = mapping_even.get(configuration[0], configuration[0]) + configuration[1:]
            elif elem in ['ODD', 'ORz', 'OPo']:
                configuration = mapping_odd.get(configuration[0], configuration[0]) + configuration[1:]
        elif '?' in label[-4:-1]:
            configuration,term = label.split('?')[0], label.split('?')[1]
        else:
            configuration = "unknown"
            term = "unknown"

    if len(term) == 3:
        if re.match(r'^[a-zA-Z]\d[a-zA-Z]$', term):
            term = f"{term[0]}({term[1:]})"
    configuration = configuration.replace(' ','')

    configuration_list.append(configuration)
    term_list.append(term)
combined_df['Configuration'] = configuration_list
combined_df['Term'] = term_list

#Here, we remove those rows with unknown labels. States are sorted based on Energy level. The first lifetime will be infinity always.
combined_df = combined_df[(combined_df['Configuration']!='unknown') & (combined_df["Term"] != 'unknown')]
combined_df = combined_df.sort_values(by = "E", ascending= True)
combined_df.at[0, 'Life(s)'] = float('inf')

combined_df.drop(["Index"],axis=1,inplace=True)
combined_df.insert(0, 'Index', range(1, len(combined_df) + 1))
#combined_df = pd.concat([index,combined_df],axis = 1)

# The reason I save .csv for states here is that the original label is much eaiser for mapping in trans files.
combined_df_alter = combined_df.copy()
combined_df_alter.drop(["ELEM","Configuration","Term"],axis=1,inplace=True)
combined_df_alter.to_csv(States_to_trans,index=False)
#combined_df_alter.to_csv("Kurucz-Si-I/States_Final.csv",index=False)
print("Saved Done")


combined_df = combined_df.drop(columns=['label','ELEM'])

order = ['Index', 'E', 'g_j', 'J', 'Uncertainty', 'Life(s)', 'g_lande', 'Configuration','Term','Abbr']
combined_df = combined_df[order]

#The following code reformat the states data into the Exomol format.

def format_energy(value):
    int_part = len(str(abs(int(value))))
    if int_part > 5:
        return f"{value:12.5f}"
    else:
        return f"{value:12.6f}"

if combined_df["J"].iloc[0].is_integer():
    format_str = ("{:>12d} {:>12} {:>6d} {:>7d} {:>12.6f} {:>12.4e} {:>10.6f} {:<12} {:<7} {:>2}\n")
else:
    format_str = ("{:>12d} {:>12} {:>6d} {:>7.1f} {:>12.6f} {:>12.4e} {:>10.6f} {:<12} {:<7} {:>2}\n")
# Write the DataFrame to a text file with the specified format
output_file = output_filename
#output_file = 'Kurucz/KuruczBaII.states'
with open(output_file, 'w') as f:
    for index, row in combined_df.iterrows():
        f.write(format_str.format(
            row['Index'], format_energy(row['E']), row['g_j'], row['J'],
            row['Uncertainty'], row['Life(s)'], row['g_lande'],
            row['Configuration'], row['Term'],row["Abbr"]
        ))

print(f"Data has been written to {output_file}")























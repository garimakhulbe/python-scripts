import pandas as pd
import numpy as np
import sys
import datetime

start = datetime.datetime.now()

def notNA(s):
  return s != 'NA' and s != ''


# Reading input values.
print("reading input file...")
print(sys.argv[1])

inputFile =  str(sys.argv[1])
outputFile = str(sys.argv[2])
# Read csv 
df_data = pd.read_csv(inputFile, low_memory=False)
print('columns before adding DX and PR:'+str(len(df_data.columns)))

a = np.zeros(shape=(len(df_data.index),670))
b = np.zeros(shape=(len(df_data.index),231))


df_dxs = pd.DataFrame(a,columns=['DXCCS_'+str(i) for i in range(1,671)])
df_prs = pd.DataFrame(b,columns=['PRCCS_'+str(i) for i in range(1,232)])

df =  pd.concat([df_data,df_dxs,df_prs], axis=1)
print('rows:'+str(len(df.index)))
df = df.drop(['o_diag_p', 'o_proc_p','osrcroute', 'osrcsite', 'osrclicns'], axis=1)
print('columns after adding 671+231 columns:' + str(len(df.columns)))


df_cols = df.columns.tolist()
dxColumns = [ z for z in df_cols if ((z.find('odiag') >= 0) or (z.find('diag_p') >= 0)) ]
prColumns = [ z for z in df_cols if ((z.find('oproc') >= 0) or (z.find('proc_p') >= 0)) ]

df[dxColumns] = df[dxColumns].fillna(0)
df[prColumns] = df[prColumns].fillna(0)

df[dxColumns] = df[dxColumns].astype(int)
df[prColumns] = df[prColumns].astype(int)

# for i in range(0, len(df.index)):
#   df.ix[i]['oproc15']
#   type(df.ix[i][c])
# for i in range(0, len(df.index)):
#   print('------ row'+str(i))
#   for c in dxColumns:
#     print(df.ix[i][c])
#     print(type(df.ix[i][c]))
#     print(c)
#     print(np.isfinite(df.ix[i][c]))


for i, row in df.iterrows():
  print(i)
  d = set(['DXCCS_'+str(row[c]) for c in dxColumns if row[c]!=0 ])
  p = set(['PRCCS_'+str(row[c]) for c in prColumns if row[c]!=0 ])
  l = d.union(p)
  df.ix[i, l] = 1

print('writing in outfile:'+outputFile)
df.to_csv(outputFile+'.csv', cols=df.columns.tolist(), index=False)

data = df[df.columns[(df != 0).any()]]
print(len(data.columns))
f = open('Cols.txt', 'w')
print('columns after removing all zeros columns:' + str(len(data.columns)))
f.write(str(data.columns.tolist()))
f.close()

print('writing in outfile with all zeros columns:'+outputFile)
df.to_csv(outputFile+'_delallZeroes.csv', cols=df.columns.tolist(), index=False)

end  = datetime.datetime.now()
print(end - start)  

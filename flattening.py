import pickle
import sys
import datetime


start = datetime.datetime.now()
# Read input and output file names. args[0] is script name.
inputFile = str(sys.argv[1])
outputFile = str(sys.argv[2])
print(inputFile)
print(outputFile)
# inputFile = "test_final.csv"
# outputFile = "final_output.csv"
f = open(inputFile, 'r')

line = f.readline().strip('\n').replace('"', '')
items = line.split(',')

# Creating hashmap for column names.
col = dict()
for i in range(len(items)):
  col[items[i]] = i;

def parse(item):
  if item.find('"') >= 0:
    # it is a string, possibly a date or empty
    return item.replace('"', '')
  elif item == 'NA':
    # it is NA without double quote
    return 'NA'
  elif item.find('.') >= 0:
    # it is a decimal
    return float(item)
  else:
    # it should be an integer, let it throw if it isn't
    return item


# below code will convert csv to python object
data = []
while (True):
  line = f.readline()
  if not line:
    break
  datum=[]
  for item in line.strip('\n').split(','):
    datum.append(parse(item));
  data.append(datum)

f.close()

print(len(data))

def notNA(s):
  return s != 'NA' and s != ''


for row in data:
  for item in col.items():
    if (((item[0].find('odiag') >= 0) or (item[0].find('diag_p') >= 0)) and notNA(row[item[1]])):
      row[col['DXCCS_' + str(row[item[1]])]] = 1


# data = []
# i = 0
# while (i < 10):
#   line = f.readline()
#   if not line:
#     break
#   datum=[]
#   for item in line.strip('\n').split(','):
#     datum.append(parse(item));
#   data.append(datum)
#   i = i +1

# for item in col.items():
#   item


f = open(outputFile, 'w')
items = list(col.items())
items.sort(key = lambda item: item[1])
f.write(','.join(['"' + item[0] + '"' for item in items]) + '\n')

def serialize(item):
  if item == 'NA':
    # it is NA, just return NA without quotes
    return 'NA'
  elif isinstance(item, str):
    # it is a string other than NA, possible empty, add double quotes
    return '"' + item + '"'
  else:
    # it should be an number, convert to str without quotes
    return str(item)

f.writelines([(','.join([serialize(item) for item in row]) + '\n') for row in data])
f.close()

end  = datetime.datetime.now()
print(end - start)  

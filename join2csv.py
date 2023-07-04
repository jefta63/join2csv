import sys

RED = '\033[31m'
GREEN = '\033[32m'

if len(sys.argv) < 3:
   print (f'Must include filenames.\nUsage: {RED}join2csv.py file1 file2')
   sys.exit()

file1,file2 = sys.argv[1],sys.argv[2]

try:
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines_f1 = f1.read().splitlines()
        lines_f2 = f2.read().splitlines()
except:
    print(f'{RED}Something\'s wrong with file(s) or don\'t exists!')
    sys.exit()

f3 = open("joined.csv", 'a')

remark = 0
q = ["\"",""]
c = ","
num_cols = len(lines_f1[0].split(c))
header = lines_f1[0].replace(*q)
last_col = header[header.rfind(c)+1:]
new_header = header + c + last_col + "_New"
f3.write(new_header + '\n')

f1_ids = [i.replace(*q).split(c)[0] for i in lines_f1[1:]]
f2_ids = [i.replace(*q).split(c)[0] for i in lines_f2[1:]]

only_in_f1 = [x for x in f1_ids if x not in f2_ids]
only_in_f2 = [x for x in f2_ids if x not in f1_ids]

for i in lines_f1[1:]:
    row1 = i.replace(*q)
    id1 = row1.split(c)[0]
    for j in lines_f2[1:]:
        row2 = j.replace(*q)
        id2 = row2.split(c)[0]
        if id1 == id2:
            new_row = row1 + c + row2.split(c)[num_cols-1]
            f3.write(new_row+ '\n')
    if id1 in only_in_f1:
        f3.write(row1+ ",0" + '\n')
for k in lines_f2[1:]:
    row3 = k.replace(*q)
    col_new = row3.split(c)[num_cols-1]
    id3 = row3.split(c)[0]
    row3_new = []

    if id3 in only_in_f2:
        for n in range(num_cols-1):
            row3_new.append(row3.split(c)[n])
        row3_new.append('0')
        row3_new.append(col_new)
        remark = 1
        f3.write(','.join(row3_new) + '\n')
f3.close()
print (f'Successfully joined {file1} and {file2} in {GREEN}joined.csv {RED}{"New rows added!" if remark == 1 else ""}')
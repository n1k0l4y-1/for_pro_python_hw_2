import csv
import re

with open("phonebook_raw.csv", 'r', encoding="utf8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

notebook = []

pattern_fio = r'(^[А-Я]\w+) ?,?(\w+) ?,?(\w+)?'
subst_pattern_fio = r'\1,\2,\3'

for i in contacts_list:
    i = list(dict.fromkeys(i))
    i.remove('') if i.count('') else ''
    result = re.sub(pattern_fio, subst_pattern_fio, ','.join(i))
    notebook.append(result)

pattern_num_phone = r'(\+7|8) ?\(?(\d{3})\)?-? ?(\d{3})\-? ?(\d{2})-? ?(\d{2}) ?\(?(доб\.)? ?(\d+)?(\))?'
subst_pattern_num = r'+7(\2)\3-\4-\5 \6\7'

for i, j in enumerate(notebook):
    j = j.split(',')
    result = re.sub(pattern_num_phone, subst_pattern_num, ','.join(j))
    notebook[i] = result

notebook_dict = {}

for _ in notebook:
    if list(notebook_dict.keys()).count(','.join(_.split(',')[0:2])):
        notebook_dict[','.join(_.split(',')[0:2])] += f",{','.join(_.split(',')[2:])}"
    else:
        notebook_dict.setdefault(','.join(_.split(',')[0:2]), ','.join(_.split(',')[2:]))

notebook_sort = []
for i, j in notebook_dict.items():
    notebook_sort.append(list(i.split(',')) + list(j.split(',')))

notebook_final = []
for i in notebook_sort:
    i = list(dict().fromkeys(i))
    for j in i:
        if j[0] == '+':
            if j.count('доб'):
                i.append(i.pop(i.index(j)))
            else:
                if j.count(' '):
                    i.append(i.pop(i.index(j)).replace(' ', ''))

    for k in i:
        if k.count('@'):
            i.append(i.pop(i.index(k)))

    notebook_final.append(i)

pattern_final = r'([А-Я]\w+),(\w+),(\w+),(\w+),([А-Яа-яA-za-z –]+)?([0-9\+\(\)-]+ ?\w+\.?\d+)'
subst_pattern_final = r'\1,\2,\3,\4,\5,\6'
sorted_list = []

for i in notebook_final:
    result = re.sub(pattern_final, subst_pattern_final, ','.join(i))
    sorted_list.append(result.split(','))

with open("phonebook.csv", "w", encoding="utf8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(sorted_list)
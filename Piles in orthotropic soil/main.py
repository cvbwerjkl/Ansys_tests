# Results processing

import matplotlib.pyplot as plt

n0 = {}
n1 = {}
n2 = {}
n3 = {}
n11 = {}
n22 = {}
x = []
y = []
z = []

with open('nlist.txt') as f:
    for k in f:
        d = k.split()
        if 3 < len(d) < 5 and d[0].isdigit():
            n0[int(d[0])] = [float(d[1]), float(d[2])]

# print(len(n0))

with open('1.txt') as f:
    for k in f:
        d = k.split()
        if len(d) > 6 and d[0].isdigit():
            if int(d[0]) in n0:
                n1[int(d[0])] = [n0[int(d[0])][0], n0[int(d[0])][1], float(d[3])]

with open('2.txt') as f:
    for k in f:
        d = k.split()
        if len(d) > 3 and d[0].isdigit():
            if int(d[0]) in n0:
                n11[int(d[0])] = [n0[int(d[0])][0], n0[int(d[0])][1], float(d[3])]

i = 0
with open('pile_pos.txt') as f:
    for k in f:
        d = k.split()
        n2[i] = [float(d[0]), float(d[1]), 0, 0]
        i += 1

# print(n1)
# print(n2)
# print(len(n1), " ", len(n2))

for j in n1:
    for k in n2:

        xx = (n1[j][0] - n2[k][0]) ** 2
        yy = (n1[j][1] - n2[k][1]) ** 2
        # print(n1[j][0], " ", n2[k][0])
        # print(n1[j][1], " ", n2[k][1])
        # print("x=", xx, " y=", yy)
        #if ((xx + yy) ** 0.5) < 0.9:
        # print(" d = ", (xx + yy) ** 0.5)
        if (xx + yy) ** 0.5 < 1.1:
            n2[k] = [n2[k][0], n2[k][1], n2[k][2] + n1[j][2], n2[k][3] + 1]

for j in n11:
    for k in n2:
        xx = (n11[j][0] - n2[k][0]) ** 2
        yy = (n11[j][1] - n2[k][1]) ** 2
        # print(n1[j][0], " ", n2[k][0])
        # print(n1[j][1], " ", n2[k][1])
        # print("x=", xx, " y=", yy)
        # if ((xx + yy) ** 0.5) < 0.9:
        # print(" d = ", (xx + yy) ** 0.5)
        if (xx + yy) ** 0.5 < 1.1:
            n22[k] = [n2[k][0], n2[k][1], n2[k][2] + n11[j][2], n2[k][3] + 1]

# print(n2)

for k in n2:
    x.append(n2[k][0])
    y.append(n2[k][1])
    n3[k] = [((n2[k][2] / n2[k][3] * 3.14) - (n22[k][2] / n22[k][3] * 3.14)) / (n2[k][2] / n2[k][3] * 3.14) * 100,
             (n2[k][2] / n2[k][3] * 3.14), (n22[k][2] / n22[k][3] * 3.14)]
    z.append(n3[k][0])

# print(n2)
# print(len(z))

with open("output.txt", "w") as f:
    for i in n3:
        ss = str(i) + ' ' + str(n3[i][0]) + ' ' + str(n3[i][1]) + ' ' + str(n3[i][2])
        print(ss, file=f)

fig = plt.figure(1)

s = plt.scatter(x, y, c=z, cmap='Spectral', marker='o', s=50)

cb = plt.colorbar(s)

plt.show()

# for settlement analysis

Sett1 = {}  # библиотека перемещений 1
Sett2 = {}  # библиотека перемещений 2
DicNX = {}  # библиотека координат Х всех узлов фундамента
DicNY = {}  # библиотека координат У всех узлов фундамента

with open('nlist2.txt') as f:
    for k in f:
        d = k.split()
        if 3 < len(d) < 5 and d[0].isdigit():
            DicNX[int(d[0])] = float(d[1])
            DicNY[int(d[0])] = float(d[2])

# print(DicNX)

with open('1s.txt') as f:
    for k in f:
        d = k.split()
        if len(d) == 2 and d[0].isdigit():
            # print(float(d[1]))
            if int(d[0]) in DicNY:
                Sett1[int(d[0])] = float(d[1])

# print(Sett1)

with open('2s.txt') as f:
    for k in f:
        d = k.split()
        if len(d) == 2 and d[0].isdigit():
            if int(d[0]) in DicNY:
                Sett2[int(d[0])] = float(d[1])
# print(Sett1)

# определение махимальной относительной разности осадок 1
AngDist = 0
DicAngular = 0
DicAngularN = ''
file_out = 'out1.txt'
for keyX in DicNX:
    XXfirst = DicNX[keyX]
    YYfirst = DicNY[keyX]
    for keyY in DicNY:
        XXsecond = DicNX[keyY]
        YYsecond = DicNY[keyY]
        Ldif = (((XXfirst - XXsecond) ** 2) + ((YYfirst - YYsecond) ** 2)) ** 0.5
        # print (str(Ldif))
        if Ldif > 2 and Ldif < 7:
            DifSett = abs(float(Sett1[keyX]) - float(Sett1[keyY]))
            AngDistset = (DifSett / 1) / Ldif
            # maximum
            if AngDistset >= DicAngular:
                DicAngular = AngDistset
                DicAngularN = str(XXfirst) + ' ' + str(YYfirst) + ' ' + str(keyX) + ' ' + str(XXsecond) + ' ' + str(
                    YYsecond) + ' ' + str(keyY) + ' ' + str(Ldif)

# Запись в текстовые файлы
with open(file_out, 'w') as ouf:
    ouf.write('AngularDis Max = ' + str(DicAngular) + '\n')
    ouf.write('AngularDis Max info ' + DicAngularN + '\n')
    ouf.write('MaxSet ' + str(min(Sett1.values())) + '\n')
    ouf.write('AvgSet ' + str(sum(Sett1.values()) / len(Sett1)) + '\n')


# определение махимальной относительной разности осадок 1
AngDist = 0
DicAngular = 0
DicAngularN = ''
file_out2 = 'out2.txt'
for keyX in DicNX:
    XXfirst = DicNX[keyX]
    YYfirst = DicNY[keyX]
    for keyY in DicNY:
        XXsecond = DicNX[keyY]
        YYsecond = DicNY[keyY]
        Ldif = (((XXfirst - XXsecond) ** 2) + ((YYfirst - YYsecond) ** 2)) ** 0.5
        # print (str(Ldif))
        if Ldif > 2 and Ldif < 7:
            DifSett = abs(float(Sett2[keyX]) - float(Sett2[keyY]))
            AngDistset = (DifSett / 1) / Ldif
            # maximum
            if AngDistset >= DicAngular:
                DicAngular = AngDistset
                DicAngularN = str(XXfirst) + ' ' + str(YYfirst) + ' ' + str(keyX) + ' ' + str(XXsecond) + ' ' + str(
                    YYsecond) + ' ' + str(keyY) + ' ' + str(Ldif)

# Запись в текстовые файлы
with open(file_out2, 'w') as ouf:
    ouf.write('AngularDis Max = ' + str(DicAngular) + '\n')
    ouf.write('AngularDis Max info ' + DicAngularN + '\n')
    ouf.write('MaxSet ' + str(min(Sett2.values())) + '\n')
    ouf.write('AvgSet ' + str(sum(Sett2.values()) / len(Sett2)) + '\n')

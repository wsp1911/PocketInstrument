import os

data = ["" for _ in range(18)]

data[0] += "011001110000" + "1111"
data[0] = hex(int(data[0], 2))
# print(data[0])

data[1] = "0x0d8C"
data[2] = "0x0016"

serial = "1234"
data[3] = hex(ord(serial[0])) + hex(2 * len(serial) + 2)[2:]
if len(data[3]) == 5:
    data[3] = data[3][:4] + "0" + data[3][4]
n = 0
for i in range(1, len(serial), 2):
    if i < len(serial) - 2:
        data[4] += hex(ord(serial[i + 1])) + hex(ord(serial[i]))[2:] + ", "
    elif i == len(serial) - 2:
        data[4] += hex(ord(serial[i + 1])) + hex(ord(serial[i]))[2:]
    else:
        data[4] += "0x00" + hex(ord(serial[i]))[2:]
    n += 2
for i in range(n, 12, 2):
    data[4] += ", 0x0000"
print(data[3] + ", " + data[4])

string = "EE Pocket Instrument"
data[5] = hex(ord(string[0])) + hex(2 * len(string) + 2)[2:]
if len(data[5]) == 5:
    data[5] = data[5][:4] + "0" + data[5][4]
n = 0
for i in range(1, len(string), 2):
    if i < len(string) - 2:
        data[6] += hex(ord(string[i + 1])) + hex(ord(string[i]))[2:] + ", "
    elif i == len(string) - 2:
        data[6] += hex(ord(string[i + 1])) + hex(ord(string[i]))[2:]
    else:
        data[6] += "0x00" + hex(ord(string[i]))[2:]
    n += 2
for i in range(n, 30, 2):
    data[6] += ", 0x0000"
print(data[5] + ", " + data[6])

man_string = "C-Media Electronics Inc."
data[7] = hex(ord(man_string[0])) + hex(2 * len(man_string) + 2)[2:]
if len(data[7]) == 5:
    data[7] = data[7][:4] + "0" + data[7][4]
n = 0
for i in range(1, len(man_string), 2):
    if i < len(man_string) - 2:
        data[8] += hex(ord(man_string[i + 1])) + hex(ord(man_string[i]))[2:] + ", "
    elif i == len(string) - 2:
        data[8] += hex(ord(man_string[i + 1])) + hex(ord(man_string[i]))[2:]
    else:
        data[8] += "0x00" + hex(ord(man_string[i]))[2:]
    n += 2
for i in range(n, 30, 2):
    data[8] += ", 0x0000"
print(data[7] + ", " + data[8])

data[9] += "0000000"  # DAC initial volume, 7 bit
# data[9] += "1111111"

data[9] += "011111"  # ADC initial volume, 6 bit
# data[9] += "000000"
data[9] += "1" + "1" + "1"
data[9] = hex(int(data[9], 2))
# print(data[9])

data[10] += "00000"  # AA initial volume, 5 bit
data[10] += "0" + "1" + "0" + "0" + "0"
data[10] += "0"  # MIC High Pass Filter
data[10] += "0"
data[10] += "0"  # MIC Boost
data[10] += "0" + "1" + "0"

data[10] = hex(int(data[10], 2))
# print(data[10])


def NOT(s):
    res = []
    for each in s[2:]:
        res.append("1" if each == "0" else "0")
    s = "".join(res)
    if len(s) < 8:
        s = "1" * (8 - len(s)) + s
    return "0b" + s


def dec2hex(n):
    if n >= 0:
        return hex(n) + "00"
    else:
        return hex(int(NOT(bin(-n)), 2) + 1) + "00"


# default values
# data[11] = dec2hex(-37)  # DAC min
# data[12] = dec2hex(0)  # DAC max
# data[13] = dec2hex(-12)  # ADC min
# data[14] = dec2hex(23)  # ADC max
# data[15] = dec2hex(-23)  # AA min
# data[16] = dec2hex(8)  # AA max

data[11] = dec2hex(-37)  # DAC min
data[12] = dec2hex(0)  # DAC max

data[13] = dec2hex(-12)  # ADC min
data[14] = dec2hex(23)  # ADC max

data[15] = dec2hex(-23)  # AA min
data[16] = dec2hex(8)  # AA max

data[17] = "0x0003"

s = "word writeBuffer[]={" + ", ".join(data) + "};"
print(s)


def addToClipBoard(text):
    command = "echo " + text.strip() + "| clip"
    os.system(command)


addToClipBoard(s)
# with open("./hardware/data.txt", "w") as f:
#     f.write(s)

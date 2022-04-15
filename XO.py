field = {'00':'-', '10':'-', '20':'-',
        '01':'-', '11':'-', '21':'-',
        '02':'-', '12':'-', '22':'-'}
player = 0
tripleX = 'xxx'
triple0 = '000'

def inputchoise():
    global player
    if not player:
        index = "".join(input('Crosses GO (enter index):').split())
        while field[index] != '-':
            index = "".join(input('Put another index:').split())
        field[index] = 'x'
    else:
        index = "".join(input('Zeros GO (enter index):').split())
        while field[index] != '-':
            index = "".join(input('Put another index:').split())
        field[index] = '0'
    player = not player

def printfield(field):
    print(f"""{"0 1 2":>7}
0 {field['00']} {field['10']} {field['20']}
1 {field['01']} {field['11']} {field['21']}
2 {field['02']} {field['12']} {field['22']}\n""")

printfield(field)
while True:
    inputchoise()
    printfield(field)
    checkfield = "".join(field.values())
    checkxxx = (checkfield[0:3] == tripleX,
                checkfield[3:6] == tripleX,
                checkfield[6:9] == tripleX,
                checkfield[0:9:3] == tripleX,
                checkfield[1:9:3] == tripleX,
                checkfield[2:9:3] == tripleX,
                checkfield[0:9:4] == tripleX,
                checkfield[2:8:2] == tripleX)
    check000 = (checkfield[0:3] == triple0,
                checkfield[3:6] == triple0,
                checkfield[6:9] == triple0,
                checkfield[0:9:3] == triple0,
                checkfield[1:9:3] == triple0,
                checkfield[2:9:3] == triple0,
                checkfield[0:9:4] == triple0,
                checkfield[2:8:2] == triple0)
    if any(checkxxx):
        print("CROSSES WIN!")
        break
    if any(check000):
        print("ZEROS WIN!")
        break

print("CONGRATULATIONS!\n")
exit = input('Anykey to exit')

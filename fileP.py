


def filelist(path):
    # part = ""
    part = path
    part0 = "SC4"
    part41 = "E0-PSG-EegData.txt"
    part42 ="E0-PSG-EegLabel.txt"
    part1 = 0
    part2 = 0
    part3 = 0
    name = [[],[]]
    for i in range(0,40):
        if (i % 2 == 0 and i != 0):
            part2 = part2 + 1
        if (i % 20 == 0 and i != 0):
            part1 = part1 + 1
        temp = part+part0+str(part1)+str(part2%10)+str(part3%2+1)
        if(str(part1)+str(part2%10)+str(part3%2+1)=="132"):
            part3 = part3+1
            continue
        name[0].append(temp+part41)
        name[1].append(temp+part42)
        part3 = part3+1
    return name

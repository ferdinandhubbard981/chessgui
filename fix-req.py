


def main():
    readFile = "requirements.txt"
    writeFile = "newrequirements.txt"
    f = open(readFile, "r")
    w = open(writeFile, "w")

    line = f.readline()
    while line:
        index = findSecondEqualsIndex(line)
        newLine = line[:index]
        w.write(newLine + "\n")
        line = f.readline()

    f.close()
    w.close()

def findSecondEqualsIndex(line):
    foundFirst = False
    for i in range(len(line)):
        if line[i] == '=':
            if foundFirst:
                return i
            else:
                foundFirst = True
    return len(line)

if __name__ == "__main__":
    main()
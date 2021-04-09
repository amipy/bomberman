import json, os

#def getOrder():
#    with open("levels/lvlOrder.txt") as f:
#        return json.load(f)


def getOrder(filename=""):
    with open("levels/lvlOrder.txt") as f:
        levels = json.load(f)
        return list(filter(lambda x: x != filename, levels))

def setOrder(order):
    with open("levels/lvlOrder.txt", "w") as f:
        json.dump(order, f)

def trimOrder():
    with open("levels/lvlOrder.txt") as f:
        files=json.load(f)
    trimmed=[]
    dirFiles=[f for f in os.listdir("levels") if os.path.isfile(os.path.join("levels", f))]
    for i in files:
        if i in dirFiles:
            trimmed.append(i)
    with open("levels/lvlOrder.txt", "w") as f:
        json.dump(trimmed, f)

if __name__ == "__main__":
    trimOrder()
import random

floor = random.randint(0, 100)
dropCount = 2

print(floor)

def dropegg(dropFloor):
    global dropCount
    global floor
    assert dropCount > 0
    if dropFloor > floor:
        dropCount = dropCount - 1
        return True
    else:
        return False

def findFloor():
	for i in range(100): 
		if dropegg(i) == True: #broke
			return i-1

def findFloorBetter():
	for i in range(0,100,2):
		if dropegg(i) == True:
			if dropegg(i-1) == True:
				return i-2
			return i-1

print(findFloor())
dropCount = 2
print(findFloorBetter())
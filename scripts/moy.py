import numpy as np

file = open("../data/univnantes","r")
res = file.read();
res = res.split("\n")
res = map(lambda l : l.split(" ")[2] if len(l.split(" "))>2 else "", res)
res = map(lambda l : l.split(","), res)
res = map(lambda l : len(l), res)
print("Moyenne de liens par page: "+str(np.mean(res)))
file.close()

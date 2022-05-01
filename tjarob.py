
dict = {}

dict["b"] = 2
dict["aaa"] = 0.8
dict["aba"] = 0.8
dict["bbb"] = 0.8
dict["a"] = 0.6

print(dict)


list = []
for key in sorted(dict.items(), key=lambda x: (-x[1], x[0])):
    list.append(key[0])


#print(s)
print(list)

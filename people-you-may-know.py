# Author Kim Kiogora <kimkiogora@gmail.com>
list_m = {
    'kim': ['john', 'Mary', 'Kate'],
    'john': ['Mercy', 'Sophie', 'linda'],
    'linda': ['patrick'],
    'patrick': ['muller', 'james'],
    'muller': ['candice', 'fredrick', 'jen'],
}

def people_you_may_know(name, list_y):
    data = []
    if name not in list_y.keys():
        pass
    else:
        init_friends = list_y[name]  # john,mary,kate
        keys = list_y.keys()
        for i in init_friends:
            data.append(i)
            if i in keys:
                more_friends = list_y[i]
                for x in more_friends:
                    data.append(x)
                    d = people_you_may_know(x, list_y)
                    for z in d:
                        data.append(z)
    return sorted(data)


#print people_you_may_know('kim', list_m)
#print people_you_may_know('john', list_m)
#print people_you_may_know('muller', list_m)
#print people_you_may_know('patrick', list_m)
print people_you_may_know('linda', list_m)


def lecture_dataset() :
    mon_fichier = open("iris.data", "r")
    contenu = mon_fichier.readline()
    data_set = []
    count =0

    while contenu != '':
        data_set.append([])
        temp=""
        for i in range(len(contenu)):
            if contenu[i] == ',' or contenu[i] == '\n':
                data_set[count].append(temp)
                temp=""
            else:
                temp += contenu[i]
        contenu = mon_fichier.readline()
        count+=1
    
    return data_set


data_set = lecture_dataset()
print(data_set)
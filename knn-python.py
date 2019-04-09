from statistics import mean, variance,stdev


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
                try:
                    data_set[count].append(float(temp))
                except :
                    data_set[count].append(temp)
                temp=""
            else:
                temp += contenu[i]

        contenu = mon_fichier.readline()
        count+=1

    return data_set

def centrer_reduire(data_set):
    data_set_centre_reduit= data_set.copy()
    moy = []
    ecart_type = []

    for i in range(len(data_set[0])-1):
        moy.append(mean(data_set[j][i]for j in range(len(data_set) ) ))
        ecart_type.append(stdev(data_set[j][i]for j in range(len(data_set) ) ))

    for i in range(len(data_set[0])-1):
        for j in range(len(data_set)):
            data_set_centre_reduit[j][i] = (data_set[j][i] -moy[i])/ecart_type[i]
            #print(data_set_centre_reduit[j])
            
    
    return data_set_centre_reduit



data_set = lecture_dataset()
data_set_centre_reduit = centrer_reduire(data_set)

#print(data_set_centre_reduit)



#print(mean(data_set_centre_reduit[j][0]for j in range(len(data_set) ) ))
#print(stdev(data_set_centre_reduit[j][0]for j in range(len(data_set) ) ))
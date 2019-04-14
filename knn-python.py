from statistics import mean,stdev
from math import sqrt

import matplotlib.pyplot as plt
import numpy as np

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


def centrer_reduire_data(data_set):
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

    return data_set_centre_reduit, moy,ecart_type


def centrer_reduire_test(data_test,moyenne,ecart_type):
    data_test_centre_reduit = data_test.copy()
    for i in range(len(data_test)):
        data_test_centre_reduit[i] = (data_test[i] -moyenne[i])/ecart_type[i]

    return data_test_centre_reduit


def calcul_distance(data_set,data_test):
    data_set_distance = data_set.copy()
    
    for j in range(len(data_set_distance)):
        somme_difference_carre = 0
        for i in range(len(data_set_distance[j])-1):
            somme_difference_carre += pow((data_set_distance[j][i]-data_test[i]),2)
        data_set_distance[j].append(sqrt(somme_difference_carre))
    
    return data_set_distance

def takeSixth(elem):
    return elem[5]

def trier_distance(data_set):
    data_set_distance_triee = data_set.copy()
    data_set_distance_triee.sort(key=takeSixth)
    return data_set_distance_triee

data_set = lecture_dataset()
data_set_centre_reduit,moyenne,ecart_type = centrer_reduire_data(data_set)

data_test = [6.5,3.4,5,2]
data_test_centre_reduit = centrer_reduire_test(data_test,moyenne,ecart_type)

data_set_distance = calcul_distance(data_set_centre_reduit,data_test_centre_reduit)

data_set_distance_triee =trier_distance(data_set_distance)


# uncomment for use of matplotlib
#test =[]
#for i in range(len(data_set_distance_triee)):
#    test.append(data_set_distance_triee[i][5])
#plt.plot(test)
#plt.show()


# uncomment for steps visualisation
#print(data_set_distance)

#print(data_set_centre_reduit)
#print(data_test_centre_reduit)

#print(mean(data_set_centre_reduit[j][0]for j in range(len(data_set) ) ))
#print(stdev(data_set_centre_reduit[j][0]for j in range(len(data_set) ) ))
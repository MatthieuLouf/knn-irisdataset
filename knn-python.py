from statistics import mean,stdev
from math import sqrt

#lecture du data set des iris fourni
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

#modification des 4 premières colonnes du data set pour centrer et réduire les valeurs
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

#on centre et réduit également la donnée test, pour la comparer au data set
def centrer_reduire_test(data_test,moyenne,ecart_type):
    data_test_centre_reduit = data_test.copy()
    for i in range(len(data_test)):
        data_test_centre_reduit[i] = (data_test[i] -moyenne[i])/ecart_type[i]

    return data_test_centre_reduit

#calcul de la distance euclidienne entre chaque donnée du data set et la donnée test
def calcul_distance(data_set,data_test):
    data_set_distance = data_set.copy()
    
    for j in range(len(data_set_distance)):
        somme_difference_carre = 0
        for i in range(len(data_set_distance[j])-1):
            somme_difference_carre += pow((data_set_distance[j][i]-data_test[i]),2)
        data_set_distance[j].append(sqrt(somme_difference_carre))
    
    return data_set_distance

#fonction secondaire pour le tri sur la 6 colonne dans trier_distance()
def takeSixth(elem):
    return elem[5]

#tri du data set selon la distance à la donnée test
def trier_distance(data_set):
    data_set_distance_triee = data_set.copy()
    data_set_distance_triee.sort(key=takeSixth)
    return data_set_distance_triee

#selection des k données les plus proches et comptage de la class la plus représentée
def prediction_class(data_set_triee,k):
    top_k_iris = []
    for i in range(k):
        top_k_iris.append(data_set_triee[i][4])

    count_iris_apparition = []
    for i in range(len(top_k_iris)):
        count_iris_apparition.append(top_k_iris.count(top_k_iris[i]))

    return top_k_iris[count_iris_apparition.index(max(count_iris_apparition))]

#fonction centrale de l'algo knn, utilise toutes les fonctions précédentes
def knn(data_set,data_test,k):

    data_set_centre_reduit,moyenne,ecart_type = centrer_reduire_data(data_set)

    data_test_centre_reduit = centrer_reduire_test(data_test,moyenne,ecart_type)

    data_set_distance = calcul_distance(data_set_centre_reduit,data_test_centre_reduit)

    data_set_distance_triee =trier_distance(data_set_distance)

    class_prediction = prediction_class(data_set_distance_triee,k)

    return class_prediction


k=5 #nombre de plus proches voisins à sélectionner
data_set = lecture_dataset() #lecture du data_set
data_test = [6.5,3.4,5,2] #création d'une donnée test

class_prediction = knn(data_set,data_test,k) #prédiction de la class de la donnée test
print(class_prediction)

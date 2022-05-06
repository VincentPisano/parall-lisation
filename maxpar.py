# Projet réalisé par Seycha Oudeinguene, Mupuanga Lumbanzila Jeancy et Pisano Vincent
from graphviz import Digraph
import threading
import time

class MonThread (threading.Thread):
    def __init__(self, jusqua, event):# event = objet Event
        threading.Thread.__init__(self)# = donnée supplémentaire
        self.jusqua = jusqua
        self.event = event# on garde un accès à l'objet Event

   
    def run(self):
        for i in range(0, self.jusqua):
            print("thread iteration ", i)
        #   time.sleep(0.1)#sleep inutile car on veut maximiser la parallélisation et le sleep ralentit 
        self.event.set()# on indique qu'on a fini :



class Task:
    name= ""
    reads= []
    writes= []
    run =None

X =None
Y =None
Z =None

class TaskSystem:
    
    def __init__(self, listeTaches, preferences, preferencesFinal):
        self.listeTaches = listeTaches
        self.preferences = preferences
        self.preferencesFinal = preferencesFinal 

        #Bonus 2 affichage du système de parallélisme maximal   
        #Génération du fichier demo.dot avec les dépendances de préférences correctes
        g = Digraph('G', filename='demo.dot')
        
        #On parcour toutes les tâches
        for i in listeTaches :
            self.getDependencies(i,g,self.preferencesFinal)   
        #Créer le PDF du graphe 
        g.view()
        print("Voici le dictionnaire des preferences sans les taches non-interferentes : ",self.preferencesFinal)

    def getDependencies(self,nomTache,g,preferencesFinal):              
        
         #Génère l'image avec les bonnes préférences selon les conditions de Bernstein
         preferencesFinal[nomTache.name] = ""
         for i in preferences[nomTache.name]:           
            for j in listeTaches:
                #on vérifie que le name de l'objet par exemple t1 == la string "T1"
                if(j.name == i):
                    if(self.interferente(nomTache,j)==True):
                        #Si les 2 tâches sont interférentes alors on ajoute le chemin dans le dictionnaire de préférence final
                        preferencesFinal[nomTache.name]+=i
                        #On ajoute le chemin dans le graphe 
                        g.edge(i, nomTache.name)
                        
    def run(self):
        #Réaliser la partie run avec le dictionnaire des preferencesFinal en appelant des Threads quand on peut parallélisé
        print("executer les taches du systeme en parallelisant celles qui peuvent etre parallelisees selon la specification du parallelisme maximal.")

    def interferente(self, tache1, tache2):
        #La fonction marche et implémente les conditions de bernstein ci dessous
        for i in tache1.writes :
            for j in tache2.writes :
                if i==j:
                    #print("il y a interference avec E1 et E2 , on doit garder ce chemin")
                    return True
                    
        for i in tache1.reads :
            for j in tache2.writes :
                if i==j:
                    #print("il y a interference L1 et E2 , on doit garder ce chemin")
                    return True
                   
        for i in tache1.writes :
            for j in tache2.reads :
                if i==j:
                    #print("il y a interference E1 et L2 , on doit garder ce chemin")
                    return True
        #print("il n'y a interference, on peut enlever cette dependance garder ce chemin")            
        return False
                    
#éxecuter la tache 1
def runT1():
    global X 
    X = 1
#éxecuter la tache 2
def runT2():
    global Y 
    Y = 2
#éxecuter la tache tsomme
def runTsomme():
    global X, Y, Z 
    Z = X + Y
    
    
t1 = Task()
t1.name= "T1"
t1.writes= ["X"]
t1.run= runT1

t2 = Task()
t2.name= "T2"
t2.writes= ["X"]
t2.run= runT2

tSomme= Task()
tSomme.name= "somme"
tSomme.reads= ["X", "Y"]
tSomme.writes= ["Z"]
tSomme.run = runTsomme

t3 = Task()
t3.name= "T3"
t3.writes= ["Z"]
t3.reads= ["Y"]
t3.run= runT2

 
#t1.run()
#t2.run()
#tSomme.run()
#print(X)
#print(Y)
#print(Z)

def veriflisteTaches( listeTaches):
    namesTaches =[]
    for i in listeTaches :
         namesTaches.append(i.name)
    #print(namesTaches)
    if len(namesTaches) == len(set(namesTaches)):
        print("Pas de double des noms des taches")
        return True
    else:
         print("Erreur !! Il y a au moins 1 double dans les noms des taches suivante : ", namesTaches)
         return False

def verifPreferences(listeTaches,preferences):
    namesTaches =[]
    for i in listeTaches :
         namesTaches.append(i.name)
    
    for i in preferences:
        if(i not in namesTaches):
            print("Erreur !! Il y a au moins 1 tache dont le nom est inexistant il s'agit de la tache : ", i)
            return False

    for i in namesTaches:
        for j in preferences[i]:
            if(j not in namesTaches):
                print("Erreur !! Il y a au moins 1 tache dont le nom est inexistant dans les preferences de la tache ", i," : ",j)
                return False

    for i in namesTaches:
        for j in preferences[i]:
            if len(preferences[i]) == len(set(preferences[i])):
                print("Pas de double dans les preferences de la tache")
                
            else:
                print("Erreur !! Il y a au moins 1 double dans les preferences de la tache ", i," : ",preferences[i] )
                return False
               
    return True
            

#Liste des tâches
listeTaches = [t1, t2, t3, tSomme] 


#Préférences données qui peut avoir des chemins non-interférents à enlevés
preferences = {"T1": [],"T2": ["T1"], "somme": ["T1","T2"],"T3": ["T1","T2","somme"]}


#Dictionnaire qui stockera les préférences qui non-interférents et qu'on doit garder
preferencesFinal = {}

#Bonus 1 validation des entrées 
if(veriflisteTaches(listeTaches) == True and verifPreferences(listeTaches,preferences) == True):
    # On créer la classe TaskSystem seulement si la liste des tâches n'a pas de doublon
    test =  TaskSystem(listeTaches,preferences,preferencesFinal)

    print("debut Thread")
    #Exemple d'utilisation de la class MonThread que on devrait employer dans le run() de la class TaskSystem
    event = threading.Event()       # on crée un objet de type Event
    event.clear()                   # on désactive l'ojet Event
    m = MonThread(10, event)        # crée un thread
    m.start()                       # démarre le thread,
    event.wait()                    # on attend jusqu'à ce que l'objet soit activé
    print("Fin Thread")      

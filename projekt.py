import matplotlib.pyplot as plt
import numpy as np
import random

#Parametry wzorów
ilosc_wzorow = 6
szerokosc = 4
wysokosc = 4
powtorzenia = 1000 #dla bardziej skomplikowanych wzorów optymalna ilość powtórzeń to 1000000, oczywiście
                    #skutkuje to długim czasem pracy, dla łatwych małych wzorów 1000 powinno być ok.

#Tworzenie wzorów
wzor = np.zeros ((ilosc_wzorow, szerokosc * wysokosc))

#Tutaj ustawiamy wygląd figury wpisując wartości "1" lub "-1" 
wzor[0] = [-1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1]
wzor[1] = [-1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1]
wzor[2] = [-1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1]
wzor[3] = [-1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1]
wzor[4] = [-1, -1, 1, 1, -1, 1, 1, 1, 1, 1, 1, -1, 1, 1, -1, -1]
wzor[5] = [1, 1, -1, -1, 1, 1, -1, -1, -1, -1, 1, 1, -1, -1, 1, 1]

#Tutaj ustawiamy uszkodzony wzór (który będzie odzyskiwany)
uszkodzony_wzor = np.array([-1, -1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

#-----------------------------------------------------------------------------------------------
#Auto generowanie wzorów, jeżeli chcemy generować z dużą ilością pixeli, lub dużą ilością wzorów
'''uszkodzony_wzor = np.empty(0)
for i in range(ilosc_wzorow):
    for j in range(szerokosc*wysokosc):
        losowo = random.randrange(-1, 1, 1)
        losowo2 = random.randrange(-1, 1, 1)
        if losowo == 0:
            losowo = 1
        wzor[i,j] = losowo
        if i == 0:
            uszkodzony_wzor = np.append(uszkodzony_wzor, losowo2)'''
#-----------------------------------------------------------------------------------------------

#Wyświetlanie wzorów na ekran dzięki axes
fig, ax = plt.subplots(1, ilosc_wzorow, figsize=(10, 5))

for i in range(ilosc_wzorow):
    ax[i].matshow(wzor[i].reshape((wysokosc, szerokosc)), cmap='terrain')
    ax[i].set_xticks([]) #schowanie współrzędnych x,y na obrazkach
    ax[i].set_yticks([])
    
plt.show()

#Tworzenie sieci hopfielda
W = np.zeros((szerokosc * wysokosc, szerokosc * wysokosc))

for i in range(szerokosc * wysokosc):
    for j in range(szerokosc * wysokosc):
        if i == j or W[i, j] != 0.0:
            continue
        
        w = 0.0
        
        for n in range(ilosc_wzorow):
            w += wzor[n, i] * wzor[n, j]
            
        W[i, j] = w / wzor.shape[0]
        W[j, i] = W[i, j]

#Wzor do odzyskania
odzyskany_wzor = uszkodzony_wzor.copy()

for _ in range(powtorzenia):
    for i in range(szerokosc * wysokosc):
        if np.dot(W[i], odzyskany_wzor) > 0:
            odzyskany_wzor[i] = 1.0
        else:
            odzyskany_wzor[i] = -1.0

#Wyswietlenie wzorów przed i po zastosowaniu sieci
fig, ax = plt.subplots(1, 2, figsize=(10, 5))

ax[0].matshow(uszkodzony_wzor.reshape(szerokosc, wysokosc), cmap='terrain')
ax[0].set_title('Uszkodzony')
ax[0].set_xticks([])
ax[0].set_yticks([])

ax[1].matshow(odzyskany_wzor.reshape(szerokosc, wysokosc), cmap='terrain')
ax[1].set_title('Odzyskany')
ax[1].set_xticks([])
ax[1].set_yticks([])

plt.show()

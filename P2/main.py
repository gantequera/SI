# Importamos las librerias que necesitaremos
import numpy as np
import matplotlib.pyplot as plt
import test

npzfile = np.load("mnist.npz")  # Datos
mnist_X = npzfile['x']
mnist_Y = npzfile['y']

T = 10
A = 500

At = range(100, 1301, 80)
Ta = range(40, 321, 40)

(rA, rT) = test.valorarAT(mnist_X, mnist_Y, A, T, At, Ta)

rAcorr = [np.average(i) for i in rA]
rTcorr = [np.average(i) for i in rT]

plt.figure()
plt.plot(At, rAcorr, 'r-o')
plt.title(f"Precisión del sistema en función de A con T = {T}")
plt.savefig("valAc.pdf", format="pdf")
plt.close()

plt.figure()
plt.plot(Ta, rTcorr, 'b-o')
plt.title(f"Precisión del sistema en función de T con A = {A}")
plt.savefig("valTc.pdf", format="pdf")

#(clasificadores, alphas) = entrenar_sistema(mnist_X, mnist_Y, T, A)
#(testX, testY) = utils.adaptar_conjuntos_test(mnist_X, mnist_Y)
#print(f"Porcentaje de aciertos del sistema para clase 0: {testn(testX, testY, clasificadores, alphas, 8) * 100}")
#precision = test(testX, testY, clasificadores, alphas)

#plt.figure()
#plt.plot(range(10), precision, 'r-o')
#for cordx,cordy in zip(range(10),precision):
#    label = "{:.2f}".format(cordy)
#    plt.annotate(label, (cordx,cordy), textcoords="offset points", xytext=(0,10), ha='center')
#plt.title('Aciertos sobre el total de imagenes por dígito (%)')
#plt.show()
#print(f"Media del sistema: {(np.average(precision) * 100)}%")

from math import *
from tkinter import *
from tkinter import ttk
from functools import partial
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


roboInicialX = 0
roboInicialY = 0
roboFinalX = 0
roboFinalY = 0
tempofinal = 0
intercept = 1

def main():
    Ball_T = []
    Ball_X = []
    Ball_Y = []


    #coloca os valores do arquivo nas listas
    settingLists(Ball_T, Ball_X, Ball_Y)

    #definição padrão para textos
    fontDef = ("Times New Romam", 14)
    #cria a interface gráfica
    window = Tk()
    window.title("Trabalho de Física")
    window.geometry("800x600")

    #entradas para o robô

    X_axis = Label(window, text="Eixo X do Robô: ", font=fontDef)
    X_axis.place(relx=0.4, rely=0.15, anchor=E)

    X_inp = Entry(window, width=5, font=fontDef)
    X_inp.place(relx=0.4, rely=0.15, anchor=W)

    Y_axis = Label(window, text="Eixo Y do Robô: ", font=fontDef)
    Y_axis.place(relx=0.7, rely=0.15, anchor=E)

    Y_inp = Entry(window, width=5, font=fontDef)
    Y_inp.place(relx=0.7, rely=0.15, anchor=W)

    #partial para fazer os cálculos
    Robot_Partial = partial(interception, X_inp, Y_inp, Ball_T, Ball_X, Ball_Y)

    graph1_partial = partial(Grafico1, Ball_X, Ball_Y, Ball_T)

    #botão para fazer as contas e verificar se há interceptação
    verify = Button(window, text="Calcular", font=fontDef, command=Robot_Partial)
    verify.place(relx=0.5, rely=0.3, anchor=CENTER)

    graph1 = Button(window, text="Gráfico 1", font=fontDef, command=graph1_partial)
    graph1.place(relx=0.3, rely=0.4, anchor=CENTER)

    graph2 = Button(window, text="Gráfico 2", font=fontDef, command=Grafico2)
    graph2.place(relx=0.3, rely=0.6, anchor=CENTER)

    graph3 = Button(window, text="Gráfico 3", font=fontDef, command=Grafico3)
    graph3.place(relx=0.3, rely=0.8, anchor=CENTER)

    graph4 = Button(window, text="Gráfico 4", font=fontDef, command=Grafico4)
    graph4.place(relx=0.7, rely=0.4, anchor=CENTER)

    graph5 = Button(window, text="Gráfico 5", font=fontDef, command=Grafico5)
    graph5.place(relx=0.7, rely=0.6, anchor=CENTER)

    window.mainloop()

def settingLists(Time, X, Y):
    #abre o arquivo da trajetória
    archive = open("trajetoria.txt","r")

    i = 0

    for lines in archive.readlines():
        #troca as víguas por pontos
        lines = lines.replace(",",".")
        #separa as informações em listas menores
        Slines = lines.split()
        #pula a primeira linha
        if i == 0:
            pass
        #adiciona cada elemento na sua respectiva lista
        elif i <= 240:
            Time.append(float(Slines[0]))
            X.append(float(Slines[1]))
            Y.append(float(Slines[2]))
        else:
            break
        i += 1

    archive.close()

def interception(X_inp, Y_inp, Ball_T, Ball_X, Ball_Y):
    global roboInicialX, roboInicialY
    #pega as informações entradas pelo usuário
    Robot_X = float(X_inp.get())
    Robot_Y = float(Y_inp.get())

    roboInicialX = Robot_X
    roboInicialY = Robot_Y

    H_Bot = "Humanóide"
    HumanoidTime = []
    HumanoidSpeed = 0.2

    SS_Bot = "Small Size"
    SmallSizeTime = []
    SmallSizeSpeed = 2.3
    SmallSizeAceleration = 2.3
    SmallSizeBreak = 1.6

    #calcula a distância entre o robô humanóide e o ponto em que a bola está, divide pela velocidade para calcular o tempo
    TimeClaculator(HumanoidTime, Robot_X, Robot_Y, Ball_X, Ball_Y, Ball_T, HumanoidSpeed, 0, 0)

    #faz a mesma coisa para o Small Size
    TimeClaculator(SmallSizeTime, Robot_X, Robot_Y, Ball_X, Ball_Y, Ball_T, SmallSizeSpeed, SmallSizeAceleration, SmallSizeBreak)

    #verifica se o robô humanóide chega no ponto de interceptação
    print("Hum")
    Intercept_Verify(HumanoidTime, Ball_X, Ball_Y, Ball_T, H_Bot)
    # verifica se o robô Small Size chega no ponto de interceptação
    print("Small")
    Intercept_Verify(SmallSizeTime, Ball_X, Ball_Y, Ball_T, SS_Bot)

def TimeClaculator(RobotTime, Robot_X, Robot_Y, Ball_X,Ball_Y,Ball_T, speed, Acceleration, Break):
    for i in range(0,240):
        X_axis = Ball_X[i] - Robot_X
        Y_axis = Ball_Y[i] - Robot_Y

        dist = sqrt((X_axis**2) + (Y_axis**2))

        # Para o Humanóide
        if Acceleration == 0 or Break == 0:
            time = (dist-0.15)/speed

        #Para o Small Size
        else:
        	#tempo acelerando
            Acc_Time = speed/Acceleration #tempo que deora para atingir vel max
            #velocidade enquanto acelera
            Acc_Speed = Acceleration * Ball_T[i] #velocidade acelerando
            #Breking_Time = speed/Break

            #se o tempo da aceleração (1) for maior que o da bola, o cálculo é feito com esse tempo
            if Acc_Time >= Ball_T[i]:
                Acc_Dist = sqrt((Robot_X ** 2) + (Robot_Y ** 2)) + (Acceleration*(Ball_T[i])**2)/2#distancia percorrida enquanto o robo acelera

                #se o tempo da bola for diferente de zero, o cálculo é relizado normalmente
                if Ball_T[i] != 0:
                    time = (Acc_Dist - 0.92)/Acc_Speed
                #se não for, o tempo é definido como zero, pois não houve movimentação
                else:
                    time = 0

            else:
                time = ((dist - 0.92)/speed) + 1

        RobotTime.append(time)

robo = []
def Intercept_Verify(RobotTime, Ball_X, Ball_Y, Ball_T, Bot):
    global roboFinalY, roboFinalX, tempofinal, intercept


    for j in range(0,240):
        #print(RobotTime[j],"/",Ball_T[j])
        #caso o robô chegue antes da bola no ponto de interceptação
        if Ball_T[j] >= RobotTime[j] and RobotTime[j] != 0:
            result = " intercepta no instante\n          "
            roboFinalX = Ball_X[j]
            roboFinalY = Ball_Y[j]
            tempofinal = Ball_T[j]
            #se o tempo for menor que 0, indica que o instante da intercaptação é 0
            if RobotTime[j] <= 0:
                result = " intercepta no instante\n          "
                Stime = str(RobotTime[j-1])
            #se o tempo for maior que 0, indica o instante de interceptação
            else:
                Stime = str(RobotTime[j])

            return(PopUp(result, Stime, Bot))
        #caso o robô não chegue a tempo, passa para a próxima comparação
        else:
            pass

    #se o robô não alcançar a bola na comparação anterior, significa que a mesma deixou o campo
    result = " não intercepta a bola."
    return(PopUp(result, 0, Bot))

def PopUp(result, time, Bot):
    #cria um "pop up" que mostra o tempo de interceptação
    popup = Tk()
    popup.geometry("350x150")
    popup.title("Resultado " + Bot)
    F_result = "O " + Bot + result
    #escreve os resultados obtidos no cálculo no pop up
    if time == 0:
        label = ttk.Label(popup, text=F_result, font=("Times New Romam", 14))
    else:
        label = ttk.Label(popup, text=F_result + time, font=("Times New Romam", 14))
    label.place(relx=0.5, rely=0.25, anchor=CENTER)
    button = ttk.Button(popup, text="Okay", command=popup.destroy)
    button.place(relx=0.5, rely=0.7, anchor=CENTER)

    popup.mainloop


#--------------------------------------------------------------------------------------------------------------------------------
def Grafico1(Ball_X, Ball_Y, Ball_T): #Gráfico das trajetórias da bola e do robô em um plano xy, até o ponto de interceptação;

    popup = Tk()
    popup.geometry("200x200")
    popup.title("Selecione o robô:")

    parcial1 = partial(Grafico1Hum, Ball_X, Ball_Y, Ball_T)
    parcial2 = partial(Grafico1Small, Ball_X, Ball_Y, Ball_T)

    hum = ttk.Button(popup, text="Humanóide",command=parcial1)
    hum.place(relx=0.3, rely=0.5, anchor=CENTER)

    Small = ttk.Button(popup, text="Small Size", command=parcial2)
    Small.place(relx=0.7, rely=0.5, anchor=CENTER)


def Grafico2():
    popup = Tk()
    popup.geometry("200x200")
    popup.title("Selecione o robô:")

    hum = ttk.Button(popup, text="Humanóide")
    hum.place(relx=0.3, rely=0.5, anchor=CENTER)

    Small = ttk.Button(popup, text="Small Size")
    Small.place(relx=0.7, rely=0.5, anchor=CENTER)

def Grafico3():
    popup = Tk()
    popup.geometry("200x200")
    popup.title("Selecione o robô:")

    hum = ttk.Button(popup, text="Humanóide")
    hum.place(relx=0.3, rely=0.5, anchor=CENTER)

    Small = ttk.Button(popup, text="Small Size")
    Small.place(relx=0.7, rely=0.5, anchor=CENTER)

def Grafico4():
    popup = Tk()
    popup.geometry("200x200")
    popup.title("Selecione o robô:")

    hum = ttk.Button(popup, text="Humanóide")
    hum.place(relx=0.3, rely=0.5, anchor=CENTER)

    Small = ttk.Button(popup, text="Small Size")
    Small.place(relx=0.7, rely=0.5, anchor=CENTER)

def Grafico5():
    popup = Tk()
    popup.geometry("200x200")
    popup.title("Selecione o robô:")

    hum = ttk.Button(popup, text="Humanóide")
    hum.place(relx=0.3, rely=0.5, anchor=CENTER)

    Small = ttk.Button(popup, text="Small Size")
    Small.place(relx=0.7, rely=0.5, anchor=CENTER)



def Grafico1Hum(Ball_X, Ball_Y, Ball_T):
    global intercept, roboInicialX, roboFinalX, roboInicialY, roboFinalY

    if intercept:
        auxBall_X = []
        auxBall_Y = []

        i = 0
        while (Ball_T[i] < tempofinal):
            auxBall_X.append(Ball_X[i])
            auxBall_Y.append(Ball_Y[i])
            i+=1

        plt.title("Trajetória do robô Hum e da bola em um plano XY")
        plt.plot(auxBall_X, auxBall_Y)
        plt.plot([roboInicialX, roboFinalX], [roboInicialY, roboFinalY])

    else:
        plt.title("Trajetória do robô Hum e da bola em um plano XY")
        plt.plot(Ball_X, Ball_Y)
        plt.plot([roboInicialX, roboFinalX], [roboInicialY, roboFinalY])

    plt.xlabel("x/m")
    plt.ylabel("y/m")


    blue_patch = mpatches.Patch(color='orange', label="Trajetória do robô")
    orange_patch = mpatches.Patch(color='blue', label="Trajetória da bola")

    plt.legend(handles=[orange_patch, blue_patch])
    plt.xlim(0,9)
    plt.ylim(0,6)
    plt.grid()
    plt.show()





def Grafico1Small(Ball_X, Ball_Y, Ball_T):
    global roboInicialX, roboFinalX, roboInicialY, roboFinalY
    plt.title("Trajetória do robô SS e da bola em um plano XY")
    plt.plot(Ball_X, Ball_Y)
    plt.plot([roboInicialX, roboFinalX], [roboInicialY, roboFinalY])
    plt.xlabel("x/m")
    plt.ylabel("y/m")

    blue_patch = mpatches.Patch(color='orange', label="Trajetória do robô")
    orange_patch = mpatches.Patch(color='blue', label="Trajetória da bola")

    plt.legend(handles=[orange_patch, blue_patch])
    plt.xlim(0,9)
    plt.ylim(0,6)
    plt.grid()
    plt.show()


#def Grafico2Small():


#def Grafico3Small():


#def Grafico4Small():


#def Grafico5Small():






    #plt.scatter(x,y) #indica os eixos x e y
    #plt.show() #mostra o Graficos



main()

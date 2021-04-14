from tkinter import *

root = Tk()
root.title("Polinomi")

okno = Frame(master=root, padx=20, pady=20)
okno.pack()


w = Label(okno, text="Polinom:")
w.grid(row=0, column=0)

polja_polinom = []
for i in range(3):
    polja_polinom.append(Entry(okno, width=3))
    polja_polinom[-1].grid(row=0, column=(i+1) * 2 - 1)

def lepe_potence(eksponent):
	eksponent = str(eksponent)
	gor = dict()
	gor["1"] = "¹"
	gor["2"] = "²"
	gor["3"] = "³"
	gor["4"] = "⁴"
	gor["5"] = "⁵"
	gor["6"] = "⁶"
	gor["7"] = "⁷"
	gor["8"] = "⁸"
	gor["9"] = "⁹"
	gor["0"] = "⁰"
	lep_eksponent = ""
	for st in eksponent:
		lep_eksponent += gor[st]
	return lep_eksponent

x_okras = []
def popravi_polja():
	global polja_polinom, x_okras
	for i in x_okras:
		i.destroy()
	na = len(polja_polinom) - 1
	for i, polje in enumerate(polja_polinom):
		tekst = "x" + lepe_potence(na) + " +"
		if tekst == "x⁰ +":
			tekst = ""
		elif tekst == "x¹ +":
			tekst = "x +"
		x_okras.append(Label(okno, text=tekst, font=("Segoe", 11)))
		x_okras[-1].grid(row=0, column=(i+1) * 2)
		na -= 1

odgovor = Label(okno, pady=30)
odgovor.grid(row=5, column=0)

st_gumbov = 3
def dodaj_f():
    global st_gumbov, polja_polinom
    st_gumbov += 1
    polja_polinom.append(Entry(okno, width=3))
    polja_polinom[-1].grid(row=0, column=st_gumbov * 2 - 1)
    popravi_polja()
    if st_gumbov > 2:
    	daj_stran["state"] = "normal"

def odstrani_f():
    global st_gumbov, polja_polinom
    st_gumbov -= 1
    polja_polinom[-1].destroy()
    polja_polinom.pop()
    popravi_polja()
    if st_gumbov <= 2:
    	daj_stran["state"] = "disabled"

import iskalec_nicel

def calc():
    global polja_polinom, odgovor
    cleni = []
    for polje in polja_polinom:
        try:
            float(polje.get())
        except ValueError:
            if polje.get() == "":
                print("eno od polj je prazno")
            else:
                print(polje.get(), "pa ni številka")
            return
        else:
            cleni.append(float(polje.get()))
    while cleni[0] == 0:
    	cleni = cleni[1:]
    polinom = iskalec_nicel.polinom(cleni)
    nicle = polinom.najdi_nicle()

    lepe_nicle = ""
    for n in nicle:
        try:
            int(n)
        except:
            zaokrozen = complex(round(n.real, 3), round(n.imag, 3))
            lepe_nicle += str(zaokrozen) + ", "
        else:
            lepe_nicle += str(round(n, 3)) + ", "
    if lepe_nicle[:-2] == "":
        odgovor["text"] = "Ni najdel nobenih ničel."
    else:
        odgovor["text"] = "Ničle: " + lepe_nicle[:-2]

def narisi_graf():
    global polja_polinom
    import matplotlib.pyplot as plt
    cleni = []
    for polje in polja_polinom:
        try:
            float(polje.get())
        except ValueError:
            print(polje.get(), "pa ni številka")
            return
        else:
            cleni.append(float(polje.get()))
    
    polinom = iskalec_nicel.polinom(cleni)

    graf_x = []
    graf_y = []
    korak = 0.1
    lev_rob = -10
    desni_rob = 10
    while lev_rob < desni_rob:
        graf_x.append(lev_rob)
        lev_rob += korak

    for x in graf_x:
        graf_y.append(polinom.vrednost_pri(x))


    fig, graf = plt.subplots(num="Graf polinoma v matplotlib-u")
    graf.plot(graf_x, graf_y, color="green")
    plt.grid(True)
    graf.set_ylim(bottom=-10, top=10)
    plt.axhline(y=0, color="black")
    plt.axvline(x=0, color="black")
    plt.title("Graf polinoma")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

dodaj = Button(okno, text="Dodaj člen", command=dodaj_f)
dodaj.grid(row=1, column=0)
daj_stran = Button(okno, text="Odstrani člen", command=odstrani_f)
daj_stran.grid(row=2, column=0)
recunaj = Button(okno, text="Izračunaj ničle", command=calc)
recunaj.grid(row=3, column=0)
risi = Button(okno, text="Nariši graf", command=narisi_graf)
risi.grid(row=4, column=0)


popravi_polja()
root.mainloop()

import random
ZAOKRIZI_PRI = 0.0001 #če je številka toliko stran od celega števila jo zaokrožimo na celo število

def pogojno_zaokrozi(stevila):
    global ZAOKRIZI_PRI
    """zaokroži stevila, če so zelo blizu celih števil, stevila je lahko int ali seznam"""
    if isinstance(stevila, list):
        #če je dobil seznam, potem zaokroži vsak element seznama
        for i, stevilo in enumerate(stevila):
            stevila[i] = pogojno_zaokrozi(stevilo)
    elif isinstance(stevila, int) or isinstance(stevila, float):
        #pogleda, če ke število blizu celega števila, če je ga spremeni v int
        if abs(round(stevila) - stevila) < ZAOKRIZI_PRI:
            stevila = round(stevila)
    elif isinstance(stevila, complex):
        #če je kompleksno zaokroži realni in imaginarni del
        stevila = complex(pogojno_zaokrozi(stevila.real), pogojno_zaokrozi(stevila.imag))
    else:
        raise TypeError("argument pogojno_zaokrozi mora biti int ali seznam")
    return stevila

class polinom:
    def __init__(self, cleni):
        self.cleni = cleni
    
    def stopnja(self):
        """vrne stopnjo polinoma"""
        return len(self.cleni) - 1

    def vrednost_pri(self, x):
        """vrednost funkcije polinoma pri danem x"""
        stopnja = self.stopnja()
        vrednost = 0
        for clen in self.cleni:
            vrednost += clen * (x ** stopnja)
            stopnja -= 1
        return vrednost

    def odvod(self):
        """vrne odvod polinoma"""
        odvod = []
        eksponent = self.stopnja()
        for i in self.cleni[:-1]:
            odvod.append(i * eksponent)
            eksponent -= 1
        return polinom(odvod)

    def formule(self):
        """Uporabi formule, da reši polinom prve ali druge stopnje"""
        if self.stopnja() == 1:
            odgovor = -1 * self.cleni[1] / self.cleni[0]
            #ničla = -a/b
            return [pogojno_zaokrozi(odgovor)]
        elif self.stopnja() == 2:
            nicle = []
            a = self.cleni[0]
            b = self.cleni[1]
            c = self.cleni[2]

            D = b**2 - 4*a*c
            if D < 0:
                x1 = ( (-b + D**0.5) / (2 * a) )
                x2 = ( (-b - D**0.5) / (2 * a) )
                x1 = complex(round(x1.real, 3), round(x1.imag, 3))
                x2 = complex(round(x2.real, 3), round(x2.imag, 3))
                nicle.append(x1)
                nicle.append(x2)
            else:
                x1 = ( (-b + D**0.5) / (2 * a) )
                x2 = ( (-b - D**0.5) / (2 * a) )
                nicle.append(x1)
                nicle.append(x2)

            return pogojno_zaokrozi(nicle)
            #D = b² - 2ac
            #ničla = (-b +- √D) / 2a
        else:
            return []

    def newtonova(self, rekurzija=0):
        """Z uporabo newtonove metode najde eno ničlo funkcije"""
        if rekurzija > 10:
            return [] #če je že desetkrat poskušal, obupa
        x = (random.random() - 0.5) * 10 #začnemo na naključni točko od -5 do 5
        #newtonova metoda se lahko "zatakne" na lokalnem ekstremu ali na poli
        for i in range(30):
            if self.odvod().vrednost_pri(x) != 0:
                x = x - (self.vrednost_pri(x) / self.odvod().vrednost_pri(x))
                #boljši_približek = star_približek - f(x)/f'(x)
            else:
                break
        if self.vrednost_pri(x) < 0.0001:
            #GUI kaže 3 decimalna mesta natančno, če je v tej toleranci ga spustim skozi
            return pogojno_zaokrozi(x)
        else:
            #mogoče je začel na slabem mestu
            return self.newtonova(rekurzija + 1)

    def __truediv__(self, delitelj):
        """deli polinom z linearnim polinomom ( številom ), uporablja hornerjev algoritem"""
        spodaj = []
        for i, clen in enumerate(self.cleni):
            if i == 0:
                spodaj.append(clen) #prvi gre direkt skoz
            else:
                spodaj.append((spodaj[i-1] * delitelj) + clen) #lepo dela hornerja
        return polinom(spodaj[:-1])
        #zadnji člen je ostanek
        #če je delitelj ničla polinoma, je ostanek nič

    def __str__(self):
        return str(self.cleni)

    def najdi_nicle(self):
        nicle = []
        while self.stopnja() > 2:
            #z newtonovo metodo išče ničle
            #in deli polinom z ničlo, postopek ponavlja
            #dokler ne pride do polinoma s stopnjo 2
            nicla = self.newtonova()
            nicle.append(nicla)
            self = self / nicla
        #zadnje dve ( ali eno ) ničlo zračina s formulami
        nicle += self.formule()
        return nicle

if __name__ == "__main__":
    p = polinom([1, -2, -29, -42])
    print(p.najdi_nicle())
from random import randint
from giocatore import *
from oggetti import *

class Personaggio:
    def __init__(self, nome):
        self.nome=nome

    def __str__(self):
        return self.nome

class Cantastorie(Personaggio):
    def __init__(self):
        super().__init__('Messi il cantastorie')
    
    def racconta_storia(self,dado=0):
        if dado==0:
            dado=randint(1,3)
        if dado==1:
            print(open('./immagini_storie/prima_storia.txt').read())
        elif dado==2:
            print(open('./immagini_storie/seconda_storia.txt').read())
        elif dado==3:
            print(open('./immagini_storie/terza_storia.txt').read())
        

class Commerciante(Personaggio):
    def __init__(self):
        self.oro = 100
        self.inventario = [Marionberrypie(),Strudel(),PozioneCurativa(),
                           PozioneCurativa(),Roccia(),Pugnale(),Spada(),Arco(),Frecce()]
        super().__init__('Commerciante')


class Nemico(Personaggio):
    def __init__(self, nome, vita, danno):        
        self.vita=vita
        self.danno=danno
        super().__init__(nome)

    def vivo(self):
        return self.vita > 0
    
    def attacco(self,giocatore):
        if self.vivo():
            giocatore.vita = giocatore.vita - self.danno
            if giocatore.vita <= 0:
                print("\nStremato cadi a terra e muori")
            else:
                print("\nRicevi {} danni. Hai ancora {} di vita.".format(
                self.danno, giocatore.vita))

class NemicoFacile(Nemico):
    def __init__(self):
        self.descrizione_vivo = '\nUn Ragno Gigante ti sbarra la strada.\n'
        self.descrizione_morto = '\nOsservi i resti del Ragno ucciso.\n'
        super().__init__('Ragno Gigante', 10, 2)        

class NemicoMedio(Nemico):
    def __init__(self):
        self.descrizione_vivo = '\nUna Tigre feroce ti vuole sbranare.\n'
        self.descrizione_morto = "\nOsservi i resti della Tigre uccisa.\n"        
        super().__init__('Tigre', 30, 10)             

class NemicoNumeroso(Nemico):
    def __init__(self):
        self.descrizione_vivo = '\nUno Sciame di api ti ronza intorno per pungerti, sbarrandoti la strada.\n'
        self.descrizione_morto = '\nOsservi i resti delle api distese per terra.\n'        
        super().__init__('Sciame di api',100,4)

class NemicoForte(Nemico):
    def __init__(self):
        self.descrizione_vivo = '\nUn Lupo bianco, molto affamato, prova a mangiarti.\n'
        self.descrizione_morto = '\nOsservi i resti del Lupo ucciso.\n'        
        super().__init__('Lupo bianco',80,15)

class NemicoBoss(Nemico):
    def __init__(self):
        self.descrizione_vivo = '\nLa strega malefica Gargamella ti impedisce di proseguire.\n'
        self.descrizione_morto = '\nOsservi i resti della strega uccisa.\n'        
        super().__init__('Gargamella',120,15)
        
        
# --------------------------
# test
# --------------------------
if __name__ == '__main__':
    ricette=vars().copy()
    print('Lista nemici:')
    for chiave,ricetta in ricette.items():
        if isinstance(ricetta, type) and issubclass(ricetta, Nemico) and ricetta!=Nemico:
            tmp=ricetta()                
            print('Nome:{:<30} - Vita:{:>5} - Danno:{:>5}'.format(tmp.nome,tmp.vita,tmp.danno))
            print('  Descrizione vivo:  {}'.format(tmp.descrizione_vivo.strip()))
            print('  Descrizione morto: {}'.format(tmp.descrizione_morto.strip()))
    print('\nCantastorie:')                
    for chiave,ricetta in ricette.items():
        if isinstance(ricetta, type) and ricetta==Cantastorie:
            tmp=ricetta()                
            print('Nome:{:<30}'.format(tmp.nome))
            for storia in range(1,4):
                print('\nStoria n:',storia)
                tmp.racconta_storia(storia)
    print('\nCommerciante:')
    for chiave,ricetta in ricette.items():
        if isinstance(ricetta, type) and ricetta==Commerciante:
            tmp=ricetta()                
            print('  Nome:{:<30} - Oro:{:>5}'.format(tmp.nome,tmp.oro))
            print('  Inventario:')
            print('    Lista mangiabili:')
            for oggetto in tmp.inventario:                
                if isinstance(oggetto, Mangiabile):                    
                    print('      Nome:{:<20} - Descrizione:{:<30} - Prezzo:{:>5} - Recupero:{:>5}'.format(oggetto.nome,oggetto.descrizione,oggetto.prezzo,oggetto.recupero))    
            print('    Lista armi:')
            for oggetto in tmp.inventario:
                if isinstance(oggetto, Arma):
                    print('      Nome:{:<20} - Descrizione:{:<30} - Prezzo:{:>5} - Danno:{:>5}'.format(oggetto.nome,oggetto.descrizione,oggetto.prezzo,oggetto.danno))    
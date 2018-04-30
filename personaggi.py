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
        super().__init__('Omero il cantastorie')
    
    def racconta_storia(self,dado=0):
        if dado==0:
            dado=randint(1,3)
        if dado==1:
            print(open('./immagini_storie/prima_storia.txt', encoding='utf8').read())
        elif dado==2:
            print(open('./immagini_storie/seconda_storia.txt', encoding='utf8').read())
        elif dado==3:
            print(open('./immagini_storie/terza_storia.txt', encoding='utf8').read())
        

class Commerciante(Personaggio):
    def __init__(self):
        self.oro = 100
        self.inventario = [Mela(),Mela(),Pane(),
                           Pane(),Pane(),PozioneCurativa(),
                           PozioneCurativa(),Roccia(),Pugnale(),
                           Spada(),Polpo(),Fiocina(),Powerhead(),Calamaro(),Frustadialghe(),Rana(),Conchiglie()]
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
        self.descrizione_vivo = '\nUn Pesce spada da sconfiggere è qui.\n'
        self.descrizione_morto = '\nOsservi la spada del tuo nemico sconfitto.\n'
        super().__init__('Pesce spada', 10, 2)        

class NemicoMedio(Nemico):
    def __init__(self):
        self.descrizione_vivo = "\nUn'Orca è pronta a mangiarti. Sconfiggila.\n"
        self.descrizione_morto = "\nAdesso l'Orca giace in fondo all'Oceano.\n"        
        super().__init__('Orca', 30, 10)

class NemicoNumeroso(Nemico):
    def __init__(self):
        self.descrizione_vivo = '\nDei granchi ti vogliono pizzicare.\n'
        self.descrizione_morto = '\nGuardi i resti dei granchi senza vita.\n'        
        super().__init__('Gruppo di granchi',100,4)

class NemicoForte(Nemico):
    def __init__(self):
        self.descrizione_vivo = '\nUn grande Squalo ti sbarra la strada.\n'
        self.descrizione_morto = '\nOsservi lo Squalo sconfitto.\n'        
        super().__init__('Squalo',80,15)

class NemicoBoss(Nemico):
    def __init__(self):
        self.descrizione_vivo = '\nUn Drago marino vuole fermarti.\n'
        self.descrizione_morto = '\nSei riuscito a sconfiggere questo mostro.\n'        
        super().__init__('Drago marino',120,15)
        
        
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
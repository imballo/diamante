class Oggetto:
    def __init__(self,nome,descrizione,prezzo=0):
        self.nome = nome
        self.descrizione = descrizione
        self.prezzo=prezzo

    def __str__(self):
        return self.nome

class Arma(Oggetto):
    def __init__(self,nome,descrizione,danno,prezzo):
        self.danno = danno
        super().__init__(nome,descrizione,prezzo)
        
class Mangiabile(Oggetto):
    def __init__(self,nome,descrizione,recupero,prezzo):
        self.recupero = recupero
        super().__init__(nome,descrizione,prezzo)
        
class Chiave(Oggetto):
    def __init__(self):
        super().__init__('Chiave','Una chiave che apre una porta',70)

class Fune(Oggetto):
    def __init__(self):
        super().__init__('Fune','Una lunga fune da arrampicata',70)
        
class Dinamite(Oggetto):
    def __init__(self):
        super().__init__('Dinamite','Una potente carica di dinamite',70)        

class Roccia(Arma):
    def __init__(self):
        super().__init__("Roccia","Una semplice roccia",5,1)

class Pugnale(Arma):
    def __init__(self):
        super().__init__("Pugnale","Una piccolo pugnale",10,10)

class Spada(Arma):
    def __init__(self):
        super().__init__("Spada","Una spada ad una mano",20,50)
                
class Pane(Mangiabile):
    def __init__(self):
        super().__init__("Pane","Una pagnotta di pane",10,5)
        
class Mela(Mangiabile):
    def __init__(self):
        super().__init__("Mela","Una mela rossa",5,5)

class PozioneCurativa(Mangiabile):
    def __init__(self):
        super().__init__("Pozione curativa","Una pozione guarente",50,20)
        
class Arco(Arma):
    def __init__(self):
        super().__init__("Arco","l'arco è in grado di fare danno a distanza",15,50)
                         
class PozioneAdArea(Arma):
    def __init__(self):
        super().__init__('Pozione ad area','la pozione ad area è in grado di fare danno a tanti piccoli mostri',3,10)

class BarrettaEnergetica(Mangiabile):
    def __init__(self):
        super().__init__("Barretta Energetica","Barretta Al Cioccolato ",50,20)
 
                         


# --------------------------
# test
# --------------------------
if __name__ == '__main__':
    ricette=vars().copy()
    print('Lista mangiabili:')
    for chiave,ricetta in ricette.items():
        if isinstance(ricetta, type) and issubclass(ricetta, Mangiabile) and ricetta!=Mangiabile:
                tmp=ricetta()                
                print('Nome:{:<20} - Descrizione:{:<30} - Prezzo:{:>5} - Recupero:{:>5}'.format(tmp.nome,tmp.descrizione,tmp.prezzo,tmp.recupero))    
    print('\nLista armi:')                
    for chiave,ricetta in ricette.items():
        if isinstance(ricetta, type) and issubclass(ricetta, Arma) and ricetta!=Arma:
                tmp=ricetta()
                print('Nome:{:<20} - Descrizione:{:<30} - Prezzo:{:>5} - Danno   :{:>5}'.format(tmp.nome,tmp.descrizione,tmp.prezzo,tmp.danno))            

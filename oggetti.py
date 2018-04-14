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
        
class Spadaunicorno(Arma):
    def __init__(self):
        super().__init__("Spada degli unicorni ","Una spada ad una mano forgiata da un unicorno",20,50)

class SpadaArcobeleno(Arma):
    def __init__(self):
        super().__init__("Spada degli arcobeleni ","Una spada ad una mano a forma di arcobeleno",20,50)

class SpadaLaser(Arma):
    def __init__(self):
        super().__init__("SpadaLaser","Una spada laser che stordisce con l'emissione di luce colorata",20,50)

class Pozionefrullatodialghe(Mangiabile):
    def __init__(self):
        super().__init__("Pozione frullato di alghe","Una pozione guarente frullato di alghe",50,20)

class Pozionepolveredimadreperla(Mangiabile):
    def __init__(self):
        super().__init__("Pozione polvere di madreperla","Una pozione cicatrizzante e rinvigorente",50,20)
        
class Fruttidimare(Mangiabile):
    def __init__(self):
        super().__init__("Frutti di mare","Una ciotola di frutti di mare",10,5)

class Polpettemarinare(Mangiabile):
    def __init__(self):
        super().__init__("Polpettemarinare","Una porzione di polpettine",10,5)
        
class Cacciucco(Mangiabile):
    def __init__(self):
        super().__init__("Cacciucco","Una ciotola di pane arrostito e cacciucco",10,5)



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

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

class Bàng(Arma):
    def __init__(self):
        super().__init__("Bàng","Una Bàng(una lancia Cinese) pronta a essere lanciata",10,5)

class StellineNinja(Arma):
    def __init__(self):
        super().__init__("Stelline ninja","Delle stelline ninja piccole ma potenti",20,11)

class Katana(Arma):
    def __init__(self):
        super().__init__("Katana","Una katana affilata",50,110)
                
class InvoltiniPrimavera(Mangiabile):
    def __init__(self):
        super().__init__("Involtini Primavera","Dei gustosi e raffinati Involtini",17,9)
        
class RisottoAllaCantonese(Mangiabile):
    def __init__(self):
        super().__init__("Risotto alla cantonese","Un risotto caldo pronto a essere mangiato",23,31)

class TeAlGelsomino(Mangiabile):
    def __init__(self):
        super().__init__("Te' al gelsomino","Un caldo tè al gelsomino molto energetico",50,20)
        

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

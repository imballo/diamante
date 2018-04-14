from random import *
from personaggi import *
from oggetti import *

class CasellaMappa: 
    def __init__(self):
        self.visitata = False

class CasellaInizio(CasellaMappa):
    def __str__(self):
        return 'II'
    
    def descrizione(self):
        if self.visitata:
            return "\nQuesta è una zona noiosa della caverna.\n"
        else:
            s=open('./immagini_storie/immagine_inizio.txt').read()
            s=s+"""
Benvenuto nella nostra avventura fantastica creata 
dagli Inventori per te. Buona fortuna e divertiti!!
"""
            return s
        
class CasellaNoiosa(CasellaMappa):
    def __str__(self):
        return '  '
    
    def descrizione(self):
        if self.visitata:
            d1="\nQuesta è una casella noiosa in cui non succede niente di interessante.\n"
            d2="\nIn questa casella non c'è niente di interessante\n"
        else:
            d1="\nQuesta è una zona noiosa della caverna.\n"
            d2="\nQuesta zona non contiene niente di importante.\n"
        return choice([d1,d2])
    
class CasellaFine(CasellaMappa):
    def __str__(self):
        return 'FF'
    
    def descrizione(self):
        d=open('./immagini_storie/immagine_fine.txt').read()        
        d1= \
"""
Hai ucciso la strega e trovato tuo figlio....
Sei un eroe!
"""
        d2=d1
        d3=d1            
        return d+choice([d1,d2,d3])
    
class CasellaBuca(CasellaFine):
    def __str__(self):
        return 'BB'
    
    def descrizione(self):
        d1 = """
Caschi in un burrone da cui non uscirai più.
"""
        d2 = """
Trovi nell'erba una trappola per orsi che ti uccide.
"""
        return choice([d1,d2])
    
class CasellaVuota(CasellaMappa):
    def __str__(self):
        return '[]'
    
    def descrizione(self):
        d1 = "\nNon puoi passare c'è un filo d'erba altissimo che ti sbarra la strada\n"
        d2 = "\nDelle rose molto alte ti sbarrano la strada\n"
        d3 = "\nUn ramoscello caduto ti sbarra la strada\n"
        return choice([d1,d2,d3])
    
class CasellaCantastorie(CasellaMappa):
    def __init__(self,storia=0):
        self.cantastorie = Cantastorie()
        self.storia=storia
        super().__init__()
        
    def __str__(self):
        return 'ZZ'
    
    def descrizione(self):        
        if self.visitata:
            return '\nVuoi ascoltare la storia del cantastorie?\n'
        else:
            return '\nIl cantastorie ti ha raccontato tutto?\n'

class CasellaOro(CasellaMappa):
    def __init__(self,oro=30):
        self.oro = randint(oro/2,oro)
        super().__init__()
        
    def __str__(self):
        return 'OO'
    
    def descrizione(self):
        if self.oro>0:
            return "\nHai trovato dell'oro che raccogli senza esitare.\n"
        else:
            return "\nTi ricordi quando hai raccolto l'oro, che bello che era!\n"

class CasellaOggetto(CasellaMappa):
    def __init__(self,oggetto='Chiave'):
        self.raccolto = False        
        self.oggetti = [eval(oggetto+'()')]        
        super().__init__()
    
    def __str__(self):
        return 'KK'
    
    def prendi_oggetto(self):
        oggetto = None
        if self.oggetti != []:
            oggetto = self.oggetti[0]
            self.oggetti.remove(oggetto)
            if self.oggetti == []:
                self.raccolto = True
        return oggetto

    def descrizione(self):
        if self.raccolto:
            return "\nCerchi bene ma non riesci a trovare un altro oggetto.\n"
        else:
            return "\nNell'angolo vedi una {} che raccogli senza esitare.\n".format(self.oggetti[0])                

class CasellaPorta(CasellaMappa):
    def __init__(self, tipo='Porta'):
        self.porta_aperta = False
        self.tipo=tipo
        super().__init__()
        
    def __str__(self):
        return 'PP'
    
    def muovi_bloccato(self,dx,dy):
        if self.porta_aperta:
            return False
        elif dx != self.dx_bloccato or dy != self.dy_bloccato:
            return False
        else:
            return True
    
    def descrizione(self):
        if self.porta_aperta:
            if self.tipo=='Porta':
                return "\nQuesta porta è già aperta.\n"
            elif self.tipo=='Crepaccio':
                return "\nLa fune ti permette ora di attraversare il crepaccio.\n"
            elif self.tipo=='Roccia':
                return "\nOsservi le rocce che ti bloccavano il passaggio.\n"
        else:
            if self.tipo=='Porta':
                return "\nHai trovato una porta, trova la chiave per aprirla.\n"
            elif self.tipo=='Crepaccio':
                return "\nTi trovi di fronte ad un crepaccio troppo profondo da attraversare.\n"
            elif self.tipo=='Roccia':
                return "\nUna roccia imponente ti blocca il passaggio.\n"

class CasellaMostro(CasellaMappa):
    def __str__(self):
        return 'MM'
    
    def __init__(self):
        r = random()
        if r < 0.5:
            self.nemico = NemicoFacile()
        elif r < 0.80:
            self.nemico = NemicoMedio()
        elif r <0.95:
            self.nemico = NemicoNumeroso()
        else:
            self.nemico = NemicoForte()
        super().__init__()

    def descrizione(self):
        if self.nemico.vivo():
            if hasattr(self.nemico, 'descrizione_vivo'):
                return self.nemico.descrizione_vivo
            else:
                return "\nUn {} ti aspetta!\n".format(self.nemico.nome)                
        else:
            if hasattr(self.nemico, 'descrizione_morto'):
                return self.nemico.descrizione_morto
            else:
                return "\nHai sconfitto il {}\n".format(self.nemico.nome)
            
class CasellaBoss(CasellaMostro):
    def __str__(self):
        return 'MB'
    def __init__(self):        
        super().__init__()
        self.nemico = NemicoBoss()
    def descrizione(self, veloce=False):
        s=''
        if self.nemico.vivo() and not self.visitata:
            s=open('./immagini_storie/immagine_boss.txt').read()
        return s+super().descrizione()
            
class CasellaCommerciante(CasellaMappa):
    def __str__(self):
        return 'CC'
    
    def __init__(self):
        self.commerciante = Commerciante()
        super().__init__()
    
    def descrizione(self):
        if self.visitata:
            return '\nBen tornato nel mio emporio.\n'
        else:
            return '\nBenvenuto nel mio emporio.\n'
    
    def vuoi_commerciare(self, giocatore):
        trovato = False
        while not trovato:
            scelta=input("""
Cosa vuoi fare:
0: non voglio scambiare
1: voglio comprare
2: voglio vendere
Scelta: """);
            if scelta.isnumeric() and int(scelta)<=2 and int(scelta)>=0:
                trovato = True
                if int(scelta)==1:
                    self.commercia(giocatore, self.commerciante)
                elif int(scelta)==2:
                    self.commercia(self.commerciante, giocatore)
            else:
                print("\nScelta errata. Riprovare.\n")
    
    def commercia(self, compratore, venditore):
        if venditore.inventario == []:
            print("\nIl venditore non ha niente da vendere\n")
            return
        i = 1
        print("\nOggetti in vendita:")
        for oggetto in venditore.inventario:
            print("{}: {} - {} oro".format(i, oggetto.nome, oggetto.prezzo))
            i += 1
        print("\nOro compratore:{}".format(compratore.oro)) 
        trovato = False
        while not trovato:
            scelta = input("Inserisci il numero (0 per uscire): ")
            if scelta.isnumeric() and int(scelta)<=len(venditore.inventario) \
               and int(scelta)>=0:
                if int(scelta)==0:
                    return
                oggetto_scelto = venditore.inventario[int(scelta)-1]
                self.scambia(compratore,venditore,oggetto_scelto)
                trovato = True
            else:
                print("\nScelta errata. Riprovare.\n")

    def scambia(self, compratore, venditore, oggetto):
        if oggetto.prezzo > compratore.oro:
            print('\nOro non sufficiente.\n')
            return
        venditore.inventario.remove(oggetto)
        compratore.inventario.append(oggetto)
        venditore.oro = venditore.oro + oggetto.prezzo
        compratore.oro = compratore.oro - oggetto.prezzo
        print('\nScambio effettuato\n')
    
II = CasellaInizio
NN = CasellaNoiosa
FF = CasellaFine
VV = CasellaVuota
MM = CasellaMostro
MB = CasellaBoss
CC = CasellaCommerciante
OO = CasellaOro
BB = CasellaBuca
PP = CasellaPorta
KK = CasellaOggetto
ZZ = CasellaCantastorie
    
class Mappa():
    def __init__(self,nome_file=''):
        self.facile=False
        if nome_file=='':
            mondo = """FF(),MM(),MM(),MM(),CC(),OO(),
              VV(),VV(),VV(),VV(),VV(),NN(),
              MM(),II(),NN(),VV(),OO(),MM(),
              VV(),NN(),VV(),BB(),MM(),NN(),
              VV(),NN(),VV(),BB(),NN(),VV(),
              CC(),NN(),OO(),NN(),NN(),VV()"""
        else:
            with open(nome_file) as file:
                mondo = file.read()                
        righe = mondo.splitlines()
        mondo=[]
        for riga in righe:
            mondo.append(riga.split(','))
        self.mappa = []        
        for riga in mondo:
            riga_mappa = []            
            for cella in riga:
                if cella[-1:]!=')':
                    riga_mappa.append(eval((cella+'()')))
                else:
                    riga_mappa.append(eval((cella)))
            self.mappa.append(riga_mappa)        
                
    def gioco_facile(self):        
        self.facile=True
        for riga in self.mappa:            
            for stanza in riga:            
                if isinstance(stanza,CasellaMostro):
                    stanza.nemico.danno=int(stanza.nemico.danno*0.5)
                    stanza.nemico.vita=int(stanza.nemico.vita*0.5)
                if isinstance(stanza,CasellaOro):
                    stanza.oro = int(stanza.oro*2)        

    def casella_iniziale(self):
        x=0        
        for riga in self.mappa:
            y=0                    
            for cella in riga:
                if isinstance(cella,CasellaInizio):
                    return (x,y)
                y += 1                
            x += 1
        return (0,0)
                
    def casella_a(self, x, y):        
        if x<0 or y<0 or y>(len(self.mappa)-1) or x>(len(self.mappa[0])-1):
            return False
        else:
            return self.mappa[y][x]
           
    def mappa_visitata(self, giocatore):
        print("""
Legenda mappa:
MM: mostro
CC: commerciante
OO: oro
II: iniziale
PP: porta/roccia/crepaccio
KK: chiave/dinamite/fune
ZZ: cantastorie
[]: muro
**: non visitata
##: posizione attuale

Mappa:
""")
        casella_giocatore = self.casella_a(giocatore.x,giocatore.y)        
        mappa = "╔══════════════════════════════╗"
        for righe in self.mappa:
            mappa +="\n"
            prima=True
            for cella in righe:
                if not prima:
                    mappa +='' #print('-',end='')
                else:
                    mappa +='║'
                prima=False
                if cella == casella_giocatore:
                    mappa +='##' #print('##',end='')
                elif cella.visitata or self.facile:
                    mappa +=str(cella) # print(cella,end='')
                else:
                    mappa +='**' #print('**',end='')
            mappa+='║'
        mappa += "\n╚══════════════════════════════╝\n"
        print(mappa)
        

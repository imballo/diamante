from oggetti import *
from mondo import *
from random import random

class Giocatore:
    def __init__(self, mappa):
        self.inventario = [PozioneCurativa(),
                           DinamiteSilenziata(),
                           PaninoAlSalame(),
                           MelaDiArgento(),
                           BombaFumogena(),
                           SpadaSolare(),
                           PugnaleDiRambo()]
        self.arma = self.arma_potente()
        self.vita = 100
        self.oro=50
        self.mappa = mappa
        self.y,self.x = mappa.casella_iniziale()
        self.casella = self.mappa.casella_a(self.x, self.y)
        self.facile=False
            
    def gioco_facile(self):
        self.facile=True
        self.inventario.append(SpadaSolare())
        self.inventario.append(PaninoAlSalame())
        self.vita=int(self.vita*2)
        self.oro=int(self.oro*2)
        
    def vivo(self):
        if self.vita>0:
            return True
        else:
            return False
    
    def muovi(self,dx,dy):
        nuova_casella = self.mappa.casella_a(self.x+dx, self.y+dy)
        if not nuova_casella:
            print("\nDi qui non puoi andare!")
        elif isinstance(nuova_casella,CasellaVuota):
            nuova_casella.visitata=True
            print(nuova_casella.descrizione())            
        elif isinstance(nuova_casella,CasellaPorta) and not nuova_casella.porta_aperta:
            nuova_casella.visitata=True
            print(nuova_casella.descrizione())            
        else:
            self.x = self.x+dx
            self.y = self.y+dy
            self.casella = nuova_casella
        return self.casella == nuova_casella
    
    def muovi_nord(self):
        return self.muovi(dx=0,dy=-1)

    def muovi_sud(self):
        return self.muovi(dx=0,dy=1)

    def muovi_est(self):
        return self.muovi(dx=1,dy=0)

    def muovi_ovest(self):
        return self.muovi(dx=-1,dy=0)
    
    def stampa_inventario(self):
        print("\nInventario:")
        for oggetto in self.inventario:            
            print("* {}".format(oggetto))            
        print("* Oro: {}".format(self.oro))
        if (self.arma == None):
            print("* Arma corre: nessuna")
        else:
            print("* Arma corrente: {}".format(self.arma.nome))
        print("")
    
    def lista_armi(self):
        armi = []
        for oggetto in self.inventario:
            if isinstance(oggetto,Arma):
                armi.append(oggetto)
        return armi
        
    def lista_mangiabili(self):
        mangiabili = []
        for oggetto in self.inventario:
            if isinstance(oggetto,Mangiabile):
                mangiabili.append(oggetto)
        return mangiabili    

    def arma_potente(self):
        arma  = None
        for oggetto in self.lista_armi():
            if arma == None or oggetto.danno > arma.danno:
                arma = oggetto
        return arma            

    def attacco(self, nemico):
        migliore_arma = self.arma_potente()
        if migliore_arma == None:
            print("\nNon hai più armi con cui combattere\n")
            return
        if self.arma == None or self.arma not in self.inventario:
            self.arma=migliore_arma
        print ("\nUsi la {} contro {}!".format(self.arma.nome, nemico.nome))
        nemico.vita -= self.arma.danno
        if not nemico.vivo():
            print ("\nHai ucciso {}!".format(nemico.nome))
            tesoro=randint(0,5)
            if tesoro>0:
                print("\nTrovi {} monete d'oro che raccogli!!".format(tesoro))
                self.oro += tesoro
            print('\nLa tua vita residua è: {}'.format(self.vita))
        else:            
            print("\nLa vita residua di {} è di {}".format(nemico.nome,nemico.vita))
        r = random()            
        if r < 0.05:
            print("\nCon un fragore il/la {} si rompe!".format(self.arma.nome))
            self.inventario.remove(self.arma)
            self.arma=None
            
    def usa_oggetto(self):
        oggetti = self.inventario
        if oggetti == []:
            print("\nNon hai nessun oggetto\n")
            return
        trovato = False
        while not trovato:
            print("\nCosa vuoi usare:")
            i = 1
            for oggetto in oggetti:
                print("{}: {}".format(i,oggetto.nome))
                i += 1
            scelta = input("Inserisci il numero: ")
            if scelta.isnumeric() and int(scelta)<=len(oggetti) \
               and int(scelta)>0:
                oggetto_scelto = oggetti[int(scelta)-1]
                #if isinstance(self.casella,CasellaPorta) and isinstance(oggetto_scelto,Chiave) and not self.casella.porta_aperta:
                if isinstance(oggetto_scelto,Chiave) or isinstance(oggetto_scelto,Fune) or isinstance(oggetto_scelto,Dinamite):
                    direzioni=[[-1,0],[1,0],[0,-1],[0,1]]
                    for direzione in direzioni:
                        stanza=self.mappa.casella_a(self.x+direzione[0], self.y++direzione[1])
                        if isinstance(stanza,CasellaPorta) and not stanza.porta_aperta and stanza.tipo=='Porta' and isinstance(oggetto_scelto,Chiave):                            
                            oggetti.remove(oggetto_scelto)
                            stanza.porta_aperta=True
                            print("\nLa chiave apre la porta permettendoti di passare.\n")
                            break;
                        if isinstance(stanza,CasellaPorta) and not stanza.porta_aperta and stanza.tipo=='Roccia' and isinstance(oggetto_scelto,Dinamite):                            
                            oggetti.remove(oggetto_scelto)
                            stanza.porta_aperta=True
                            print("\nFai esplodere la dinamite liberando il passaggio.\n")
                            break;
                        if isinstance(stanza,CasellaPorta) and not stanza.porta_aperta and stanza.tipo=='Crepaccio' and isinstance(oggetto_scelto,Fune):                            
                            oggetti.remove(oggetto_scelto)
                            stanza.porta_aperta=True
                            print("\nUtilizzi la fune per creare un passaggio attraverso il crepaccio.\n")
                            break;                        
                elif isinstance(oggetto_scelto,Arma):
                    self.arma=oggetto_scelto
                    print('\nImpugni la tua nuova arma\n')
                else:
                    print("\n{} non ha alcun effetto\n".format(oggetto_scelto.nome))
                trovato = True
            else:
                print("\nScelta errata. Riprovare.\n")

    def mangia(self):
        mangiabili = self.lista_mangiabili()
        if mangiabili == []:
            print("\nNon hai niente da mangiare\n")
            return
        trovato = False
        while not trovato:
            print("\nCosa vuoi mangiare:")
            i = 1
            for oggetto in mangiabili:
                print("{}: {}".format(i,oggetto.nome))
                i += 1
            scelta = input("Inserisci il numero: ")
            if scelta.isnumeric() and int(scelta)<=len(mangiabili) \
               and int(scelta)>0:
                oggetto_scelto = mangiabili[int(scelta)-1]
                self.vita=self.vita + oggetto_scelto.recupero
                self.inventario.remove(oggetto_scelto)
                print('La tua vita residua è: {}\n'.format(self.vita))
                trovato = True
            else:
                print("\nScelta errata. Riprovare.\n")
                
    def raccogli_oro(self,stanza):
        self.oro = self.oro + stanza.oro
        stanza.oro = 0
    
    def raccogli_oggetto(self,stanza):
        oggetto = stanza.prendi_oggetto()
        if oggetto != None:
            self.inventario.append(oggetto)        
                
        

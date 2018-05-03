from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
import kivy.base
import pickle
import os.path
import timeit
import sys
import builtins as __builtin__

def print(*args, veloce=False, ritardo=0.05, nome_file='', **kwargs):
    return __builtin__.print(*args, **kwargs)
    
class Printer:    
    def write(self,msg):
        app.s.scrivi(msg)
    def flush(self):
        pass
    
sys.stdout = Printer()
    
from giocatore import *
from mondo import *


def usa_oggetto(self, oggetto_nome=''):
    oggetti = self.inventario
    if oggetti == []:
        print("\nNon hai nessun oggetto\n")
        return []    
    if oggetto_nome=='':        
        print("\nCosa vuoi usare:")
        i = 1
        bottoni = []
        for oggetto in oggetti:
            print("{}: {}".format(i,oggetto.nome))
            bottoni.append(oggetto.nome)
            i += 1
        return bottoni
    else:
        oggetto_scelto = oggetti[[oggetto.nome for oggetto in giocatore.inventario].index(oggetto_nome)]
        if isinstance(oggetto_scelto,Chiave) or isinstance(oggetto_scelto,Fune) or isinstance(oggetto_scelto,Dinamite):
            direzioni=[[-1,0],[1,0],[0,-1],[0,1]]
            for direzione in direzioni:
                stanza=self.mappa.casella_a(self.x+direzione[0], self.y+direzione[1])
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

def mangia(self, oggetto_nome=''):
    mangiabili = self.lista_mangiabili()
    if mangiabili == []:
        print("\nNon hai niente da mangiare\n")
        return []
    if oggetto_nome=='':
        print("\nCosa vuoi mangiare:")
        i = 1
        bottoni = []
        for oggetto in mangiabili:
            print("{}: {}".format(i,oggetto.nome))
            bottoni.append(oggetto.nome)
            i += 1
        return bottoni
    else:
        oggetto_scelto = mangiabili[[oggetto.nome for oggetto in giocatore.lista_mangiabili()].index(oggetto_nome)]
        self.vita=self.vita + oggetto_scelto.recupero
        self.inventario.remove(oggetto_scelto)
        print('La tua vita residua è: {}\n'.format(self.vita))

Giocatore.usa_oggetto = usa_oggetto
Giocatore.mangia = mangia

def vuoi_commerciare(self, giocatore,scelta=''):
    print("""
Cosa vuoi fare:
0: non voglio scambiare
1: voglio comprare
2: voglio vendere
Scelta: """);
    scelte=['esco','compro','vendo']
    if scelta=='':
        return scelte
    else:
        if scelta=='compro':
            return self.commercia(giocatore, self.commerciante)
        elif scelta=='vendo':
            return self.commercia(self.commerciante, giocatore)
        else:
            return []

def commercia(self, compratore, venditore, oggetto=''):
    if venditore.inventario == []:
        print("\nIl venditore non ha niente da vendere\n")
        return []
    i = 1
    if oggetto=='':
        print("\nOggetti in vendita:")
        lista_oggetti = []
        for oggetto in venditore.inventario:
            print("{}: {} - {} oro".format(i, oggetto.nome, oggetto.prezzo))
            i += 1
            if compratore==giocatore:
                lista_oggetti.append('c-'+oggetto.nome)
            else:
                lista_oggetti.append('v-'+oggetto.nome)
        print("\nOro compratore:{}".format(compratore.oro))
        if compratore==giocatore:
            lista_oggetti.append('c-esci')
        else:
            lista_oggetti.append('v-esci')
        return lista_oggetti
    else:
        if oggetto!='esci':
            oggetto_scelto = venditore.inventario[[tmp_oggetto.nome for tmp_oggetto in venditore.inventario].index(oggetto)]
            self.scambia(compratore,venditore,oggetto_scelto)    

CasellaCommerciante.vuoi_commerciare = vuoi_commerciare
CasellaCommerciante.commercia = commercia

lista_azioni = ['nord','sud','est','ovest','inventario','mangia','attacca','commercia','mappa','usa','ascolta','aiuto-crediti-esci']

nomi_mappe = {'Il labirinto della fantasia':'./mappe/ap.csv',
              'La mappa dello zig zag':'./mappe/g.csv',
              'La mappa della mortalità':'./mappe/l.csv'}

help = """
Le possibili azioni sono:
h, H, aiuto: aiuto
n, N, nord: muovi verso il nord
s, S, sud: muovi verso il sud
e, E, est: muovi verso l'est
o, O, ovest: muovi verso l'ovest
i, I, inventario: mostra inventario
g, G, mangia: guarisci
a, A, attacca: attacca mostro
c, C, commercio: commercia
m, M, mappa: mappa
u, U, usa: usa oggetto
z, Z, ascolta: ascolta
"""

def carica_gioco(nome_mappa=''):
    global mappa, giocatore, stanza
    mappa = Mappa(nome_mappa)
    giocatore = Giocatore(mappa)
    stanza = giocatore.casella

class Schermo(BoxLayout):
    def chiudi(self,dt):
        print("\nLe GO.ZY vi aspettano per la prossima avventura.")        
        #App.get_running_app().on_pause()
        App.get_running_app().stop()
        Window.close()
        #kivy.base.stopTouchApp()
    
    def scrivi(self,testo):
        testo_tmp = self.testo.text + testo
        max_length = 80*40
        if len(testo_tmp)> max_length:
            testo_tmp = testo_tmp[-max_length:]        
        self.testo.text = testo_tmp
        self.testo.texture_update()
    
    def azione(self,instance):
        global stanza
        azione = instance.text
        if azione == 'Termina avventura':
            Clock.schedule_interval(self.chiudi,2) 
        if azione in lista_azioni or azione in ['continua a giocare','crediti','esci','sono sicuro']:
            if azione in ['h','H','aiuto-crediti-esci','continua a giocare','esci','crediti','sono sicuro']:                
                if azione=='continua a giocare' or azione=='crediti':
                    if azione =='crediti':
                        print(open('./immagini_storie/crediti.txt', encoding='utf8').read(),veloce=True)
                    self.crea_bottoni(lista_azioni)                
                elif azione=='esci':
                    print('\nSei sicuro di volere smettere. Tutti i dati verrano persi.')
                    self.crea_bottoni(['continua a giocare','sono sicuro'])
                elif azione=='sono sicuro':
                    giocatore.vita = 0
                    Clock.schedule_interval(self.chiudi,5)
                    return
                else:
                    print(help)
                    self.crea_bottoni(['continua a giocare','crediti','esci'])
            elif azione in ['n','N','nord'] and not(hasattr(stanza, 'nemico') and stanza.nemico.vivo()):
                if not giocatore.muovi_nord():
                    azione='h'
            elif azione in ['s','S','sud'] and not(hasattr(stanza, 'nemico') and stanza.nemico.vivo()):
                if not giocatore.muovi_sud():
                    azione='h'                    
            elif azione in ['e','E','est'] and not(hasattr(stanza, 'nemico') and stanza.nemico.vivo()):
                if not giocatore.muovi_est():
                    azione='h'
            elif azione in ['o','O','ovest'] and not(hasattr(stanza, 'nemico') and stanza.nemico.vivo()):
                if not giocatore.muovi_ovest():
                    azione='h'
            elif azione in ['i','I','inventario']:
                giocatore.stampa_inventario()
            elif azione in ['g','G','mangia']:
                lista_oggetti=giocatore.mangia()                
                if len(lista_oggetti)>0:
                    self.crea_bottoni(lista_oggetti)
            elif azione in ['u','U','usa']:
                lista_oggetti=giocatore.usa_oggetto()                
                if len(lista_oggetti)>0:
                    self.crea_bottoni(lista_oggetti)
            elif azione in ['m','M','mappa']:
                mappa.mappa_visitata(giocatore)
            elif hasattr(stanza, 'nemico') and stanza.nemico.vivo()  and azione in ['a','A','attacca']:
                giocatore.attacco(stanza.nemico)
            elif hasattr(stanza, 'commerciante') and azione in ['c','C','commercia']:
                lista_scelte=stanza.vuoi_commerciare(giocatore)
                if len(lista_scelte)>0:
                    self.crea_bottoni(lista_scelte)
            elif hasattr(stanza, 'cantastorie') and azione in ['z','Z','ascolta']:
                stanza.cantastorie.racconta_storia(stanza.storia)                
            else:
                print('\nAzione non valida!')
        elif azione in [oggetto.nome for oggetto in giocatore.lista_mangiabili()]:
            giocatore.mangia(azione)            
            self.crea_bottoni(lista_azioni)
            stanza.visitata = True
            return
        elif azione in [oggetto.nome for oggetto in giocatore.inventario]:
            giocatore.usa_oggetto(azione)            
            self.crea_bottoni(lista_azioni)
            stanza.visitata = True
            return
        elif azione in ['esco','compro','vendo']:
            lista_oggetti=stanza.vuoi_commerciare(giocatore,azione)
            if lista_oggetti==[]:
                self.crea_bottoni(lista_azioni)
            else:
                self.crea_bottoni(lista_oggetti)
        elif azione[0:2]=='c-':
            stanza.commercia(giocatore,stanza.commerciante, azione[2:])
            self.crea_bottoni(lista_azioni)
        elif azione[0:2]=='v-':
            stanza.commercia(stanza.commerciante,giocatore, azione[2:])
            self.crea_bottoni(lista_azioni)
        elif azione in ['facile','difficile']:            
            if azione=='facile':                
                mappa.gioco_facile()
                giocatore.gioco_facile()
            print("\nLe GO.ZY sono liete di presentarvi questa fantastica avventura.")
            print("\nDigita h/H help per ricevere aiuto sui comandi!\n")
            print(stanza.descrizione(),end='')
            self.crea_bottoni(lista_azioni)
        elif azione in [*nomi_mappe]:            
            nome_mappa=nomi_mappe[azione]
            carica_gioco(nome_mappa)
            print('Scegli il livello di difficoltà')
            self.crea_bottoni(['facile','difficile'])            
        if hasattr(stanza, 'nemico'):
            stanza.nemico.attacco(giocatore)            
        if not stanza.visitata and not azione in [*nomi_mappe]:
            stanza.visitata = True                
        stanza = mappa.casella_a(giocatore.x,giocatore.y)
        if azione not in  ['h','H','aiuto-crediti-esci','continua a giocare','esci','crediti','sono sicuro','facile','difficile'] \
          and azione not in [*nomi_mappe] and azione not in ['u','U','usa'] and azione not in ['g','G','mangia']:
            print(stanza.descrizione())
        if isinstance(stanza, CasellaOro):
            giocatore.raccogli_oro(stanza)
        if isinstance(stanza, CasellaOggetto):
            giocatore.raccogli_oggetto(stanza)
        if isinstance(stanza,CasellaFine) or not giocatore.vivo():
            print("\nLa tua avventura finisce qui.\n")
            self.crea_bottoni(['Termina avventura'])
                                
        
    def imposta_pro(self,proprieta,valore):
        lista=proprieta.split('.')
        oggetto=self
        i=1
        while (i<(len(lista)-1)):
            oggetto=getattr(self,lista[i])
            i +=1
        setattr(oggetto,lista[i],valore)
        
    def crea_bottoni(self, lista):
        self.bottoni.clear_widgets()
        i = 0
        for elemento in lista:
            self.bottoni.add_widget(Button(text=elemento,on_press=self.azione, font_size='15sp')) #font per telefono 10sp
            
        
    def __init__(self, **kwargs): 
        super(Schermo, self).__init__(**kwargs)
        self.orientation='vertical'
        self.testo = Label(text='',font_name='RobotoMono-Regular', font_size='10sp', text_size=(self.width,None),valign='bottom', size_hint_y=None) # font per telefono 7sp
        self.testo.bind(size=lambda instance,size: self.imposta_pro('self.testo.text_size',(size[0],None)))                
        self.testo.bind(texture_size=lambda instance,size: self.imposta_pro('self.testo.height',size[1]))        
        self.sv = ScrollView()
        self.sv.scroll_y=0        
        self.sv.add_widget(self.testo)
        self.add_widget(self.sv)
        self.bottoni = GridLayout(rows=2, size_hint_y=0.25)                
        self.add_widget(self.bottoni)
        self.crea_bottoni(lista_azioni)
    

class GiocoApp(App):   
    def build(self):
        self.s = Schermo()
        return self.s
    
    def on_pause(self):        
        global mappa, giocatore, stanza        
        file_giocatore = open('./salvataggio/giocatoreData.dat','wb')
        file_testo = open('./salvataggio/testo.dat','wb')
        pickle.dump(giocatore, file_giocatore)
        pickle.dump(self.s.testo.text, file_testo)
        file_giocatore.close
        file_testo.close        
        return True
    
    def on_stop(self):        
        global mappa, giocatore, stanza
        if 'giocatore' in globals():
            file_giocatore = open('./salvataggio/giocatoreData.dat','wb')
            file_testo = open('./salvataggio/testo.dat','wb')
            pickle.dump(giocatore, file_giocatore)
            pickle.dump(self.s.testo.text, file_testo)
            del stanza
            del mappa
            del giocatore
            file_giocatore.close
            file_testo.close
        return True

    def on_resume(self):
        pass

    def on_start(self):
        global mappa, giocatore, stanza
        if os.path.isfile('./salvataggio/testo.dat') and os.path.isfile('./salvataggio/giocatoreData.dat'):
            try:
                with open('./salvataggio/giocatoreData.dat','rb') as file_giocatore:
                    giocatore = pickle.load(file_giocatore)
                    mappa=giocatore.mappa
                    stanza=giocatore.casella
                with open('./salvataggio/testo.dat','rb') as file_testo:                        
                    testo = pickle.load(file_testo)
            except (EOFError) as error:
                carica_gioco()
        if isinstance(stanza,CasellaFine) or not giocatore.vivo():
            print('Scegli la mappa:')
            scelte=[*nomi_mappe]
            self.s.crea_bottoni(scelte)
        elif isinstance(stanza,CasellaInizio) and not stanza.visitata:
            print('Scegli la mappa:')
            scelte=[*nomi_mappe]
            self.s.crea_bottoni(scelte)
        else:
            self.s.scrivi(testo)        

carica_gioco()
app = GiocoApp()
app.run()

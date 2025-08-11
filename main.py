from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.uix.scrollview import ScrollView


import wget
import bleak
import asyncio
import time

from android.storage import primary_external_storage_path
primary_ext_storage = primary_external_storage_path()
from android.permissions import request_permissions, Permission 
#These permissions guys are required if the app wants to use the bluetooth, the storage one is for uploading updates.
request_permissions([Permission.BLUETOOTH_CONNECT,Permission.BLUETOOTH_SCAN, Permission.ACCESS_COARSE_LOCATION, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE ])

ids=[]
macs=[]
codes=[]
def setUp(filename):
	bikes=open(filename,'r')

	BIKES=bikes.readlines()
	bikes.close()
	global ids
	global macs
	global codes
	ids=[]
	macs=[]
	codes=[]

	for b in BIKES:
		bb=b.split(" ")
		ids.append(bb[0])
		s=bb[1]
		s=':'.join(s[i:i+2] for i in range(0, len(s), 2))
		macs.append(s)
		codes.append(bb[2])

setUp('./TOT_BIKES.txt')
biketau="""
_______||||______|_______|__||||________|_||||||
|||______|||________||||________||__________||__
_________|__________|______|_________||_______|||||
 """
declare=open('./important.txt','r')
important=declare.read()
declare.close()

kv = """
ScreenManager:
    in_class: text
    id: sc_m
        
    Screen:
        name: 'welcome'
        canvas:
            Color:
                rgba: 0.85, 0.85, 1, 0.8
            Rectangle:
                size: self.size
                pos: self.pos
        MDLabel:
            text: 'Ridegodi'
            font_style: 'H5'
            font_name: '77'
            pos_hint: {'center_x': 0.6, 'center_y': 0.8}
        MDLabel:
            text: ''
            font_size: 11
            id: bike
            pos_hint: {'center_x': 0.9, 'center_y': 0.8}
        MDTextField:
            mode: "round"
            id: text
            hint_text: 'bikeID (IE..)'
            helper_text: 'Check availability'
            helper_text_mode: "on_focus" 
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}
            size_hint_x: None 
            width: 300
            icon_left: "key-variant"
            required: True
        MDCheckbox:
            size_hint: None, None
            size: "48dp", "48dp"
            pos_hint: {'center_x': 0.75, 'center_y': 0.4}
            on_active: app.on_checkbox_active(*args)
        MDLabel:
            adaptive_size: True
            text: 'use update'
            pos_hint: {'center_x': .75, 'center_y': .45}
        MDFillRoundFlatIconButton:
            md_bg_color: "orange"
            icon: "bee-flower"
            icon_color: "black"
            text_color: "black"
            
            text: 'Check'
            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
            on_press:
                app.auth()
                
        MDLabel:
            text: ''
            font_size: 25
            id: show
            pos_hint: {'center_x': 0.6, 'center_y': 0.3}


        MDRoundFlatIconButton:
            line_color: "red"
            text_color: "red"
            text: ''
            font_name: '77'
            id: but
            pos_hint: {'center_x': 0.5, 'center_y': 0.1}
            on_press:
                app.open()
        MDFillRoundFlatIconButton:
            md_bg_color: "orange"
            text: "Info/Menu"
            icon: "folder"
            pos_hint: {'right': 1, 'top': 1}
            on_press: app.callback1()

    Screen:
        name: 'menu'
        canvas:
            Color:
                rgba: 1, 0.74, 0.6, 0.8
            Rectangle:
                size: self.size
                pos: self.pos

        MDFillRoundFlatIconButton:
            md_bg_color: "orange"
            text: "Update keys"
            icon: "key"
            pos_hint: {'center_x': 0.5, 'center_y': 0.8 }
            on_press: app.callback()

        MDFillRoundFlatIconButton:
            md_bg_color: "orange"
            text: "Instructions"
            icon: "folder"
            pos_hint: {'center_x': 0.5, 'center_y': 0.6 }
            on_press: app.instructions()
        MDFillRoundFlatIconButton:
            md_bg_color: "orange"
            text: "Why this hack? README"
            icon: "bee"
            pos_hint: {'center_x': 0.5, 'center_y': 0.4 }
            on_press: app.why()
    Screen:
        name: 'instructions'
        ScrollView:
            do_scroll_y: True
            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                MDFillRoundFlatIconButton:
                    md_bg_color: "orange"
                    text: "Home"
                    icon: "folder"
                    pos_hint: {'right': 1, 'top': 1}
                    on_press: app.homeback()
                Label:
                    height: self.texture_size[1]
                    size_hint_y: None
                    text_size: self.width, None
                    padding: 10, 10
                    text: "\\n \\n \\n \\n Italian: \\n Beh, che dire, l uso è abbastanza intuitivo: \\n  -Inserite il codice identificativo della Mobike\\n  nella prima casella di testo. \\n (il codice si trova sul telaio o sotto il QR code) \\n - ora premere il pulsante Check e verificare la \\n disponibilità nei nostri archivi pirata. \\n - nel caso in cui la bici sia stata \\n riconosciuta dai nostri sistemi \\n IN QUESTA VERSIONE A QUESTO PUNTO DOVRETE FARE UNA SCANSIONE BLUETOOTH MANUALE: ABBASSATE LA TENDINA DEL VOSTRO TELEFONO E TENETE PREMUTO L ICONA DEL BLUETOOTH, A QUESTO PUNTO AVVIATE LA SCANSIONE E ASPETTATE FINCHÈ NON SARÀ VISIBILE TRA I DISPOSITIVI IL NOME MOOV,\\n se anche questa ricerca va a buon fine \\n il vostro telefono ha riconosciuto  la bici nei paraggi e il pulsante \\n finale sarà allora disponibile\\n \\n Premetelo e tirate un bel sospiro: \\n esiste ancora, per fortuna, la magia. \\n \\n --->Read the Why this Hack<--- \\n \\n Aggiornamenti: \\n Se si è trovato un file di aggiornamento \\n per le chiavi di sblocco, \\n andate nella sezione update e caricatelo, \\n una volta fatto ciò basterà cliccare \\n sul box nella schermata iniziale \\n per usare i nuovi codici." 
                    color: 'black'


    Screen:
        name: 'why'
        ScrollView:
            do_scroll_y: True
            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                MDFillRoundFlatIconButton:
                    md_bg_color: "orange"
                    text: "Home"
                    icon: "folder"
                    pos_hint: {'right': 1, 'top': 1}
                    on_press: app.homeback()

                Label:
                    id: whylab
                    color: 'black'
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None
                    padding: 10, 10
                    text: ''


    Screen:
        name: 'update'
        canvas:
            Color:
                rgba: 1, 0.7, 0.2, 0.5
            Rectangle:
                size: self.size
                pos: self.pos

        MDFillRoundFlatIconButton:
            md_bg_color: "orange"
            text: "Home"
            icon: "folder"
            pos_hint: {'right': 1, 'top': 1}
            on_press: app.homeback()

        MDLabel:
            text: "They might change the keys \\n or simply we don't have them yet, \\n in that case stick to the original ones \\n or upload them from \\n a file when updates are available, \\n in need of aid new keys \\n will be published somehow, don't worry."
            color: 'black'
            pos_hint: {'center_x': 0.6, 'center_y': 0.8}

        MDFillRoundFlatIconButton:
            id: upload
            md_bg_color: "orange"
            icon: "city"
            icon_color: "black"
            text_color: "black"

            text: 'Upload File'
            pos_hint: {'center_x': 0.5, 'center_y': 0.3}
            on_release: app.file_manager_open()
        
        
"""
def copyfile_example(source, dest):
    # Beware, this example does not handle any edge cases!
    with open(source, 'rb') as src, open(dest, 'wb') as dst:
        dst.write(src.read())

async def writeccc(address,self):
    client =bleak.BleakClient(address)
    try:
        await client.connect()
        await client.write_gatt_char('6e40ff02-5fe1-46a8-9330-9b4670ca5106',bytes.fromhex(codes[self.current]),True)
        self.root.ids.show.text="hop hop and go!"
    except Exception as e:
        self.root.ids.show.text=str(e)
    finally:
        await client.disconnect()
        

class Main(MDApp):
    current=0
    in_class = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(kv)
        bik= self.screen.ids.bike
        bik.text=biketau
        self.screen.ids.whylab.text=important
        self.manager_open = False
    def build(self):
        self.icon = 'free.jpeg'
        return self.screen
        
        
    def auth(self):
        if self.root.in_class.text.upper() in ids:
            self.current=ids.index(self.root.in_class.text.upper())
            label = self.root.ids.show
            label.text = "The bike is available, \n open the bluetooth scan option of your phone \n and wait to see a MOOV device \n then, Break it!"
            self.root.ids.but.text="Sblokka!"
        else:
            label = self.root.ids.show
            label.text = "Bike not available for the moment"
            
    def open(self):
    	asyncio.run(writeccc(macs[self.current],self))

    def callback1(self):
        self.root.current='menu'
    def callback(self):
        self.root.current='update'
    def instructions(self):
        self.root.current='instructions'
    def why(self):
        self.root.current='why'
    def homeback(self):
        print("presses")
        self.root.current='welcome'
    def on_checkbox_active(self, checkbox, value):
        if value:
             try:
                 setUp('./Update.txt')
             except:
                 pass
        else:
             setUp('./TOT_BIKES.txt')

    def file_manager_open(self):
        if not self.manager_open:
            self.file_manager = MDFileManager(
                exit_manager=self.exit_manager, select_path=self.select_path)
            self.file_manager.show(primary_ext_storage)

    def select_path(self, path):
        copyfile_example(path, './Update.txt')
        self.screen.ids.upload.md_bg_color='green'
        self.exit_manager()
        toast(path)

    def exit_manager(self, *args):
        self.file_manager.close()
        self.manager_open = False

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device..'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


Main().run()

import PySimpleGUI as sg
from darbuotojai_back import Darbuotojai
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class DarbuotojaiGui:
    def get_data(self):
        self.darbuotoju_sarasas = session.query(Darbuotojai).all()
        data = [
            [item.id, item.vardas, item.pavarde, item.gimimo_data, item.pareigos, item.atlyginimas, item.nuo_kada_dirba]
            for item in self.darbuotoju_sarasas
        ]
        return data

    def __init__(self):
        data = self.get_data()
        headers = ['ID', 'Vardas', 'Pavarde', 'Gimimo data', 'Pareigos', 'Atlyginimas', 'Nuo kada dirba']
        self.table = sg.Table(values=data, headings=headers, auto_size_columns=True, key='-TABLE-', enable_events=True)
        self.layout = [
            [self.table],
            [sg.Button('Prideti nauja darbuotoja', key='prideti'), sg.Button('Atnaujinti darbuotojo info', key='atnaujinti'), sg.Button('Istrinti darbuotoja', key='istrinti'), sg.Button('Uzdaryti programa', key='uzdaryti')],
        ]
        self.window = sg.Window('Darbuotojai', layout=self.layout)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == 'uzdaryti':
                break
            elif event == 'prideti':
                darbuotojas = self.prideti_darbuotoja()
                if isinstance(darbuotojas, Darbuotojai):
                    self.table.update(values=self.get_data())
            elif event == 'istrinti':
                pasirinkta_eilute = values['-TABLE-']
                if pasirinkta_eilute:
                    pasirinkta_eilute = pasirinkta_eilute[0]
                    trinamas_darbuotojas = session.query(Darbuotojai).get(self.darbuotoju_sarasas[pasirinkta_eilute].id)
                    session.delete(trinamas_darbuotojas)
                    session.commit()
                    if isinstance(trinamas_darbuotojas, Darbuotojai):
                        del self.darbuotoju_sarasas[pasirinkta_eilute]
                        self.table.update(values=self.get_data())
            elif event == 'atnaujinti':
                pasirinkta_eilute = values['-TABLE-']
                if pasirinkta_eilute:
                    pasirinkta_eilute = pasirinkta_eilute[0]
                    atnaujinamas_darbuotojas = self.darbuotoju_sarasas[pasirinkta_eilute]
                    atnaujintas_darbuotojas = self.atnaujinti_darbuotoja(atnaujinamas_darbuotojas)
                    self.table.update(values=self.get_data())

    def prideti_darbuotoja(self):

        layout = [
            [sg.Text('Iveskite varda:'), sg.Input('', key='vardas')],
            [sg.Text('Iveskite pavarde:'), sg.Input('', key='pavarde')],
            [sg.Text('Iveskite gimimo data:'), sg.Input('', key='gimimo_data')],
            [sg.Text('Iveskite pareigas:'), sg.Input('', key='pareigos')],
            [sg.Text('Iveskite atlyginima:'), sg.Input('', key='atlyginimas')],
            [sg.Text('Iveskite idarbinimo data:'), sg.Input('', key='nuo_kada_dirba')],
            [sg.Button('Prideti', key='Prideti'), sg.Button('Atsaukti', key='Atsaukti')]
        ]
        window_add = sg.Window('Prideti nauja darbuotoja', layout=layout)

        while True:
            event, values = window_add.read()
            if event in (None, 'Atsaukti'):
                window_add.close()
                return None
            elif event == 'Prideti':
                try:
                    darbuotojas = Darbuotojai(
                        vardas=values['vardas'], 
                        pavarde=values['pavarde'], 
                        gimimo_data=values['gimimo_data'], 
                        pareigos=values['pareigos'], 
                        atlyginimas=values['atlyginimas'], 
                        nuo_kada_dirba=values['nuo_kada_dirba'])
                    session.add(darbuotojas)
                    session.commit()
                except Exception as e:
                    print(e)
                else:
                    window_add.close()
                    return darbuotojas
                
    def atnaujinti_darbuotoja(self, darbuotojas):
                
        layout = [
            [sg.Text('Vardas:'), sg.Input(darbuotojas.vardas, key='vardas')],
            [sg.Text('Pavarde:'), sg.Input(darbuotojas.pavarde, key='pavarde')],
            [sg.Text('Gimimo data:'), sg.Input(darbuotojas.gimimo_data, key='gimimo_data')],
            [sg.Text('Pareigos:'), sg.Input(darbuotojas.pareigos, key='pareigos')],
            [sg.Text('Atlyginimas:'), sg.Input(darbuotojas.atlyginimas, key='atlyginimas')],
            [sg.Text('Idarbinimo data:'), sg.Input(darbuotojas.nuo_kada_dirba, key='nuo_kada_dirba')],
            [sg.Button('Atnaujinti', key='Atnaujinti'), sg.Button('Atsaukti', key='Atsaukti')]
        ]
        window_add = sg.Window('Atnaujinti darbuotojo info', layout=layout)

        while True:
            event, values = window_add.read()
            if event in (None, 'Atsaukti'):
                window_add.close()
                return None
            elif event == 'Atnaujinti':
                try:
                    darbuotojas.vardas = values['vardas']
                    darbuotojas.pavarde = values['pavarde']
                    darbuotojas.gimimo_data = values['gimimo_data']
                    darbuotojas.pareigos = values['pareigos']
                    darbuotojas.atlyginimas = values['atlyginimas']
                    darbuotojas.nuo_kada_dirba = values['nuo_kada_dirba']
                    session.commit()
                except Exception as e:
                    print(e)
                else:
                    window_add.close()
                    return darbuotojas
              

darbuotojai = DarbuotojaiGui()
darbuotojai.run()

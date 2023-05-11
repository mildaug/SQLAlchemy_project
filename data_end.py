from typing import Any
from sqlalchemy import create_engine, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column
from datetime import datetime

engine = create_engine('sqlite:///data.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    pass


class Darbuotojai(Base):
    __tablename__ = "Darbuotojai"
    id = mapped_column(Integer, primary_key=True)
    vardas = mapped_column(String(50), nullable=False)
    pavarde = mapped_column(String(50), nullable=False)
    gimimo_data = mapped_column(String(50), nullable=False)
    pareigos = mapped_column(String(50), nullable=False)
    atlyginimas = mapped_column(Float(50), nullable=False)
    nuo_kada_dirba = mapped_column(String(50), nullable=False)

    def __init__(self, **kw: Any):
        # super().__init__(**kw)
        for key, value in kw.items():
            setattr(self, key, value)
    
    def __repr__(self) -> str:
        return f"({self.id}, {self.vardas}, {self.pavarde}, {self.gimimo_data}, {self.pareigos}, {self.atlyginimas}, {self.nuo_kada_dirba})"
    
Base.metadata.create_all(engine)

def spausdinti(session):
    darbuotojai = session.query(Darbuotojai).all()
    print("-------------------")
    for darbuotojas in darbuotojai:
        print(darbuotojas)
    print("-------------------")
    return darbuotojai


while True:
    pasirinkimas = input("""[===Pasirinkite veiksma===]: 
1 - Perziureti darbuotojus
2 - Sukurti darbuotoja
3 - Atnaujinti darbuotojo info
4 - Istrinti darbuotoja
0 - Uzdaryti programa
""")

    try:
        pasirinkimas = int(pasirinkimas)
    except:
        pass

    if pasirinkimas == 1:
        spausdinti(session)

    elif pasirinkimas == 2:
        vardas = input("Iveskite varda: ")
        pavarde = input("Iveskite pavarde: ")
        gimimo_data = input("Iveskite gimimo data: ")
        pareigos = input("Iveskite pareigas: ")
        atlyginimas = input("Iveskite atlyginima: ")
        nuo_kada_dirba = input("Iveskite idarbinimo data: ")
        darbuotojas = Darbuotojai(vardas=vardas, pavarde=pavarde, gimimo_data=gimimo_data, pareigos=pareigos, atlyginimas=atlyginimas, nuo_kada_dirba=nuo_kada_dirba)
        session.add(darbuotojas)
        session.commit()

    elif pasirinkimas == 3:
        darbuotojai = spausdinti(session)
        try:
            keiciamas_darbuotojas_id = int(input("Pasirinkite norimo pakeisti darbuotojo ID: "))
            keiciamas_darbuotojas = session.get(Darbuotojai, keiciamas_darbuotojas_id)
        except Exception as e:
            print(f"Klaida: {e}")
        else:
            pakeitimas = int(input("Ka norite pakeisti: 1 - varda, 2 - pavarde, 3 - gimimo data, 4 - pareigas, 5 - atlyginima, 6 - idarbinimo data: "))
            if pakeitimas == 1:
                keiciamas_darbuotojas.vardas = input("Iveskite nauja varda: ")
            if pakeitimas == 2:
                keiciamas_darbuotojas.pavarde = input("Iveskite nauja pavarde: ")
            if pakeitimas == 3:
                keiciamas_darbuotojas.gimimo_data = input("Iveskite nauja gimimo data: ")
            if pakeitimas == 4:
                keiciamas_darbuotojas.pareigos = input("Iveskite naujas pareigas: ")
            if pakeitimas == 5:
                keiciamas_darbuotojas.atlyginimas = input("Iveskite nauja atlyginima: ")
            if pakeitimas == 6:
                keiciamas_darbuotojas.pavarde = input("Iveskite nauja idarbinimo data: ")
            session.commit()

    elif pasirinkimas == 4:
        darbuotojai = spausdinti(session)
        trinamo_darbuotjo_id = int(input("Pasirinkite norimo istrinti darbuotojo ID: "))
        try:
            trinamas_darbuotojas = session.get(Darbuotojai, trinamo_darbuotjo_id)
            session.delete(trinamas_darbuotojas)
            session.commit()
        except Exception as e:
            print(f"Klaida: {e}")

    elif pasirinkimas == 0:
        print("Aciu, kad naudojotes programa")
        break
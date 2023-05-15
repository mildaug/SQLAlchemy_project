from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# DB
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    f_name = Column(String(50))
    l_name = Column(String(50))
    email = Column(String(50))
    orders = relationship('Order', back_populates='customer')

class Order(Base):
    __tablename__ = 'order_'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    date_ = Column(String(50))
    status_id = Column(Integer, ForeignKey('status.id'))
    customer = relationship('Customer', back_populates='orders')
    products = relationship('ProductOrder', back_populates='order')
    status = relationship('Status', back_populates='orders')

def print_orders(session):
    uzsakymai = session.query(Order).all()
    for uzsakymas in uzsakymai:
        print(uzsakymas)
    return uzsakymai

class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    orders = relationship('Order', back_populates='status')

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Float(50))
    orders = relationship('ProductOrder', back_populates='product')

class ProductOrder(Base):
    __tablename__ = 'product_order'
    order_id = Column(Integer, ForeignKey('order_.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    quantity = Column(Integer)
    order = relationship('Order', back_populates='products')
    product = relationship('Product', back_populates='orders')


engine = create_engine('sqlite:///shop_project.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Backend
while True:
    choice = input('''[===Pasirinkite veiksma===]: 
1 - Prideti pirkeja
2 - Prideti produkta
3 - Prideti statusa
4 - Prideti uzsakyma
5 - Istraukti uzsakyma pagal ID
6 - Pakeisti uzsakymo statusa pagal ID
7 - Prideti i uzsakyma produktus su kiekiais
0 - Uzdaryti programa
''').strip()

    try:
        choice = int(choice)
    except ValueError:
        pass

    if choice == 1:
        f_name = input('Iveskite varda: ')
        l_name = input('Iveskite pavarde: ')
        email = input('Iveskite el. pasta: ')

        klientas = Customer(f_name=f_name, l_name=l_name, email=email)
        session.add(klientas)
        session.commit()

    elif choice == 2:
        name = input('Iveskite produkta: ')
        price = input('Iveskite kaina: ')

        produktas = Product(name=name, price=price)
        session.add(produktas)
        session.commit()

    elif choice == 3:
        name = input('Iveskite statusa: ')

        statusas = Status(name=name)
        session.add(statusas)
        session.commit()

    elif choice == 4:
        customer_id = input('Iveskite kliento ID: ')
        date_ = input('Iveskite uzsakymo data: ')
        status_id = input('Iveskite uzsakymo statusa: ')

        uzsakymas = Order(customer_id=customer_id, date_=date_, status_id=status_id)
        session.add(uzsakymas)
        session.commit()

    elif choice == 5:
        uzsakymo_id = int(input('Iveskite uzsakymo ID: '))
        uzsakymo_info = session.query(Order).filter(Order.id == uzsakymo_id).first()
        if uzsakymo_info:
            print(f"Uzsakymo ID: {uzsakymo_info.id}")
            print("Uzsakyma sudaro:")
            for product_order in uzsakymo_info.products:
                product = product_order.product
                print(f"Produkto ID: {product.id}, Pavadinimas: {product.name}, Kaina: {product.price}")
        else:
            print('Uzsakymas su nurodytu numeriu nerastas.')

    elif choice == 6:
        def print_orders(session):
            uzsakymai = session.query(Order).all()
            for uzsakymas in uzsakymai:
                print(uzsakymas)
            return uzsakymai

        keiciamas_uzsakymas_id = int(input('Pasirinkite norimo pakeisti uzsakymo ID: '))
        keiciamas_uzsakymas = session.query(Order).filter(Order.id == keiciamas_uzsakymas_id).first()

        if keiciamas_uzsakymas:
            naujas_statusas_id = input('Iveskite nauja statuso ID: ')
            keiciamas_uzsakymas.status_id = naujas_statusas_id
            session.commit()
        else:
            print('Uzsakymas su nurodytu ID nerastas.')

    elif choice == 7:
        order_id = int(input('Iveskite uzsakymo ID: '))
        product_id = int(input('Iveskite produkto ID: '))
        quantity = int(input('Iveskite kieki: '))

        order = session.query(Order).filter(Order.id == order_id).first()
        product = session.query(Product).filter(Product.id == product_id).first()

        if order and product:
            product_order = ProductOrder(order_id=order_id, product_id=product_id, quantity=quantity)
            session.add(product_order)
            session.commit()
        else:
            print('Uzsakymas arba produktas su nurodytu ID nerastas.')

    elif choice == 0:
        print('Aciu, kad naudojotes programa')
        break
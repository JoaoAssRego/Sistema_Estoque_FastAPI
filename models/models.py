from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType
from datetime import datetime
from enum import Enum

# Configuração do banco de dados SQLite
db = create_engine("sqlite:///./banco.db")

# Criação da base declarativa
Base = declarative_base()

# Enums para tipos de dados
class OccupationType(Enum):
    PACKER = "packer"
    SYSTEM_ADMIN = "system_admin"
    LOGISTICS_COORDINATOR = "logistics_coordinator"

class MovementType( Enum):
    IN = "in"
    OUT = "out"

class OrderStatus(Enum): # Utilizado no lugar de uma tupla para melhor clareza e segurança
    PENDENTE = "pendente"
    ENVIADO = "enviado"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    occupation = Column(ChoiceType(choices=[
        (OccupationType.PACKER.value, 'Packer'),
        (OccupationType.SYSTEM_ADMIN.value, 'System Admin'),
        (OccupationType.LOGISTICS_COORDINATOR.value, 'Logistics Coordinator')
    ]), nullable=False)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now, nullable=True)

    def __init__(self, occupation, name, email, password, active=True, admin=False):
        self.occupation = occupation
        self.name = name
        self.email = email
        self.password = password
        self.active = active
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, occupation={self.occupation}, active={self.active})>"

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, description={self.description})>"
    
class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    contact_info = Column(String(20))

    def __init__(self, name, contact_info):
        self.name = name
        self.contact_info = contact_info

    def __repr__(self):
        return f"<Supplier(id={self.id}, name={self.name}, contact_info={self.contact_info})>"

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))

    # Relacionamentos
    category = relationship("Category")
    supplier = relationship("Supplier")
    stock_level = relationship("StockLevel", uselist=False, back_populates="product")

    def __init__(self, name, description, price, category_id, supplier_id, created_at=None):
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id
        self.supplier_id = supplier_id
        self.created_at = created_at or datetime.now()
    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, description={self.description}, price={self.price})>"

class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    movement_type = Column(ChoiceType(choices=[
        (MovementType.IN.value, 'In'),
        (MovementType.OUT.value, 'Out')
    ]), nullable=False)
    quantity = Column(Integer, nullable=False)
    reference_type = Column(String(20))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    product = relationship("Product")
    user = relationship("User")

    def __init__(self, product_id, movement_type, quantity, user_id, reference_type=None, created_at=None):
        self.product_id = product_id
        self.movement_type = movement_type
        self.quantity = quantity
        self.reference_type = reference_type
        self.user_id = user_id
        self.created_at = created_at or datetime.now()

    def __repr__(self):
        return f"<StockMovement(id={self.id}, product_id={self.product_id}, movement_type={self.movement_type}, quantity={self.quantity})>"

class StockLevel(Base):
    __tablename__ = "stock_levels"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, unique=True)  # Um produto = um nível de estoque
    current_quantity = Column(Integer, default=0)
    minimum_quantity = Column(Integer, default=0)
    maximum_quantity = Column(Integer)
    location = Column(String(50))
    
    # Relacionamento
    product = relationship("Product", back_populates="stock_level")

    def __init__(self, product_id, current_quantity=0, minimum_quantity=0, maximum_quantity=None, location=None):
        self.product_id = product_id
        self.current_quantity = current_quantity
        self.minimum_quantity = minimum_quantity
        self.maximum_quantity = maximum_quantity
        self.location = location
    
    def __repr__(self):
        return f"<StockLevel(id={self.id}, product_id={self.product_id}, current_quantity={self.current_quantity})>"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    status = Column(ChoiceType(choices=[
        (OrderStatus.PENDENTE.value, 'Pendente'),
        (OrderStatus.ENVIADO.value, 'Enviado'),
        (OrderStatus.ENTREGUE.value, 'Entregue'),
        (OrderStatus.CANCELADO.value, 'Cancelado')
    ]), default=OrderStatus.PENDENTE.value)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    total_price = Column(Float, nullable=False, default=0.0)
    
    # Relacionamentos
    user = relationship("User")
    product = relationship("Product")
    
    def __init__(self, status, user_id, product_id, quantity, total_price):
        self.status = status
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.total_price = total_price

    def __repr__(self):
        return f"<Order(id={self.id}, status={self.status}, user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity})>"

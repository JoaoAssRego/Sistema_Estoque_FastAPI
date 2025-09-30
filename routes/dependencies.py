from models import db # Importa o engine do banco de dados
from sqlalchemy.orm import sessionmaker # Importa sessionmaker para criar sessões

# Dependência para fornecer uma sessão do banco de dados
def session_dependencies():
    try:
        Session = sessionmaker(bind=db)
        yield Session() # Fornece a sessão e o yield permite que o FastAPI gerencie o ciclo de vida da sessão
    finally:
        Session().close() # Garante que a sessão seja fechada após o uso

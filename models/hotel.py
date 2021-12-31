from sql_alchemy import banco

class HotelModel(banco.Model):
    __tablename__ = 'hoteis' # cria o nome da tabela
    
    hotel_id = banco.Column(banco.String(255), primary_key=True) # cria a coluna hotel_id STRING(255) como PK
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1)) # cria a coluna estrelas como REAL 2 casas decimais
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))
    
    def __init__(self,hotel_id,nome,estrelas,diaria,cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
    
    def json(self):
        return {
            'hotel_id':self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade,
        }
    
    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first() #SELECT * FROM hoteis WHERE hotel_id = $hotel_id LIMIT=1;
        if hotel:
            return hotel
        return None
    
    def save_hotel(self):
        banco.session.add(self) # Pega a sessão do banco, e salva o propio obj no bannco
        banco.session.commit()
        
        
    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()
        
    def update_hotel(self,nome,estrelas,diaria,cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
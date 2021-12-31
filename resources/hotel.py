from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3


def normalize_path_params(cidade=None,estrelas_min=0,estrelas_max=5,diaria_min=0,
                          diaria_max=99999,limit=50,offset=0,**data):
    if cidade:
         return {
             'estrelas_min': estrelas_min,
             'estrelas_max': estrelas_max,
             'diaria_min': diaria_min,
             'diaria_max': diaria_max,
             'cidade': cidade,
             'limit': limit,
             'offset': offset,
         }
    return {
             'estrelas_min': estrelas_min,
             'estrelas_max': estrelas_max,
             'diaria_min': diaria_min,
             'diaria_max': diaria_max,
             'limit': limit,
             'offset': offset,
         }


path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

class Hoteis(Resource):
    
    def get(self):
        
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()
        
        data = path_params.parse_args()
        valid_data = {chave:data[chave] for chave in data if data[chave] is not None}
        params = normalize_path_params(**valid_data)
        
        if not params.get('cidade'):
            query = "SELECT * FROM hoteis WHERE ( estrelas >= ? and estrelas <= ? ) and \
                        (diaria >= ? and diaria <= ? ) LIMIT ? OFFSET ?"
                        
            values = tuple([params[chave] for chave in params])
            result = cursor.execute(query,values)
            
        else:
            query = "SELECT * FROM hoteis WHERE ( estrelas >= ? and estrelas <= ? ) and \
                        (diaria >= ? and diaria <= ? ) and cidade = ? LIMIT ? OFFSET ?"

            values = tuple([params[chave] for chave in params])
            result = cursor.execute(query,values)
        
        
        hoteis = []
        for line  in result:
            hoteis.append({
            'hotel_id': line[0],
            'nome':line[1],
            'estrelas': line[2],
            'diaria': line[3],          
            'cidade': line[4],
            })
        return {'hoteis':hoteis} #SELECT * FROM hoteis
        
        
            
            
        
        #return {'hoteis':[hotel.json() for hotel in HotelModel.query.all()]}# SELECT * FROM hotel

class Hotel(Resource):
    
    attributes = reqparse.RequestParser()     
    attributes.add_argument('nome', type=str,required=True ,help="The field 'name' cannot be left blank")
    attributes.add_argument('estrelas')
    attributes.add_argument('diaria')
    attributes.add_argument('cidade',type=str,required=True ,help="The field 'cidade' cannot be left blank")
    
    def get(self,hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        
        if hotel:
            return hotel.json()
        return {'mensage': 'Hotel {} not found'.format(hotel_id)}, 404 # Not Found
    
    @jwt_required()
    def put(self,hotel_id):
        data= Hotel.attributes.parse_args() # recupera os datainseridos pelo cliente
        hotel_found = HotelModel.find_hotel(hotel_id) # procura pelo hotel
        
        if hotel_found: # se encontrar
            try:
                hotel_found.update_hotel(**data) #atualiza apenas os dados, id continua o mesmo
                hotel_found.save_hotel()
            except:
                return {'mensage':'An internal error occurred while updating'}, 500
            return {"mensage": 'Successful updating lista'},200
        
        hotel= HotelModel(hotel_id,**data)
        try:
            hotel.save_hotel()
        except:
            return {"mensage":"An internal error occurred while saving"}, 500 #Internnal server error
        return hotel.json(),201 # created criado
        
            
    @jwt_required()           
    def delete(self,hotel_id):
        # esta é uma forma mais simples criada pelo professor
        """
        global hoteis
        
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        eturn {"mensage": 'Hotel deleted successfully'}, 200 # ok
        """
        
        # forma criada por mim
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'mensage':'An error occurred while deleting'}, 500 # Internal Server error   
            return {"mensage": 'Hotel deleted successfully'},200 # ok
        
        return {"mensage": 'Hotel id {} Not Found'.format(hotel_id)}, 404 # Not Found
 
    @jwt_required()
    def post(self,hotel_id):
        
        if HotelModel.find_hotel(hotel_id):
            return {"mensage":"Hotel id {} already exists".format(hotel_id)}, 400 #Bad request
        
        data= Hotel.attributes.parse_args()
        hotel= HotelModel(hotel_id, **data)
        try:
            hotel.save_hotel() # 200 OK
        except:
            return {'mensage':'An internal error occurred to save the hotel'}, 500 #Internal Server Error
        return hotel.json() # Ok
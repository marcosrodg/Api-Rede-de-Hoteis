from sql_alchemy import banco
import hashlib

class UserModel(banco.Model):
    __tablename__ = 'users'
    
    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(50))
    password = banco.Column(banco.String(128))
    
    def __init__(self,login,password):
        self.login = login
        self.password = password
    
    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login
        }

    def get_hash(self,*args):

        word = ''
        for arg in args :
            tmp = str(arg)
            word += tmp
        
        m = hashlib.sha512()
        m.update(word.encode('utf-8'))
        return m.hexdigest()
    
    @classmethod
    def find_user(cls,user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None
    
    @classmethod
    def find_by_login(cls,login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user 
        return None
    
    def save_user(self):
        banco.session.add(self)
        banco.session.commit()
    
    def user_delete(self):
        banco.session.delete(self)
        banco.session.commit()
    
    
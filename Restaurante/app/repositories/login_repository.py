from app import db
from app.models import Login
from app.models import User  
class LoginRepository:
    @staticmethod
    def create_login(id_usuario, username, password_hash):
        user = User.query.get(id_usuario)
        if not user:
            raise ValueError("El ID de usuario no existe en la tabla User")
        
        new_login = Login(id_usuario=id_usuario, username=username, password_hash=password_hash)
        db.session.add(new_login)
        db.session.commit()
        return new_login

    @staticmethod
    def get_login_by_id(login_id):
        return Login.query.get(login_id)

    @staticmethod
    def get_login_by_username(username):
        return Login.query.filter_by(username=username).first()

    @staticmethod
    def update_login(login_id, id_usuario=None, username=None, password_hash=None):
        login = Login.query.get(login_id)
        if login:
            if id_usuario is not None:
                user = User.query.get(id_usuario)
                if not user:
                    raise ValueError("El ID de usuario no existe")
                login.id_usuario = id_usuario

            if username is not None:
                login.username = username
            if password_hash is not None:
                login.password_hash = password_hash

            db.session.commit()
        return login

    @staticmethod
    def delete_login(login_id):
        login = Login.query.get(login_id)
        if login:
            db.session.delete(login)
            db.session.commit()
        return login

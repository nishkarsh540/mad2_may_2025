from flask import Flask,jsonify,make_response
from flask_restful import Api,Resource,reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token,get_jwt_identity,unset_jwt_cookies
from flask_cors import CORS
from model import db,User,Product,Category
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'grocery'

db.init_app(app)
CORS(app,origins='*')

jwt= JWTManager(app)
api = Api(app)


class SignupResource(Resource):
    def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('username',type=str,required=True)
            parser.add_argument('email', type=str, required=True)
            parser.add_argument('password', type=str, required=True)
            parser.add_argument('role', type=str, default='user')

            args= parser.parse_args()

            if User.query.filter_by(username=args['username']).first():
                 return make_response(jsonify({'message': 'Username already exists'}), 400)
            hashed_password = generate_password_hash(args['password']) 
            new_user = User(username=args['username'], email=args['email'], password=hashed_password, role=args['role'])

            db.session.add(new_user)
            db.session.commit() 

            return {"message": "User created successfully"}, 201
    
class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)

        args = parser.parse_args()

        user = User.query.filter_by(username=args['username']).first()
        if not user or not check_password_hash(user.password, args['password']):
            return make_response(jsonify({'message': 'Invalid credentials'}), 401)

        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        user_info = {
            'username': user.username,
            'email':user.email,
            'role': user.role
        }
        return {'access_token': access_token, 'user': user_info}, 200


class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        response = make_response(jsonify({'message': 'Logged out successfully'}), 200)
        unset_jwt_cookies(response)
        return response

class UserInfo(Resource):
        @jwt_required()
        def get(self):

            current_user = get_jwt_identity()
            print(current_user['role'])
            users = User.query.all()
            user_info = [{
                'id': user.id,
                'username':user.username,
                'email': user.email
            } for user in users]

            return user_info


class CategoryResource(Resource):
    @jwt_required()
    def get(self):
        role = get_jwt_identity()['role']
        if role != 'admin':
            return make_response(jsonify({'message': 'Unauthorized access'}), 403)
        categories  = Category.query.all()
        category_list = [{'id': category.id, 'name': category.name} for category in categories]

        return jsonify(category_list)
    
    @jwt_required()
    def post(self):
            role = get_jwt_identity()['role']
            if role != 'admin':
                return make_response(jsonify({'message': 'Unauthorized access'}), 403)
         
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str,required=True)
            args = parser.parse_args()

            if Category.query.filter_by(name=args['name']).first():
               return make_response(jsonify({'message': 'Category already exists'}), 400)

            new_category = Category(name=args['name'])

            db.session.add(new_category)
            db.session.commit()

            return make_response(jsonify({'message': 'Category created successfully'}), 201)

    @jwt_required()
    def put(self):
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=int, required=True)
            parser.add_argument('name', type=str, required=True)
            args = parser.parse_args()

            category = Category.query.get(args['id'])
            if not category:
                    return make_response(jsonify({'message': 'Category not found'}), 404)

            category.name = args['name']
            db.session.commit()
            return make_response(jsonify({'message': 'Category updated successfully'}), 200)
    
    @jwt_required()
    def delete(self):
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=int, required=True)
            args = parser.parse_args()

            category = Category.query.get(args['id'])
            if not category:
                return make_response(jsonify({'message': 'Category not found'}), 404)

            db.session.delete(category)
            db.session.commit()
            return make_response(jsonify({'message': 'Category deleted successfully'}), 200)

api.add_resource(CategoryResource, '/categories')
api.add_resource(SignupResource, '/signup')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(UserInfo, '/user_info')
# 400 -- error, 200 -- success, 201 -- created, 401 -- unauthorized, 403 -- forbidden, 404 -- not found

if __name__ == '__main__':
    app.run(debug=True)
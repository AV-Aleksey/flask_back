from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

# Создание приложения и обозначение точки входа
app = Flask(__name__)
api = Api(app)

# Создание и подключение базы данных sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# Модель видео для SQL
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"


# Query для запроса put video
video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="Name of the video", required=True)
video_put_args.add_argument(
    "views", type=int, help="views of the video", required=True)
video_put_args.add_argument(
    "likes", type=int, help="likes of the video", required=True)

# Query для запроса update video
video_update_args = reqparse.RequestParser()
video_update_args.add_argument(
    "name", type=str, help="Name of the video")
video_update_args.add_argument(
    "views", type=int, help="views of the video")
video_update_args.add_argument(
    "likes", type=int, help="likes of the video")

# Типизация для запроса (используется с декоратором @marshal_with в классе запросов)
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

# Создание базы и моделей
db.create_all()


# Класс запросов
class Video(Resource):
    @marshal_with(resource_fields)
    def get(sefl, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="not found")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id taken")
        video = VideoModel(
            id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()

        if not result:
            abort(404, message="Video not found")
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()

        return {"status": "done"}

    def delete(self, video_id):
        del videos[video_id]
        return {"status": 'ok', "code": 204}


# Пишем url ручки и добавляем параметры
api.add_resource(Video, "/api/video/<int:video_id>")

# Запуск приложения
if __name__ == "__main__":
    app.run(debug=True)

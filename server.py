from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="Name of the video", required=True)
video_put_args.add_argument(
    "views", type=str, help="views of the video", required=True)
video_put_args.add_argument(
    "likes", type=str, help="likes of the video", required=True)

videos = {
    "1": [1, 2, 3]
}


class Video(Resource):
    def get(sefl, video_id):
        return videos[video_id]

    def put(self, video_id):
        args = video_put_args.parse_args()
        return {"data": "Posted"}


api.add_resource(Video, "/api/video/<string:video_id>")

if __name__ == "__main__":
    app.run(debug=True)

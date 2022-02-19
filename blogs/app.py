from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:bigjoe11@51.89.220.72:5432/postgres'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class BlogModel(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Blog {self.name}>"

class Blog(Resource):
    def get(self, id):
        blog = BlogModel.query.get_or_404(id)
        result = { "name": blog.name, "description": blog.description}

        return {"blog": result}

    def post(self, id):
        if request.json:
            data = request.get_json()
            new_blog = BlogModel(id=id, name=data['name'], description=data['description'])
            db.session.add(new_blog)
            db.session.commit()
            return {"message": f"blog {new_blog.name} has been created successfully"}
        else:
            return {"eror": "The request payload is not in JSON format"}

    def delete(self, id):
        blog = BlogModel.query.get_or_404(id)
        db.session.delete(blog)
        db.session.commit()
        return {"message": "Blog deleted"}

    def put(self, id):
        blog = BlogModel.query.get_or_404(id)
        data = request.get_json()
        blog.name = data['name']
        blog.model = data['description']
        db.session.add(blog)
        db.session.commit()
        return {"message": f"blog {blog.name} successfully updated"}


class Blogs(Resource):
    def get(self):
        blogs = BlogModel.query.all()
        results = [
            {
                "name": blog.name,
                "description": blog.description,
            } for blog in blogs]

        return {"count": len(results), "blogs": results}

class hello(Resource):
    def get(self):
        return "<h1>Hello World</h1>"

api.add_resource(hello, "/hello")
api.add_resource(Blogs, "/blogs")
api.add_resource(Blog, "/blog/<id>")  # http://localhost/blog/name

if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")
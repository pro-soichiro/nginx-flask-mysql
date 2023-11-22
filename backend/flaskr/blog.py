from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flaskr.models.blog import Blog
bp = Blueprint('blog', __name__, url_prefix='/blogs')

@bp.route('/', methods=['GET'])
def index():
    blogs = Blog.all()
    return render_template('/blog/index.html', blogs=blogs)

@bp.route('/new')
def new():
    return render_template('/blog/new.html')

@bp.route('/', methods=['POST'])
def create():
    title = request.form['title']
    body = request.form['body']
    user_id = request.form['user_id']
    blog = Blog(title=title, body=body, user_id=user_id)
    blog.save()
    return redirect(url_for('blog.show', id=blog.id))

@bp.route('/<int:id>', methods=['GET'])
def show(id):
    blog = Blog.find(id)
    if blog is None:
        return render_template('not_found.html'), 404
    return render_template('/blog/show.html', blog=blog)

@bp.route('/<int:id>/edit')
def edit(id):
    blog = Blog.find(id)
    if blog is None:
        return render_template('not_found.html'), 404
    return render_template('/blog/edit.html', blog=blog)

@bp.route('/<int:id>', methods=['PATCH'])
def update(id):
    blog = Blog.find(id)
    title = request.json['title']
    body = request.json['body']
    blog.update(title, body)
    return jsonify({ 'status': 'success' })

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    blog = Blog.find(id)
    blog.delete()
    return jsonify({ 'status': 'success' })
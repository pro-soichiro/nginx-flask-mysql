from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flaskr.models.blog import Blog
from flask_login import login_required
bp = Blueprint('blog', __name__, url_prefix='/blogs')

@bp.route('/', methods=['GET'])
@login_required
def index():
    blogs = Blog.all()
    return render_template('/blog/index.html', blogs=blogs)

@bp.route('/new')
@login_required
def new():
    return render_template('/blog/new.html')

@bp.route('/', methods=['POST'])
@login_required
def create():
    title = request.form['title']
    body = request.form['body']
    user_id = request.form['user_id']
    blog = Blog(title=title, body=body, user_id=user_id)
    blog.save()
    return redirect(url_for('blog.show', id=blog.id))

@bp.route('/<int:id>', methods=['GET'])
@login_required
def show(id):
    blog = Blog.find(id)
    if blog is None:
        return render_template('not_found.html'), 404
    return render_template('/blog/show.html', blog=blog)

@bp.route('/<int:id>/edit')
@login_required
def edit(id):
    blog = Blog.find(id)
    if blog is None:
        return render_template('not_found.html'), 404
    return render_template('/blog/edit.html', blog=blog)

@bp.route('/<int:id>', methods=['PATCH'])
@login_required
def update(id):
    blog = Blog.find(id)
    title = request.json['title']
    body = request.json['body']
    blog.update(title, body)
    return jsonify({ 'status': 'success' })

@bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete(id):
    blog = Blog.find(id)
    blog.delete()
    return jsonify({ 'status': 'success' })
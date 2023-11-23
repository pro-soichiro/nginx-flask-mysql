from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flaskr.models.blog import Blog
from flaskr.models.forms import BlogForm
from flask_login import login_required, current_user
bp = Blueprint('blog', __name__, url_prefix='/blogs')

@bp.route('/', methods=['GET'])
@login_required
def index():
    blogs = Blog.all()
    return render_template('/blog/index.html', blogs=blogs)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = BlogForm(request.form)
    if request.method == 'POST' and form.validate():
        blog = Blog(title=form.title.data, body=form.body.data, user_id=current_user.id)
        blog.save()
        return redirect(url_for('blog.show', id=blog.id))
    return render_template('/blog/new.html', form=form)

@bp.route('/<int:id>', methods=['GET'])
@login_required
def show(id):
    blog = Blog.find(id)
    if blog is None:
        return render_template('not_found.html'), 404
    return render_template('/blog/show.html', blog=blog)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    blog = Blog.find(id)
    if blog is None:
        return render_template('not_found.html'), 404
    form = BlogForm(request.form, obj=blog)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        blog.update(title, body)
        return redirect(url_for('blog.show', id=blog.id))
    return render_template('/blog/edit.html', blog=blog, form=form)

@bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete(id):
    blog = Blog.find(id)
    if blog.user_id == current_user.id:
        blog.delete()
        return jsonify({ 'status': 'success' })
    return jsonify({ 'status': 'failure' })
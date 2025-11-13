from flask import render_template, redirect, url_for, flash, request
from app import db
from . import posts_bp
from .models import Post, CategoryEnum
from .forms import PostForm


@posts_bp.route('/')
def all_posts():
    stmt = db.select(Post).where(Post.is_active == True).order_by(
        Post.posted.desc()
    )
    posts = db.session.scalars(stmt).all()
    return render_template('all_posts.html', posts=posts)


@posts_bp.route('/<int:id>')
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template('detail_post.html', post=post)


@posts_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        from flask import session
        author = session.get('username', 'Anonymous')

        post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.enabled.data,
            posted=form.publish_date.data,
            category=CategoryEnum[form.category.data],
            author=author
        )

        db.session.add(post)
        db.session.commit()

        flash('Пост успішно створено!', 'success')
        return redirect(url_for('posts_bp.all_posts'))

    return render_template(
        'add_post.html',
        form=form,
        title='Створити пост'
    )


@posts_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)

    if request.method == 'GET':
        form.publish_date.data = post.posted
        form.enabled.data = post.is_active
        form.category.data = post.category.value

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.enabled.data
        post.posted = form.publish_date.data
        post.category = CategoryEnum[form.category.data]

        db.session.commit()

        flash('Пост успішно оновлено!', 'success')
        return redirect(url_for('posts_bp.detail_post', id=post.id))

    return render_template(
        'add_post.html',
        form=form,
        title='Редагувати пост'
    )


@posts_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = db.get_or_404(Post, id)

    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()

        flash('Пост успішно видалено!', 'success')
        return redirect(url_for('posts_bp.all_posts'))

    return render_template('delete_confirm.html', post=post)

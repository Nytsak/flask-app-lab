from flask import render_template, redirect, url_for, flash
from app import db
from . import posts_bp
from .models import Post
from .forms import PostForm


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
            category=form.category.data,
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

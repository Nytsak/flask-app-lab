import unittest
from app import create_app, db
from app.posts.models import Post, CategoryEnum
from datetime import datetime


class TestPostsBlueprint(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.test_post = Post(
            title='Test Post',
            content='Test content for the post',
            category=CategoryEnum.tech,
            author='TestUser',
            is_active=True
        )
        db.session.add(self.test_post)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_all_posts_page(self):
        """Test the /post route - list all posts."""
        response = self.client.get('/post/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Post', response.data)

    def test_detail_post_page(self):
        """Test the /post/<id> route - view specific post."""
        response = self.client.get(f'/post/{self.test_post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Post', response.data)
        self.assertIn(b'Test content for the post', response.data)

    def test_detail_post_404(self):
        """Test viewing non-existent post returns 404."""
        response = self.client.get('/post/9999')
        self.assertEqual(response.status_code, 404)

    def test_create_post_get(self):
        """Test GET request to /post/create shows form."""
        response = self.client.get('/post/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'form', response.data)

    def test_create_post_post(self):
        """Test POST request to /post/create creates a post."""
        with self.client:
            response_get = self.client.get('/post/create')

            post_data = {
                'title': 'New Post',
                'content': 'New content for testing',
                'enabled': True,
                'publish_date': datetime.utcnow().strftime('%Y-%m-%dT%H:%M'),
                'category': CategoryEnum.news.value
            }
            response = self.client.post(
                '/post/create',
                data=post_data,
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)

            post = db.session.execute(
                db.select(Post).where(Post.title == 'New Post')
            ).scalar_one_or_none()
            self.assertIsNotNone(post)
            self.assertEqual(post.content, 'New content for testing')

    def test_update_post_get(self):
        """Test GET request to /post/<id>/update shows form with data."""
        response = self.client.get(f'/post/{self.test_post.id}/update')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Post', response.data)

    def test_update_post_post(self):
        """Test POST request to /post/<id>/update modifies post."""
        with self.client:
            response_get = self.client.get(f'/post/{self.test_post.id}/update')

            update_data = {
                'title': 'Updated Post',
                'content': 'Updated content',
                'enabled': True,
                'publish_date': self.test_post.posted.strftime(
                    '%Y-%m-%dT%H:%M'
                ),
                'category': CategoryEnum.publication.value
            }
            response = self.client.post(
                f'/post/{self.test_post.id}/update',
                data=update_data,
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)

            db.session.refresh(self.test_post)
            self.assertEqual(self.test_post.title, 'Updated Post')
            self.assertEqual(self.test_post.content, 'Updated content')

    def test_delete_post_get(self):
        """Test GET request to /post/<id>/delete shows confirmation."""
        response = self.client.get(f'/post/{self.test_post.id}/delete')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Post', response.data)

    def test_delete_post_post(self):
        """Test POST request to /post/<id>/delete removes post."""
        post_id = self.test_post.id
        response = self.client.post(
            f'/post/{post_id}/delete',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

        post = db.session.get(Post, post_id)
        self.assertIsNone(post)

    def test_inactive_posts_not_shown(self):
        """Test that inactive posts are not shown in the list."""
        inactive_post = Post(
            title='Inactive Post',
            content='This should not be visible',
            category=CategoryEnum.other,
            author='TestUser',
            is_active=False
        )
        db.session.add(inactive_post)
        db.session.commit()

        response = self.client.get('/post/')
        self.assertNotIn(b'Inactive Post', response.data)

    def test_post_author_from_session(self):
        """Test that post author is taken from session."""
        with self.client:
            with self.client.session_transaction() as sess:
                sess['username'] = 'SessionUser'

            response_get = self.client.get('/post/create')

            post_data = {
                'title': 'Session Post',
                'content': 'Content by session user',
                'enabled': True,
                'publish_date': datetime.utcnow().strftime('%Y-%m-%dT%H:%M'),
                'category': CategoryEnum.tech.value
            }
            response = self.client.post(
                '/post/create',
                data=post_data,
                follow_redirects=True
            )

            post = db.session.execute(
                db.select(Post).where(Post.title == 'Session Post')
            ).scalar_one_or_none()
            self.assertIsNotNone(post)
            self.assertEqual(post.author, 'SessionUser')

    def test_post_anonymous_author(self):
        """Test that post author defaults to Anonymous when no session."""
        with self.client:
            response_get = self.client.get('/post/create')

            post_data = {
                'title': 'Anonymous Post',
                'content': 'Content by anonymous',
                'enabled': True,
                'publish_date': datetime.utcnow().strftime('%Y-%m-%dT%H:%M'),
                'category': CategoryEnum.other.value
            }
            response = self.client.post(
                '/post/create',
                data=post_data,
                follow_redirects=True
            )

            post = db.session.execute(
                db.select(Post).where(Post.title == 'Anonymous Post')
            ).scalar_one_or_none()
            self.assertIsNotNone(post)
            self.assertEqual(post.author, 'Anonymous')


if __name__ == '__main__':
    unittest.main()

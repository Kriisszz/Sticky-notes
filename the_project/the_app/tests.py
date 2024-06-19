from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Task, Post, Comment
from django.utils import timezone
from .forms import TaskForm, PostForm, CommentForm
from django.urls import reverse


class TaskModelTest(TestCase):
    """Testing models."""
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            date=timezone.now(),
            completed=False
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.user.username, 'testuser')

    def test_task_is_expired(self):
        self.assertFalse(self.task.is_expired())


class PostModelTest(TestCase):
    """Unit test for models(Post)"""
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author.username, 'testuser')


class CommentModelTest(TestCase):
    """Unit test for commenting"""
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test Comment'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'Test Comment')
        self.assertEqual(self.comment.author.username, 'testuser')
        self.assertEqual(self.comment.post.title, 'Test Post')


class TaskFormTest(TestCase):
    """Unit test for forms."""

    def test_valid_form(self):
        data = {'title': 'Test Task', 'description': 'Test Description',
                'date': '2024-06-12 12:00', 'completed': False}
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'title': '', 'description': 'Test Description',
                'date': '2024-06-12 12:00', 'completed': False}
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())


class PostFormTest(TestCase):
    """Unit test for posting forms."""
    def test_valid_form(self):
        data = {'title': 'Test Post', 'content': 'Test Content'}
        form = PostForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'title': '', 'content': 'Test Content'}
        form = PostForm(data=data)
        self.assertFalse(form.is_valid())


class CommentFormTest(TestCase):
    """Unit test for comment form."""
    def test_valid_form(self):
        data = {'content': 'Test Comment'}
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'content': ''}
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())


class TaskViewTest(TestCase):
    """Unit test for views."""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.client.login(username='testuser', password='12345')

    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'the_app/task_list.html')

    def test_task_add_view(self):
        response = self.client.post(reverse('task_add'),
                                    {'title': 'New Task',
                                     'description': 'New Description',
                                     'date': '2024-06-12 12:00',
                                     'completed': False})
        self.assertEqual(response.status_code, 302)


class PostViewTest(TestCase):
    """Unit test for viewing the post"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.client.login(username='testuser', password='12345')
        self.post = Post.objects.create(title='Test Post',
                                        content='Test Content',
                                        author=self.user)

    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'the_app/post_list.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'the_app/post_detail.html')

    def test_post_add_view(self):
        self.client.logout()
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_add'),
                                    {'title': 'New Post',
                                     'content': 'New Content'})
        self.assertEqual(response.status_code, 302)

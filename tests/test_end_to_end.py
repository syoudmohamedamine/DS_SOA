import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from boards.models import Board, Topic, Post
from django.test import Client

@pytest.mark.django_db
def test_end_to_end_forum(client):
    """
    Test complet de bout en bout pour une application Django de forum :
    - Inscription
    - Connexion
    - Création d'un tableau
    - Création d'un sujet
    - Réponse au sujet
    - Déconnexion
    """
    # Étape 1 : Inscription
    user = signup_user(client)
    # Étape 2 : Connexion
    login_user(client, user)
    # Étape 3 : Création d'un tableau
    board = create_board(client)
    # Étape 4 : Création d'un sujet
    topic = create_topic(client, board)
    # Étape 5 : Répondre au sujet
    reply_to_topic(client, board, topic)
    # Étape 6 : Déconnexion
    logout_user(client)


# Méthodes pour chaque étape du test

def signup_user(client):
    """Inscription d'un nouvel utilisateur"""
    print("\nÉtape 1 : Inscription")
    signup_url = reverse('signup')
    signup_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password1': 'securepassword123',
        'password2': 'securepassword123',
    }
    response = client.post(signup_url, signup_data)
    print(f"Code de réponse de l'inscription : {response.status_code}")
    assert response.status_code == 302
    print(f"Redirection vers : {response.url}")
    assert response.url == reverse('home')
    # Récupérer l'utilisateur créé
    user = User.objects.get(username='testuser')
    print(f"Utilisateur créé : {user.username}, email : {user.email}")
    assert user.email == 'testuser@example.com'
    assert user.check_password('securepassword123')
    return user


def login_user(client, user):
    """Connexion de l'utilisateur"""
    print("\nÉtape 2 : Connexion")
    login_url = reverse('login')
    login_data = {
        'username': user.username,
        'password': 'securepassword123',
    }
    response = client.post(login_url, login_data)
    print(f"Code de réponse de la connexion : {response.status_code}")
    assert response.status_code == 302
    print(f"Redirection vers : {response.url}")
    assert response.url == reverse('home')
    assert '_auth_user_id' in client.session
    print(f"L'utilisateur {user.username} est connecté.")


def create_board(client):
    """Création d'un tableau"""
    print("\nÉtape 3 : Création d'un tableau")
    create_board_url = reverse('add_board')
    board_data = {'name': 'Test Board', 'description': 'This is a test board.'}
    response = client.post(create_board_url, board_data)
    print(f"Code de réponse de la création du tableau : {response.status_code}")
    assert response.status_code == 302

    # Récupérer le tableau créé
    board = Board.objects.get(name='Test Board')
    print(f"Tableau créé : {board.name}, description : {board.description}")
    return board


def create_topic(client, board):
    """Création d'un sujet"""
    print("\nÉtape 4 : Création d'un sujet")
    create_topic_url = reverse('new_topic', kwargs={'board_id': board.id})
    topic_data = {'subject': 'Test Topic', 'message': 'This is a test topic message.'}
    response = client.post(create_topic_url, topic_data)
    print(f"Code de réponse de la création du sujet : {response.status_code}")
    assert response.status_code == 302
    print(f"Redirection vers : {response.url}")
    assert response.url == reverse('board_topics', kwargs={'board_id': board.id})

    # Récupérer le sujet créé
    topic = Topic.objects.get(subject='Test Topic')
    print(f"Sujet créé : {topic.subject}")

    # Vérifier le message du post
    post = Post.objects.get(topic=topic)
    print(f"Message du post : {post.message}")
    assert post.message == 'This is a test topic message.'
    return topic


def reply_to_topic(client, board, topic):
    """Répondre au sujet"""
    print("\nÉtape 5 : Répondre au sujet")
    reply_topic_url = reverse('reply_topic', kwargs={'board_id': board.id, 'topic_id': topic.id})
    reply_data = {'message': 'This is a test reply to the topic.'}
    response = client.post(reply_topic_url, reply_data)
    print(f"Code de réponse de la réponse : {response.status_code}")
    assert response.status_code == 302
    print(f"Redirection vers : {response.url}")
    assert response.url == reverse('topic_posts', kwargs={'board_id': board.id, 'topic_id': topic.id})

    # Vérifier la réponse
    reply_post = Post.objects.get(topic=topic, message='This is a test reply to the topic.')
    print(f"Réponse postée : {reply_post.message}")
    assert reply_post.message == 'This is a test reply to the topic.'


def logout_user(client):
    """Déconnexion de l'utilisateur"""
    print("\nÉtape 6 : Déconnexion")
    logout_url = reverse('logout')
    response = client.post(logout_url)
    print(f"Code de réponse de la déconnexion : {response.status_code}")
    assert response.status_code == 302
    print(f"Redirection vers : {response.url}")
    assert response.url == reverse('home')
    assert '_auth_user_id' not in client.session
    print("L'utilisateur est déconnecté.")

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Board

@pytest.mark.django_db
def test_board_list_view(client):
    # Créer un utilisateur et un board
    user = User.objects.create_user(username='testuser', password='password')
    board = Board.objects.create(name='Test Board', description='Description du test')

    # Se connecter
    client.login(username='testuser', password='password')

    # Accéder à la vue des boards
    url = reverse('home')  # Assurez-vous que 'home' est l'URL nommée pour BoardListView
    response = client.get(url)

    # Vérifier que la réponse est 200 OK
    assert response.status_code == 200

    # Vérifier que le board créé est dans le contexte
    assert board.name in response.content.decode()  # Vérifie si le nom du board est dans la page

from django.urls import reverse
from boards.models import Board, Topic
from test_plus import TestCase  # Import de TestCase de django-test-plus

class TestTopicDeletion(TestCase):
    """Test pour la suppression d'un topic."""

    def setUp(self):
        """Méthode pour configurer les objets de test avant chaque méthode."""
        # Créer un board
        self.board = Board.objects.create(name="Test Board", description="Test Board Description")

        # Créer les utilisateurs avec make_user
        self.user = self.make_user(username="testuser", password="testpassword")
        self.other_user = self.make_user(username="otheruser", password="otherpassword")

        # Créer un topic
        self.topic = Topic.objects.create(board=self.board, subject="Test Topic", created_by=self.user)

    def test_delete_topic_authorized(self):
        """Test la suppression d'un topic pour un utilisateur autorisé."""
        # Connecter l'utilisateur avec login
        self.login(username="testuser", password="testpassword")
        
        # Construire l'URL de suppression
        url = reverse("delete_topic", kwargs={"board_id": self.board.id, "topic_id": self.topic.id})

        # Effectuer la requête POST pour supprimer le topic
        response = self.post(url)

        # Vérifier que la suppression a été effectuée
        self.response_302(response)  # Vérifie qu'il s'agit d'une redirection HTTP 302
        self.assertRedirects(response, reverse("board_topics", kwargs={"board_id": self.board.id}))  # Vérification de la redirection
        self.assertEqual(Topic.objects.filter(id=self.topic.id).count(), 0)  # Le topic n'existe plus

    def test_delete_topic_unauthorized(self):
        """Test qu'un utilisateur non autorisé est redirigé et ne peut pas supprimer un topic."""
        # Connecter l'autre utilisateur
        self.login(username="otheruser", password="otherpassword")

        # Construire l'URL de suppression
        url = reverse("delete_topic", kwargs={"board_id": self.board.id, "topic_id": self.topic.id})

        # Effectuer la requête POST pour tenter de supprimer le topic
        response = self.post(url)

        # Vérifier que l'utilisateur non autorisé est redirigé vers la page "unauthorized_delete"
        self.response_302(response)  # Vérifie qu'il s'agit d'une redirection HTTP 302
        self.assertRedirects(response, reverse("unauthorized_delete"))  # Vérifie la redirection vers 'unauthorized_delete'

        # Vérifier que le topic n'a pas été supprimé
        self.assertTrue(Topic.objects.filter(id=self.topic.id).exists())  # Le topic existe toujours

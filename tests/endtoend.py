import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL de l'application
signup_url = "http://127.0.0.1:8000/signup/"
login_url = "http://127.0.0.1:8000/login/"
home_url = "http://127.0.0.1:8000/"
create_board_url = "http://127.0.0.1:8000/add_board/"  # URL pour créer un tableau

# Fixture pour le WebDriver
@pytest.fixture
def driver():
    # Initialisation du WebDriver
    driver = webdriver.Chrome()
    yield driver  # Le test utilise ce driver
    driver.quit()  # Fermer le navigateur après le test

# Fonction pour se connecter
def login(driver, username, password):
    driver.get(login_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
    # Remplir les champs de connexion
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    # Soumettre le formulaire de connexion
    driver.find_element(By.XPATH, "//button[@type='submit']").click()



def create_board(driver, board_name):
    driver.get(create_board_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "name")))
    assert "Add a new Board" in driver.page_source
    print("Page de création de tableau chargée")

    # Saisir le nom du tableau
    driver.find_element(By.NAME, "name").send_keys(board_name)
    driver.find_element(By.NAME, "description").send_keys("This is a test board description.")
    # Attendre que le bouton de soumission soit visible et cliquable
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "submit-board-button"))
    )

    # Cliquer sur le bouton
    submit_button.click()

# 1. Test d'inscription, Connexion, Création de tableau et Déconnexion
@pytest.mark.django_db
def test_complete_scenario(driver):
    # Inscription
    driver.get(signup_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
    assert "Sign up" in driver.page_source
    print("Page d'inscription chargée")

    driver.find_element(By.NAME, "username").send_keys("tpipnr")
    driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
    driver.find_element(By.NAME, "password1").send_keys("TestPassword123!")
    driver.find_element(By.NAME, "password2").send_keys("TestPassword123!")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Attendre la redirection vers la page d'accueil après inscription
    WebDriverWait(driver, 10).until(EC.url_to_be(home_url))
    assert driver.current_url == home_url
    print("Inscription réussie, redirection vers la page d'accueil.")

    # Connexion
    login(driver, "tpipnr", "TestPassword123!")
    WebDriverWait(driver, 10).until(EC.url_to_be(home_url))
    assert driver.current_url == home_url
    print("Connexion réussie, redirection vers la page d'accueil.")

    

    

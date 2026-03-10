import pytest
from flask import url_for
from app import create_app, db
from app.models.usuario import Usuario


@pytest.fixture
def app():
    app = create_app()
    # Override to use in-memory SQLite for tests
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "LOGIN_DISABLED": False,
        "SERVER_NAME": "localhost",
        "SECRET_KEY": "test",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin_user(app):
    with app.app_context():
        admin = Usuario(nombre="Admin", email="admin@example.com", rol="admin")
        admin.set_password("Admin123*")
        db.session.add(admin)
        db.session.commit()
        return admin


@pytest.fixture
def normal_user(app):
    with app.app_context():
        user = Usuario(nombre="User", email="user@example.com", rol="usuario")
        user.set_password("User123*")
        db.session.add(user)
        db.session.commit()
        return user


def login(client, email, password):
    return client.post("/login", data={"email": email, "password": password}, follow_redirects=True)


class TestUsuariosRoutes:
    # 1. Should require authentication for listing users
    def test_list_requires_login(self, client):
        resp = client.get("/usuarios/")
        assert resp.status_code in (301, 302)
        assert "/login" in resp.headers.get("Location", "")

    # 2. Should forbid non-admin access (redirect to index)
    def test_list_forbidden_for_non_admin(self, client, normal_user):
        login(client, normal_user.email, "User123*")
        resp = client.get("/usuarios/", follow_redirects=True)
        assert resp.status_code == 200
        assert b"No tienes permisos" in resp.data

    # 3. Should allow admin to list users
    def test_list_allows_admin(self, client, admin_user):
        login(client, admin_user.email, "Admin123*")
        resp = client.get("/usuarios/")
        assert resp.status_code == 200
        assert b"usuarios" in resp.data.lower()

    # 4. Should create a new user with valid data and unique email
    def test_create_user_success(self, client, admin_user, app):
        login(client, admin_user.email, "Admin123*")
        form = {"nombre": "Nuevo", "email": "nuevo@example.com", "password": "Passw0rd*", "rol": "usuario"}
        resp = client.post("/usuarios/crear", data=form, follow_redirects=True)
        assert resp.status_code == 200
        # Flash message present
        assert b"Usuario creado correctamente" in resp.data
        with app.app_context():
            assert Usuario.query.filter_by(email="nuevo@example.com").first() is not None

    # 5. Should reject user creation when required fields missing
    def test_create_user_missing_fields(self, client, admin_user):
        login(client, admin_user.email, "Admin123*")
        form = {"nombre": "", "email": "", "password": "", "rol": "usuario"}
        resp = client.post("/usuarios/crear", data=form, follow_redirects=True)
        assert resp.status_code == 200
        assert b"Todos los campos son obligatorios" in resp.data

    # 6. Should reject user creation when email already exists
    def test_create_user_duplicate_email(self, client, admin_user, app):
        login(client, admin_user.email, "Admin123*")
        with app.app_context():
            u = Usuario(nombre="Existente", email="dup@example.com", rol="usuario")
            u.set_password("Passw0rd*")
            db.session.add(u)
            db.session.commit()
        form = {"nombre": "Otro", "email": "dup@example.com", "password": "Passw0rd*", "rol": "usuario"}
        resp = client.post("/usuarios/crear", data=form, follow_redirects=True)
        assert resp.status_code == 200
        assert b"El correo ya est\xc3\xa1 registrado" in resp.data or b"El correo ya est\xe1 registrado" in resp.data

    # 7. Should edit an existing user
    def test_edit_user_success(self, client, admin_user, app):
        login(client, admin_user.email, "Admin123*")
        with app.app_context():
            u = Usuario(nombre="A", email="a@example.com", rol="usuario")
            u.set_password("Passw0rd*")
            db.session.add(u)
            db.session.commit()
            uid = u.id
        resp = client.post(f"/usuarios/editar/{uid}", data={"nombre": "B", "email": "b@example.com", "rol": "admin"}, follow_redirects=True)
        assert resp.status_code == 200
        assert b"Usuario actualizado correctamente" in resp.data
        with app.app_context():
            u2 = Usuario.query.get(uid)
            assert u2.nombre == "B"
            assert u2.email == "b@example.com"
            assert u2.rol == "admin"

    # 8. Should return 404 when editing non-existent user
    def test_edit_user_not_found(self, client, admin_user):
        login(client, admin_user.email, "Admin123*")
        resp = client.get("/usuarios/editar/999999")
        assert resp.status_code == 404

    # 9. Should prevent admin from deleting own account
    def test_delete_prevent_self(self, client, admin_user):
        login(client, admin_user.email, "Admin123*")
        resp = client.get(f"/usuarios/eliminar/{admin_user.id}", follow_redirects=True)
        assert resp.status_code == 200
        assert b"No puedes eliminar tu propia cuenta" in resp.data

    # 10. Should delete a different user
    def test_delete_other_user(self, client, admin_user, app):
        login(client, admin_user.email, "Admin123*")
        with app.app_context():
            u = Usuario(nombre="Del", email="del@example.com", rol="usuario")
            u.set_password("Passw0rd*")
            db.session.add(u)
            db.session.commit()
            uid = u.id
        resp = client.get(f"/usuarios/eliminar/{uid}", follow_redirects=True)
        assert resp.status_code == 200
        assert b"Usuario eliminado correctamente" in resp.data
        with app.app_context():
            assert Usuario.query.get(uid) is None

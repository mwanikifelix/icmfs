import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_admin_can_list_users():
    admin = User.objects.create_superuser(
        username="admin",
        email="admin@test.com",
        password="admin123"
    )

    client = APIClient()
    client.force_authenticate(user=admin)

    url = reverse("admin-users")
    response = client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, list)

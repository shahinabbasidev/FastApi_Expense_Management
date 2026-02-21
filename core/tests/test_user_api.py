

def test_login_response_404(anon_client):
    payload = {
        "username" : "shahin_ab",
        "password" : "shahin123456"
    }
    response = anon_client.post("/users/login",json=payload)
    assert response.status_code == 404


def test_register(anon_client):
    payload = {
        "first_name" : "shahin",
        "last_name" : "abbasi",
        "username" : "shahin_ab",
        "password" : "shahin123456"
    }
    response = anon_client.post("/users/register",json=payload)
    assert response.status_code == 201
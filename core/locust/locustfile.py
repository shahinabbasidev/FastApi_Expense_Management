from locust import HttpUser, task, between
import random
import string


def random_string(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))


class QuickstartUser(HttpUser):
    # pace users so each completes a task roughly every 1-2 seconds
    wait_time = between(1, 2)

    def on_start(self):
        """Called when a Locust user starts running. We'll ensure there's a
        valid account and perform a login to obtain cookies for auth.
        """
        # try logging in with a known test user; if it doesn't exist, register it
        username = "testuser"
        password = "testpass"
        resp = self.client.post("/users/login", json={"username": username, "password": password})
        if resp.status_code == 404:
            # register the account and try again
            self.client.post(
                "/users/register",
                json={
                    "first_name": "load",
                    "last_name": "tester",
                    "username": username,
                    "password": password,
                },
            )
            resp = self.client.post("/users/login", json={"username": username, "password": password})
        # we'll assume login now succeeded; cookies are stored on the client
        if resp.status_code != 200:
            # if login still failed, print a warning for debug
            print(f"warning: login returned {resp.status_code} - {resp.text}")

    @task(2)
    def list_expenses(self):
        """Fetch the list of expenses (authenticated)."""
        self.client.get("/expenses")

    @task(1)
    def add_expense(self):
        """Create a new expense with random data."""
        payload = {
            "expense_name": random_string(10),
            "mount": round(random.random() * 1000, 2),
        }
        self.client.post("/expenses", json=payload)

    @task(1)
    def retrieve_random_expense(self):
        # choose an id between 1 and 20; some may not exist
        eid = random.randint(1, 20)
        self.client.get(f"/expense/{eid}")

    @task(1)
    def update_random_expense(self):
        eid = random.randint(1, 20)
        payload = {"expense_name": random_string(12), "mount": round(random.random() * 500, 2)}
        self.client.put(f"/expense_update/{eid}", json=payload)

    @task(1)
    def delete_random_expense(self):
        # occasionally delete an expense
        eid = random.randint(1, 20)
        self.client.delete(f"/expense/{eid}")

    @task(1)
    def refresh_token(self):
        # attempt token refresh; if cookies are missing it will 404 which is fine
        self.client.post("/users/refresh-token")

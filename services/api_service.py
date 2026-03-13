from playwright.sync_api import APIRequestContext

class ApiService:
    def __init__(self, api_context: APIRequestContext):
        self.request = api_context
        self.token = None

    def set_token(self, token: str):
        self.token = token

    def _get_headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    # --- User Endpoints ---
    def register_user(self, payload: dict):
        return self.request.post("/users", data=payload)

    def login(self, email, password):
        payload = {"email": email, "password": password}
        return self.request.post("/users/login", data=payload)

    def delete_me(self):
        return self.request.delete("/users/me", headers=self._get_headers())

    # --- Contact Endpoints ---
    def add_contact(self, payload: dict):
        return self.request.post("/contacts", data=payload, headers=self._get_headers())

    def get_contact(self, contact_id: str):
        return self.request.get(f"/contacts/{contact_id}", headers=self._get_headers())

    def update_contact_put(self, contact_id: str, payload: dict):
        return self.request.put(f"/contacts/{contact_id}", data=payload, headers=self._get_headers())

    def update_contact_patch(self, contact_id: str, payload: dict):
        return self.request.patch(f"/contacts/{contact_id}", data=payload, headers=self._get_headers())

    def delete_contact(self, contact_id: str):
        return self.request.delete(f"/contacts/{contact_id}", headers=self._get_headers())
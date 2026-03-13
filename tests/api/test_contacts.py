import pytest
import time
from playwright.sync_api import APIRequestContext

class TestContactsAPI:
    token: str = None
    contact_id: str = None
    user_payload: dict = None

    @pytest.fixture(autouse=True, scope="class")
    def setup_and_teardown_user(self, api_context):
        from services.api_service import ApiService
        service = ApiService(api_context)
        timestamp = int(time.time() * 1000)
        payload = {
            'firstName': 'Api', 'lastName': 'User',
            'email': f'apiuser_{timestamp}@test.com', 'password': 'apiPassword123!'
        }
        res = service.register_user(payload)
        assert res.ok
        TestContactsAPI.token = res.json()['token']
        TestContactsAPI.user_payload = payload
        
        yield
        # Teardown: Delete user
        service.set_token(TestContactsAPI.token)
        service.delete_me()

    def test_add_contact(self, api_service: ApiService):
        api_service.set_token(self.token)
        payload = {'firstName': 'John', 'lastName': 'Doe', 'email': 'jdoe@test.com'}
        
        res = api_service.add_contact(payload)
        assert res.status == 201
        TestContactsAPI.contact_id = res.json()['_id']

    def test_get_contact(self, api_service: ApiService):
        assert self.contact_id is not None, "contact_id was not passed from previous test"
        
        api_service.set_token(self.token)
        res = api_service.get_contact(self.contact_id)

        assert res.status == 200
        assert res.json()['_id'] == self.contact_id

    def test_update_contact_put(self, api_service: ApiService):
        assert self.contact_id is not None, "Cannot update: Contact ID is missing."

        updated_contact = {
            'firstName': 'Jane',
            'lastName': 'Smith',
            'birthdate': '2008-02-02',
            'email': 'jsmith@test.com',
            'phone': '8005551234',
            'street1': 'St. Second',
            'street2': '2D',
            'city': 'Othercity',
            'stateProvince': 'ProvinceNew',
            'postalCode': '54321',
            'country': 'Spain'
        }

        api_service.set_token(self.token)
        res = api_service.update_contact_put(self.contact_id, updated_contact)

        assert res.status == 200
        body = res.json()
        assert body['firstName'] == 'Jane'
        assert body['email'] == 'jsmith@test.com'

    def test_update_contact_patch(self, api_service: ApiService):
        assert self.contact_id is not None, "Cannot patch: Contact ID is missing."

        patch_data = {'firstName': 'Anna'}

        api_service.set_token(self.token)
        res = api_service.update_contact_patch(self.contact_id, patch_data)

        assert res.status == 200
        body = res.json()
        assert body['firstName'] == 'Anna'
        assert body['lastName'] == 'Smith'

    # --- Negative Tests ---

    def test_add_contact_invalid_data(self, api_service: ApiService):
        api_service.set_token(self.token)
        invalid_payload = {'firstName': 'MissingLastName'}
        res = api_service.add_contact(invalid_payload)
        assert res.status == 400
        assert "Contact validation failed" in res.text()

    def test_get_contact_unauthorized(self, api_service: ApiService):
        api_service.set_token("invalid_token_123")
        res = api_service.get_contact(self.contact_id)
        assert res.status == 401
        assert "Please authenticate" in res.text()

    def test_get_non_existent_contact(self, api_service: ApiService):
        api_service.set_token(self.token)
        fake_id = "60b8d5415756d10015555555" # Valid format, but non-existent ID
        res = api_service.get_contact(fake_id)
        assert res.status == 404

    # --- Final Step: Delete ---

    def test_delete_contact(self, api_service: ApiService):
        assert self.contact_id is not None, "Cannot delete: Contact ID is missing."

        api_service.set_token(self.token)
        
        delete_res = api_service.delete_contact(self.contact_id)
        assert delete_res.status == 200, f"Delete failed with status: {delete_res.status}"
      
        verify_res = api_service.get_contact(self.contact_id)
        assert verify_res.status == 404, f"Expected 404 for deleted contact, but got {verify_res.status}"

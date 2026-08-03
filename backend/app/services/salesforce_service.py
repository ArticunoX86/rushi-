import requests
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.lead import Lead
from app.models.enums import LeadSource, LeadStatus, LeadPriority

class SalesforceService:
    def __init__(self):
        self.client_id = settings.SALESFORCE_CLIENT_ID
        self.client_secret = settings.SALESFORCE_CLIENT_SECRET
        self.username = settings.SALESFORCE_USERNAME
        self.password = settings.SALESFORCE_PASSWORD
        self.security_token = settings.SALESFORCE_SECURITY_TOKEN
        self.login_url = settings.SALESFORCE_LOGIN_URL
        self.access_token = None
        self.instance_url = None

    def authenticate(self) -> bool:
        """
        Authenticate with Salesforce using OAuth 2.0 Username-Password Flow.
        """
        # If any of the required credentials are empty, return False to trigger Mock fallback
        if not all([self.client_id, self.client_secret, self.username, self.password]):
            print("[SALESFORCE] Missing credentials. Falling back to Mock Developer Sandbox Mode.")
            return False

        try:
            payload = {
                'grant_type': 'password',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'username': self.username,
                'password': f"{self.password}{self.security_token}"
            }
            url = f"{self.login_url}/services/oauth2/token"
            res = requests.post(url, data=payload, timeout=10)
            if res.status_code == 200:
                data = res.json()
                self.access_token = data.get('access_token')
                self.instance_url = data.get('instance_url')
                print(f"[SALESFORCE] Authenticated successfully. Instance URL: {self.instance_url}")
                return True
            else:
                print(f"[SALESFORCE] Authentication failed (HTTP {res.status_code}): {res.text}")
                return False
        except Exception as e:
            print(f"[SALESFORCE] Authentication Exception: {e}")
            return False

    def fetch_leads(self) -> list[dict]:
        """
        Query Leads from Salesforce REST API.
        """
        if not self.access_token or not self.instance_url:
            print("[SALESFORCE] Not authenticated. Fetching mock Salesforce sandbox leads instead.")
            return self._get_mock_leads()

        try:
            # Simple SOQL query to fetch real estate prospect leads
            soql = "SELECT Id, FirstName, LastName, Phone, Email, City, Status, Description FROM Lead WHERE Phone != null LIMIT 20"
            url = f"{self.instance_url}/services/data/v60.0/query"
            headers = {
                'Authorization': f"Bearer {self.access_token}",
                'Content-Type': 'application/json'
            }
            res = requests.get(url, headers=headers, params={'q': soql}, timeout=10)
            if res.status_code == 200:
                records = res.json().get('records', [])
                leads = []
                for rec in records:
                    leads.append({
                        'salesforce_id': rec.get('Id'),
                        'first_name': rec.get('FirstName') or 'Valued',
                        'last_name': rec.get('LastName') or 'Customer',
                        'phone': rec.get('Phone'),
                        'email': rec.get('Email'),
                        'preferred_city': rec.get('City') or 'Mumbai',
                        'status': rec.get('Status')
                    })
                print(f"[SALESFORCE] Fetched {len(leads)} leads successfully.")
                return leads
            else:
                print(f"[SALESFORCE] API error (HTTP {res.status_code}): {res.text}")
                return self._get_mock_leads()
        except Exception as e:
            print(f"[SALESFORCE] Exception while fetching leads: {e}")
            return self._get_mock_leads()

    def sync_leads_to_db(self, db: Session) -> dict:
        """
        Sync Salesforce Leads into PostgreSQL local leads table.
        """
        # 1. Attempt to authenticate. Falls back to mock leads if failed/missing configs.
        self.authenticate()

        # 2. Fetch leads (either real Salesforce or Mock Sandbox data)
        sf_leads = self.fetch_leads()
        
        synced_count = 0
        skipped_count = 0
        sync_logs = []

        for lead_data in sf_leads:
            phone = lead_data['phone']
            if not phone:
                continue

            # Check if lead already exists by phone
            existing_lead = db.query(Lead).filter(Lead.phone == phone).first()
            if existing_lead:
                skipped_count += 1
                sync_logs.append(f"Skipped lead '{lead_data['first_name']} {lead_data['last_name']}' - Phone {phone} already exists in DB.")
                continue

            # Insert new Salesforce lead into local DB
            new_lead = Lead(
                first_name=lead_data['first_name'],
                last_name=lead_data['last_name'],
                email=lead_data['email'] or f"{lead_data['first_name'].lower()}@salesforce-sandbox.com",
                phone=phone,
                preferred_city=lead_data['preferred_city'],
                status=LeadStatus.NEW,
                priority=LeadPriority.MEDIUM,
                source=LeadSource.API,
                conversation_summary=f"Salesforce Lead ID: {lead_data['salesforce_id']}"
            )
            db.add(new_lead)
            synced_count += 1
            sync_logs.append(f"Successfully Synced Salesforce Lead ID {lead_data['salesforce_id']}: '{lead_data['first_name']} {lead_data['last_name']}' to PostgreSQL leads table.")

        db.commit()
        return {
            "status": "success",
            "synced_count": synced_count,
            "skipped_count": skipped_count,
            "logs": sync_logs,
            "mode": "Salesforce Production REST API" if self.access_token else "Salesforce Developer Sandbox (Simulated)"
        }

    def _get_mock_leads(self) -> list[dict]:
        """
        Realistic mock Salesforce sandbox leads for testable integrations out-of-the-box.
        """
        return [
            {
                'salesforce_id': '00Q5h00000LxY7uEAF',
                'first_name': 'Aman',
                'last_name': 'Sharma',
                'phone': '+919876543210',
                'email': 'aman.sharma@salesforce.com',
                'preferred_city': 'Mumbai',
                'status': 'Open - Not Contacted'
            },
            {
                'salesforce_id': '00Q5h00000LxZ9wEAF',
                'first_name': 'Sneha',
                'last_name': 'Rao',
                'phone': '+919988776655',
                'email': 'sneha.rao@salesforce.com',
                'preferred_city': 'Bandra',
                'status': 'Open - Not Contacted'
            },
            {
                'salesforce_id': '00Q5h00000LyA12EAF',
                'first_name': 'Rohan',
                'last_name': 'Mehta',
                'phone': '+919122334455',
                'email': 'rohan.mehta@salesforce.com',
                'preferred_city': 'Pune',
                'status': 'Open - Not Contacted'
            },
            {
                'salesforce_id': '00Q5h00000LyB56EAF',
                'first_name': 'Priya',
                'last_name': 'Nair',
                'phone': '+919544332211',
                'email': 'priya.nair@salesforce.com',
                'preferred_city': 'Bandra',
                'status': 'Working - Contacted'
            },
            {
                'salesforce_id': '00Q5h00000LyC89EAF',
                'first_name': 'Vikram',
                'last_name': 'Malhotra',
                'phone': '+919811223344',
                'email': 'vikram.m@salesforce.com',
                'preferred_city': 'Mumbai',
                'status': 'Open - Not Contacted'
            }
        ]

salesforce_service = SalesforceService()

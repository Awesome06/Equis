import plaid
from plaid.api import plaid_api
from app.config import settings

# Configuration for Plaid API client
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox if settings.PLAID_ENV == "sandbox" 
         else plaid.Environment.Development if settings.PLAID_ENV == "development" 
         else plaid.Environment.Production,
    api_key={
        'clientId': settings.PLAID_CLIENT_ID,
        'secret': settings.PLAID_SECRET,
    }
)

api_client = plaid.ApiClient(configuration)
plaid_client = plaid_api.PlaidApi(api_client)

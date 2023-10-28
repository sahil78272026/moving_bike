from storages.backends.azure_storage import AzureStorage
class AzureMediaStorage(AzureStorage):
    account_name = 'trackerfilestore' 
    account_key = 'zQRt9U7P3ULFSJI0P5zLy+LPKmZDCvG9rxZniqvcssAjvPH/htQnO6FH2KRpYY6Dlrzt4dJfdbGd+AStohehvw=='
    azure_container = 'trackerbackendimage'
    expiration_secs = None

# class AzureStaticStorage(AzureStorage):
#     account_name = 'mystorageaccount'
#     account_key = '<my key>'
#     azure_container = 'static'
#     expiration_secs = None
endpoints = [
    "https://uri-api.example.com/bi/getFiscalInvoice",
    "https://uri-api.example.com/res/getGuestChecks",
    "https://uri-api.example.com/org/getChargeBack",
    "https://uri-api.example.com/trans/getTransactions",
    "https://uri-api.example.com/inv/getCashManagementDetails",
]

payload = {'busDt': '2024-11-25', 'storeId': '001'}

BUCKET_NAME = 'cb_bucket'
FOLDER_BASE = 'data_lake'
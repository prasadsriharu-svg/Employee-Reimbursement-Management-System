
import requests

API_URL = "http://127.0.0.1:8000"


def login(username, password):
    response = requests.post(
        f"{API_URL}/auth/login",
        data={
            "username": username,
            "password": password
        },
        timeout=10
    )

    if response.status_code == 200:
        return response.json()

    return None


def get_current_user(access_token):
    response = requests.get(
        f"{API_URL}/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        timeout=10
    )

    if response.status_code == 200:
        return response.json()

    return None


def get_claims(access_token):
    response = requests.get(
        f"{API_URL}/claims",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        timeout=10
    )

    if response.status_code == 200:
        return response.json()

    return None


# def submit_claim(access_token, amount, category, description):
#     response = requests.post(
#         f"{API_URL}/claims",
#         headers={
#             "Authorization": f"Bearer {access_token}"
#         },
#         json={
#             "amount": amount,
#             "category": category,
#             "description": description
#         },
#         timeout=10
#     )

#     print("Status code:", response.status_code)
#     print("Response:", response.text)

#     if response.status_code in (200,201):
#         return response.json()

#     return None

def submit_claim(access_token, amount, category, description, receipt_filename):
    response = requests.post(
        f"{API_URL}/claims",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "amount": amount,
            "category": category,
            "description": description,
            "receipt_filename": receipt_filename
        },
        timeout=10
    )

    if response.status_code in (200, 201):
        return response.json()

    return {
        "error": response.json().get(
            "detail", "Unable to submit claim"
        )
    }



def update_claim_status(token, claim_id, status):
    response = requests.put(
        f"{API_URL}/claims/{claim_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"status": status}
    )

    if response.status_code == 200:
        return response.json()

    return None

def get_categories(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{API_URL}/categories",
        headers=headers,
        timeout=10
    )

    if response.status_code == 200:
        return response.json()

    return []


def upload_receipt(access_token, uploaded_file):
    uploaded_file.seek(0)

    response = requests.post(
        f"{API_URL}/receipts/upload",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        files={
            "receipt": (
                uploaded_file.name,
                uploaded_file,
                uploaded_file.type
            )
        },
        timeout=30
    )

    if response.status_code in (200, 201):
        return response.json()

    return {
        "error": response.json().get(
            "detail", "Receipt upload failed"
        )
    }


def get_finance_claims(token):
    response = requests.get(
        f"{API_URL}/finance/claims",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def mark_claim_paid(token, claim_id):
    response = requests.put(
        f"{API_URL}/finance/claims/{claim_id}/payment",
        headers={"Authorization": f"Bearer {token}"},
        json={"payment_status": "Paid"},
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def get_report_summary(token):
    response = requests.get(
        f"{API_URL}/reports/summary",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10
    )
    response.raise_for_status()
    return response.json()

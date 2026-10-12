from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import get_claims, insert_claim, update_claim_status,delete_claim, get_user_by_username, get_claims_by_employee, create_user, update_user_role, add_category, get_categories, set_category_limit, get_category_limit, get_approved_claims, update_payment_status, get_claim_summary, get_category_summary, save_receipt, insert_claim_with_receipt
from pydantic import BaseModel, Field, field_validator
from auth_service import verify_password
from security import create_access_token, verify_access_token
from typing import Literal
from uuid import uuid4
from pathlib import Path

###################
#      Users      #
###################

class LoginRequest(BaseModel):
    username: str
    password: str

###################
#      Claim      #
###################


class Claim(BaseModel):
    amount: float = Field(gt=0, description="Claim amount must be greater than zero")
    category: str
    description: str = Field(min_length=1, max_length=500)
    receipt_filename: str
    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Description cannot be empty.")

        return value


class ClaimStatus(BaseModel):
    status: Literal["Approved","Rejected"]

class ClaimResponse(BaseModel):
    id: int
    employee_name: str
    amount: float
    category: str
    description: str
    receipt: str
    status: str

class NewUser(BaseModel):
    employee_name: str
    username: str
    password: str
    role: str

class UserRoleUpdate(BaseModel):
    role: str

class NewCategory(BaseModel):
    category_name: str

class CategoryLimitUpdate(BaseModel):
    max_amount: float = Field(gt=0)

class PaymentStatusUpdate(BaseModel):
    payment_status: str

app = FastAPI()

#########
# Token #
#########

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_access_token(token)

def require_roles(*allowed_roles):
    def role_checker(
        current_user: dict = Depends(get_current_user)
    ):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to perform this action"
            )

        return current_user

    return role_checker

@app.get("/auth/me")
def read_current_user(
    current_user: dict = Depends(get_current_user)
):
    return current_user

@app.get("/manager/test")
def manager_test(
    current_user: dict = Depends(require_roles("Manager", "Admin"))
):
    return {
        "message": "Manager access granted",
        "username": current_user["username"],
        "role": current_user["role"]
    }

@app.get("/")
def home():
    return {"message": "Employee Reimbursement Management System API"}

@app.get("/claims", response_model=list[ClaimResponse])
def get_all_claims(
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] in ("Manager", "Admin"):
        claims = get_claims()
    else:
        claims = get_claims_by_employee(current_user["username"])

    return [
        {
            "id": claim[0],
            "employee_name": claim[1],
            "amount": claim[2],
            "category": claim[3],
            "description": claim[4],
            "receipt": claim[5],
            "status": claim[6]
        }
        for claim in claims
    ]

@app.get("/finance/claims")
def finance_get_claims(
    current_user: dict = Depends(
        require_roles("Finance", "Admin")
    )
):
    claims = get_approved_claims()

    return claims

# @app.post("/claims")
# def create_claim(
#     claim: Claim,
#     current_user: dict = Depends(require_roles("Employee", "Admin"))
# ):
#     limit = get_category_limit(claim.category)

#     if limit is not None and claim.amount > limit:
#         raise HTTPException(
#         status_code=400,
#         detail=(
#             f"Claim amount exceeds the limit of "
#             f"₹{limit:.2f} for {claim.category}"
#         )
#     )

#     insert_claim(
#         current_user["username"],
#         claim.amount,
#         claim.category,
#         claim.description,
#         "receipt.pdf",
#         "Submitted"
#     )

#     return {"message": "Claim created successfully"}
@app.post("/claims")
def create_claim(
    claim: Claim,
    current_user: dict = Depends(require_roles("Employee"))):
    valid_categories = [
        category[1] for category in get_categories()]

    if claim.category not in valid_categories:
        raise HTTPException(
            status_code=400,
            detail="Invalid reimbursement category"
    )

    limit = get_category_limit(claim.category)

    if limit is not None and claim.amount > limit:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Claim amount exceeds the limit of "
                f"₹{limit:.2f} for {claim.category}"
            )
        )

    claim_id = insert_claim_with_receipt(
        current_user["username"],
        claim.amount,
        claim.category,
        claim.description,
        claim.receipt_filename,
        current_user["user_id"]
    )

    if claim_id is None:
        raise HTTPException(
            status_code=400,
            detail="Receipt not found, already used, or does not belong to you"
        )

    return {
        "message": "Claim created successfully",
        "claim_id": claim_id
    }

@app.put("/claims/{claim_id}")
def update_claim(
    claim_id: int,
    claim: ClaimStatus,
    current_user: dict = Depends(require_roles("Manager", "Admin"))
):
    allowed_statuses = ("Approved", "Rejected")

    if claim.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Status must be Approved or Rejected"
        )

    claims = get_claims()
    existing_claim = next(
        (item for item in claims if item[0] == claim_id),
        None
    )

    if existing_claim is None:
        raise HTTPException(
            status_code=404,
            detail="Claim not found"
        )

    if existing_claim[6] != "Submitted":
        raise HTTPException(
            status_code=400,
            detail="Only Submitted claims can be reviewed"
        )

    update_claim_status(claim_id, claim.status)

    return {
        "message": f"Claim {claim_id} has been {claim.status.lower()}"
    }


# @app.delete("/claims/{claim_id}")
# def delete_claim_record(claim_id: int):
#     delete_claim(claim_id)
#     return{"message":"Claim deleted successfully"}

@app.delete("/claims/{claim_id}")
def delete_claim_record(
    claim_id: int,
    current_user: dict = Depends(require_roles("Admin"))
):
    delete_claim(claim_id)

    return {"message": "Claim deleted successfully"}

# @app.post("/auth/login")
# def login(credentials: LoginRequest):
#     user = get_user_by_username(credentials.username)

#     if user is None:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid username or password"
#         )

#     if not verify_password(
#         credentials.password,
#         user["password_hash"]
#     ):
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid username or password"
#         )

#     access_token = create_access_token(
#     user["id"],
#     user["username"],
#     user["role"]
#     )
    
#     return {
#     "access_token": access_token,
#     "token_type": "bearer",
#     "user_id": user["id"],
#     "username": user["username"],
#     "role": user["role"]
# }
@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form_data.username)

    if user is None or not verify_password(
        form_data.password,
        user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(
        user["id"],
        user["username"],
        user["role"]
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/admin/users")
def admin_create_user(
    user: NewUser,
    current_user: dict = Depends(require_roles("Admin"))
):
    allowed_roles = ["Employee", "Manager", "Finance", "Admin"]

    if user.role not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    if not user.employee_name.strip() or not user.username.strip():
        raise HTTPException(
            status_code=400,
            detail="Employee name and username cannot be empty"
        )

    if len(user.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 8 characters"
        )

    existing_user = get_user_by_username(user.username)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    create_user(
        user.employee_name.strip(),
        user.username.strip(),
        user.password,
        user.role
    )

    return {"message": "User created successfully"}

@app.put("/admin/users/{user_id}/role")
def admin_update_user_role(
    user_id: int,
    data: UserRoleUpdate,
    current_user: dict = Depends(require_roles("Admin"))
):
    allowed_roles = ["Employee", "Manager", "Finance", "Admin"]

    if data.role not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    if user_id == current_user["user_id"]:
        raise HTTPException(
            status_code=400,
            detail="You cannot change your own role"
        )

    updated_rows = update_user_role(user_id, data.role)

    if updated_rows == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {"message": "User role updated successfully"}

@app.get("/categories")
def list_categories(
    current_user: dict = Depends(get_current_user)
):
    categories = get_categories()

    return [
        {
            "id": category[0],
            "category_name": category[1]
        }
        for category in categories
    ]

@app.post("/admin/categories")
def admin_add_category(
    category: NewCategory,
    current_user: dict = Depends(require_roles("Admin"))
):
    category_name = category.category_name.strip()

    if not category_name:
        raise HTTPException(
            status_code=400,
            detail="Category name cannot be empty"
        )

    result = add_category(category_name)

    if not result:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    return {"message": "Category added successfully"}

@app.put("/admin/categories/{category_id}/limit")
def admin_set_category_limit(
    category_id: int,
    data: CategoryLimitUpdate,
    current_user: dict = Depends(require_roles("Admin"))
):
    result = set_category_limit(
        category_id,
        data.max_amount
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return {
        "message": "Category limit updated successfully",
        "category_id": category_id,
        "max_amount": data.max_amount
    }

@app.put("/finance/claims/{claim_id}/payment")
def finance_update_payment(
    claim_id: int,
    data: PaymentStatusUpdate,
    current_user: dict = Depends(
        require_roles("Finance", "Admin")
    )
):
    if data.payment_status != "Paid":
        raise HTTPException(
            status_code=400,
            detail="Only 'Paid' status is allowed"
        )

    updated_rows = update_payment_status(
        claim_id,
        data.payment_status
    )

    if updated_rows == 0:
        raise HTTPException(
            status_code=400,
            detail="Claim not found, not approved, or already paid"
        )

    return {
        "message": "Payment status updated successfully",
        "claim_id": claim_id,
        "payment_status": data.payment_status
    }

@app.get("/reports/summary")
def report_summary(
    current_user: dict = Depends(
        require_roles("Admin", "Manager", "Finance")
    )
):
    return get_claim_summary()

@app.get("/reports/categories")
def report_categories(
    current_user: dict = Depends(
        require_roles("Admin", "Manager", "Finance")
    )
):
    return get_category_summary()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_TYPES = {
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/png": ".png"
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def is_valid_receipt(content, content_type):
    if content_type == "application/pdf":
        return content.startswith(b"%PDF-")

    if content_type == "image/png":
        return content.startswith(b"\x89PNG\r\n\x1a\n")

    if content_type == "image/jpeg":
        return content.startswith(b"\xff\xd8\xff")

    return False
@app.post("/receipts/upload")
async def upload_receipt(
    receipt: UploadFile = File(...),
    current_user: dict = Depends(
        require_roles("Employee")
    )
):
    if receipt.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPG and PNG files are allowed"
        )

    content = await receipt.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Receipt must be 5 MB or smaller"
        )
    if not is_valid_receipt(content, receipt.content_type):
        raise HTTPException(
        status_code=400,
        detail="Invalid receipt file content"
    )

    extension = ALLOWED_TYPES[receipt.content_type]
    filename = f"{uuid4().hex}{extension}"

    file_path = UPLOAD_DIR / filename
    
    try:
        file_path.write_bytes(content)
        save_receipt(
        filename,
        current_user["user_id"]
    )
    except Exception as e:
        #file_path.unlink(missing_ok=True)
        print("RECEIPT SAVE ERROR:", repr(e))

        file_path.unlink(missing_ok=True)

        raise HTTPException(
        status_code=500,
        detail="Failed to save receipt"
    )

    return {
        "message": "Receipt uploaded successfully",
        "filename": filename
    }

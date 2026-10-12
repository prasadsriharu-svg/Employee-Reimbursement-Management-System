
import streamlit as st

from api_client import (
    login,
    get_current_user,
    get_claims,
    submit_claim,
    update_claim_status,
    get_categories,
    upload_receipt,
    get_finance_claims,
    mark_claim_paid,
    get_report_summary,
)

st.set_page_config(
    page_title="Reimbursement Management System",
    page_icon="💼",
    layout="wide",
)


st.markdown("""
<style>

/* Main application background */
.stApp {
    background: linear-gradient(
        135deg,
        #E8F5E1 0%,
        #F5FAF2 55%,
        #FFFFFF 100%
    );
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E2EBDD;
}

/* Main headings */
h1, h2, h3 {
    color: #263A31 !important;
}

/* Form containers */
[data-testid="stForm"] {
    background-color: #FFFFFF;
    border: 1px solid #E2EBDD;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 8px 24px rgba(38, 58, 49, 0.06);
}

/* Buttons */
.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background-color: #FF8273;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    font-weight: 600;
}

.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {
    background-color: #F46D60;
    color: #FFFFFF;
}

/* Dashboard metrics */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #E2EBDD;
    box-shadow: 0 4px 16px rgba(38, 58, 49, 0.04);
}

/* General containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 16px;
}


/* Login input fields */
div[data-testid="stTextInput"] input {
    background-color: #E9EDF2 !important;
    color: #263A31 !important;
    border: 1px solid #AAB8B0 !important;
    border-radius: 9px !important;
    padding: 12px !important;
}

/* Darker border when input is selected */
div[data-testid="stTextInput"] input:focus {
    background-color: #E9EDF2 !important;
    border: 2px solid #4E8B78 !important;
    box-shadow: 0 0 0 2px rgba(78, 139, 120, 0.15) !important;
}

/* Placeholder text */
div[data-testid="stTextInput"] input::placeholder {
    color: #7B8790 !important;
}

/* Input field labels */
div[data-testid="stTextInput"] label {
    color: #263A31 !important;
    font-weight: 600 !important;
}

/* Keep sidebar at a consistent width */
[data-testid="stSidebar"] {
    min-width: 250px !important;
    max-width: 250px !important;
}

[data-testid="stSidebar"] > div:first-child {
    width: 250px !important;
}

/* Give dashboard content enough room */
.block-container {
    max-width: 1400px !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Session initialization
# -----------------------------

for key in ("access_token", "username", "role"):
    if key not in st.session_state:
        st.session_state[key] = None


def logout():
    for key in ("access_token", "username", "role"):
        st.session_state[key] = None
    st.rerun()


def format_amount(amount):
    return f"₹{amount:,.2f}"


# -----------------------------
# Login page
# -----------------------------

if not st.session_state.access_token:
    st.title("💼 Employee Reimbursement Portal")
    st.caption("Secure reimbursement management for your organization")

    login_column,image_column = st.columns([1, 1], gap="large")

    with login_column:
        with st.container(border=True):
            st.subheader("Welcome Back")
            st.write("Sign in to access your dashboard.")

            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input(
                    "Password",
                    type="password"
                )
                login_clicked = st.form_submit_button(
                    "Sign In",
                    use_container_width=True,
                    type="primary",
                )

            if login_clicked:
                try:
                    result = login(username, password)

                    if not result:
                        st.error("Invalid username or password.")
                    else:
                        token = result["access_token"]
                        user = get_current_user(token)

                        if user:
                            st.session_state.access_token = token
                            st.session_state.username = user["username"]
                            st.session_state.role = user["role"]
                            st.rerun()
                        else:
                            st.error("Unable to retrieve user details.")

                except Exception as exc:
                    st.error(f"Login failed: {exc}")

    with image_column:
        st.markdown("""
        <div style="
            background: linear-gradient(
                145deg, #B9DCC8, #4E8B78
            );
            border-radius: 22px;
            padding: 65px 35px;
            min-height: 400px;
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <h2 style="color:white !important;">
                Welcome to ERMS
            </h2>
            <p style="font-size:18px; color:white;">
                A smarter way to manage employee
                reimbursements.
            </p>
            <p style="color:white;">
                Submit claims, track approvals,
                and manage payments in one place.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.stop()


# -----------------------------
# Sidebar navigation
# -----------------------------

role = st.session_state.role
token = st.session_state.access_token

st.sidebar.title("💼 Reimbursement Portal")
st.sidebar.divider()

st.sidebar.write(f"**User:** {st.session_state.username}")
st.sidebar.write(f"**Role:** {role}")

st.sidebar.divider()

navigation = {
    "Employee": [
        "Dashboard",
        "Submit Claim",
        "My Claims",
    ],
    "Manager": [
        "Dashboard",
        "Review Claims",
        "All Claims",
    ],
    "Finance": [
        "Dashboard",
        "Payments",
        "Payment History",
    ],
    "Admin": [
        "Dashboard",
        "Users",
        "Categories",
        "Reports",
    ],
}

pages = navigation.get(role, ["Dashboard"])

page = st.sidebar.radio(
    "Navigation",
    pages,
    key="navigation",
)

st.sidebar.divider()

if st.sidebar.button("🚪 Logout", use_container_width=True):
    logout()


# -----------------------------
# Shared dashboard helpers
# -----------------------------


def show_claims_table(claims):
    if not claims:
        st.info("No claims found.")
        return

    display_claims = []

    for claim in claims:
        display_claims.append({
            "Claim ID": claim["id"],
            "Category": claim["category"],
            "Amount (₹)": claim["amount"],
            "Description": claim["description"],
            "Status": claim["status"],
        })

    st.dataframe(
        display_claims,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Amount (₹)": st.column_config.NumberColumn(
                "Amount (₹)",
                format="₹%.2f",
            ),
            "Description": st.column_config.TextColumn(
                "Description",
                width="large",
            ),
            "Status": st.column_config.TextColumn(
                "Status",
                width="medium",
            ),
        },
    )



def show_dashboard(claims):
    st.title(f"Welcome, {st.session_state.username}!")
    st.caption(f"{role} Dashboard")

    total = len(claims)
    submitted = sum(
        1 for claim in claims
        if claim.get("status") == "Submitted"
    )
    approved = sum(
        1 for claim in claims
        if claim.get("status") == "Approved"
    )
    rejected = sum(
        1 for claim in claims
        if claim.get("status") == "Rejected"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Claims", total)
    col2.metric("Pending Approval", submitted)
    col3.metric("Approved", approved)
    col4.metric("Rejected", rejected)

    st.divider()
    st.subheader("Recent Claims")

    show_claims_table(claims[-10:])


# -----------------------------
# Employee pages
# -----------------------------

if role == "Employee":

    if page == "Dashboard":
        claims = get_claims(token)

        if claims is None:
            st.error("Unable to retrieve claims.")
        else:
            show_dashboard(claims)

    elif page == "My Claims":
        st.title("My Reimbursement Claims")

        claims = get_claims(token)

        if claims is None:
            st.error("Unable to retrieve claims.")
        else:
            show_claims_table(claims)

    elif page == "Submit Claim":
        st.title("Submit New Reimbursement Claim")
        st.caption("Enter your expense details and upload a receipt.")

        try:
            category_data = get_categories(token)
            category_names = [
                item["category_name"]
                for item in category_data
            ]
        except Exception:
            category_names = []

        with st.form("new_claim_form"):
            col1, col2 = st.columns(2)

            with col1:
                amount = st.number_input(
                    "Claim Amount (₹)",
                    min_value=0.01,
                    step=100.0,
                )

            with col2:
                category = st.selectbox(
                    "Expense Category",
                    category_names,
                    index=None,
                    placeholder="Select a category",
                )

            description = st.text_area(
                "Description",
                max_chars=500,
            )

            receipt = st.file_uploader(
                "Upload Receipt",
                type=["pdf", "jpg", "jpeg", "png"],
                help="PDF, JPG or PNG. Maximum 5 MB.",
            )

            submitted = st.form_submit_button(
                "Submit Reimbursement Claim",
                type="primary",
                use_container_width=True,
            )

        if submitted:
            if not category:
                st.warning("Please select a category.")
            elif not description.strip():
                st.warning("Please enter a description.")
            elif receipt is None:
                st.warning("Please upload a receipt.")
            elif receipt.size > 5 * 1024 * 1024:
                st.warning("Receipt must be 5 MB or smaller.")
            else:
                try:
                    with st.spinner("Uploading receipt..."):
                        upload_result = upload_receipt(
                            token,
                            receipt,
                        )

                    if not upload_result or upload_result.get("error"):
                        st.error(
                            (upload_result or {}).get(
                                "error", "Receipt upload failed."
                            )
                        )
                    else:
                        receipt_filename = upload_result.get(
                            "filename"
                        )

                        if not receipt_filename:
                            st.error(
                                "Receipt uploaded, but the API did "
                                "not return a filename. Check the "
                                "upload response."
                            )
                        else:
                            with st.spinner("Submitting claim..."):
                                result = submit_claim(
                                    token,
                                    amount,
                                    category,
                                    description,
                                    receipt_filename,
                                )

                            if result and not result.get("error"):
                                st.success(
                                    "Claim submitted successfully!"
                                )
                                st.write(
                                    "Claim ID:",
                                    result.get("claim_id")
                                )
                            else:
                                st.error(
                                    (result or {}).get(
                                        "error",
                                        "Claim submission failed.",
                                    )
                                )

                except Exception as exc:
                    st.error(f"Unable to submit claim: {exc}")


# -----------------------------
# Manager pages
# -----------------------------

elif role == "Manager":

    claims = get_claims(token)

    if claims is None:
        st.error("Unable to retrieve claims.")
        st.stop()

    if page == "Dashboard":
        show_dashboard(claims)

    elif page == "All Claims":
        st.title("All Reimbursement Claims")
        show_claims_table(claims)

    elif page == "Review Claims":
        st.title("Review Pending Claims")

        pending_claims = [
            claim for claim in claims
            if claim.get("status") == "Submitted"
        ]

        if not pending_claims:
            st.success("No pending claims to review.")

        for claim in pending_claims:
            with st.container(border=True):
                st.subheader(
                    f"Claim #{claim['id']} — "
                    f"{claim['employee_name']}"
                )

                st.write(
                    f"**Amount:** "
                    f"{format_amount(claim['amount'])}"
                )
                st.write(
                    f"**Category:** {claim['category']}"
                )
                st.write(
                    f"**Description:** {claim['description']}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "Approve",
                        key=f"approve_{claim['id']}",
                        type="primary",
                        use_container_width=True,
                    ):
                        result = update_claim_status(
                            token,
                            claim["id"],
                            "Approved",
                        )

                        if result is not None:
                            st.success("Claim approved.")
                            st.rerun()
                        else:
                            st.error("Approval failed.")

                with col2:
                    if st.button(
                        "Reject",
                        key=f"reject_{claim['id']}",
                        use_container_width=True,
                    ):
                        result = update_claim_status(
                            token,
                            claim["id"],
                            "Rejected",
                        )

                        if result is not None:
                            st.success("Claim rejected.")
                            st.rerun()
                        else:
                            st.error("Rejection failed.")


# -----------------------------
# Finance and Admin placeholders
# -----------------------------


elif role == "Finance":
    st.title("Finance Management")
    st.caption("Manage employee reimbursement payments")

    try:
        finance_claims = get_finance_claims(token)
        summary = get_report_summary(token)
    except Exception as exc:
        st.error(f"Unable to load Finance data: {exc}")
        st.stop()

    if page == "Dashboard":
        st.subheader("Finance Dashboard")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric(
            "Total Claims",
            summary.get("total_claims", 0))
        col2.metric(
            "Total Requested",
            format_amount(summary.get("total_amount", 0))
        )

        col3.metric(
            "Amount Paid",
            format_amount(summary.get("paid_amount", 0))
        )

        col4.metric(
            "Pending Payment",
            format_amount(
                summary.get("pending_payment_amount", 0)
            )
        )
        st.subheader("Claims Awaiting Payment")
        show_claims_table(finance_claims)

    
    elif page == "Payments":
        st.subheader("Process Payments")

        pending_claims = [
            claim for claim in finance_claims
            if claim.get("status") == "Approved"
            and claim.get("payment_status") == "Pending"
        ]

        if not pending_claims:
            st.success("No payments are currently pending.")

        for claim in pending_claims:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(
                        f"**Claim #{claim['id']} — "
                        f"{claim['employee_name']}**"
                    )
                    st.write(
                        f"Category: {claim['category']}"
                    )
                    st.write(
                        f"Description: {claim['description']}"
                    )
                    st.write(
                        f"Amount: {format_amount(claim['amount'])}"
                    )

                with col2:
                    st.write("Payment Status")
                    st.warning("Pending")

                    if st.button(
                        "Mark as Paid",
                        key=f"pay_{claim['id']}",
                        type="primary",
                        use_container_width=True,
                    ):
                        try:
                            result = mark_claim_paid(
                                token,
                                claim["id"],
                            )

                            st.success(
                                f"Claim #{claim['id']} "
                                "marked as Paid."
                            )
                            st.rerun()

                        except Exception as exc:
                            st.error(
                                f"Payment update failed: {exc}"
                            )


    
    elif page == "Payment History":
        st.subheader("Payment History")

        paid_claims = [
            claim for claim in finance_claims
            if claim.get("payment_status") == "Paid"
        ]

        if paid_claims:
            st.dataframe(
                [
                    {
                        "Claim ID": claim["id"],
                        "Employee": claim["employee_name"],
                        "Category": claim["category"],
                        "Amount (₹)": claim["amount"],
                        "Payment Status": claim["payment_status"],
                    }
                    for claim in paid_claims
                ],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Amount (₹)": st.column_config.NumberColumn(
                        "Amount (₹)",
                        format="₹%.2f",
                    ),
                },
            )
        else:
            st.info("No paid claims found.")




elif role == "Admin":

    if page == "Dashboard":
        st.title("Administration Dashboard")
        st.caption("Overview of employee reimbursement activity")

        try:
            summary = get_report_summary(token)

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Total Claims",
                summary.get("total_claims", 0)
            )

            col2.metric(
                "Total Requested",
                format_amount(summary.get("total_amount", 0))
            )

            col3.metric(
                "Approved Claims",
                summary.get("approved_claims", 0)
            )

            col4.metric(
                "Pending Approval",
                summary.get("submitted_claims", 0)
            )

            st.divider()
            st.subheader("Financial Overview")

            col5, col6 = st.columns(2)

            col5.metric(
                "Amount Paid",
                format_amount(summary.get("paid_amount", 0))
            )

            col6.metric(
                "Pending Payment",
                format_amount(
                    summary.get("pending_payment_amount", 0)
                )
            )

        except Exception as exc:
            st.error(f"Unable to load dashboard: {exc}")

    elif page == "Users":
        st.title("User Management")
        st.info("User management will be connected next.")

    elif page == "Categories":
        st.title("Category Management")
        st.info("Category management will be connected next.")

    elif page == "Reports":
        st.title("Reimbursement Reports")
        st.info("Reports will be connected next.")

else:
    st.error("Unknown user role.")

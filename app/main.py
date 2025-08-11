from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, constr, ValidationError
from pathlib import Path

app = FastAPI()

usersList = [
    {"id": 1, "name": "Ahmed", "email": "example@hotmail.com", "password": "password123", "balance": 1000},
    {"id": 2, "name": "Khalil", "email": "example@gmail.com", "password": "password234", "balance": 500},
    {"id": 3, "name": "Mohamed", "email": "example@outlook.com", "password": "password345", "balance": 250}
]

all_transactions = [
    {"email": "example@hotmail.com", "To Account": 1, "Amount": 100},
    {"email": "example@gmail.com", "To Account": 2, "Amount": 50},
    {"email": "example@outlook.com", "To Account": 3, "Amount": 25}
]

user_transactions = []
user_balance = 0
logged_in_user = None

# Define the static directory path
STATIC_DIR = Path(__file__).resolve().parent / "static"

# Serve files from the "static" folder
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Model for validating form input
class SignupForm(BaseModel):
    name: constr(min_length=1, max_length=100)
    email: str
    password: str

class LoginForm(BaseModel):
    email: str
    password: str

class TransactionForm(BaseModel):
    to_account_id: int
    amount:float

@app.get("/", response_class=HTMLResponse)
def get_signup_form():
    html_path = STATIC_DIR / "P2P_system.html"
    return html_path.read_text()


@app.post("/signup")
def post_signup(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    global usersList
    global users_counter
    try:
        form = SignupForm(name=name, email=email, password=password)
        if any(user["email"].lower() == email.lower() for user in usersList):
                return JSONResponse(
                status_code=409,
                content={"message": "User with this email already exists"}
            )
        users_counter = len(usersList) + 1  # Increment user count
        usersList.append({"id" : users_counter, "name": form.name, "email": form.email, "password": form.password, "balance": 1000})  # Add to usersList
        return {"message": f"Thanks for Signing up, {form.name}!"}
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content={"detail": e.errors()}
        )

@app.post("/login")
def post_login(
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        form = LoginForm(email=email, password=password)
       # Check if the user exists by email
        user = next((user for user in usersList if user["email"] == form.email), None)
        if not user:
            return JSONResponse(
                status_code=404,
                content={"detail": "User not found"}
            )
        # Check if the password matches
        if user["password"] != form.password:
            return JSONResponse(
                status_code=401,
                content={"detail": "Incorrect password"}
            )
       
        global logged_in_user 
        logged_in_user = email
        global user_balance
        user_balance = user["balance"]  # Set the user's balance
        global user_transactions
        # Filter transactions for the logged-in user
        user_transactions = [transaction for transaction in all_transactions if transaction["email"] == logged_in_user]
        return {"message": f"Log in successful!"}
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content={"detail": e.errors()}
        )

@app.get("/balance")
def get_balance():
    global user_balance
    # Assuming user_balance is set based on the logged-in user
    user_balance = next((user["balance"] for user in usersList if user["email"] == logged_in_user), 0)
    return {"balance": user_balance}

def process_transaction(logged_in_user, user_balance, usersList, all_transactions, user_transactions, to_account_id, amount):
    if user_balance < amount:
        return {"error": "Insufficient balance"}
    for user in usersList:
        if user["email"] == logged_in_user and user["id"] == to_account_id:
            return {"error": "Cannot send money to yourself"}
    if to_account_id <= 0 or to_account_id > len(usersList):
        return {"error": "Invalid account ID"}
    # Deduct the amount from the user's balance
    user_balance -= amount
    # Add the transaction to the all_transactions list
    transaction = {
        "email": logged_in_user,
        "To Account": to_account_id,
        "Amount": amount
    }
    all_transactions.append(transaction)
    user_transactions.append(transaction)
    # Update the user's balance in the usersList
    for user in usersList:
        if user["email"] == logged_in_user:
            user["balance"] -= amount
            break
    for user in usersList:
        if user["id"] == to_account_id:
            user["balance"] += amount
            break
    return {"message": f"Transaction of {amount} to account {to_account_id} successful!", "user_balance": user_balance}

@app.post("/send_transaction")
def post_send_transaction(
    to_account_id: int = Form(...),
    amount: float = Form(...)
):
    global user_balance
    try:
        form = TransactionForm(to_account_id=to_account_id, amount=amount)
        result = process_transaction(
            logged_in_user,
            user_balance,
            usersList,
            all_transactions,
            user_transactions,
            form.to_account_id,
            form.amount
        )
        if "error" in result:
            return JSONResponse(
                status_code=400,
                content={"detail": result["error"]}
            )
        user_balance = result["user_balance"]  # update global
        return {"message": result["message"]}
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content={"detail": e.errors()}
        )

# chage transactiosn name issue
@app.get("/view_transcaitons")
def get_transcaitons():
    if len(user_transactions) > 0:
        return JSONResponse(content=user_transactions)

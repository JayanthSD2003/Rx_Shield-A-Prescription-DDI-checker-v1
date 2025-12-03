import bcrypt
from core.database import add_user, get_user, init_db

# Initialize DB on module load (or call explicitly in main)
init_db()

def register(username, password):
    if not username or not password:
        return False, "Username and password are required."
    
    if get_user(username):
        return False, "Username already exists."

    # Hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    if add_user(username, hashed.decode('utf-8')):
        return True, "Registration successful."
    else:
        return False, "Registration failed."

def login(username, password):
    user = get_user(username)
    if user:
        stored_hash = user['password_hash'].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return True, "Login successful."
    
    return False, "Invalid username or password."

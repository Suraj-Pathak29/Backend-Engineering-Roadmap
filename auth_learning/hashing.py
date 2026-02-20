import bcrypt

def create_password_hash(plain_password):

    #Takes a plain strirng (e.g., 'hunter2') and turns it into a secret hash

    # 1. Convert string to bytes (bcrypt requires bytes)
    password_bytes = plain_password.encode('utf-8')

    # 2. Generate Salt (Random data to make the hash unique every time)
    salt = bcrypt.gensalt()

    # 3. Hash it
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    # 4. Return it (usually as a string for the database)
    return hashed_password


def verify_password(plain_password, stored_hash):
     
    #Checks if the password user typed matches the hash in the DB.
    password_bytes = plain_password.encode('utf-8')

    # checkpw does the math to see if they match
    return bcrypt.checkpw(password_bytes , stored_hash)

# --- THE EXPERIMENT ---
if __name__ == '__main__':
    user_input = 'my_super_secret_password'

    print(f"1. User types: {user_input}")

    # Step 1: Hash it (This is what happens when you Register)
    secure_hash = create_password_hash(user_input)

    # Step 2: Verify it (This is what happens when you Login)
    login_attempt = input("\nSimulate Login - Enter Password: ")

    if verify_password(login_attempt, secure_hash):
        print("Access Granted!")
    
    else:
        print("Accesss denied! (Police siren Wail)")

    
    
    
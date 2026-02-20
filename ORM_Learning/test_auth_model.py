from models import User

user = User(username = 'secure_user' , email = 'safe@test.com')

print("Setting password to 'secret123'...")
user.set_password('secret123')

# 3. Check the internal storage
print(f"Stored hash: {user.password_hash}")
# (It should look like $2b$12$......)


# 4. Verify
print("\n--- Verifying ---")
is_correct = user.check_password('secret123')
print(f"Password 'secret123' is correct? {is_correct}")

is_wrong = user.check_password('wrong_pass')
print(f"Password 'wrong_pass is correct? {is_wrong}")


      


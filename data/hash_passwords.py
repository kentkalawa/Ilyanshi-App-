import bcrypt
import pandas as pd

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Define users with plain passwords
users = [
    {"username": "kent", "password": "admin2026", "role": "Admin", "name": "Kent Kalawa"},
    {"username": "jbanda", "password": "officer123", "role": "Officer", "name": "John Banda"},
    {"username": "mphiri", "password": "officer456", "role": "Officer", "name": "Mary Phiri"},
    {"username": "dmwale", "password": "viewer123", "role": "Viewer", "name": "David Mwale"},
]

# Hash all passwords
for user in users:
    user["password"] = hash_password(user["password"])

# Save to CSV
df = pd.DataFrame(users)
df.to_csv("users_hashed.csv", index=False)
print("✅ users_hashed.csv created successfully")
print(df)
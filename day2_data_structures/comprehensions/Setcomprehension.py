# Set Comprehension: Cleaning Username Signups
raw_usernames = ["AliceM", "bob_99", "ALICEM", "charlie_brown", "bob_99"]
clean_usernames = {name.lower() for name in raw_usernames} # Set comprehension lowercase-ifies and removes duplicates automatically
print("Original:", raw_usernames)
print("Cleaned Set:", clean_usernames)

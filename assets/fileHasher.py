import hashlib

# Initialize a list to store the hash and file name pairs
hash_list = []

# File to save file hashes and file name in csv format
# hashFile  = "fileHashes.csv"
directory = "data"

def fileHasher(file_path):

    try:
        # Generate SHA-256 hash for the file
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as file:
            while True:
                data = file.read()
                if not data: break
                sha256.update(data)

        payload_hash = format(sha256.hexdigest())
        return payload_hash
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}\n")



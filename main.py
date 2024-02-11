import os
import hashlib
import pickle
from tqdm import tqdm
from collections import defaultdict
from datetime import datetime
from multiprocessing import Pool

CACHE_FILE = "cache.smc"
NUM_PROCESSES = os.cpu_count()
POOL_SIZE = min(NUM_PROCESSES, 8)

def get_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def calculate_hash(file_path):
    try:
        return file_path, get_file_hash(file_path)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def generate_hash_cache(directory):
    hash_cache = {}
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_paths.append(os.path.join(root, file_name))

    with Pool(POOL_SIZE) as pool:
        with tqdm(total=len(file_paths), desc="Building Hash Cache", unit="file") as pbar:
            for file_path, file_hash in pool.imap_unordered(calculate_hash, file_paths):
                if file_hash is not None:
                    if file_hash in hash_cache:
                        hash_cache[file_hash].append(file_path)
                    else:
                        hash_cache[file_hash] = [file_path]
                    pbar.update(1)
    return hash_cache

def save_cache(cache):
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(cache, f)

def load_cache():
    if not os.path.exists(CACHE_FILE):
        print("Cache file does not exist.")
        return None
    with open(CACHE_FILE, 'rb') as f:
        cache = pickle.load(f)

    print("Validating Cache...")
    valid_cache = {}
    with Pool(POOL_SIZE) as pool_load:
        for hash_value, file_paths in tqdm(cache.items(), desc="Validating Hash Cache", unit="hash"):
            validated_files = pool_load.map(lambda file_path: validate_file(file_path, hash_value), file_paths)
            validated_files = [file_path for file_path, is_valid in validated_files if is_valid]
            if validated_files:
                valid_cache[hash_value] = validated_files
    print("Cache validation complete.")
    return valid_cache

def validate_file(file_path, hash_value):
    return file_path, os.path.exists(file_path) and get_file_hash(file_path) == hash_value

def delete_duplicate_folders(hash_cache):
    duplicate_count = 0
    for hash_value, file_paths in hash_cache.items():
        if len(file_paths) > 1:
            folder_map = defaultdict(list)
            for file_path in file_paths:
                folder_path = os.path.dirname(file_path)
                folder_map[folder_path].append(file_path)

            for folder_path, files in folder_map.items():
                if len(files) > 1:
                    duplicate_count += 1
                    oldest_file = min(files, key=lambda x: os.path.getctime(x))
                    print(f"Duplicate files found in folder: {folder_path}")
                    for file in files:
                        try:
                            if file != oldest_file:
                                os.remove(file)
                        except PermissionError:
                            print(f"Permission denied to delete file: {file}")
    print(f"Total duplicate folders found: {duplicate_count}")


if __name__ == "__main__":
    directory = input("Enter the directory path: ")

    if os.path.exists(CACHE_FILE):
        use_cache = input("Cache file exists. Do you want to use it? (yes/no): ").lower() == "yes"
    else:
        use_cache = False

    if use_cache:
        hash_cache = load_cache()
        if hash_cache is None:
            hash_cache = generate_hash_cache(directory)
            save_cache(hash_cache)
    else:
        hash_cache = generate_hash_cache(directory)
        save_cache(hash_cache)

    delete_duplicates = input("Do you want to delete duplicate files (yes/no)? ").lower() == "yes"
    if delete_duplicates:
        delete_duplicate_folders(hash_cache)

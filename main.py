import re, random, string, argparse
import os, threading

import hashlib
from Crypto.Hash import MD4

def generate_random_string(length):
    # Includes a-z, A-z, 0-9, and all special characters
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def generate_md4_hash_with_salt(data: str, salt: str, method: str) -> str:

    # Checking salting method
    if method == 'append':
        salted_data = data + salt
    elif method == 'prepend':
        salted_data = salt + data
    else:
        raise ValueError("Invalid salting method. Use 'append' or 'prepend'.")
    
    # Generating the hash
    hash_hex = MD4.new(salted_data.encode()).hexdigest()

    return hash_hex

def generate_md5_hash_with_salt(data: str, salt: str, method: str) -> str:

    # Checking salting method
    if method == 'append':
        salted_data = data + salt
    elif method == 'prepend':
        salted_data = salt + data
    else:
        raise ValueError("Invalid salting method. Use 'append' or 'prepend'.")
    
    # Generating the hash
    hash_hex = hashlib.md5(salted_data.encode()).hexdigest()

    return hash_hex

def check_hash_format(hash_str: str) -> bool:
   
    # Using regular expression to get a hash that matches "0e[Numbers]"
    pattern = r'^0e\d+$'
    
    # Use re.match to check if the hash matches the pattern
    if re.match(pattern, hash_str):
        return True
    else:
        return False

def hash_finder(stop_event, length, salt, algorithm, method):
   
    # Searches for a desired hash
    while not stop_event.is_set():
        random_data = generate_random_string(length)
        if algorithm == 'md5':
            hash_result = generate_md5_hash_with_salt(random_data, salt, method)
        elif algorithm == 'md4':
            hash_result = generate_md4_hash_with_salt(random_data, salt, method)

        # If the hash matches regular expression we have found a magic hash candidate
        if check_hash_format(hash_result):
            print(f"[+] Match found! Data: {random_data}, Hash: {hash_result}")
            stop_event.set()
            break

def get_optimal_thread_count():
    # Used to find a candidate for how many threads user's computer can provide
    cpu_count = os.cpu_count() or 4 
    return max(4, cpu_count)

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Generate a hash with given parameters.')

    # Add arguments
    parser.add_argument('-l', '--length', type=int, required=True, help='Length of the string to hash.')
    parser.add_argument('-s', '--salt', type=str, required=True, help='Salt to append/prepend to the string before hashing.')
    parser.add_argument('-a', '--algorithm', type=str, required=True, choices=['md5', 'md4'], help='Hashing algorithm to be used.')
    parser.add_argument('-m', '--method', type=str, required=True, choices=['append', 'prepend'], help='Hash method to use (append or prepend).')

    # Parse arguments
    args = parser.parse_args()

    stop_event = threading.Event()
    threads = []

    thread_count = get_optimal_thread_count()

    print('[+] Generating Magic Hash.')

    for _ in range(thread_count):
        thread = threading.Thread(target=hash_finder, args=(stop_event, args.length, args.salt, args.algorithm, args.method))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
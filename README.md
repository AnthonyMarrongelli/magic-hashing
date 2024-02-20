# Magic Hash Finder

## Description

This Python program is designed to find "magic hashes" that meet specific criteria. A magic hash for MD5 with a salt is a hash that starts with `0e` followed by digits, interpreted as zero in loose comparisons in PHP. This tool allows you to specify a salt, the method of applying the salt (either append or prepend), and the length of the random string to be hashed.
- Note that this program may take several minutes to find a solution.

## Requirements

- Python 3.x

## Usage

1. **Clone the repository or download the script** to your local machine.

2. **Navigate to the script's directory** in your terminal.

3. **Execute the script** with the required parameters:

   ```bash
   python main.py -l <length> -s <salt> -a <algorithm> -m <method>
   ```
   - "-l" or "--length" specifies the length of the random string to hash.
   - "-s" or "--salt" specifies the salt to append/prepend to the string before hashing.
   - "-a" or "--algorithm" specifies the hashing algorithm to be used (md5 or md4).
   - "-m" or "--method" specifies the method to use for salting (append or prepend).

## Current Supported Hashing Algorithms

- md5
- md4

# Magic Hashes

## Overview

Magic hash collisions refer to a peculiar behavior in PHP where two seemingly different values are considered equal due to PHP's loose comparison operator (`==`). This phenomenon is notably observed when comparing hash values.

## How Do They Occur?

Magic hash collisions happen during PHP's loose comparison (`==`) between strings and numbers, or between two strings that are numeric. PHP attempts to convert the string into a number for the comparison, leading to unexpected results.

### The Role of Hashing Algorithms

Hashing algorithms like MD5 or SHA1 can produce outputs that start with `0e` followed by digits. PHP interprets the `0e` prefix as scientific notation, effectively treating the hash as zero. For example, `0e830400451993494058024219903391` (MD5) and `0e462097431906509019562988736854` (another MD5 hash) are considered equal in PHP under loose comparison because both are interpreted as zero.

## How Can We Exploit This?

Given a security system that has a magic hash collision vulnerability, we can generate a 'matching' hash that can authenticate someone that should not be authenticated.

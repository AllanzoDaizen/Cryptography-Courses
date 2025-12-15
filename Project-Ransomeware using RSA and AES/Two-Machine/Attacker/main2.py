import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.generate_key import generate_rsa_keys

def main():
    generate_rsa_keys()

if __name__ == "__main__":
    main()
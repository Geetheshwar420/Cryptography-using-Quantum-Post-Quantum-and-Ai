from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# AI Encryption Class
class AIEncryption:
    def __init__(self):
        self.model_weights = [7, 3, 9, 2, 5]  # Example neural network weights

    def encrypt(self, message, key):
        encrypted = ""
        for char in message:
            encrypted += chr((ord(char) + sum(self.model_weights) + key) % 256)
        return encrypted

    def decrypt(self, encrypted_message, key):
        decrypted = ""
        for char in encrypted_message:
            decrypted += chr((ord(char) - sum(self.model_weights) - key) % 256)
        return decrypted

# Quantum Encryption Class
class QuantumEncryption:
    def __init__(self):
        self.key = None

    def generate_key(self, password):
        self.key = hashlib.sha256(password.encode()).digest()

    def encrypt(self, message):
        if not self.key:
            raise ValueError("Key not set. Please set a password to encrypt.")
        return ''.join(chr((ord(char) + sum(self.key)) % 256) for char in message)

    def decrypt(self, encrypted_message, password):
        self.generate_key(password)
        return ''.join(chr((ord(char) - sum(self.key)) % 256) for char in encrypted_message)

# Post Quantum Encryption Class
class PostQuantumEncryption:
    def __init__(self):
        self.private_key = hashlib.sha256().digest()  # Simple placeholder

    def generate_shared_key(self, password):
        return hashlib.sha256(password.encode()).digest()

    def encrypt(self, message, shared_key):
        encrypted_message = ''.join(chr((ord(char) + shared_key[0]) % 256) for char in message)
        return encrypted_message

    def decrypt(self, encrypted_message, shared_key):
        decrypted_message = ''.join(chr((ord(char) - shared_key[0]) % 256) for char in encrypted_message)
        return decrypted_message

# Initialize Encryption Classes
ai_encryption = AIEncryption()
quantum_encryption = QuantumEncryption()
post_quantum_encryption = PostQuantumEncryption()

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        data = request.json
        message = data.get("message")
        password = data.get("password")
        encryption_type = data.get("type")

        if not message or not password or not encryption_type:
            return jsonify({"error": "Message, password, and encryption type are required."}), 400

        if encryption_type == "ai":
            key = sum(ord(char) for char in password)  # Generate simple key
            encrypted_message = ai_encryption.encrypt(message, key)
        elif encryption_type == "quantum":
            quantum_encryption.generate_key(password)
            encrypted_message = quantum_encryption.encrypt(message)
        elif encryption_type == "post_quantum":
            shared_key = post_quantum_encryption.generate_shared_key(password)
            encrypted_message = post_quantum_encryption.encrypt(message, shared_key)
        else:
            return jsonify({"error": "Unknown encryption type."}), 400

        return jsonify({"encrypted_message": encrypted_message})
    except Exception as e:
        return jsonify({"error": f"Encryption failed: {str(e)}"}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        data = request.json
        encrypted_message = data.get("encrypted_message")
        password = data.get("password")
        encryption_type = data.get("type")

        if not encrypted_message or not password or not encryption_type:
            return jsonify({"error": "Encrypted message, password, and encryption type are required."}), 400

        if encryption_type == "ai":
            key = sum(ord(char) for char in password)  # Generate simple key
            decrypted_message = ai_encryption.decrypt(encrypted_message, key)
        elif encryption_type == "quantum":
            decrypted_message = quantum_encryption.decrypt(encrypted_message, password)
        elif encryption_type == "post_quantum":
            shared_key = post_quantum_encryption.generate_shared_key(password)
            decrypted_message = post_quantum_encryption.decrypt(encrypted_message, shared_key)
        else:
            return jsonify({"error": "Unknown encryption type."}), 400

        return jsonify({"decrypted_message": decrypted_message})
    except Exception as e:
        return jsonify({"error": f"Decryption failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

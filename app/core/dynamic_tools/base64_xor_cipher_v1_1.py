def base64_xor_cipher(payload: str, key: str = "key", operation: str = "encrypt") -> str:
    import base64
    # Simple XOR mapping
    key_bytes = key.encode('utf-8')
    payload_bytes = payload.encode('utf-8')
    xor_bytes = bytearray(len(payload_bytes))
    for i in range(len(payload_bytes)):
        xor_bytes[i] = payload_bytes[i] ^ key_bytes[i % len(key_bytes)]
        
    if operation == "encrypt":
        return base64.b64encode(xor_bytes).decode('utf-8')
    else:
        # Base64 decode, then decrypt (XOR is symmetric)
        decoded = base64.b64decode(payload.encode('utf-8'))
        decrypted_bytes = bytearray(len(decoded))
        for i in range(len(decoded)):
            decrypted_bytes[i] = decoded[i] ^ key_bytes[i % len(key_bytes)]
        return decrypted_bytes.decode('utf-8')

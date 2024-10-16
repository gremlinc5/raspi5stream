def cypher_XTEA(data, key):
    """
    Cifra i dati utilizzando l'algoritmo XTEA.
    
    :param data: I dati da cifrare come array di byte.
    :param key: La chiave di cifratura (16 byte).
    :return: I dati cifrati come array di byte.
    """
    num_rounds = 32
    delta = 0x9E3779B9
    
    # Assicurati che la chiave sia lunga 16 byte
    if len(key) != 16:
        raise ValueError("La chiave deve essere lunga esattamente 16 byte.")
    
    # Calcola la dimensione originale e il padding necessario
    original_size = len(data)
    padding_size = 8 if (original_size % 8) == 0 else original_size % 8
    
    # Prepara i dati con il padding
    padded_data = bytes([padding_size]) + bytes(padding_size - 1) + data

    # Aggiungi padding di 0 fino al multiplo di 8
    while len(padded_data) % 8 != 0:
        padded_data += bytes([0])

    # Crea un array di byte per contenere i dati cifrati
    encrypted_data = bytearray(padded_data)
    
    # Cifra ogni blocco di 8 byte
    for i in range(0, len(encrypted_data), 8):
        v0 = int.from_bytes(encrypted_data[i:i+4], 'little')
        v1 = int.from_bytes(encrypted_data[i+4:i+8], 'little')
        
        # Leggi la chiave di 128 bit
        k = [int.from_bytes(key[j:j+4], 'little') for j in range(0, 16, 4)]
        
        # Ciclo di cifratura
        sum_value = 0
        for _ in range(num_rounds):
            v0 = (v0 + (((v1 << 4 ^ v1 >> 5) + v1) ^ (sum_value + k[0]))) & 0xFFFFFFFF
            sum_value = (sum_value + delta) & 0xFFFFFFFF
            v1 = (v1 + (((v0 << 4 ^ v0 >> 5) + v0) ^ (sum_value + k[1]))) & 0xFFFFFFFF
        
        # Scrivi i valori cifrati nel bytearray
        encrypted_data[i:i+4] = v0.to_bytes(4, 'little')
        encrypted_data[i+4:i+8] = v1.to_bytes(4, 'little')
    
    return bytes(encrypted_data)


def decypher_XTEA(data, key):
    """
    Decifra i dati cifrati utilizzando l'algoritmo XTEA.
    
    :param data: I dati cifrati come array di byte.
    :param key: La chiave di decifratura (16 byte).
    :return: I dati decifrati come array di byte.
    """
    num_rounds = 32
    delta = 0x9E3779B9
    
    # Assicurati che la chiave sia lunga 16 byte
    if len(key) != 16:
        raise ValueError("La chiave deve essere lunga esattamente 16 byte.")
    
    # Crea un array di byte per contenere i dati decifrati
    decrypted_data = bytearray(data)
    
    # Decifra ogni blocco di 8 byte
    for i in range(0, len(decrypted_data), 8):
        v0 = int.from_bytes(decrypted_data[i:i+4], 'little')
        v1 = int.from_bytes(decrypted_data[i+4:i+8], 'little')
        
        # Leggi la chiave di 128 bit
        k = [int.from_bytes(key[j:j+4], 'little') for j in range(0, 16, 4)]
        
        # Ciclo di decifratura
        sum_value = (delta * num_rounds) & 0xFFFFFFFF
        for _ in range(num_rounds):
            v1 = (v1 - (((v0 << 4 ^ v0 >> 5) + v0) ^ (sum_value + k[1]))) & 0xFFFFFFFF
            sum_value = (sum_value - delta) & 0xFFFFFFFF
            v0 = (v0 - (((v1 << 4 ^ v1 >> 5) + v1) ^ (sum_value + k[0]))) & 0xFFFFFFFF
        
        # Scrivi i valori decifrati nel bytearray
        decrypted_data[i:i+4] = v0.to_bytes(4, 'little')
        decrypted_data[i+4:i+8] = v1.to_bytes(4, 'little')
    
    # Leggi il numero di byte di padding dal primo byte
    padding_size = decrypted_data[0]
    
    # Rimuovi il padding dal risultato finale
    decrypted_data = decrypted_data[padding_size:]
    
    return bytes(decrypted_data)

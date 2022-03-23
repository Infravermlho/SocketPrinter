from ursina import *
import socket


class SaveManager:
    def __init__(self, name="placeholder.3dm", tooltip="texto tooltip"):
        self.label = name
        self.tooltip = tooltip

    def save(self, datapack):
        linhas = ['{', f'label="{self.label}",', f'tooltip="{self.tooltip}",', 'shapes={']
        with open(f'Recursos/Saves/{self.label}', 'w') as f:
            f.write('\n'.join(linhas))

            for block in datapack:
                f.write('\n     {' f'{int(block.x * 2)},{int(block.y - 2) * 2},{int(block.z * 2)},{int(block.x * 2 + 4)},'
                        f'{int((block.y - 2) * 2 + 4)},{int(block.z * 2 + 4)},'
                        f'texture="{self.stringtreatment(str(block.texture))}"' + '},')

            f.writelines('\n  }')
            f.writelines('\n}')

    def stringtreatment(self, string):
        return f'wool_colored_{string.split("_")[0]}'

    def transfer(self, datapack):
        import socket

        HOST = ("127.0.0.1")
        PORT = 50343

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                conn.sendall(b'CONNECT:\n')

                conn.sendall(bytes(self.label, 'utf8'))
                conn.sendall(b'\n')
                conn.sendall(bytes(self.tooltip, 'utf8'))
                conn.sendall(b'\n')

                for block in datapack:
                    shape = f'{int(block.x * 2)},{int(block.y - 2) * 2},{int(block.z * 2)},{int(block.x * 2 + 4)},' \
                            f'{int((block.y - 2) * 2 + 4)},{int(block.z * 2 + 4)},' \
                            f'{self.stringtreatment(str(block.texture))}'
                    conn.sendall(bytes(shape, 'utf8'))
                    conn.sendall(b'\n')
                conn.sendall(b'END:')
                conn.sendall(b'\n')

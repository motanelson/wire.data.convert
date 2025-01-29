import struct
import os
import sys

class ISO9660Reader:
    SECTOR_SIZE = 2048

    def __init__(self, iso_path):
        self.iso_path = iso_path
        self.current_dir_sector = 17  # Diretório raiz padrão
        self.current_path = '/'
        self.iso_file = None
        
        try:
            self.iso_file = open(iso_path, "rb")
            print(f"ISO '{iso_path}' aberto com sucesso.")
        except FileNotFoundError:
            print(f"Erro: Arquivo {iso_path} não encontrado.")
            sys.exit(1)

    def read_sector(self, sector_number):
        self.iso_file.seek(sector_number * self.SECTOR_SIZE)
        return self.iso_file.read(self.SECTOR_SIZE)

    def list_directory(self):
        sector_data = self.read_sector(self.current_dir_sector)
        index = 0

        print("Conteúdo do diretório:")
        while index < len(sector_data):
            record_length = sector_data[index]
            if record_length == 0:
                break

            name_length = sector_data[index + 32]
            name = sector_data[index + 33:index + 33 + name_length].decode('ascii')

            # Ignorar diretórios "." e ".." para saída mais clara
            if name not in ['.', '..']:
                print(name)

            index += record_length

    def read_file(self, filename):
        sector_data = self.read_sector(self.current_dir_sector)
        index = 0

        while index < len(sector_data):
            record_length = sector_data[index]
            if record_length == 0:
                break

            name_length = sector_data[index + 32]
            name = sector_data[index + 33:index + 33 + name_length].decode('ascii')
            
            if name == filename:
                start_sector = struct.unpack('<I', sector_data[index + 2:index + 6])[0]
                size = struct.unpack('<I', sector_data[index + 10:index + 14])[0]

                file_data = self.read_sector(start_sector)[:size]
                print(file_data.decode('ascii'))
                return

            index += record_length

        print(f"Erro: Arquivo '{filename}' não encontrado.")

    def change_directory(self, dirname):
        if dirname == '..':
            print("Voltar ao diretório raiz")
            self.current_dir_sector = 17
            self.current_path = '/'
            return

        sector_data = self.read_sector(self.current_dir_sector)
        index = 0

        while index < len(sector_data):
            record_length = sector_data[index]
            if record_length == 0:
                break

            name_length = sector_data[index + 32]
            name = sector_data[index + 33:index + 33 + name_length].decode('ascii')

            if name == dirname:
                start_sector = struct.unpack('<I', sector_data[index + 2:index + 6])[0]
                print(f"Mudando para o diretório '{dirname}'")
                self.current_dir_sector = start_sector
                self.current_path = os.path.join(self.current_path, dirname)
                return

            index += record_length

        print(f"Erro: Diretório '{dirname}' não encontrado.")

    def close(self):
        if self.iso_file:
            self.iso_file.close()


def main():
    iso_path = input("Digite o caminho do arquivo ISO: ")
    reader = ISO9660Reader(iso_path)

    while True:
        command = input(f"{reader.current_path}> ").strip()

        if command == "exit":
            reader.close()
            print("Saindo do programa.")
            break
        elif command == "ls":
            reader.list_directory()
        elif command.startswith("cat"):
            parts = command.split(maxsplit=1)
            if len(parts) == 2:
                reader.read_file(parts[1])
            else:
                print("Uso: cat <nome_arquivo>")
        elif command.startswith("cd"):
            parts = command.split(maxsplit=1)
            if len(parts) == 2:
                reader.change_directory(parts[1])
            else:
                print("Uso: cd <nome_diretorio>")
        else:
            print("Comando desconhecido. Comandos disponíveis: ls, cat, cd, exit")

if __name__ == "__main__":
    print("\033c\033[43;30m\n")
    main()


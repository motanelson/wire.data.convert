import os
import shutil
import struct
import datetime
import sys

class ISOExtractor:
    SECTOR_SIZE = 2048

    def __init__(self, iso_path):
        self.iso_path = iso_path
        self.iso_file = None
        self.target_directory="./tmp/"
        self.current_dir_sector = 17  # Diretório raiz padrão
        self.current_path = '/'
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
    
    def open_iso(self):
        try:
            self.iso_file = open(self.iso_path, "rb")
            print(f"ISO '{self.iso_path}' aberto com sucesso.")
        except FileNotFoundError:
            print(f"Erro: Arquivo {self.iso_path} não encontrado.")
            sys.exit(1)

    def read_sector(self, sector_number):
        self.iso_file.seek(sector_number * self.SECTOR_SIZE)
        return self.iso_file.read(self.SECTOR_SIZE)
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
                f1=open(self.target_directory+filename,"w")
                f1.write(file_data.decode('ascii'))
                f1.close()
                return

            index += record_length

        print(f"Erro: Arquivo '{filename}' não encontrado.")
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
                self.read_file(name)

            index += record_length

    def extract_all(self, target_directory):
        print(f"Extraindo conteúdo para: {target_directory}")
        self.iso_file.seek(0, os.SEEK_END)
        total_size = self.iso_file.tell()
        total_sectors = total_size // self.SECTOR_SIZE

        os.makedirs(target_directory, exist_ok=True)
        
        self.list_directory()
        print("Extração completa.")

    def close_iso(self):
        if self.iso_file:
            self.iso_file.close()


def generate_temp_directory():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    temp_dir = os.path.join("/tmp", timestamp)
    return temp_dir


def execute_start_script(directory):
    start_script_path = directory
    if os.path.exists(start_script_path):
        print("Executando start.py...\n")
        os.system(f"python3 {start_script_path}")
    else:
        print("Erro: start.py não encontrado no diretório temporário.")


def cleanup_directory(directory):
    print(f"Removendo diretório temporário: {directory}")
    shutil.rmtree(directory, ignore_errors=True)


def main():
    iso_path = input("Digite o caminho da ISO a executar: ").strip()
    if not os.path.isfile(iso_path):
        print("Erro: Arquivo ISO não encontrado.")
        return

    temp_directory = "./tmp"

    try:
        # Abre e extrai o conteúdo da ISO
        extractor = ISOExtractor(iso_path)
        extractor.open_iso()
        extractor.extract_all(temp_directory)
        extractor.close_iso()

        # Executa o start.py dentro do diretório temporário
        execute_start_script(temp_directory+"/start.py")
        print(temp_directory+"/start.py")
    
    finally:
        # Limpa o diretório temporário
        print("")
        #cleanup_directory(temp_directory)

    print("Programa encerrado.")


if __name__ == "__main__":
    print("\033c\033[43;30m\n")
    main()


class TextFileManager:
    def write_text_to_file(self, text, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)

    def read_text_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

import os


def text_to_bits(text):
    return ''.join(format(ord(char), '08b') for char in text)
def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])
def embed_message(container_text, message):
    bits = text_to_bits(message)
    sentences = container_text.split('. ')
    new_text = []
    bit_index = 0

    for sentence in sentences:
        sentence = sentence.rstrip()
        if bit_index < len(bits):
            if bits[bit_index] == '0':
                sentence += ' '
            else:
                sentence += '  '
            bit_index += 1
        new_text.append(sentence)

    return '. '.join(new_text), bit_index
def extract_message(stego_text, bit_length):
    sentences = stego_text.split('. ')
    bits = []

    for sentence in sentences:
        if sentence.endswith('  '):
            bits.append('1')
        elif sentence.endswith(' '):
            bits.append('0')
        if len(bits) >= bit_length:
            break

    return bits_to_text(''.join(bits))

def save_to_file(file_name, content):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)
def read_from_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()
def calculate_text_weight(file_name):
    content = read_from_file(file_name)
    weight_in_bits = len(content) * 8
    return weight_in_bits


container_file = 'F:\\Учёба\\4 курс\\Стеганография\\Лаб1\\Программа\\lab1_stegan\\txt\\container.txt'  # Файл-контейнер
message_file = 'F:\\Учёба\\4 курс\\Стеганография\\Лаб1\\Программа\\lab1_stegan\\txt\\secret.txt'      # Файл-сообщение
secret = 'F:\\Учёба\\4 курс\\Стеганография\\Лаб1\\Программа\\lab1_stegan\\txt\\output.txt'      # Файл-сообщение

with open(secret, 'r+') as f:
    f.truncate(0)  # Ассоциация – "щелчок Таноса" потому что всё содержимое файла исчезает!

container_text = read_from_file(container_file)

message = read_from_file(message_file)

stego_text, inserted_bits = embed_message(container_text, message)
print(f'Внедрено бит: {inserted_bits}')


output_file = 'F:\\Учёба\\4 курс\\Стеганография\\Лаб1\\Программа\\lab1_stegan\\txt\\output.txt'
save_to_file(output_file, stego_text)
print(f"Изменённый контейнер сохранён в {output_file}")

retrieved_message = extract_message(stego_text, len(text_to_bits(message)))
print(f'Извлечённое сообщение: {retrieved_message}')
print(f'Кол-во бит в изначальном сообщении: {calculate_text_weight(container_file)}')
print(f'Кол-во бит в итоговом сообщении: {calculate_text_weight(secret)}')


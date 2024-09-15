import json
import hashlib

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from dataclasses import dataclass


@dataclass
class EncrypterArgs:
    pic_name: str
    debug: bool


class HideousEncrypter:
    def __init__(self, args: EncrypterArgs):
        self.debug = args.debug

        self.original_file = './original/' + args.pic_name
        self.extended_file = './encoded/extended_' + args.pic_name
        self.encoded_file = './encoded/encoded_' + args.pic_name
        self.decoded_file = './decoded/decoded_' + args.pic_name
        self.dict_file = './decoded/dict.txt'

    def extend(self):
        extended, dict = [], []

        with open(self.original_file, 'rb') as file:
            data = file.read()
            for b in range(0, 256):
                dict.append([b] + [0] * 15)

            for b in data:
                extended.append([b] + [0] * 15)

        with open(self.extended_file, 'wb') as file:
            for b in dict:
                file.write(bytes(b))
            for b in extended:
                file.write(bytes(b))

    def encode(self):
        blocks, output = [], []

        with open(self.extended_file, 'rb') as file:
            data = file.read()

        i, j = 0, 16
        for _ in range(int(len(data) / 16)):
            blocks.append(data[i:j])
            i += 16
            j += 16

        key = hashlib.sha256(get_random_bytes(16)).digest()
        cipher = AES.new(key, AES.MODE_ECB)
        for block in blocks:
            output.append(cipher.encrypt(bytes(block)))

        with open(self.encoded_file, 'wb') as file:
            for byte in output:
                file.write(byte)

    def translate(self):
        blocks, dict_encoded, translation = [], [], []
        with open(self.encoded_file, 'rb') as f:
            data = f.read()

        dict = data[:4096]
        for b in dict:
            dict_encoded.append(b)

        i, j = 0, 16
        dict_len = int(len(dict_encoded) / 16)
        for _ in range(dict_len):
            blocks.append(dict_encoded[i:j])
            i += 16
            j += 16

        for b in range(0, 256):
            print(b, ' : ', blocks[b])
            translation.append((blocks[b], b))

        with open(self.dict_file, 'w') as f:
            json.dump(translation, f)

    def decode(self):
        output = []

        with open(self.dict_file, 'r') as f:
            dict = json.load(f)

        with open(self.encoded_file, 'rb') as f:
            data = f.read()
            data_bytes, data_blocks = [], []
            for k in data[4096:]:
                data_bytes.append(k)

            i, j = 0, 16
            data_len = int(len(data_bytes) / 16)
            for _ in range(data_len):
                data_blocks.append(data_bytes[i:j])
                i += 16
                j += 16

        for data_block in data_blocks:
            for dict_block in dict:
                if data_block == dict_block[0]:
                    output.append(dict_block[1])

        with open(self.decoded_file, 'wb') as f:
            for j in output:
                result = self.num_2_hex(j)
                if result != 0:
                    if len(result) % 2 == 0:
                        f.write(bytes.fromhex(result))
                    else:
                        result = '0' + result
                        f.write(bytes.fromhex(result))
                else:
                    f.write(bytes(0))

    def num_2_hex(self, num):
        if isinstance(num, str):
            number = int(num, 10)
        else:
            number = int(num)
        symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if number < 16:
            return symbols[number]
        else:
            return self.num_2_hex(number // 16) + symbols[number % 16]
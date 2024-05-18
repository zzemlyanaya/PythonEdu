import sys
from typing import List

"""
Constants
"""
BYTE = 1
WORD = 4
BE_FORMAT = '032b'
HEX8_FORMAT = '08x'
BIN8_FORMAT = '08b'
REG_COUNT = 32
DATA_MEM_SIZE = 64 * 1024
DATA_START_ADDRESS = 0x10000000

R_TYPE = 'R_TYPE'
I_TYPES = 'I_TYPES'
I_TYPE_ARITHMETIC = 'I_TYPE_ARITHMETIC'
I_TYPE_LOAD = 'I_TYPE_LOAD'
I_TYPE_JALR = 'I_TYPE_JALR'
S_TYPE = 'S_TYPE'
SB_TYPE = 'SB_TYPE'
U_TYPES = 'U_TYPES'
U_TYPE_LUI = 'U_TYPE_LUI'
U_TYPE_AUIPC = 'U_TYPE_AUIPC'
UJ_TYPE = 'UJ_TYPE'

opcodes = {
    R_TYPE: {'0110011'},
    I_TYPES: {'0010011', '0000011', '1100111'},
    I_TYPE_ARITHMETIC: {'0010011'},
    I_TYPE_LOAD: {'0000011'},
    I_TYPE_JALR: {'1100111'},
    S_TYPE: {'0100011'},
    SB_TYPE: {'1100011'},
    U_TYPES: {'0110111', '0010111'},
    U_TYPE_LUI: {'0110111'},
    U_TYPE_AUIPC: {'0010111'},
    UJ_TYPE: {'1101111'}
}

"""
RISCV32Simulator: simulate RISC-V instructions execution
"""


class RISCV32Simulator:
    def __init__(self):
        self.assembly_instructions = []
        self.registers = [0 for _ in range(REG_COUNT)]
        self.data_mem = ['11111111' for _ in range(DATA_MEM_SIZE)]
        self.PC = 0

    def __str__(self):
        return '\n'.join([
            'x' + str(i) + ': 0x' + format((self.registers[i] & ((1 << 32) - 1)), HEX8_FORMAT)
            for i in range(32)
        ])

    def read_data(self, filename: str):
        data = []
        with open(filename, 'rb') as f:
            while True:
                byte = f.read(BYTE)
                if not byte:
                    break

                ascii_value = ord(byte)
                bin_value = format(ascii_value, BIN8_FORMAT)
                data.append(bin_value)

        self.data_mem[0:len(data)] = data

    def execute(self, bin_instructions: List[str], IC: int):
        for i in range(IC):
            if self.PC >= len(bin_instructions):
                break
            self.execute_bin(bin_instructions[int(self.PC)])

    def execute_bin(self, bits: str):
        opcode = bits[25:32]

        if opcode in opcodes[R_TYPE]:
            funct7 = bits[0:7]
            rs2 = bits[7:12]
            rs1 = bits[12:17]
            funct3 = bits[17:20]
            rd = bits[20:25]

            if funct3 == '000' and funct7 == '0000000':
                self.write_reg(rd, self.read_reg(rs1) + self.read_reg(rs2))
                self.PC += 1
            elif funct3 == "000" and funct7 == '0100000':
                self.write_reg(rd, self.read_reg(rs1) - self.read_reg(rs2))
                self.PC += 1
            elif funct3 == '001' and funct7 == '0000000':
                self.write_reg(rd, self.read_reg(rs1) << (self.read_reg(rs2) & 0b11111))
                self.PC += 1
            elif funct3 == '010' and funct7 == '0000000':
                if self.read_reg(rs1) < self.read_reg(rs2):
                    self.write_reg(rd, 1)
                else:
                    self.write_reg(rd, 0)
                self.PC += 1
            elif funct3 == "100" and funct7 == '0000000':
                self.write_reg(rd, self.read_reg(rs1) ^ self.read_reg(rs2))
                self.PC += 1
            elif funct3 == '101' and funct7 == '0000000':
                if self.read_reg(rs2) == 0:
                    self.write_reg(rd, self.read_reg(rs1))
                else:
                    self.write_reg(rd, (self.read_reg(rs1) & 0xFFFFFFFF) >> (self.read_reg(rs2) & 0b11111))
                self.PC += 1
            elif funct3 == '101' and funct7 == '0100000':
                self.write_reg(rd, self.read_reg(rs1) >> (self.read_reg(rs2) & 0b11111))
                self.PC += 1
            elif funct3 == '110' and funct7 == '0000000':
                self.write_reg(rd, self.read_reg(rs1) | self.read_reg(rs2))
                self.PC += 1
            elif funct3 == '111' and funct7 == '0000000':
                self.write_reg(rd, self.read_reg(rs1) & self.read_reg(rs2))
                self.PC += 1

        elif opcode in opcodes[I_TYPES]:
            imm = bits[0:12]
            rs1 = bits[12:17]
            funct3 = bits[17:20]
            rd = bits[20:25]

            if opcode in opcodes[I_TYPE_ARITHMETIC]:
                if funct3 == '000':
                    self.write_reg(rd, self.read_reg(rs1) + self.imm2dec(imm))
                    self.PC += 1
                elif funct3 == '010':
                    if self.read_reg(rs1) < self.imm2dec(imm):
                        self.write_reg(rd, 1)
                    else:
                        self.write_reg(rd, 0)
                    self.PC += 1
                elif funct3 == '100':
                    self.write_reg(rd, self.read_reg(rs1) ^ self.imm2dec(imm))
                    self.PC += 1
                elif funct3 == '110':
                    self.write_reg(rd, self.read_reg(rs1) | self.imm2dec(imm))
                    self.PC += 1
                elif funct3 == '111':
                    self.write_reg(rd, self.read_reg(rs1) & self.imm2dec(imm))
                    self.PC += 1
                elif funct3 == '001' and imm[0:7] == '0000000':
                    self.write_reg(rd, self.read_reg(rs1) << (self.imm2dec(imm) & 0b11111))
                    self.PC += 1
                elif funct3 == "101" and imm[0:7] == '0000000':
                    if self.imm2dec(imm) == 0:
                        self.write_reg(rd, self.read_reg(rs1))
                    else:
                        self.write_reg(rd, (self.read_reg(rs1) & 0xFFFFFFFF) >> (self.imm2dec(imm) & 0b11111))
                    self.PC += 1
                elif funct3 == '101' and imm[0:7] == '0100000':
                    self.write_reg(rd, self.read_reg(rs1) >> (self.imm2dec(imm) & 0b11111))
                    self.PC += 1

            elif opcode in opcodes[I_TYPE_LOAD]:
                if funct3 == '010':
                    if self.get_address(rs1, self.imm2dec(imm)) == 0x20000000:
                        user_input = int(input())
                        self.write_reg(rd, user_input)
                    else:
                        self.write_reg(rd, self.read_memory(self.get_address(rs1, self.imm2dec(imm))))
                    self.PC += 1

            elif opcode in opcodes[I_TYPE_JALR] and funct3 == '000':
                self.write_reg(rd, self.PC * 4 + 4)
                self.PC = int((self.read_reg(rs1) + self.imm2dec(imm)) / 4)

        elif opcode in opcodes[S_TYPE]:
            imm = bits[0:7] + bits[20:25]
            rs2 = bits[7:12]
            rs1 = bits[12:17]
            funct3 = bits[17:20]

            if funct3 == '010':
                if self.get_address(rs1, self.imm2dec(imm)) == 0x20000000:
                    print(chr(self.read_reg(rs2)), end='')
                else:
                    self.write_memory(
                        self.get_address(rs1, self.imm2dec(imm)),
                        self.read_reg(rs2),
                    )
                self.PC += 1

        elif opcode in opcodes[SB_TYPE]:
            imm = bits[0] + bits[24] + bits[1:7] + bits[20:24] + '0'
            rs2 = bits[7:12]
            rs1 = bits[12:17]
            funct3 = bits[17:20]

            if funct3 == '000':
                if self.read_reg(rs1) == self.read_reg(rs2):
                    self.PC += int(self.imm2dec(imm) / 4)
                else:
                    self.PC += 1
            elif funct3 == '001':
                if self.read_reg(rs1) != self.read_reg(rs2):
                    self.PC += int(self.imm2dec(imm) / 4)
                else:
                    self.PC += 1
            elif funct3 == '100':
                if self.read_reg(rs1) < self.read_reg(rs2):
                    self.PC += int(self.imm2dec(imm) / 4)
                else:
                    self.PC += 1
            elif funct3 == '101':
                if self.read_reg(rs1) >= self.read_reg(rs2):
                    self.PC += int(self.imm2dec(imm) / 4)
                else:
                    self.PC += 1

        elif opcode in opcodes[U_TYPES]:
            imm = bits[0:20] + '000000000000'
            rd = bits[20:25]

            if opcode in opcodes[U_TYPE_LUI]:
                self.write_reg(rd, self.imm2dec(imm))
                self.PC += 1
            elif opcode in opcodes[U_TYPE_AUIPC]:
                self.write_reg(rd, (self.PC * 4) + (self.imm2dec(imm)))
                self.PC += 1

        elif opcode in opcodes[UJ_TYPE]:
            imm = (bits[0] + bits[12:20] + bits[11] + bits[1:11] + '0')
            rd = bits[20:25]
            self.write_reg(rd, self.PC * 4 + 4)
            self.PC += int(self.imm2dec(imm) / 4)

    def read_reg(self, reg: str) -> int:
        reg = int(reg, 2)
        if reg == 0:
            return 0
        else:
            return self.registers[reg]

    def write_reg(self, reg: str, value: int):
        reg = int(reg, 2)
        if reg != 0:
            self.registers[reg] = int(value)

    def get_address(self, rs1: str, imm: int) -> int:
        rs1 = int(rs1, 2)
        return self.registers[rs1] + imm

    def read_memory(self, address: int) -> int:
        address -= DATA_START_ADDRESS
        binary = ''
        for i in range(4):
            binary += self.data_mem[address + (3 - i)]
        return self.imm2dec(binary)

    def write_memory(self, address: int, decimal: int):
        address -= DATA_START_ADDRESS
        binary = format(decimal, BE_FORMAT)
        for i in range(4):
            self.data_mem[address + (3 - i)] = binary[8 * i: 8 * (i + 1)]

    def bin2hex(self, bits: str) -> str:
        return format(int(bits, 2), HEX8_FORMAT)

    def imm2dec(self, bits: str) -> int:
        if bits[0] == '1':
            return -(int(''.join(['1' if bit == '0' else '0' for bit in bits[1:]]), 2) + 1)
        else:
            return int(bits, 2)

    def int2hex(self, integer) -> str:
        if integer < 0:
            return format((1 << 32) + integer, HEX8_FORMAT)
        else:
            return format(integer, HEX8_FORMAT)

    def clear(self):
        self.assembly_instructions = []
        self.registers = []
        self.data_mem = []
        self.PC = 0


"""
Read file with binary code and split it into 32-bit instructions, each converted to BigEndian format
"""


def try_read_binary_instructions(filename: str):
    try:
        data = []
        with open(filename, 'rb') as f:
            while True:
                binary_le = f.read(WORD)
                if not binary_le:
                    break

                decimal = int.from_bytes(binary_le, byteorder='little', signed=False)
                binary_be = format(decimal, BE_FORMAT)
                data.append(binary_be)
        return data

    except Exception:
        return None


"""
Main: read data from binary file and use `RISCV32Simulator` to dissemble it
"""
if __name__ == "__main__":
    inst_file = sys.argv[1]
    if inst_file is None or inst_file == '':
        print('Error: no input file provided! Exiting...')
        sys.exit(1)

    bin_instr = try_read_binary_instructions(inst_file)
    if bin_instr is not None:
        simulator = RISCV32Simulator()

        IC = 0
        if len(sys.argv) == 3:
            IC = int(sys.argv[2])
        elif len(sys.argv) == 4:
            IC = int(sys.argv[3])
            data_file = sys.argv[2]
            if data_file is None or data_file == '':
                print('Error: incorrect data file provided! Exiting...')
                sys.exit(1)
            simulator.read_data(data_file)

        simulator.execute(bin_instr, IC)
        print(simulator)
        simulator.clear()
    else:
        print('Error: could not read binary data from file! Exiting...')

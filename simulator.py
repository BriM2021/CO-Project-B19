from sre_parse import FLAGS
import sys
def read_file():
	# x=input()
	# print(x)
	# return x.split("\n")
	# f=open("A.txt", "r")
	# list_file_line= f.readlines()
	# return list_file_line
	l=[]
	for line in sys.stdin:
		# print(line+"\n")
		if(line!="\n"):
			l.append(line)
	return l

opcode = {
'10000' : ['add', 'A'],
'10001' : ['sub', 'A'],
'10010' : ['mov', 'B'],
'10011' : ['mov', 'C'],
'10100' : ['ld', 'D'],
'10101': ['st', 'D'],
'10110': ['mul', 'A'],
'10111': ['div', 'C'],
'11000': ['rs','B'],
'11001': ['ls', 'B'],
'11010': ['xor', 'A'],
'11011': ['or', 'A'],
'11100': ['and', 'A'],
'11101': ['not', 'C'],
'11110': ['cmp', 'C'],
'11111': ['jmp', 'E'],
'01100': ['jlt', 'E'],
'01101': ['jgt', 'E'],
'01101': ['jgt', 'E'],
'01111': ['je', 'E'],
'01010': ['hlt',-1]
}

type_A=["add", "sub", "mul", "xor", "or", "and"]
type_B=["mov", "ls", "rs"]
type_C=["mov", "div", "not" , "cmp" ]
type_D=["ld", "st"]
type_E=["jmp","jlt", "jgt","je" ]
type_F=["hlt"]

unused_bit = {"A": 2, "B": 0, "C": 5, "D": 0, "E": 3, "F": 11}

#no. of registers, immediates
type_info = {
'type_A' : [3,0],
'type_B' : [1,1],
'type_C' : [2,0],
'type_D' : [1,0],
'type_E' : [0,0],
'type_F' : [-1,-1]
}

is_memory = { 'A':0, 'B':0,'C':0,'D':1,'E':1,'F':0 }
'''how many value entered per register :
A :4
B: 3
C:3
D:3
E:2
F:1'''

register_codes =  {
'R0' : '000',
'R1' : '001',
'R2' : '010',
'R3' : '011',
'R4' : '100',
'R5' : '101',
'R6' : '110',
'FLAGS' :'111' }

op_register_codes = {
 '000': 'R0' ,
'001':'R1',
'010':'R2' ,
'011':'R3' ,
'100':'R4' ,
'101':'R5',
'110':'R6' ,
'111':'FLAGS' 

}

register_values = {
'R0' : 0000000000000000,
'R1' : 0000000000000000,
'R2' : 0000000000000000,
'R3' : 0000000000000000,
'R4' : 0000000000000000,
'R5' : 0000000000000000,
'R6' : 0000000000000000
}

FLAG = ['0','0','0','0']

MEMORY_ADDRESS = '00000000'

#input the intruction :
#check the opcode, assign the type and process according to the type 
def extract_instruction(instruction):
#instruction is the text we get from readlines 
#instruct bceomes a list with all the different codes for the paritcular line this 

    instruct =[]
    types = opcode[instruction[0:4]][1]
    if types == "A":
    #assign the actual actution into instruct 
        action = opcode[instruction[0:4]][0]
        instruct = instruct + [instruction[7:10]] + [instruction[10:13]] + [instruction[13:16]]

    elif types == "B":
    #assign the actual actution into instruct 
        action = opcode[instruction[0:4]][0]
        instruct = instruct + [instruction[5:8]] + [instruction[8:16]] 

    elif types == "C":
    #assign the actual actution into instruct 
        action = opcode[instruction[0:4]][0]
        instruct = instruct + [instruction[10:13]] + [instruction[13:16]] 

    elif types == "D":
    #assign the actual actution into instruct 
        action = opcode[instruction[0:4]][0]
        instruct = instruct + [instruction[5:8]] + [instruction[8:16]] 

    elif types == "E":
    #assign the actual actution into instruct 
        action = opcode[instruction[0:4]][0]
        instruct = instruct + [instruction[5:8]] + [instruction[8:16]]

    elif types == "F":
    #assign the actual actution into instruct 
        action = opcode[instruction[0:4]][0]
        instruct = instruct + [instruction[5:16]] 

    return [ types, action, instruct ]

#Values of registers as we traverse the file


def binaryToDecimal(n):
    return int(n,2)

def decimal_to_binary_16bit(n):
    return 2


#make different functions to execute different functions 
#A

def A(action, register_2, register_3):
# type_A=["add", "sub", "mul", "xor", "or", "and"]
    if action == "add" :
        x = int(register_values[register_2]) + int(register_values[register_3])
        if x > pow(2,16)-1:
            y = decimal_to_binary_16bit(x)
            return [y,1]
        x = decimal_to_binary_16bit(x)
        return [x,0]

    if action == "sub" :
        x = int(register_values[register_2]) - int(register_values[register_3])
        if x < 0 :
            return [0000000000,1]
        x = decimal_to_binary_16bit(x)
        return x

    if action == "mul" :
        x = int(register_values[register_2]) * int(register_values[register_3])
        if x > pow(2,16)-1:
            y = decimal_to_binary_16bit(x)
            return [y,1]
        x = decimal_to_binary_16bit(x)
        return [x,0]

    if action == "xor" :
        x = register_values[register_2]^register_values[register_3]
        return x

    if action == "or" :
        x = register_values[register_2] | register_values[register_3]
        return x

    if action == "and" :
        x = register_values[register_2]&register_values[register_3]
        return x

#def B,C,D,E,F

def B(action, register, imm):
    if action == "mov":
        return imm
    if action == "rs":
        return register_values[register] >> imm
    if action == "rs":
        return register_values[register] << imm



#type_C=["mov", "div", "not" , "cmp" ]
def C(action, register_1, register_2 ):
    if action == "mov" :
        register_values[register_1] = register_values[register_2]
    if action == "div":
        r_2 = binaryToDecimal(register_values[register_2])
        r_1 = binaryToDecimal(register_values[register_1])
        quo = r_1//r_2
        register_values[register_1] = decimal_to_binary_16bit(quo)
        register_values[register_2] = decimal_to_binary_16bit(r_1%r_2)
    if action == "not":
        register_values[register_1] = ~register_2
    if action == "cmp":
        r_2 = binaryToDecimal(register_values[register_2])
        r_1 = binaryToDecimal(register_values[register_1])
        if r_1 > r_2:
            return 1
        else :
            return 0
    
#type_D=["ld", "st"]
def D(action, register_1, memory_ad):
    if action =="ld":
        register_values[register_1] = memory_ad
    if action == "st":
        MEMORY_ADDRESS = register_values[register_1]

#type_E=["jmp","jlt", "jgt","je" ]
def E(action, FLAG, memory_ad):
    if action == "jmp":
        MEMORY_ADDRESS = memory_ad
    if action =="jlt":
        if FLAG[1] == '1':
            MEMORY_ADDRESS = memory_ad
    if action == "jgt":
        if FLAG[2] == '1':
            MEMORY_ADDRESS = memory_ad
    if action == "je":
        if FLAG[3] == "1":
            MEMORY_ADDRESS = memory_ad

def F():
    h = 'halt'



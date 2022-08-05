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
'01010': ['hlt','F']
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

# register_codes =  {
# 'R0' : '000',
# 'R1' : '001',
# 'R2' : '010',
# 'R3' : '011',
# 'R4' : '100',
# 'R5' : '101',
# 'R6' : '110',
# 'FLAGS' :'111' }

# op_register_codes = {
#  '000': 'R0' ,
# '001':'R1',
# '010':'R2' ,
# '011':'R3' ,
# '100':'R4' ,
# '101':'R5',
# '110':'R6' ,
# '111':'FLAGS' 

# }

register_values = {
'000' : 0000000000000000, #R0
'001' : 0000000000000000, #R1
'010' : 0000000000000000, #R2
'011' : 0000000000000000, #R3
'100' : 0000000000000000, #R4
'101' : 0000000000000000, #R5
'110' : 0000000000000000, #R6
'111' : ['0','0','0','0'] #flag
}

PC_MEMORY_ADDRESS = '00000000'




#input the intruction :
#check the opcode, assign the type and process according to the type 
def extract_instruction(instruction):
#instruction is the text we get from readlines 
#instruct bceomes a list with all the different codes for the paritcular line this 

    instruct =[]
    dict = (opcode[instruction[0:5]])
    types = dict[1]
    action=""
    if types == "A":
    #assign the actual actution into instruct 
        action = opcode[instruction[0:5]][0]
        instruct = instruct + [instruction[7:10]] + [instruction[10:13]] + [instruction[13:16]]

    elif types == "B":
    #assign the actual actution into instruct 
        action = opcode[instruction[0:5]][0]
        instruct = instruct + [instruction[5:8]] + [instruction[8:16]] 

    elif types == "C":
    #assign the actual actution into instruct 
        action = opcode[instruction[0:5]][0]
        instruct = instruct + [instruction[10:13]] + [instruction[13:16]] 

    elif types == "D":
    #assign the actual actution into instruct 
        action = opcode[instruction[0:5]][0]
        instruct = instruct + [instruction[5:8]] + [instruction[8:16]] 

    elif types == "E":
    #assign the actual actution into instruct 
        action = opcode[instruction[0:5]][0]
        instruct = instruct + [instruction[8:16]]

    elif types == "F":
    #assign the actual actution into instruct 
        action = opcode[instruction[0:5]][0]
        instruct = instruct + [instruction[5:16]] 
    l=[]
    l.append(types)
    l.append(action)
    l.append(instruct)
    return l

#Values of registers as we traverse the file


def binaryToDecimal(n):
    x=int(n)
    ans=0
    i=0
    while(x>0):
        t=x%10
        ans+=t*pow(2, i)
        x=x//10
        i+=1
    return ans

def decimal_to_binary_16bit(decimal):
    binary = str(bin(decimal))[2:]
    if len(binary) > 16:
        return int(binary[-16:])
    else:
        return int('0'*(16-len(binary)) + binary)

def eightto16(a):
	return (16-len(a))*'0' + a
	
	


#make different functions to execute different functions 
#A

def A(action, register_2, register_3):
# type_A=["add", "sub", "mul", "xor", "or", "and"]
    if action == "add" :
        x = binaryToDecimal(register_values[register_2]) + (binaryToDecimal(register_values[register_3]))
        if x > pow(2,16)-1:
            y = decimal_to_binary_16bit(x)
            return [y,'1']
        x = decimal_to_binary_16bit(x)
        return [x,'0']

    if action == "sub" :
        x = binaryToDecimal(register_values[register_2]) - binaryToDecimal(register_values[register_3])
        if x < 0 :
            return [0000000000000000,'1']
        x = decimal_to_binary_16bit(x)
        return [x,'0']

    if action == "mul" :
        x = binaryToDecimal(register_values[register_2]) * binaryToDecimal(register_values[register_3])
        if x > pow(2,16)-1:
            y = decimal_to_binary_16bit(x)
            return [y,'1']
        x = decimal_to_binary_16bit(x)
        return [x,'0']

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
        register_values[register] = int(eightto16(imm))
    if action == "rs":
        t = binaryToDecimal(imm)
        if t >= 16 :
            convert = 0000000000000000
        else:
            convert = str(register_values[register])
            convert = convert[:-t]
            convert = "0"*(16-len(convert)) + (convert)
        
        register_values[register] = int(convert)
    if action == "ls":
        t = binaryToDecimal(imm)
        if t >= 16 :
            convert = 0000000000000000
        else:
            convert = "0"*(16-len(str(register_values[register]))) + str(register_values[register]) 
            convert = convert[t:]
            convert = convert + "0"*(16-len(convert))
        register_values[register] = int(convert)



#type_C=["mov", "div", "not" , "cmp" ]
def C(action, register_1, register_2 ):
    if action == "mov" :
        if register_2 == '111':
            x = '000000000000'

            for i in range(4):
                x += register_values[register_2][i]

            x = int(x)
            register_values[register_1] = x
            
        else :
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
            return '1'
        else :
            return '0'
    
#type_D=["ld", "st"]
def D(action, register_1, memory_ad):
    global PC_MEMORY_ADDRESS
    if action =="ld":
        register_values[register_1] = memory_ad
    if action == "st":
        PC_MEMORY_ADDRESS = register_values[register_1]

#type_E=["jmp","jlt", "jgt","je" ]
def E(action, memory_ad):
    global PC_MEMORY_ADDRESS
    global FLAG
    if action == "jmp":
        PC_MEMORY_ADDRESS = memory_ad
    if action =="jlt":
        if register_values['111'][1] == '1':  #flag == '1':
            PC_MEMORY_ADDRESS = memory_ad
    if action == "jgt":
        if register_values['111'][2] == '1': #flag
            PC_MEMORY_ADDRESS = memory_ad
    if action == "je":
        if register_values['111'][3] == '1': #flag
            PC_MEMORY_ADDRESS = memory_ad

def F():
    global halt 
    halt = 1
	
	
def PCupdate(x):
    new = bin(int(x, 2) + int('00000001', 2))
    new_1=new[2:]
    return "0"*(8-len(new_1)) + new_1



##############################################
#name = input()
# f = open(name, "r")
total_lines = read_file()
# print("DISDIOSH")
# print(total_lines)
# total_lines = f.readlines()
halt = 0

#reading the file - not done yet above is just a placeholder for the actual code   
#return [ types, action, instruct ]
memory_dump = []
for i in range(len(total_lines)):
    memory_dump.append(total_lines[i])

for i in range(256-len(total_lines)):
    memory_dump += ['0000000000000000']

count = []
cycle = 0

def PCdump():
    print( PC_MEMORY_ADDRESS, end = ' ')
    x = register_values.values()
    for i in x:
        print("0"*(16-len(str(i)))+str(i), end = ' ')
    print("")
		
	


while (halt == 0):
    # print("jksdfb\n")
    # print(PC_MEMORY_ADDRESS, "num\n" )
    # print(PC_MEMORY_ADDRESS)
    # print(binaryToDecimal(PC_MEMORY_ADDRESS))
    instruction = total_lines[binaryToDecimal(PC_MEMORY_ADDRESS)]
    info = extract_instruction(instruction)

    if info[0] == "A":
        if info[1] == 'add':
            check = A(info[1], info[2][1], info[2][2])
            if check[1] == "0":
                register_values[info[2][0]] = check[0]
            else :
                register_values['111'][0] = '1'#flag
                register_values['111'][1] = '0'#flag
                register_values['111'][2] = '0'
                register_values['111'][3] = '0'#flag

                register_values[info[2][0]] = check[0]
  


        if info[1] == "sub":
            check = A(info[1], info[2][1], info[2][2])
            if check[1] == '1':
                register_values[info[2][0]] = check[0]
                register_values['111'][0] = '1'#flag
                register_values['111'][1] = '0'#flag
                register_values['111'][2] = '0'
                register_values['111'][3] = '0'#flag
            else :
                register_values[info[2][0]] = check[0]



        if info[1] == 'mul':
            check = A(info[1], info[2][1], info[2][2])
            if check[1] == "0":
                register_values[info[2][0]] = check[0]
            else :
                register_values['111'][0] = '1'#flag
                register_values['111'][1] = '0'#flag
                register_values['111'][2] = '0'
                register_values['111'][3] = '0'#flag
                register_values[info[2][0]] = check[0]



        if info[1] == 'xor':
            register_values[info[2][0]] = A(info[1], info[2][1], info[2][2])

        if info[1] == 'or':
            register_values[info[2][0]] = A(info[1], info[2][1], info[2][2])

        if info[1] == 'and':
            register_values[info[2][0]] = A(info[1], info[2][1], info[2][2])

        cycle += 1
        count += [[cycle,PC_MEMORY_ADDRESS]]
    
    if info[0] == 'B':
        B(info[1], info[2][0], (info[2][1]))

        cycle += 1
        count += [[cycle,PC_MEMORY_ADDRESS]]

    if info[0] == 'C':
        if info[2] == "cmp ":
            check = C(info[1], info[2][0], info[2][1])
            if check == '1':
                register_values['111'][0] = '0'#flag
                register_values['111'][1] = '0'#flag
                register_values['111'][2] = '1'
                register_values['111'][3] = '0'#flag
                
        else :
            C(info[1], info[2][0], info[2][1])

        cycle += 1
        count += [[cycle,PC_MEMORY_ADDRESS]]


    if info[0] == 'D':
        D(info[1], info[2][0], info[2][1])
        cycle += 1
        count += [[cycle,PC_MEMORY_ADDRESS]]
    
    if info[0] == 'E':
        E(info[1], info[2][0])
        cycle += 1
        count += [[cycle,PC_MEMORY_ADDRESS]]
    
    if info[0] =='F':
        halt = 1
        cycle += 1
        count += [[cycle,PC_MEMORY_ADDRESS]]
        PCdump()	
        PC_MEMORY_ADDRESS = PCupdate(PC_MEMORY_ADDRESS)
        # print(PC_MEMORY_ADDRESS)
        break
    PCdump()	
    PC_MEMORY_ADDRESS = PCupdate(PC_MEMORY_ADDRESS)

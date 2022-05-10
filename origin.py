#Global Declarations
intbox = {}
floatbox = {}
stringbox = {}
functionsbox = {}
loopsbox = {}
conditionsbox = {}
controlstatementsbox = {"if":"if(" ,"if(":"if(" ,"if (":"if(" ,"elif ":"else if(" ,"elif(":"else if(", "elif (":"else if(", "else":"else", "while ":"while(", "while(":"While(","while (":"while(", "for ":"for("}
pyinputcode = []
pre_space_count = 0
bracescount = 1
coutputcode = ['#include<stdio.h>', '#include<conio.h>', '#include<stdlib.h>',"","int main()","{"]
functions_container = []
functions_container1 = []
operators = ["+","-","*","/","%"]

# Function to Convert Print Statements
def printstatements(linecode,functions_flag):
    linecode = linecode.strip()
    no_quotes = linecode.count('''"''')
    statements = []
    linecode1 = '''printf("'''

    #If Output statements in the print statement
    if(no_quotes != 0):
        while('''"''' in linecode):
            quotes_place = linecode.find('''"''')
            quotes_place2 = linecode[quotes_place + 1:].find('''"''') + 1 +quotes_place
            statements.append(linecode[quotes_place + 1:quotes_place2])
            linecode = linecode[:quotes_place] + linecode[quotes_place2 + 1:]
        if(linecode.strip().startswith("print(")):
            linecode = linecode.replace("print(",'')
        else:
            linecode = linecode.replace("print (",'')
        linecode = linecode.replace(")",'')
        variable = linecode.split(",")
        ind = 0 
        for i in variable:
            if(i == ''):
                linecode1 += statements[ind]
                ind += 1 
            else:
                if(i in intbox):
                    linecode1 += "%d "
                elif(i in floatbox):
                    linecode1 += "%f "
                elif(i+"[100]" in stringbox):
                    linecode1 += "%s "
                elif('+' in i or '-' in i or '*' in i or '/' in i or '%' in i):
                    for j in operators:
                        if(j in i):
                            operator = j 
                    variables = i.split(operator)
                    
                    if(((variables in intbox) and (variables not in floatbox)) and ("." not in variables)):
                        linecode1 += "%d "
                    elif((variables in floatbox) or "." in variables):
                        linecode1 += "%f "
                    elif((variables+"[100]" in stringbox and variables not in floatbox and variables not in intbox) or '''"''' in i):
                        linecode1 += "%s "
                    else:
                        linecode1 += "%d "
            
        linecode1 += '''"'''
        for i in variable:
            if(i == ''):
                variable.remove(i)
        if(len(variable) != 0):
            linecode1 += ","
            for i in variable:
                linecode1 += i 
                if(variable.index(i) != len(variable) - 1):
                    linecode1 += ","
    
    #If only variables
    else:
        if(linecode.strip().startswith("print(")):
            linecode = linecode.replace("print(",'')
        else:
            linecode = linecode.replace("print (",'')
        linecode = linecode.replace(")",'')
        variable = linecode.split(",")
        for i in variable:
            if(i in intbox):
                linecode1 += "%d "
            elif(i in floatbox):
                linecode1 += "%f "
            elif(i+"[100]" in stringbox):
                linecode1 += "%s "
            elif('+' in i or '-' in i or '*' in i or '/' in i or '%' in i):
                variables1 = []
                variables1.append(i)
                for j in operators:
                    for k in range(len(variables1)):
                        if(j in variables1[k]):
                            variables2 = variables1[k].split(j)
                            variables1.remove(variables1[k])
                            for m in variables2:
                                variables1.append(m)
                
                if(all(var.strip() not in floatbox for var in variables1) and all('.' not in var for var in variables1) and all('''"''' not in var for var in variables1)):
                    linecode1 += "%d "
                elif(all(var.strip() not in intbox for var in variables1) and all('''"''' not in var for var in variables1)):
                    linecode1 += "%f "
                elif((all(var.strip() not in intbox for var in variables1) and all(var.strip() not in floatbox for var in variables1))):
                    linecode1 += "%s "
                else:
                    linecode1 += "%d "

        linecode1 += '''",'''
        for i in variable:
            linecode1 += i 
            if(variable.index(i) != len(variable) - 1):
                linecode1 += ","
                
    linecode1 += ")"
    if(functions_flag):
        functions_container1.append(linecode1)
    else:
        coutputcode.append(linecode1)        

# Function to Convert Input Statements
def inputfunctions(linecode,functions_flag):
    thesplit = linecode.split('=')
    variables = thesplit[0].split(',')
    prompts = thesplit[1].split("),") 
    
    for i in range(len(variables)):
        declaration = variables[i].strip()
        
        #For input statements with prompts
        if ('''input("''' in prompts[i]):
            linecode1 = '''printf('''
            quotesplace = prompts[i].index('''"''')
            try:
                bracketplace = prompts[i].index(")")
            except:
                bracketplace = len(prompts[i])
            linecode1 += prompts[i][quotesplace:bracketplace] + ")"
            coutputcode.append(linecode1)

            if (prompts[i].strip().startswith("int")):
                linecode = '''scanf("%d",&''' + variables[i].strip() + ")"
                intbox[declaration] = "User"
    
            elif (prompts[i].strip().startswith("float")):
                linecode = '''scanf("%f",&''' + variables[i].strip() + ")"
                floatbox[declaration] = "User"
    
            else:
                linecode = '''scanf("%s",''' + variables[i].strip() + ")"
                declaration += "[100]"
                stringbox[declaration] = "User"
        
        #Input Statements without Prompts
        else:

            if (prompts[i].strip().startswith("int")):
                linecode = '''scanf("%d",&''' + variables[i].strip() + ")"
                intbox[declaration] = "User"
         
            elif (prompts[i].strip().startswith("float")):
                linecode = '''scanf("%f",&''' + variables[i] + ")"
                floatbox[declaration] = "User"
    
            else:
                linecode = '''scanf("%s",''' + variables[i] + ")"
                declaration += "[100]"
                stringbox[declaration] = "User"
        if(functions_flag):
            functions_container1.append(linecode)
        else:
            coutputcode.append(linecode)

# Converting Comment lines
def commentsfunction(linecode,functions_flag):
    linecode = str(linecode)
    linecode = linecode.replace("#", "//")
    if(functions_flag):
        functions_container1.append(linecode)
    else:
        coutputcode.append(linecode)

# Declaring expressions variables
def expressionsfunction(linecode,functions_flag):
    expressionsplit = linecode.split("=")
    variables = expressionsplit[0].split(",")
    declarations = expressionsplit[1].split(",")
    
    for i in range(len(variables)):
        declaration = variables[i].strip()

        #Normal Declarations without any Expressions in the Declaration
        if('+' not in declarations[i] and '-' not in declarations[i] and '*' not in declarations[i] and '/' not in declarations[i] and '%' not in declarations[i]):
            if ("." not in declarations[i] and '''"''' not in declarations[i]):
                if(variables[i].strip() not in intbox):
                    intbox[declaration] = declarations[i].strip()
            elif ("." in declarations[i] and '''"''' not in declarations[i]):
                if(variables[i].strip() not in floatbox):
                    floatbox[declaration] = declarations[i].strip()
                    if(declaration in intbox):
                        del intbox[declaration]
            elif ('''"''' in declarations[i]):
                if(variables[i]+"[100]".strip() not in stringbox):
                    declaration += "[100]"
                    stringbox[declaration] = declarations[i].strip()
                linecode = variables[i].strip() + "[100] = " + declarations[i].strip()
        
        #Declaration Statements without Expressions in it
        else:
            variables1 = []
            variables1.append(declarations[i])
            for j in operators:
                for k in range(len(variables1)):
                    if(j in variables1[k]):
                        variables2 = variables1[k].split(j)
                        variables1.remove(variables1[k])
                        for m in variables2:
                            variables1.append(m)
            if(all(var.strip() not in floatbox for var in variables1) and all('.' not in var for var in variables1) and all('''"''' not in var for var in variables1)):
                if(variables[i].strip() not in intbox):
                    intbox[declaration] = declarations[i].strip()
            elif(all(var.strip() not in intbox for var in variables1) and all('''"''' not in var for var in variables1)):
                if(variables[i].strip() not in floatbox):
                    floatbox[declaration] = declarations[i].strip()
                    if(declaration in intbox):
                        del intbox[declaration]
            elif((all(var.strip() not in intbox for var in variables1) and all(var.strip() not in floatbox for var in variables1))):
                if(variables[i]+"[100]".strip() not in stringbox):
                    declaration += "[100]"
                    stringbox[declaration] = declarations[i].strip()
                linecode = variables[i].strip() + "[100] = " + declarations[i].strip()
        if(functions_flag):
            functions_container1.append(linecode)
        else:
            coutputcode.append(linecode)


#Control Statements
def controlstatements(linecode,functions_flag):
    linecode = linecode.strip()
    linecode = linecode[:len(linecode) - 1]

    if('''"''' not in linecode):
        if("and" in linecode):
            linecode = linecode.replace("and","&&")
        elif("or" in linecode):
            linecode = linecode.replace("||","or")
        elif("not" in linecode):
            linecode.replace("!","not")
    #For if statements without parenthesis
    if(not linecode.strip().startswith("if(") and not linecode.strip().startswith("if (") and not linecode.strip().startswith("for ") and not linecode.strip().startswith("elif") and not linecode.strip().startswith("while")):
        try:
            space_index = linecode.strip().index(' ')
            linecode1 = "if("
        
            linecode = linecode1 + linecode[space_index + 1:]
        except:
            linecode = linecode
        
        linecode += ')'
    
    if(linecode.strip().startswith("else")):
        linecode = linecode.replace(')','')

    elif(linecode.strip().startswith("elif(") or linecode.strip().startswith("elif (")):
        bracket = linecode.find("(")
        linecode = "else if" + linecode[bracket:]

    elif(linecode.strip().startswith("for ")):
        fors = linecode.split()
        variable = str(fors[1])

        #If range functions is used
        if("range(" in linecode or "range (" in linecode):
            intbox[variable] = variable.strip()
            bracket = linecode.find("(")
            bracketc = linecode.find(")")
            range1 = linecode[bracket + 1:bracketc].split(',')
            initialize = str(range1[0])
            endval = str(range1[1])
            if(len(range1) == 2):
                stepval = '1'
            else:
                stepval = str(range1[2])
                if('-' in stepval):
                    minus = stepval.find("-")
                    stepval = stepval[minus + 1:]
            
            linecode = "for(" + variable +" = " + initialize + "; " + variable 
            if(initialize < endval):
                linecode += " < " + endval + "; " + variable + " += " + stepval + ")"

            else:
                linecode += " > " + endval + "; " + variable + " -= " + stepval + ")"
    if(functions_flag):
        functions_container1.append(linecode)
    else:        
        coutputcode.append(linecode)
    
def origin(datas,functions_flag):
    global coutputcode
    global bracescount
    global pre_space_count
    inside_function = 0

    #Takes each line in the Intput
    for linecode in datas:
        
        #Automatic Curly Braces Function
        curr_space_count = 0
        for spaces in linecode:
            if(spaces != ' '):
                break
            elif(spaces == ' ' or spaces == '\t'):
                curr_space_count +=1
        if(pre_space_count > curr_space_count):
            if(not inside_function):
                if(functions_flag):
                    functions_container1.append('}')
                else:
                    coutputcode.append('}')
            else:
                inside_function = 0
            bracescount += 1
        elif(pre_space_count < curr_space_count):
            if(not inside_function):
                if(functions_flag):
                    functions_container1.append('{')
                else:
                    coutputcode.append('{')
            bracescount += 1
        pre_space_count = curr_space_count
        #print(inside_function)
        if(inside_function):
            functions_container.append(linecode)
            continue

        # Converts print statement
        if (linecode.strip().startswith("print(") or linecode.strip().startswith("print (")):
            printstatements(linecode,functions_flag)

        # For input statement
        elif ("input" in linecode):
            sides = linecode.split("=")
            sides[1] = sides[1].strip()
            if(sides[1].strip().startswith('''"''')):
                expressionsfunction(linecode,functions_flag)
            else:
                inputfunctions(linecode,functions_flag)

        # For Comment lines
        elif (linecode.strip().startswith('#')):
            commentsfunction(linecode,functions_flag)
        
        elif(linecode.strip().startswith("if(") or linecode.strip().startswith("if (") or linecode.strip().startswith("if ") or linecode.strip().startswith("elif(") or linecode.strip().startswith("elif (") or linecode.strip().startswith("elif ") or linecode.strip().startswith("while(") or linecode.strip().startswith("while (") or linecode.strip().startswith("while ") or linecode.strip().startswith("for ")):
            controlstatements(linecode,functions_flag)
        
        elif((linecode.strip().startswith("else") or linecode.strip().startswith("else ")) and "=" not in linecode):
            controlstatements(linecode,functions_flag)

        elif(linecode.strip().startswith("def ") and not functions_flag):
            function_parts = linecode.strip().split()
            functionsbox[function_parts[1]] = "User - Defined"
            functions_container.append(linecode)
            inside_function = 1

        elif(linecode.strip().startswith("def ") and functions_flag):
            linecode = linecode.replace("def ","void ")
            functions_container1.append(linecode[:len(linecode) - 1])

        # For others
        else:
            equals = linecode.find("=")
            if ("=" in linecode and linecode[equals - 1] not in operators):
                expressionsfunction(linecode,functions_flag)
            else:
                coutputcode.append(linecode)
        
    # Appending the last Closing Curly Brace for main() function
    if(bracescount % 2 == 1):
        if(functions_flag):
            functions_container1.append('}')
            bracescount += 1
        else:
            coutputcode.append('}')
            bracescount += 1

print("\t\t\t\t\tPython to C Converter")
print("\nPaste your Python Program here: ")

# Getting Multi-line inputs
while True:
    line = input()
    if line:
        pyinputcode.append(line)
    else:
        break
origin(pyinputcode,0)

if(len(functions_container)):
    origin(functions_container,1)

if(len(functions_container1)):
    ind = coutputcode.index("") + 1
    ind2 = 0
    for statements in functions_container1:
        coutputcode.insert(ind + ind2,statements)
        ind2 += 1

#Function for Initial Variable Declaration
mainposition = coutputcode.index("int main()")

if(len(intbox) != 0):
    coutputcode.insert(mainposition + 2,"int ")
    count = 0
    for i in intbox:
        coutputcode[mainposition + 2] += i 
        count += 1
        if(count != len(intbox)):
            coutputcode[mainposition + 2] += ","

if(len(floatbox) != 0):
    if(len(intbox) != 0):
        j = 3
    else:
        j = 2
    coutputcode.insert(mainposition + j,"float ")
    count = 0
    for i in floatbox:
        coutputcode[mainposition + j] += i
        count += 1
        if(count != len(floatbox)):
            coutputcode[mainposition + j] += ","

if(len(stringbox) != 0):
    if(len(intbox) != 0 and len(floatbox) != 0):
        j = 4
    elif(len(intbox) !=0 and len(floatbox) == 0):
        j = 3
    elif(len(intbox) == 0 and len(floatbox) != 0):
        j = 3
    else:
        j = 2
    coutputcode.insert(mainposition + j,"char ")
    count = 0
    for i in stringbox:
        coutputcode[mainposition + j] += i
        count += 1
        if(count != len(stringbox)):
            coutputcode[mainposition + j] += ","

# Printing the Output
for linecode1 in coutputcode:
    if (linecode1.startswith('#include') or linecode1.startswith('void') or linecode1.startswith('{') or linecode1.startswith('}') or linecode1.strip().startswith("for(")):
        print(linecode1)
    elif (linecode1.startswith('//') or linecode1.strip().startswith("if(") or linecode1.strip().startswith("if (") or linecode1.strip().startswith("else") or linecode1.strip().startswith("while")):
        print(linecode1)
    elif(linecode1.startswith("void main(") or linecode1.startswith("int main(") or all(c=='' for c in linecode1)):
        print(linecode1)
    else:
        print(linecode1 + ";")

print(intbox,floatbox,stringbox,functionsbox,functions_container)
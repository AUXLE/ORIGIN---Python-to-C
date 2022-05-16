#Global Declarations
intbox = {}
floatbox = {}
stringbox = {}
loopsbox_c = []
loopsbox_python = []
conditionsbox_c = []
conditionsbox_python = []
functionsbox_c = []
functionsbox_python = []
controlstatementsbox = {"if":"if(" ,"if(":"if(" ,"if (":"if(" ,"elif ":"else if(" ,"elif(":"else if(", "elif (":"else if(", "else":"else", "while ":"while(", "while(":"While(","while (":"while(", "for ":"for("}
pyinputcode = []
coutputcode = ['#include<stdio.h>', '#include<conio.h>', '#include<stdlib.h>',"","int main()","{"]
operators = ["+","-","*","/","%"]
pre_space_count,bracescount,loop_flag,condition_flag,functions_flag,python_lines,c_lines = 0,1,0,0,0,0,0
loop_stack = []
condition_stack = []
function_stack = []
loop_lines = []
condition_lines = []
function_lines = []

# Function to Convert Print Statements
def printstatements(pylinecode,functions_flag,loop_flag,condition_flag):
    pylinecode = pylinecode.strip()
    no_quotes = pylinecode.count('''"''')
    statements = []
    c_linecode = '''printf("'''

    #If Output statements in the print statement
    if(no_quotes != 0):
        while('''"''' in pylinecode):
            quotes_place = pylinecode.find('''"''')
            quotes_place2 = pylinecode[quotes_place + 1:].find('''"''') + 1 + quotes_place
            statements.append(pylinecode[quotes_place + 1:quotes_place2])
            pylinecode = pylinecode[:quotes_place] + pylinecode[quotes_place2 + 1:]
        if(pylinecode.strip().startswith("print(")):
            pylinecode = pylinecode.replace("print(",'')
        else:
            pylinecode = pylinecode.replace("print (",'')
        pylinecode = pylinecode.replace(")",'')
        variable = pylinecode.split(",")
        ind = 0 
        for i in variable:
            if(i == ''):
                c_linecode += statements[ind]
                ind += 1 
            else:
                if(i in intbox):
                    c_linecode += "%d "
                elif(i in floatbox):
                    c_linecode += "%f "
                elif(i+"[100]" in stringbox):
                    c_linecode += "%s "
                elif('+' in i or '-' in i or '*' in i or '/' in i or '%' in i):
                    for j in operators:
                        if(j in i):
                            operator = j 
                    variables = i.split(operator)
                    
                    if(((variables in intbox) and (variables not in floatbox)) and ("." not in variables)):
                        c_linecode += "%d "
                    elif((variables in floatbox) or "." in variables):
                        c_linecode += "%f "
                    elif((variables+"[100]" in stringbox and variables not in floatbox and variables not in intbox) or '''"''' in i):
                        c_linecode += "%s "
                    else:
                        c_linecode += "%d "
            
        c_linecode += '''"'''
        for i in variable:
            if(i == ''):
                variable.remove(i)
        if(len(variable) != 0):
            c_linecode += ","
            for i in variable:
                c_linecode += i 
                if(variable.index(i) != len(variable) - 1):
                    c_linecode += ","
    
    #If only variables
    else:
        if(pylinecode.strip().startswith("print(")):
            pylinecode = pylinecode.replace("print(",'')
        else:
            pylinecode = pylinecode.replace("print (",'')
        pylinecode = pylinecode.replace(")",'')
        variable = pylinecode.split(",")
        for i in variable:
            if(i in intbox):
                c_linecode += "%d "
            elif(i in floatbox):
                c_linecode += "%f "
            elif(i+"[100]" in stringbox):
                c_linecode += "%s "
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
                    c_linecode += "%d "
                elif(all(var.strip() not in intbox for var in variables1) and all('''"''' not in var for var in variables1)):
                    c_linecode += "%f "
                elif((all(var.strip() not in intbox for var in variables1) and all(var.strip() not in floatbox for var in variables1))):
                    c_linecode += "%s "
                else:
                    c_linecode += "%d "

        c_linecode += '''",'''
        for i in variable:
            c_linecode += i 
            if(variable.index(i) != len(variable) - 1):
                c_linecode += ","
                
    c_linecode += ")"
    if(functions_flag):
        functionsbox_c.append(c_linecode)
        for i in range(len(function_lines)):
            function_lines[i] += 1
    else:
        coutputcode.append(c_linecode)   
    if(loop_flag):
        loopsbox_c.append(c_linecode)
        for i in range(len(loop_lines)):
            loop_lines[i] += 1
    if(conditionsbox_c):
        conditionsbox_c.append(c_linecode)     
        for i in range(len(condition_lines)):
            condition_lines[i] += 1

# Function to Convert Input Statements
def inputfunctions(linecode,functions_flag,loop_flag,condition_flag):
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
            functionsbox_c.append(linecode)
            for i in range(len(function_lines)):
                function_lines[i] += 1
        else:
            coutputcode.append(linecode)
        if(loop_flag):
            loopsbox_c.append(linecode)
            for i in range(len(loop_lines)):
                loop_lines[i] += 1
        if(condition_flag):
            conditionsbox_c.append(linecode)
            for i in range(len(condition_lines)):
                condition_lines[i] += 1

# Converting Comment lines
def commentsfunction(linecode,functions_flag,loop_flag,condition_flag):
    linecode = str(linecode)
    linecode = linecode.replace("#", "//")
    if(functions_flag):
        functionsbox_c.append(linecode)
        if(linecode.strip().startswith("//")):
            for i in range(len(function_lines)):
                function_lines[i] += 1
    if(loop_flag):
        loopsbox_c.append(linecode)
        for i in range(len(loop_lines)):
            loop_lines[i] += 1
    if(condition_flag):
        conditionsbox_c.append(linecode)
        for i in range(len(condition_lines)):
            condition_lines[i] += 1
    else:
        coutputcode.append(linecode)

# Declaring expressions variables
def expressionsfunction(linecode,functions_flag,loop_flag,condition_flag):
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
            functionsbox_c.append(linecode)
            for i in range(len(function_lines)):
                function_lines[i] += 1
        else:
            coutputcode.append(linecode)
        if(loop_flag):
            loopsbox_c.append(linecode)
            for i in range(len(loop_lines)):
                loop_lines[i] += 1
        if(condition_flag):
            conditionsbox_c.append(linecode)
            for i in range(len(condition_lines)):
                condition_lines[i] += 1

#Control Statements
def controlstatements(linecode,functions_flag,loop_flag,condition_flag):
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
        functionsbox_c.append(linecode)
        for i in range(len(function_lines)):
            function_lines[i] += 1
    else:        
        coutputcode.append(linecode)
    if(loop_flag):
        loopsbox_c.append(linecode)
        for i in range(len(loop_lines)):
            loop_lines[i] += 1
    if(condition_flag):
        conditionsbox_c.append(linecode)
        for i in range(len(condition_lines)):
            condition_lines[i] += 1
    
def hub(datas,functions_flag):
    global coutputcode
    global bracescount
    global pre_space_count
    global python_lines
    global condition_flag
    global loop_flag
    #inside_function = 0

    #Takes each line in the Intput
    for linecode in datas:
        python_lines += 1 
        if(loop_flag):
            loopsbox_python.append(linecode)
        if(condition_flag):
            conditionsbox_python.append(linecode)
        if(functions_flag):
            functionsbox_python.append(linecode)

        #Automatic Curly Braces Function
        curr_space_count = 0
        for spaces in linecode:
            if(spaces != ' '):
                break
            else:
                curr_space_count += 1
        if(pre_space_count > curr_space_count):
            coutputcode.append('}')
            if(loop_flag):
                last = len(loop_stack) - 1
                last_l = len(loopsbox_python) - 1
                while(last >= 0):
                    if(loop_stack.count(loop_stack[last])%2 == 1 and loop_stack[last] == curr_space_count):
                        del loop_stack[-1]
                        while(last_l >= 0):
                            if(loopsbox_python[last_l] == 0):
                                loopsbox_python[last_l] = loop_lines[-1]
                                del loop_lines[-1]
                            last_l -= 1
                        loopsbox_python.append("]")
                        loopsbox_c.append("]")
                        break
                    last -= 1
                if(len(loop_stack) == 0 or loop_stack[0] == loop_stack[-1]):
                    loop_flag = 0
                    loop_stack.clear()
                    last_l = 0
                    for i in loopsbox_python:
                        if(i == 0):
                            i = loopsbox_python[last_l]
                            last_l += 1
                            break
                    loop_lines.clear()
            elif(condition_flag):
                last = len(condition_stack) - 1
                last_l = len(conditionsbox_python) - 1
                while(last >= 0):
                    if(condition_stack.count(condition_stack[last])%2 == 1 and condition_stack[last] == curr_space_count):
                        del condition_stack[-1]
                        while(last_l >= 0):
                            if(conditionsbox_python[last_l] == 0):
                                conditionsbox_python[last_l] = condition_lines[-1]
                                del condition_lines[-1]
                                break
                            last_l -= 1
                        conditionsbox_python.append("]")
                        conditionsbox_c.append("]")
                        break
                    last -= 1
                if(len(condition_flag) == 0 or condition_flag[0] == condition_flag[-1]):
                    condition_flag = 0
                    condition_stack.clear()
                    last_l = 0
                    for i in conditionsbox_python:
                        if(i == 0):
                            i = condition_lines[last_l]
                            last_l += 1
                    condition_lines.clear()
            else:
                last = len(function_stack) - 1
                last_l = len(functionsbox_python) - 1
                while(last >= 0):
                    if(function_stack.count(function_stack[last])%2 == 1 and function_stack[last] == curr_space_count):
                        del function_stack[-1]
                        while(last_l >= 0):
                            if(functionsbox_python[last_l] == 0):
                                functionsbox_python[last_l] = function_lines[-1]
                                del function_lines[-1]
                                break
                        functionsbox_python.append("]")
                        functionsbox_c.append("]")
                        break
                    last -= 1
                if(len(functions_flag) == 0 or functions_flag[0] == functions_flag[-1]):
                    functions_flag = 0
                    function_stack.clear()
                    last_l = 0
                    for i in functionsbox_python:
                        if(i == 0):
                            i = function_lines[last_l]
                            last_l += 1
                    function_lines.clear()

        elif(pre_space_count < curr_space_count):
            coutputcode.append('{')
        pre_space_count = curr_space_count
        '''if(pre_space_count > curr_space_count):
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
        pre_space_count = curr_space_count'''
        #print(inside_function)
        '''if(inside_function):
            functionsbox_python.append(linecode)
            continue'''

        # Converts print statement
        if (linecode.strip().startswith("print(") or linecode.strip().startswith("print (")):
            printstatements(linecode,functions_flag,loop_flag,condition_flag)

        # For input statement
        elif ("input" in linecode):
            sides = linecode.split("=")
            sides[1] = sides[1].strip()
            if(sides[1].strip().startswith('''"''')):
                expressionsfunction(linecode,functions_flag,loop_flag,condition_flag)
            else:
                inputfunctions(linecode,functions_flag,loop_flag,condition_flag)

        # For Comment lines
        elif (linecode.strip().startswith('#')):
            commentsfunction(linecode,functions_flag,loop_flag,condition_flag)
        
        elif(linecode.strip().startswith("if(") or linecode.strip().startswith("if (") or linecode.strip().startswith("if ") or linecode.strip().startswith("elif(") or linecode.strip().startswith("elif (") or linecode.strip().startswith("elif ")):
            condition_flag = 1
            condition_stack.append(curr_space_count)
            conditionsbox_python.append('[')
            conditionsbox_python.append("if") if(linecode.strip().startswith("if")) else conditionsbox_python.append("elif")
            conditionsbox_python.append(python_lines)
            conditionsbox_python.append(0)
            conditionsbox_python.append(linecode)
            conditionsbox_c.append("[")
            conditionsbox_c.append("if") if(linecode.strip().startswith("if")) else conditionsbox_c.append("elif")
            conditionsbox_c.append(0)
            conditionsbox_c.append(0)

            #Creating variables for counting Lines
            condition_lines.insert(python_lines,len(condition_lines))
            controlstatements(linecode,functions_flag,loop_flag,condition_flag)
        
        elif((linecode.strip().startswith("else") or linecode.strip().startswith("else ")) and "=" not in linecode):
            condition_flag = 1
            condition_stack.append(curr_space_count)
            conditionsbox_python.append('[')
            conditionsbox_python.append(python_lines)
            conditionsbox_python.append(0)
            conditionsbox_python.append(linecode)
            conditionsbox_c.append("[")
            conditionsbox_c.append("else")
            conditionsbox_c.append(0)
            conditionsbox_c.append(0)

            condition_lines.insert(python_lines,len(condition_lines))
            controlstatements(linecode,functions_flag,loop_flag,condition_flag)

        elif(linecode.strip().startswith("while(") or linecode.strip().startswith("while (") or linecode.strip().startswith("while ") or linecode.strip().startswith("for ")):
            loop_flag = 1
            loop_stack.append(curr_space_count)
            loopsbox_python.append('[')
            loopsbox_python.append("while") if(linecode.strip().startswith("while(") or linecode.strip().startswith("while (")) else loopsbox_python.append("for")
            loopsbox_python.append(python_lines)
            loopsbox_python.append(0)
            loopsbox_python.append(linecode)
            loopsbox_c.append("[")
            loopsbox_c.append("while") if(linecode.strip().startswith("while")) else conditionsbox_c.append("for")
            loopsbox_c.append(0)
            loopsbox_c.append(0)

            loop_lines.insert(len(loop_lines),python_lines)
            controlstatements(linecode,functions_flag,loop_flag,condition_flag)

        elif(linecode.strip().startswith("def ") and not functions_flag):
            function_parts = linecode.strip().split()
            functionsbox_python.append('[')
            functionsbox_python.append(function_parts[1])
            functionsbox_python.append("void")
            functionsbox_python.append(python_lines)
            functionsbox_python.append(0)
            functionsbox_python.append(linecode)
            functionsbox_c.append('[')
            functionsbox_c.append(function_parts[1])
            functionsbox_c.append("void")
            functionsbox_c.append(0)
            functionsbox_c.append(0)

            function_lines.insert(python_lines,len(function_lines))
            function_stack.append(curr_space_count)

        elif(linecode.strip().startswith("def ") and functions_flag):
            linecode = linecode.replace("def ","void ")
            functionsbox_c.append(linecode[:len(linecode) - 1])

        # For others
        else:
            equals = linecode.find("=")
            if ("=" in linecode and linecode[equals - 1] not in operators):
                expressionsfunction(linecode,functions_flag,loop_flag,condition_flag)
            else:
                coutputcode.append(linecode)
        
    # Appending the last Closing Curly Brace for main() function
    if(bracescount % 2 == 1):
        if(functions_flag):
            functionsbox_c.append('}')
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
hub(pyinputcode,0)

if(len(functionsbox_python)):
    hub(functionsbox_python,1)

if(len(functionsbox_c)):
    ind = coutputcode.index("") + 1
    ind2 = 0
    for statements in functionsbox_c:
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

print("Integer ",intbox,"\nFloat ",floatbox,"\nStrings ",stringbox,"\nFunctions Python ",functionsbox_python,"\nLoops Python ",loop_stack,"\nConditions ",condition_stack)
print("Functions Data Python ",functionsbox_python,"\nLoop Data Python ",loopsbox_python,"\nConditions Data Python ",conditionsbox_python)
print("Functions Data C ",functionsbox_c,"\nLoop Data C ",loopsbox_c,"\nCondition Data C ",conditionsbox_c)
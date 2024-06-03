import os, sys, difflib

def displayInTerminal(left_text,right_text):

    for i in range(max(len(left_text),len(right_text))):
        if i>len(left_text):
            print("Text file 2 line "+str(i+1)+": "+right_text[i])
        elif i>len(right_text):
            print("Text file 1 line "+str(i+1)+": "+left_text[i])
        else:
            print("Text file 1 line "+str(i+1)+": "+left_text[i]+"\nText file 2 line "+str(i+1)+": "+right_text[i])

def main():
    text_files = [file for file in os.listdir(os.getcwd()) if file.endswith(".txt")]
    if len(text_files)==0 or len(text_files)==1:
        print("Fewer than 2 text files present")
        sys.exit(1)
    elif len(text_files)==2:
        file1 = 1
        file2 = 2
    else:
        print("Choose from the text files in the current directory: ")
        for i,file in enumerate(text_files):
            print(str(i+1)+": "+file)
        file1 = int(input("Input number of first text file: "))
        file2 = int(input("Input number of second text file: "))
    
    text1 = open(text_files[file1-1],'r').read().splitlines()
    text2 = open(text_files[file2-1],'r').read().splitlines()
    differ = difflib.Differ()
    
    left_text = []
    right_text = []

    while len(text1)>0 and len(text2)>0:
        
        if text1[0]=='' and text2[0]!='':
            left_text.append("\033[91m" + "<newline>" + "\033[0m")
            right_text.append('')
            text1.pop(0)
            continue
        
        if text2[0]=='' and text1[0]!='':
            right_text.append("\033[92m" + "<newline>" + "\033[0m")
            left_text.append('')
            text2.pop(0)
            continue

        diff = differ.compare(text1[0],text2[0])
        
        left_line = ''
        right_line = ''
        for char in diff:
            if char[0] == '-':
                left_line = left_line + "\033[91m" + char[2] + "\033[0m"
            elif char[0] == '+':
                right_line = right_line + "\033[92m" + char[2] + "\033[0m"
            else:
                left_line = left_line + char[2]
                right_line = right_line + char[2]

        left_text.append(left_line)
        right_text.append(right_line)
        text1.pop(0)
        text2.pop(0)
    displayInTerminal(left_text,right_text)

main()

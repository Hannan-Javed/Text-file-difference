import os, sys, difflib
import tkinter as tk

red_color = "\033[91m"
green_color = "\033[92m"

def displayInTerminal(left_text,right_text):

    left_text = getTerminalString(left_text,red_color)
    right_text = getTerminalString(right_text, green_color)
    for i in range(max(len(left_text),len(right_text))):
        if i>len(left_text):
            print("Text file 2 line "+str(i+1)+": "+right_text[i])
        elif i>len(right_text):
            print("Text file 1 line "+str(i+1)+": "+left_text[i])
        else:
            print("Text file 1 line "+str(i+1)+": "+left_text[i]+"\nText file 2 line "+str(i+1)+": "+right_text[i])

def getTerminalString(text, color):

    t_string = []
    for line in text:
        final_string = ''
        for char,tag in line:
            if tag != '':
                final_string += color + char + "\033[0m"
            else:
                final_string += char
        t_string.append(final_string)

    return t_string

def displayInWindow(left_text,right_text):

    window = tk.Tk()

    # Set the initial size of the window
    initial_width = 800
    initial_height = 600
    window.geometry(f"{initial_width}x{initial_height}")

    # Set the minimum size of the window to the initial size
    window.wm_minsize(initial_width, initial_height)
    
    # Create a frame to hold the text boxes
    frame = tk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True)

    left_text_box = tk.Text(frame, width=50, height=20)
    left_text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    right_text_box = tk.Text(frame, width=50, height=20)
    right_text_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Define the color tags
    left_text_box.tag_configure("red", foreground="red")
    left_text_box.tag_configure("green", foreground="green")
    
    right_text_box.tag_configure("red", foreground="red")
    right_text_box.tag_configure("green", foreground="green")

    # Update the text in the text boxes with colors
    for line in left_text:
        for char, tag in line:
            if tag:
                left_text_box.insert(tk.END, char, tag)
            else:
                left_text_box.insert(tk.END, char)
        left_text_box.insert(tk.END, "\n")

    for line in right_text:
        for char, tag in line:
            if tag:
                right_text_box.insert(tk.END, char, tag)
            else:
                right_text_box.insert(tk.END, char)
        right_text_box.insert(tk.END, "\n")

    # Allow the text boxes to resize with the window
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)

    # Start the GUI event loop
    window.mainloop()

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
            left_text.append([("<newline>", "red")])
            right_text.append([("", "")])
            text1.pop(0)
            continue
        
        if text2[0]=='' and text1[0]!='':
            right_text.append([("<newline>", "green")])
            left_text.append([("", "")])
            text2.pop(0)
            continue

        diff = differ.compare(text1[0],text2[0])

        left_line = []
        right_line = []
        for char in diff:
            if char[0] == '-':
                left_line.append((char[2], "red"))
                right_line.append(("", ""))
            elif char[0] == '+':
                right_line.append((char[2], "green"))
                left_line.append(("", ""))
            else:
                left_line.append((char[2], ""))
                right_line.append((char[2], ""))

        left_text.append(left_line)
        right_text.append(right_line)
        text1.pop(0)
        text2.pop(0)

    displayInTerminal(left_text,right_text)
    displayInWindow(left_text,right_text)

main()

import os
def text_wc(x,output='listoutput.txt', kwargs**):#takes list writes to text
    if '.' not in output: raise TypeError("No file extension detected.")
    mode =kwargs.get('mode', 'w')
    n_l = x
    name = output
    num = 0
    while(file_present(output)):
        num += 1
        fname_extension = output.split('.')
        fname, extension = fname_extension[0], fname_extension[1]
        output = fname + str(num) + "." + extension


    
    with open(name, 'w') as wf:
        for i in range(0, len(n_l)):
            wf.writelines(new)
    #print("%s saved to %s" % (output, output))
    return

def file_present(x):
    #only checks current working directory
    full_path = os.getcwd() + '\\' + x
    if os.path.exists(full_path):
        return True
    if not os.path.exists(full_path):
        return False

#!/usr/bin/env python
# coding: utf-8

# In[80]:


def do_():
    #print(line[12:18])
    lines = line.split()
    atom = (lines[1])
    atom_ = atom + "_"
    print(atom_)
    global LINE
    LINE = "%6s%11s%7s%7s%7s%7s%11s%11s \n"% (lines[0],atom_,lines[2],lines[3],lines[4],lines[5],lines[6],lines[7])
    fout.append(LINE)
    print(LINE)


    with open ('process.top', 'a') as f:
        f.write(LINE)


# In[81]:


fout = []

with open ('process.top', 'w') as f:
    f.close()

with open ("processed_x.top", "r") as f:
    n = 0
    ln = 1
    for line in f:

        if "; START OF PEP" in line:  #If the line is the start of the peptide topol n = 1
            n = 1
            #print(line)       

        elif "; END OF PEP" in line:
            n = 100
            fout.append(line)

        elif n == 0:
            fout.append(line)

        elif n > 99:
            fout.append(line)


        elif n == 1:                         #if before end of peptide top
            if ln < 4:                     #if line is less than 5 (start of peptide)
                ln += 1
                fout.append(line)
            elif "; residue" in line:              #ignore comments
                fout.append(line)

            else:                          #THESE LINES ARE TO BE MODIFIED.
                do_()


        else:                              #if anything else e.g all outside peptide top keep same.
            fout.append(line)
            continue




with open ('process.top', 'w') as f:
    for line in fout:
        f.write(line)

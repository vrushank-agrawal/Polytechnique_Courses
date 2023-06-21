# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 11:05:14 2020

@author: 123
"""

def split_type(line):
    """Splits off the first word in the line and returns both parts in a tuple.
    Also eliminates all leading and trailing spaces.
    Example:
        split_type('ROW ##.##') returns ('ROW', '##.##')
        split_type('CLUE (0,1) down: Of or pertaining to the voice (5)') returns
            ('CLUE', '(0,1) down: Of or pertaining to the voice (5)')
        split_type('  ROW    ##.##   ') returns ('ROW', '##.##')

    """
    if line.find('\n')!=-1:
        line=line.replace('\n','')
    ln=line.strip(' ')
    a=ln.index(' ')
    b=a+1
    while b!=a:
        if ln[b]==' ':
            b+=1
        else:
            break;
    return (ln[:a], ln[b:])


def read_row(row):
    """Reads a row of a crossword puzzle and decomposes it into a list. Every 
    '#' is blocking the current box. Letters 'A', ..., 'Z' and 'a', ..., 'z'
    are values that are already filled into the box. These letters are capitalized
    and then put into the list. All other characters stand 
    for empty boxes which are represented by a space ' ' in the list.
    Examples:
        read_row('#.#') gives ['#', ' ', '#']
        read_row('C.T') gives ['C', ' ', 'T']
        read_row('cat') gives ['C', 'A', 'T']
    """
    lst=[]
    if row.find('\n')!=-1:
        row=row.replace('\n','')
    for i in range(len(row)):
        a=row[i]
        if a.isalpha():
            a=a.upper()
            lst.append(a)
        elif a=='#':
            lst.append('#')
        else:
            lst.append(' ')
    return lst


def read_clue(cluestring):
    """Reads a clue into a tuple in the following way: The input is of the form
        '(x,y) direction: question (length)
    where x, y and length are integers, direction is 'across' or 'down'
    and question is the text of the clue. The output should then be
        ((x, y), direction, length, question)
    where (x, y) is a tuple of values of type int and length is of type int.
    None of these values are strings. There may be arbitrarily many spaces 
    between the different parts of the input.
    Example:
        read_clue('(0,1) down: Of or pertaining to the voice (5)') returns
        ((0, 1), 'down', 5, 'Of or pertaining to the voice')
    """
    if cluestring.find('ROW')!=-1:
        cluestring=cluestring.replace('ROW:','')
    elif cluestring.find('CLUE')!=-1:
        cluestring=cluestring.replace('CLUE','')
    clue=cluestring.strip()
    i=0; pos=0
    while clue[i]!=' ':
        pos+=1; i+=1
    temp=clue[:pos]
    temp=temp.replace('(','')
    temp=temp.replace(')','')
    a=temp.split(',')
    b=(int(a[0]),int(a[1]))
    clue=clue.replace(clue[:pos+1],'')
    lst=[b]                                     #appending first element   
    if clue.find('across')!=-1:                 #appending position 
        lst.append('across')
        clue=clue.replace('across:','')
    elif clue.find('down')!=-1:
        lst.append('down')
        clue=clue.replace('down:','')
    pos=clue.index('(')
    lst.append(int(clue[pos+1:len(clue)-1]))    #appending length
    clue=clue.replace(clue[pos:len(clue)],'')
    clue=clue.strip()
    lst.append(clue)                            #appending the hint
    return (lst[0],lst[1],lst[2],lst[3])


def read_file(filename):
    """Opens the file with the given filename and creates the puzzle in it. 
    Returns a pair consisting of the puzzle grid and the list of clues. Assumes
    that the first line gives the size. Afterwards, the rows and clues are given.
    The description of the rows and clues may interleave arbitrarily.
    """
    f1=open(filename, 'r')
    lst=f1.readlines()
    lst_row=[]; lst_clue=[]; lst_comment=[]
    for i in range(len(lst)):
        lst[i]=lst[i].strip()
    for i in range(1,len(lst)):
        if lst[i].startswith('ROW'):
            temp=split_type(lst[i])
            lst_row.append(read_row(temp[1]))
        elif lst[i].startswith('CLUE'):
            lst_clue.append(read_clue(lst[i]))
        elif lst[i].startswith('COMMENT'):
            temp=lst[i].replace('COMMENT','')
            lst_comment.append('#'+temp)
    if lst_comment!=[]:
        return (lst_row, lst_clue, lst_comment)
    else:
        return (lst_row, lst_clue)


def create_clue_string(clue):
    """ Given a clue, which is a tuple
    (position, direction, length, question),
    create a string in the form 'position direction: question (length)'.
    For example, given the clue
        ((2, 3), 'across', 4, 'Black bird'),
    this function will return
        '(2,3) across: Black bird (4)'
    """
    a=clue[0]
    lst=f'({a[0]},{a[1]}) {clue[1]}: {clue[3]} ({clue[2]})'
    return lst


def create_grid_string(grid):
    """Return a crossword grid as a string."""
    size = len(grid)
    separator = '  +' + ('-----+')*size
    column_number_line = '   '
    column_number_line += ''.join(f' {j:2}   ' for j in range(size))
    result = f'{column_number_line}\n{separator}\n'
    for (i, row) in enumerate(grid):
        fill = '  |'
        centre_line = f'{i:2}|'
        for entry in row:
            if entry == '#':
                fill += '#####|'
                centre_line += '#####|'
            else:
                fill += '     |'
                centre_line += f'  {entry}  |'
        result += f'{fill}\n{centre_line}\n{fill}\n{separator}\n'
    return result


def create_puzzle_string(grid, clues):
    """Return a human readable string representation of the puzzle."""
    show_grid=create_grid_string(grid)
    for i in range(len(clues)):
        show_grid=show_grid+'\n'+create_clue_string(clues[i])
    return show_grid


def fill_in_word(grid, word, position, direction):
    """Create and return a new grid (a list of lists) based on the grid
    given in the arguments, but with the given word inserted according
    to position and direction.
        - direction: is either 'down' or 'across'. 
        - position: the coordinates of the first letter of the word in the grid.
    *This function may modify its grid argument!*
    """
    for i in range(len(word)):
        if direction=='across':
            grid[position[0]][position[1]+i]=word[i]
        elif direction=='down':
            grid[position[0]+i][position[1]]=word[i]
    return grid


def create_row_string(row):
    """Returns a row representation of a string.
    Example:
        create_row_string(['#', 'A', ' ']) returns '#A.'
    """
    string=''
    for i in range(len(row)):
        string=string+str(row[i])
    string=string.replace(' ','.')
    return string


def write_puzzle(filename, grid, clues):
    """Writes the puzzle given by the grid and by the clues to the specified
    file.
    """
    f1=open(filename,'w')
    f1.write(f'SIZE {len(grid)}'+'\n')
    str_final=''
    for i in range(len(grid)):
        str_final=f'ROW {create_row_string(grid[i])}'+'\n'
        f1.write(str_final)
        str_final=''
    for i in range(len(clues)):
        str_final=f'CLUE {str_final}{create_clue_string(clues[i])}'+'\n'
        f1.write(str_final)
        str_final=''
    f1.close()


def write_comment(filename,comment):
    """A function to add comments in the textfile"""
    f1=open(filename, 'a')
    f1.write(f'COMMENT {comment}')
    while True:
        a=input(print('Do you want to add another comment(Y/N?'))
        if a=='Y':
            comment=input()
            f1.write(f'COMMENT {comment}')
        else:
            break
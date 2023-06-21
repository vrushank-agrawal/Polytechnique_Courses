"""
Created on Tue Oct  6 18:17:43 2020
    
@author: 123
"""
def average(numlist):
    """Return average of list of numbers"""
    x=0; y=numlist
    for i in range(len(y)):
        x+=numlist[i]
    avg=float(round(x/len(y),2))
    return avg
    
def student_data(data_string):
    """Compute (name, results) tuple from the string data_string."""
    x=data_string.split()
    b=[float(x[i]) for i in range(1, len(x),1)]
    return (x[0],b)

def read_student_data(filename):
    """Return list of student data from file"""
    v=[]; b=0
    f = open(filename,'r')
    s=f.readlines()
    for i in s:
        a=s[b]; b+=1
        c=student_data(a)
        v.append(c)
    f.close()  
    return v

def extract_averages(filename):
    """Return list of name and average for each line in file"""
    lst=read_student_data(filename)
    final_lst=[]; nums=[]
    for i in range(len(lst)):
        a=lst[i]
        b=str(a[1])
        c=b.replace('[','')
        d=c.replace(']','')
        nums=[float(i) for i in d.split(', ')]
        c=(a[0], average(nums))
        final_lst.append(c)
    return final_lst

def discard_scores(numlist):
    """Filter numlist: construct a new list from numlist with
    the first two, and then the lowest two, scores discarded. """
    new=numlist[2:]
    for i in range(2):
        x=new.index(min(new))
        new.remove(new[x])
    return new

def summary_per_student(infilename, outfilename):
    """Create summaries per student from the infile 
    and write the summaries to the outfile. """
    fW=open(outfilename,'w')
    intl_lst=read_student_data(infilename)
    ttl_avg=0
    for i in range(len(intl_lst)):
        a=intl_lst[i]
        b=a[1]
        c=discard_scores(b)
        d=str(c)
        e=d.replace(']','')
        f=e.replace('[','')
        g=f.replace(',','')
        new_sum=sum(c)
        new_sum=str(round(new_sum,2))
        fW.write(a[0]+' '+str(g)+' sum: '+str(new_sum)+'\n')
        ttl_avg+=float(new_sum)
    ttl_avg=round(ttl_avg/len(intl_lst),2)
    fW.write('total average: '+str(ttl_avg)+'\n')
    fW.close()

def summary_per_tutorial(infilename, outfilename):
    """Create summaries per student from infile and write to outfile."""
    data = read_student_data(infilename)
    fW=open(outfilename,'w')
    z=data[0]; lst=[]; lst_nos=[]; lst_min=[]; lst_max=[]; lst_avg=[];
    for i in range(len(data)):
        x=data[i]
        lst.append(x[1])
    for i in range(len(z[1])):
        temp1=[]
        for j in range(len(lst)):
            temp=lst[j]
            temp1.append(temp[i])
        lst_nos.append(temp1)
    for i in range(len(lst_nos)):
        temp=lst_nos[i]
        avg=round(sum(temp)/len(temp),2)
        x=min(temp)
        y=max(temp)
        lst_min.append(x)
        lst_max.append(y)
        lst_avg.append(avg)
    for i in range(len(lst_avg)):
        fW.write('TD'+str(i+1)+':'+' average: '+str(lst_avg[i])\
                 +' min: '+str(lst_min[i])+' max: '+str(lst_max[i])+'\n')
    fW.close()

def generate_emails(filename):
    """Generate emails to students with their results"""
    data = read_student_data(filename)
    for i in range(len(data)):
        a=data[i]
        m=a[0]
        x=m.split('.')
        f=open(x[0]+'_'+x[1]+'.txt', 'w')
        f.write('To: '+m+'@polytechnique.edu'+'\n'+'\n'\
                +'This is to notify you of your final results for the CSE101 course, see'+'\n'\
                +'table below. (Note that the two first and two lowest scores are'+'\n'\
                +'excluded from the result.' +'\n'+'\n')
        scores=discard_scores(a[1])
        td=''; tx=''
        for j in range(len(a[1])):
            td=td+'TD'+str(j+1)+'  '
        td=td+'Result'
        for j in range(len(td)):
            tx=tx+'-'
        f.write(td+'\n'+tx+'\n')
        score=sum(scores)
        b=a[1]
        for j in range(len(a[1])):
            a=str(b[j])
            f.write(a+'  ')
        f.write(str(score)+'\n'+'\n'+ 'Best regards,'+'\n'\
                +'and please get back to me if you have any questions,'+'\n'\
                    +'Your Teacher')
        f.close()
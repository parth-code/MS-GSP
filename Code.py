#!/usr/bin/env python
# coding: utf-8

# In[1148]:


import copy
from collections import defaultdict
def main():
    count=defaultdict(int)
    F=defaultdict(list)
    k=1
    d="data3.txt"
    p="Para3.txt"
    S=Read_Data(d)
    MS,SDC=Read_Para(p)
    N=len(S)
    M=[] # according to MIS(i)’s stored in MS
    for i ,v in sorted(MS.items(),key=lambda kv:kv[1]):
        M.append(i)
    L,Count_L=Init_Pass(M,S,N,MS)   #first pass over S
    F[k]=F1gen(L,MS,Count_L,count,N)
    printOutput(k, F[k], count)
    k=k+1
    while (F[k-1]):
        Candidates=[]
        if k==2:
            Candidates=Cand2Gen(L,Count_L,MS,SDC,N)
        else:
            Candidates=MSCandGen(F[k-1],Count_L,SDC,MS,N) # To be Written
        for t,s in S.items():
            for cand in Candidates:
                isSequence=isSubsequence(cand,s)
                if isSequence:
                    count[str(cand)]+=1
        F[k]=GenFk(Candidates,MS,count,N)
        printOutput(k, F[k], count)
        k+=1        
    return


# In[1149]:


def Read_Data(file):
    with open(file) as f:
        line=f.readline()
        cnt=0
        S=defaultdict(list)
        while line: 
            sequence=[]
            cnt+=1
            line=line.replace(">",'').replace('<','').replace("}{","_").replace("{","").replace("}","")
            for i in line.split("_"):
                element=[]
                for item in i.split(","):
                    element.append(int(item.strip(" \n")))
                sequence.append(element)
            S[cnt]=sequence
            line=f.readline()
    return S


# In[1150]:


def Read_Para(file):
    with open(file) as f:
        line=f.readline()
        MS=defaultdict()
        while line:
            if "MIS" in line:
                element=line[line.find("(")+1:line.find(")")]
                mis=line[line.find("=")+1:].lstrip(" ").lstrip("\n")
                MS[int(element)]=float(mis)
            else:SDC=float(line[line.find("=")+1:].lstrip(" "))
            line=f.readline()
    return MS,SDC
    


# In[1151]:


# Initial pass over transaction and counting the occurence of each item
#this is eliminate any item that is below the lowest MIS
def Init_Pass(M,S,N,MS):
    Count=defaultdict(int)
    Count_L=defaultdict(int)
    L=[]
    for i,s in S.items():
        for item in M:
            if item in sum(s,[]):
                Count[item]+=1
    for item in M:
        if float(Count[item]/N) >= float(MS[item]):
            Minimum_MIS,i=float(MS[item]),M.index(item)
            break
    
    for index in range(i,len(M)):
        if float(Count[M[index]]/N) >= Minimum_MIS:
            L.append(M[index])
            Count_L[M[index]]=Count[M[index]]
    return L,Count_L


# In[1152]:


def F1gen(L,MS,Count,count, N):
    F1=[]
    for item in L:
        #Item satisfying its own MIS
        if float(Count[item]/N)>=MS[item]:
            itemString= "[" + str(item) +"]"
            count[itemString] = Count[item]
#             print("item--->{0} count--->{1} ms--->{2}".format(item,Count[item],MS[item]))
            F1.append([item])
            
    return F1


# In[1153]:


def Cand2Gen(L,L_count,MS,sdc,n):
    def Duplicate_Removal(C2):
        #remove candidates with same element like [10,10] and candidates not in lexicographic order like [30,20]
        C2[:] = [c for c in C2 if type(c[0]) is int  and  c[0]<c[1] or type(c[0]) is list]
        return C2
    if L:

        c2 = []

        for elemt in L:
            if(L_count[elemt] >= MS[elemt]):

                for next_elemt in L[L.index(elemt):]:

                    if L_count[next_elemt] >= MS[elemt] and abs ( float(L_count[next_elemt]/n) - float(L_count[elemt]/n)) <= sdc:

                        c2.append([elemt, next_elemt])

                        c2.append([[elemt],[next_elemt]])

                for next_elemt in L[:L.index(elemt)]:

                    if L_count[next_elemt] >= MS[elemt] and abs(float(L_count[next_elemt]/n) - float(L_count[elemt]/n)) <= sdc:

                        c2.append([elemt, next_elemt])

                        c2.append([[elemt],[next_elemt]])
    C2=Duplicate_Removal(c2)
    return C2


# In[1154]:


def isSubsequence(c,s):
    #to handle cases like [10,20,30] convert it into [[10,20,30]]
    if type(c[0]) is int:
        c=[c] 
    NumElement_C=len(c)
    flag=[0]*len(s)
    index=-1
    for element in c:
        for i in range(index+1,len(s)):
            if len(element)==len(set(element)):
                if set(element).issubset(set(s[i])) and not flag[i]:
                    index=i
                    flag[i]=1
                    break
    if sum(flag)==NumElement_C:
        return True
    else:
        return False


# In[1155]:


def GenFk(Candidates,MS,count,N):
    F=[]
    for cand in Candidates:
        if type(cand[0]) is list:
            temp=sum(cand,[])
        else:temp=copy.deepcopy(cand)
        min_mis=float('inf')
        for item in temp:
            min_mis=min(min_mis,MS[item])
        if float(count[str(cand)]/N)>=float(min_mis) :
            F.append(cand)
    return F


# In[1156]:


def MSCandGen(F,Lcount,SDC,MS,N):
    convert=lambda s:sum(s,[]) if type(s[0]) is list else copy.deepcopy(s) # merges lists
    candlist=[]
    
    def CheckLastMIS(s2,MS):
        convert=lambda s2:sum(s2,[]) if type(s2[0]) is list else copy.deepcopy(s2) 
        temp=convert(s2)
        min_mis=float('inf')
        last_item=temp[-1]
        if len(set(temp))==1:return False # for s=[[30],[30]]
        for item in temp:
            if MS[item]<=MS[last_item] and item!=last_item:
                return False
        return True
    
    def checkIfFirstMISIsSmallest(s, MS):
        convert=lambda s2:sum(s2,[]) if type(s2[0]) is list else copy.deepcopy(s2) 
        temp=convert(s)
        min_mis=float('inf')
        first_item=temp[0]
        if len(set(temp))==1:return False
        for item in temp:
            if MS[item]<=MS[first_item] and item!=first_item:
                return False
        return True

    def Size(s):
        if type(s[0]) is list:
            return len(s)
        else:
            return 1

    def length(s):
        convert=lambda s:sum(s,[]) if type(s[0]) is list else copy.deepcopy(s)
        return len(convert(s))
    
    def Last_MIS_Less(s1,s2):
        temp_s1=convert(s1)
        temp_s2=convert(s2)
        s1first=temp_s1[0]
        s2first=temp_s2[0]
        MISfirsts1=MS[temp_s1[0]]
        MISlasts2=MS[temp_s2[-1]]
        firstS1=temp_s1.pop(0) #remove first
        if len(temp_s2) == 2 :
            secondlastS2=temp_s2.pop(0)
        else:
            secondlastS2=temp_s2.pop(-2)# remove last but 1
        if temp_s1==temp_s2 and MISlasts2<MISfirsts1 and abs(float(Lcount[firstS1]/N)-float((Lcount[secondlastS2]/N)))<=SDC:
            if type(s1[0]) is list and len(s1[0])==1:# first is seperate element in s1
                if type(s2[0]) is int: # if s2=[10,20] then first element of s1 should be added as list and appended with s2
                    cand=[]
                    cand.append(copy.deepcopy(s1[0]))
                    cand.append(copy.deepcopy(s2)) 
                    candlist.append(cand)
                    
                                     
                else:
                    cand=[copy.deepcopy(s1[0])]+copy.deepcopy(s2) #if s2=[[10],[20]] add just the first element of s1 as list to s2 .
                    candlist.append(cand)
                    
                    

                        
                if length(s2)==2 and Size(s2)==2 and s1first<s2first: # generate c2
                    cand=copy.deepcopy(s2)
                    cand[0].insert(0,s1[0][0])
                    candlist.append(cand)
                    
                    
                    

            elif (length(s2)==2 and Size(s2)==1 and s1first<s2first) or length(s2)>2: # just generate c1
                if type(s2[0]) is int:
                    cand=copy.deepcopy(s2)
                    cand.insert(0,s1[0])
                    candlist.append(cand)
                    


                else:
                    first=copy.deepcopy(s1[0])
                    if isinstance(first,list):item=first[0]
                    else:item=first                    
                    cand=copy.deepcopy(s2)
                    cand[0].insert(0,item)
                    candlist.append(cand)
                    


                    
    def DefaultJoin(s1,s2):
        temp_s1=convert(s1)
        temp_s2=convert(s2)
        firstS1=temp_s1.pop(0) #remove first
        lastS2=temp_s2.pop()#remove last 
        if temp_s1==temp_s2 and abs(float(Lcount[firstS1]/N)-float((Lcount[lastS2]/N)))<=SDC:
            last=copy.deepcopy(s2[-1])
            if type(last) is list and len(last)==1:
                if type(s1[0]) is int:                    
                    cand=[]
                    cand.append(copy.deepcopy(s1))
                    cand.append(copy.deepcopy(s2[-1]))
                    candlist.append(cand)

                else:                    
                    cand=copy.deepcopy(s1)+[copy.deepcopy(s2[-1])] 
                    candlist.append(cand)
                    
            else:
                if type(s1[0]) is int: # add the last element at end of list
                    if isinstance(last,list):
                        item=last[-1]
                    else:
                        item=last

                    cand=copy.deepcopy(s1)
                    cand.append(item)
                    candlist.append(cand)                                        



                else:

                    if isinstance(last,list):item=last[-1]
                    else:item=last
                    cand=copy.deepcopy(s1)
                    cand[-1].append(item)
                    candlist.append(cand)



                    
    def FirstMISList(s1, s2):           
            temp_s1 = convert(s1)
            temp_s2 = convert(s2)
            pop_temp_s1 = copy.deepcopy(temp_s1)
            pop_temp_s1.pop(1) #remove s1's 2nd element
            pop_temp_s2 = temp_s2[:-1] #remove last element from s1
            
            if pop_temp_s1 == pop_temp_s2 and MS[temp_s2[-1]]>= MS[temp_s1[0]] and abs(float(Lcount.get(temp_s2[-1])/N)- float(Lcount.get(temp_s1[1])/N)) <= SDC:#check if s1 without element at 2 and s2 without last element are the same
                
                if isinstance(s2[-1], list) and length(s2[-1]) == 1: #l is added at the end of the last element of s1 to form another candidate sequence c2.
                    #if last element of s2 is a list and if its the only element in it     
                    #if s1 is a not a list of lists
                    if isinstance(s1[-1], int): 
                        cand=[]
                        cand.append(copy.deepcopy(s1)) 
                        cand.append(copy.deepcopy(s2[-1]))
                        candlist.append(cand)
                        
                        
                        
                    else: #if s2 is a list
                        cand=copy.deepcopy(s1)+[copy.deepcopy(s2[-1])] #if s2=[[10],[20]] add just the first element of s1 as list to s2 .
                        candlist.append(cand)
                        
                        


                    if length(s1) == 2 and Size(s1) == 2 and temp_s2[-1] > temp_s1[-1]: 
                        #check leng and size of s1 and the last item of s2 is greater than the last item of s1
                        cand=copy.deepcopy(s1)
                        cand[-1].extend(copy.deepcopy(s2[-1]))
                        candlist.append(cand)
                        

                elif (length(s1) == 2 and Size(s1) == 1 and temp_s2[-1] > temp_s1[-1]) or length(s1) > 2:
                    


                    if type(s1[-1]) is int:
                        cand=copy.deepcopy(s1)
                        cand.append(s2[-1])
                        candlist.append(cand)
                        
                        

                    else:
                        last=copy.deepcopy(s2[-1])
                        if isinstance(last,list):item=last[-1]
                        else:item=last
                        cand=copy.deepcopy(s1)
                        cand[-1].append(item)                    
                        candlist.append(cand)            
    for s1 in F:
        for s2 in F:            
            if checkIfFirstMISIsSmallest(s1, MS):                
                FirstMISList(s1, s2)
            elif CheckLastMIS(s2,MS):
                Last_MIS_Less(s1,s2)

            else:
                DefaultJoin(s1,s2)
     
    duplicate=[]
    for i in range(0, len(candlist)-1):
        for j in range(i+1, len(candlist)-2):
            if candlist[i] == candlist[j]:
                duplicate.append(candlist[i])
    for i in duplicate:
        candlist.remove(i)
                
    for c in candlist:
        if not prune(c,MS,F):
            candlist.remove(c)
    return candlist


# In[1157]:


import copy
def prune(c,MS,F):
    def MinMIS(s, MS):
        convert=lambda s2:sum(s2,[]) if type(s2[0]) is list else copy.deepcopy(s2) 
        temp=convert(s)
        Min_MIS=float('inf')
        for item in temp:
            Min_MIS=min(Min_MIS,MS[item])
        return Min_MIS    

    Min_MIS=MinMIS(c, MS)
    if isinstance(c[0],list):
        for I in range(len(c)):
            for item in range(len(c[I])):
                temp=copy.deepcopy(c)                    
                if len(c[I])==1:
                    temp.remove(c[I])
                    if len(temp)==1:temp=temp[0]
                else:
                    temp[I].remove(c[I][item])
                temp_mis=MinMIS(temp, MS)
                if temp_mis==Min_MIS:
                    if temp not in F:
                        return False
                    
    else:
        for i in range(len(c)):
            temp=copy.deepcopy(c)
            temp.remove(c[i])
            temp_mis=MinMIS(temp, MS)
            if temp_mis==Min_MIS:
                if temp not in F:
                    return False
    return True


# In[1158]:


def printOutput(k, F, count):
    file = open("result.txt", "a")
    file.write("\nNo of length :{}  Frequent sequences: {}\n".format(k, len(F)))
    for cand in F:
        cand_string = list(str(cand))
        if isinstance(cand[-1],list):
            cand_string[0] = '<'
            cand_string[-1] = '>'
        else:
            cand_string[0] = '<{'
            cand_string[-1] = '}>'
        for i in range(0, len(cand_string)):
            if(cand_string[i] == '['):
                cand_string[i] = '{'
            if(cand_string[i] == ']'):
                cand_string[i] = '}'
            if(cand_string[i] == ','):
                if(cand_string[i-1] == '}'):
                    cand_string[i] = ''
                    cand_string[i+1] = ''
        cand_string = ''.join(cand_string)
        file.write("{} count: {}\n".format(cand_string, count[str(cand)]))


# In[1159]:


if __name__ =='__main__':main() 


from __future__ import division
import os,csv


#f=open("actual.txt","a+")


#op_file=open('output.txt', 'r')
#f=open('analysis.txt',"a+")

op_file=open('output.txt')
lines = (line.rstrip() for line in op_file) # All lines including the blank ones
lines = (line for line in lines if( not (line.startswith("Filename=") or line=="" ))) # Non-blank lines
#print(list(lines))


def classifier(fpath):
    t=fpath.split("\\")
    fname= "Filename="+"\""+t[len(t)-1]+"\""
    #print("Actaul file name"+fname)
    #print ("\n")
    with open(fpath) as actual_file:
        reader=csv.reader(actual_file)
        for line in reader:
            #f.write(" Actual tag "+line[0]+" pedicted "+op_file.next() )
            if( not line[0]=="act_tag"):
                #print(line[0])
                Actual_tag.append(line[0])



            #f.write("Actual: " + Actual_tag + " Predicted: " + predicted)

            #if(not (predicted=="\n" or predicted.startswith("Filename="))     or   not(Actual_tag.startswith("act_tag"))           ):
                #print(Actual_tag)
                #f.write("Actual: " + Actual_tag + " Predicted: " + predicted)


            #if(not (re.match("Filename=",predicted)  or re.match("act_tag",line[0])  or re.match("\n",predicted)         )):






            #f.write("\n ")

    return





Actual_tag=[]
totaltags=0
topdir="C:\\Users\\Arjun\\Desktop\\USC\\Subjets\\fall2016\\csci544\\Assignment3\\data\\predict"
#topdir=sys.argv[1]
#print(topdir)
exten = '.csv'
for root, dirs, files in os.walk(topdir):
    for file in files:
        if file.endswith(exten):
            fpath = os.path.join(root, file)  # fpath contains the fully qualified path
            classifier(fpath)



#To find accuracy


#print(str(len(Actual_tag)))
#print(str(list(lines)))

not_equal=0
correct_match=0
for act,pred in zip(Actual_tag, list(lines)):
    #f.write(" Actual "+str(act)+ " "  +" Predicted "      +str(pred))
    #f.write("\n")
    if(act==pred):
        correct_match = correct_match + 1
        #print("Correct "+str(act)+ " "+str(pred))

    else:
        not_equal = not_equal + 1
        #print("Un equal match " +str(act)+ " "+str(pred))


#print(not_equal)
#print(correct_match)

total=not_equal+correct_match
#print(total)
#print(correct_match)
accuracy= (correct_match/total)*100

print("Accuracy is:" +str(accuracy))
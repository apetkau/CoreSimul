


import os
import sys


version = sys.version


snake= str(version[0])

if snake=="2":
	print("Launching pipeline with Python 2")
elif snake=="3":
	print("Launching pipeline with Python 3")
else:
	print("Don't know this version of Python. Let's try with 3...")

print("Snake=",snake)


control_file = sys.argv[-1]

for stuff in sys.argv:
	if "master.py" in stuff:
		tmp = stuff.split("/")[-1]
		loc = stuff.split(tmp)[0]
		print("loc= ",loc,stuff)

print("Usage:  python master.py   control.txt")

print(loc)

# Default settings:
parameters={}
parameters["KAPPA"]=1
parameters["OUTPUT"]="output"
parameters["GC"]=50
parameters["LENGTH"]=10000
parameters["DELTA"]=100
parameters["RHO"]=0
parameters["CODONS"]="0.33,0.33,0.33"
parameters["RESCALE"]=1
parameters["SEQUENCE"]="none"
parameters["SUB_MODEL"] = "JC69"
parameters["SUB_RATE"]="none"


f=open(control_file,"r")
for l in f:
	l=l.strip("\n").strip("\r").strip(" ")
	if "=" in l:
		a=l.split("=")
		attribute=a[0]
		if attribute[0] != "#":
			value = a[1].split("#")[0]
			while " " in value:
				value = value.replace(" ","")
			while "\t" in value:
				value = value.replace("\t","")
			#print(value)
			try:
				parameters[attribute]=value
			except KeyError:
				print("Attribute ",attribute ," is not a valid option, ignoring...")

f.close()


#print(parameters)

print("\n### Welcome! ###\n")



path = parameters["OUTPUT"]
if path[-1] != "/":
	path += "/"
L = int(parameters["LENGTH"])
GC = float(parameters["GC"])
coeff = float(parameters["RESCALE"])
kappa = float(parameters["KAPPA"])
DELTA = int(parameters["DELTA"])
COEFF = float(parameters["RHO"])
sub = parameters["CODONS"]
path_to_seq = parameters["SEQUENCE"]
sub_rate = parameters["SUB_RATE"]
model = parameters["SUB_MODEL"]

if model not in ["JC69","K2P","K3P","GTR"]:
	print("Unknown model:",model)
	print("Exiting...")
	exit()

if sub_rate != "none" and model != "K2P":
	kappa=1

if model == "K2P" and sub_rate != "none" and kappa != 1:
	sub_rate = str(kappa)

if model == "JC69":
	kappa=1

if model == "GTR" or model == "K3P": 
	if sub_rate == "none":
		print("NO RATES PROVIDED FOR ",model," model. Switching to JC69")
		model = "JC69"

if model == "JC69":
	sub_rate="none"


if model == "K2P" and "," in str(sub_rate):
	print("Invalid SUB_RATE option for K2P model:",sub_rate)
	print("1 parameter expected")
	print("Exiting...")
	exit() 
elif model == "K3P" and  sub_rate.count(",") != 2:
	print("Invalid SUB_RATE option for K3P model:",sub_rate)
	print("3 parameters expected")
	print("Exiting...")
	exit() 
elif model == "GTR" and  sub_rate.count(",") != 5:
	print("Invalid SUB_RATE option for GTR model:",sub_rate)
	print("6 parameters expected")
	print("Exiting...")
	exit() 


while " " in sub:
	sub=sub.replace(" ","")

if "TREE" in parameters:
	TREE = parameters["TREE"]
else:
	print("A tree is needed for the simulations. Please come back with a tree. Exiting...")
	exit()



if snake=="2":
	try:
		os.mkdir(path)
	except OSError:
		print("Output folder already exists. Previous files will be lost.")
else:
	try:
		os.mkdir(path)
	except FileExistsError:
		print("Output folder already exists. Previous files will be lost.")



print("1. Reading the tree")
os.system("python " +  loc + "extract_names.py " + path + " " + TREE)



print("2. Extracting branch lengths and topology")

os.system("python " + loc + "branch_length.py " + path  + " renamed.tree"  )




print("3. Simulating")

print("\n################")
print("PARAMETERS: ")
print("OUTPUT= ",path)
print("Alignment Length= ",L,"bp")
print("GC%= ",GC,"% (default=50%)")
print("Branch rescaling= ",coeff," (default=1, no rescaling)")
print("Transition/Transversion bias, Kappa= ",kappa," (default=1, no bias)")
print("CODONS Frequency= ",sub,"")
print("STARTING GENOME= ",path_to_seq)
print("SUBSTITUTION MODEL= ",model, "with rate(s) ",sub_rate)
print("################\n")


os.system("python " + loc + "simulation.py " + model + " " + sub_rate + " "  + path_to_seq + " " + sub + " " + str(kappa) + " " + str(GC) + " " + str(L) +  " " + str(COEFF) + " " + str(DELTA) + " "  + str(coeff) + " " + path)
















import sys, json
from pprint import pprint
#from collections import namedtuple as nt

try:
    input_filename = str(sys.argv[1])
except IndexError:
    print("Missing input file!")
    sys.exit()

input_file = open(input_filename)

class dataStruct():
    def __init__(self,param):
        self.V = int(param[0])
        self.S = int(param[1])
        self.C = int(param[2])
        self.P = int(param[3])
        self.Providers = []
        self.Services = []
        self.Countries = []
        self.Projects = []

    def addProvider(self,provider):
        self.Providers.append(provider)
        #self.Providers.insert(len(self.Providers),provider)
    
    def addService(self,service):
        self.Services.append(str(service))

    def addCountry(self,country):
        self.Countries.append(str(country))

    def addProject(self,project):
        self.Projects.append(project)

    def printAll(self):
        print("Parametri iniziali: V: {}, S: {}, C: {}, P: {}".format(self.V,self.S,self.C,self.P))
        print("Servizi: {}".format(self.Services))
        print("Paesi: {}".format(self.Countries))
        print("Providers:\n")
        for index, p in enumerate(self.Providers):
            print("[{}] Provider: {}".format(index,p[0]))
            for index, r in enumerate(p[1:]): # skippa il primo elemento = nome del provider
                print("\t[{}] Region: {}".format(index,r[0]))
                print("\t\tavailability_packages: {}".format(r[1]))
                print("\t\tpackages_unit_cost: {}".format(r[2]))
                print("\t\tunits_of_services_per_package: {}".format(r[3]))
                print("\t\tlatencies: {}".format(r[4]))
                print("\t\toriginal_position: {}".format(r[5]))
        print("Progetti:")
        for index, p in enumerate(self.Projects):
            print("[{}] Penality: {}, Paese: {}, Servizi: {}".format(index,p[0],p[1],p[2]))
    
    def printToFile(self):
        data = self.printAll()
        output_filename = input_filename.split('/')[-1][:-3]
        with open(output_filename + ".out",'w') as fl:
            fl.write(json.dumps(data))
            fl.close()


# -- FIRST LINE -- #
first_line = input_file.readline().strip()
vscp = first_line.split(' ',4)
data = dataStruct(vscp)

# -- SECOND LINE -- #
second_line = input_file.readline().strip()
services_list = second_line.split(' ',data.S)
for service in services_list:
    data.addService(service)

# -- THIRD LINE -- #
third_line = input_file.readline().strip()
countries_list = third_line.split(' ',data.C)
for country in countries_list:
    data.addCountry(country)

# -- FOURTH LINE -- # 
# # -- PROVIDERS BLOCK -- # #
for v in range(data.V):
    first_provider_line = input_file.readline().strip()
    provider_data = first_provider_line.split(' ',2)
    provider_name = str(provider_data[0])
    num_region = int(provider_data[1])
    provider = []
    provider.append(provider_name)
    # # # -- REGIONS BLOCK -- # # #
    for r in range(num_region):
        region_name_line = input_file.readline().strip()
        region_name = region_name_line.split(' ',1)[0] # <-
        region_line = input_file.readline().strip()
        region_data = region_line.split(' ',2+data.S)
        region = []
        region.append(region_name)        
        region.append(int(region_data[0])) # availability_packages
        region.append(float(region_data[1])) # packages_unit_cost
        # # # # -- SERVICES IN REGION BLOCK -- # # # #
        units_of_services_per_package = []  
        for s in range(data.S):
            units_of_services_per_package.append(int(region_data[s+2]))
        region.append(units_of_services_per_package)
        # # # # -- LATENCIES IN REGION BLOCK -- # # # #
        latencies_line = input_file.readline().strip()
        latencies = latencies_line.split(' ',data.C)
        latenc = []
        for c in range(data.C):
            latenc.append(int(latencies[c]))
        region.append(latenc)
        region.append(r)
        provider.append(region)
    data.addProvider(provider)

# -- PROJECTS BLOCK -- #
for p in range(data.P):
    project_line = input_file.readline().strip()
    project_data = project_line.split(' ',2+data.S)
    unit_needed = []
    for s in range(data.S):
        unit_needed.append(int(project_data[s+2]))
    project = [
        int(project_data[0]), # 'penality': 
        project_data[1], # 'country':
        unit_needed #'unit_needed':
    ]
    data.addProject(project)

input_file.close()
data.printAll()

import cloud_adventure 

M = cloud_adventure.getMatrixP(data, data.Projects[0])
def printMatrix(M):
    for v in M.C:
        print(v, end=' ')
    print('')
    for i in range(len(M.C)):
        print('_', end=' ')
    print('')
    for row in range(len(M.A)):
        for col in range(len(M.A[0])):
            print(M.A[row][col], end=' ')
        print("<= ", M.B[row])

printMatrix(M)
		
from scipy import optimize
import math

res = optimize.linprog(M.C, M.A, M.B)

if(res.status == 0): #print output for the challenge
    c_row = 0
    provider_count = 0
    '''for p_name, provider in data['providers'].items():
        region_c = 0
        for r_name, region in provider['regions'].items():
            if(res.x[c_row] != 0):
                print(provider_count, "(", p_name, ") ", region_c, "(", r_name, ") ", int(math.ceil(res.x[c_row])), end=' ')
            c_row += 1
            region_c += 1
        provider_count += 1
    '''
    for provider in data.Providers:
        region_c = 0
        for region in provider[1:]:
            if(res.x[c_row] != 0):
                print(provider_count, "(", provider[0], ") ", region_c, "(", region[0], ") ", int(math.ceil(res.x[c_row])), end=' ')
            c_row += 1
            region_c += 1
        provider_count += 1
    
    print('')
else:
    print("status: ", res.status)
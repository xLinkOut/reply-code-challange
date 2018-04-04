import sys, json
from pprint import pprint

try:
    input_filename = str(sys.argv[1])
except IndexError:
    print("Missing input file!")
    sys.exit()

input_file = open(input_filename)

data = {
    'param': {'V': 0,'S': 0,'C': 0,'P': 0},
    'services': {},
    'countries': {},
    'providers': {},
    'projects': {}
}

# -- FIRST LINE -- #
first_line = input_file.readline().strip()
vscp = first_line.split(' ',4)
data['param']['V'] = int(vscp[0])
data['param']['S'] = int(vscp[1])
data['param']['C'] = int(vscp[2])
data['param']['P'] = int(vscp[3])

# -- SECOND LINE -- #
second_line = input_file.readline().strip()
services_list = second_line.split(' ',data['param']['S'])
for service in services_list:
    data['services'][services_list.index(service)] = service

# -- THIRD LINE -- #
third_line = input_file.readline().strip()
countries_list = third_line.split(' ',data['param']['C'])
for country in countries_list:
    data['countries'][countries_list.index(country)] = country

# -- FOURTH LINE -- # 
# # -- PROVIDERS BLOCK -- # #
for v in range(data['param']['V']):
    first_provider_line = input_file.readline().strip()
    provider_data = first_provider_line.split(' ',2)
    provider_name = str(provider_data[0])
    data['providers'][provider_name] = {
        'num_region': int(provider_data[1]),
        'regions': {},
    }
    # # # -- REGIONS BLOCK -- # # #
    for r in range(data['providers'][provider_name]['num_region']):
        region_name_line = input_file.readline().strip()
        region_name = region_name_line.split(' ',1)[0]
        region_line = input_file.readline().strip()
        region_data = region_line.split(' ',2+data['param']['S'])
        data['providers'][provider_name]['regions'][region_name] = {
            'availability_packages': int(region_data[0]),
            'packages_unit_cost':  float(region_data[1]),
            'units_of_services_per_package': {},
            'latencies': {}
        }
        # # # # -- SERVICES IN REGION BLOCK -- # # # # 
        for s in range(data['param']['S']):
            data['providers'][provider_name]['regions'][region_name]['units_of_services_per_package'][s] = int(region_data[s+2])
        # # # # -- LATENCIES IN REGION BLOCK -- # # # #
        latencies_line = input_file.readline().strip()
        latencies = latencies_line.split(' ',data['param']['C'])
        for c in range(data['param']['C']):
            data['providers'][provider_name]['regions'][region_name]['latencies'][c] = latencies[c]

# -- PROJECTS BLOCK -- #
for p in range(data['param']['P']):
    project_line = input_file.readline().strip()
    project_data = project_line.split(' ',2+data['param']['S'])
    unit_needed = {}
    for s in range(data['param']['S']):
        unit_needed[s] = int(project_data[s+2])
    project = {
        'penality': project_data[0],
        'country': project_data[1],
        'unit_needed': unit_needed
    }
    data['projects'][p] = project

#print(json.dumps(data))

#output_filename = input_filename.split('/')[-1][:-3]
#with open(output_filename + ".json",'w') as fl:
#    fl.write(json.dumps(data))
#    fl.close()

#input_file.close()

import cloud_adventure 

M = cloud_adventure.getMatrixP(data, data['projects'][0])
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
    for p_name, provider in data['providers'].items():
        region_c = 0
        for r_name, region in provider['regions'].items():
            if(res.x[c_row] != 0):
                print(provider_count, "(", p_name, ") ", region_c, "(", r_name, ") ", int(math.ceil(res.x[c_row])))
            c_row += 1
            region_c += 1
        provider_count += 1
else:
    print("status: ", res.status)

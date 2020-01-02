from sys import argv
from os.path import exists
from json import dumps

try:
    input_filename = argv[1]
    if not exists(input_filename):
        raise FileNotFoundError
except IndexError:
    exit("Missing input filename!")
except FileNotFoundError:
    exit("Input file not found!")

class Problem:

    def __init__(self,V,S,C,P):
        self.V = int(V) # Number of providers
        self.S = int(S) # Number of services
        self.C = int(C) # Number of countries
        self.P = int(P) # Number of projects

        # Constraints
        if not 1 <= self.V <= 20: raise self.ConstraintException('V')
        if not 1 <= self.S <= 500: raise self.ConstraintException('S')
        if not 1 <= self.C <= 20: raise self.ConstraintException('C')
        if not 1 <= self.P <= 100000: raise self.ConstraintException('P')

    def set_services(self,services):
        self.services = services # Save services names

    def set_countries(self,countries):
        self.countries = countries # Save countries names

    def create_providers(self):
        self.providers = dict()

    def set_provider(self,provider_name):
        self.providers[provider_name] = dict() 

    def set_provider_region(self,provider_name,region_name,region_info,latencies):
        self.providers[provider_name].update({
            region_name: {
                'available_packages': region_info[0],
                'package_unit_cost': region_info[1],
                'units_of_service_per_package': region_info[2:],
                'latencies': latencies
            }
        })
    
    def create_projects(self):
        self.projects = list()

    def set_project(self,penality,country_name,units):
        self.projects.append({
            'country': country_name,
            'penality': penality,
            'units': units
        })
    
    def pretty_print_providers(self):
        print(dumps(self.providers,indent=2,separators=(',', ': ')))
        
    def pretty_print_projects(self):
        print(dumps(self.projects,indent=2,separators=(',', ': ')))

    class ConstraintException(Exception):
        pass

with open(input_filename,'r') as input_file:
    # .readline() read one line and step
    # .replace('\n') remove last new line character

    first_line = input_file.readline().replace('\n','')
    global_parameters = first_line.split(' ')
    problem = Problem(*global_parameters)
    print(problem.V,problem.S,problem.C,problem.P)

    second_line = input_file.readline().replace('\n','')
    services = second_line.split(' ')
    problem.set_services(services)
    print(problem.services)

    third_line = input_file.readline().replace('\n','')
    countries = third_line.split(' ')
    problem.set_countries(countries)
    print(problem.countries)

    problem.create_providers()
    for v in range(problem.V):
        # Each line represent one provider
        first_v_line = input_file.readline().replace('\n','')
        provider_name, num_of_regions = first_v_line.split(' ')
        problem.set_provider(provider_name)
        print(provider_name,num_of_regions)
        for r in range(int(num_of_regions)):
            first_r_line = input_file.readline().replace('\n','')
            region_name = first_r_line

            second_r_line = input_file.readline().replace('\n','')
            region_info = second_r_line.split(' ')
            # region_info[0] = <int> total number of available packages
            # region_info[1] = <float> cost of single package
            # region_info[2:S] = <int> number of units of the i-esim service available in each package

            third_r_line = input_file.readline().replace('\n','')
            latencies = third_r_line.split(' ')
            # latencies[i] = <int> latency between that region and the i-esim country

            problem.set_provider_region(provider_name,region_name,region_info,latencies)
            #print(problem.providers[provider_name][region_name])
        print(problem.providers[provider_name])
    #print(problem.pretty_print_providers())
        
    problem.create_projects()
    for p in range(problem.P):
        first_p_line = input_file.readline().replace('\n','')
        project_info = first_p_line.split(' ')
        # project_info[0] = <int> base penality applied fot violating the SLA
        # project_info[1] = <str> country that will use the project
        # project_info[2:S] = <int> amount of unit needed for each service type

        problem.set_project(project_info[0],project_info[1],project_info[2:])
        print(problem.projects[p])
    #print(problem.pretty_print_projects())

print("Parser done.")
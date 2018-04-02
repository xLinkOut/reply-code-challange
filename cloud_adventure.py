from pprint import pprint

#Avarange project latency, vector vector matrix
def APL(pkgs, Ls, Us):
    num = 0
    den = 0
    i = 0
    for pkg in pkgs:
        n = 0
        for Ur in Us[i]:
            n += Ur
        n *= pkg
        den += n
        num += (n * Ls[i])
        i += 1
    if den == 0:
        return 0
    return float(num) / float(den)

#print ("Avarange project latency: ", APL([1, 3], [125, 130], [[1, 2], [5, 3]]))

#Overall availability index
def AI(qs):
    num = 0
    den = 0
    for qi in qs:
        num += qi
        den += (qi * qi)
    if den == 0:
        return 0
    return num / den

def OAI(Us):
    tot = 0
    for qs in Us:
        tot += AI(qs)
    return tot / len(Us)

#Operational Project Cost
def OPC(pkgs, fees):
    tot = 0
    i = 0
    for fee in fees:
        tot += (pkgs[i] * fee)
        i += 1
    return tot

#fine related to service
def Fp(bpps, Usn, Ssau):
    tot = 0
    i = 0
    for bpp in bpps:
        if(Usn[i] != 0):
            tot += (bpp * (Usn[i] - min(Usn[i], Ssau[I])) / Usn[i])
        i += 1
    return tot / i

class linprogMatrix(object):
    A = []
    B = []
    C = []

    def __init__(self, Ac, Ar, Br, Cc):
        self.A = [[0 for col in range(Ac)] for row in range(Ar)]
        self.B = [0 for row in range(Br)]
        self.C = [0 for col in range(Cc)]


def getMatrixP(obj, project):
#pprint(obj['providers'])
    pr = 0
    S = obj['param']['S']
    for k, provider in obj['providers'].items():
        pr += provider['num_region']

    res = linprogMatrix(pr, S + pr, S + pr, pr)

    col = 0
    row = 0
    rowb = 0
    
    for k, u in project['unit_needed'].items():
        res.B[rowb] = -u
        rowb += 1

    for k, provider in obj['providers'].items():
        for k, region in provider['regions'].items():
            pprint(region)
            row = 0
            for k, pkgu in region['units_of_services_per_package'].items():
                res.A[row][col] = -pkgu
                row += 1
            col += 1
            res.B[rowb] = region['availability_packages']
            rowb +=1
    
    col = 0
    for k, provider in obj['providers'].items():
        for k, region in provider['regions'].items():
            res.A[row][col] = 1
            row += 1
            col += 1

    return res
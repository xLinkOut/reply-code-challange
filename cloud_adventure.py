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
    S = obj.S
    for provider in obj.Providers:
        pr += len(provider)

    res = linprogMatrix(pr, S + pr, S + pr, pr)

    col = 0
    row = 0
    rowb = 0
    col_lim = 0
    for service in project[2]:
        res.B[rowb] = -service
        rowb += 1

    for provider in obj.Providers:
        for region in provider[1:]:
            cumulate = 0
            row = 0
            for pkgu in region[3]: #units service needed
                res.A[row][col] = -pkgu
                cumulate += pkgu
                row += 1
            res.B[rowb] = region[1] # availability packg

            # euristic
            res.C[col] = region[2] / cumulate
            # end euristic
            res.A[rowb][col] = 1
            rowb +=1
            col += 1

    return res

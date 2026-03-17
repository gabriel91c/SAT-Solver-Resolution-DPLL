def is_tautology(clause):
    return any(-lit in clause for lit in clause)

def print_clause(C):
    return "{" + ", ".join(f"P{abs(l)}" + ("'" if l < 0 else "") for l in C) + "}"



def resolution(K):
    proof = []
    K = [frozenset(c) for c in K]
    new = set()

    while True:
        pairs = [(Ci, Cj) for Ci in K for Cj in K if Ci != Cj]

        for (Ci, Cj) in pairs:
            for literal in Ci:
                if -literal in Cj:
                    resolvent = (Ci - {literal}) | (Cj - {-literal})

                    if is_tautology(resolvent):
                        proof.append(f"Tautology discarded: {print_clause(resolvent)}")
                        continue

                    resolvent_fs = frozenset(resolvent)

                    proof.append(f"Resolvent from {print_clause(Ci)} and {print_clause(Cj)} = {print_clause(resolvent)}")

                    if not resolvent:
                        proof.append("EMPTY CLAUSE DERIVED → UNSAT")
                        return False, proof

                    if resolvent_fs not in K and resolvent_fs not in new:
                        new.add(resolvent_fs)

        if new.issubset(K):
            proof.append("No new clauses → SAT")
            return True, proof

        K.extend(new)


def DP(K):
    proof = []
    K = [set(c) for c in K]

    while True:
        units = [c for c in K if len(c) == 1]
        if units:
            L = next(iter(units[0]))
            proof.append(f"UNIT CLAUSE: {print_clause({L})}")

            newK = []
            for C in K:
                if L in C:
                    proof.append(f"Delete clause (contains {print_clause({L})}): {print_clause(C)}")
                    continue
                if -L in C:
                    C2 = C - {-L}
                    proof.append(f"Delete {print_clause({-L})} from {print_clause(C)} → {print_clause(C2)}")
                    if not C2:
                        proof.append("EMPTY CLAUSE → UNSAT")
                        return False, proof
                    newK.append(C2)
                else:
                    newK.append(C)
            K = newK
            continue

        lits = set(l for C in K for l in C)
        for L in lits:
            if -L not in lits:
                proof.append(f"PURE LITERAL: {print_clause({L})}")
                K = [C for C in K if L not in C]
                continue

        sat, resolproof = resolution(K)
        proof.extend(["RESOLUTION CALLED:"] + resolproof)
        return sat, proof


def DPLL(K, proof=None, depth=0):
    indent = "  " * depth
    if proof is None:
        proof = []

    proof.append(indent + f"Current K = {[print_clause(c) for c in K]}")

    if not K:
        proof.append(indent + "Empty clause-set → SAT branch")
        return True, proof

    for C in K:
        if not C:
            proof.append(indent + "EMPTY CLAUSE → UNSAT branch")
            return False, proof

    for C in K:
        if len(C) == 1:
            L = next(iter(C))
            proof.append(indent + f"Unit propagate {print_clause({L})}")
            return DPLL(assign_literal(K, L, proof, indent), proof, depth)

    lits = set(l for C in K for l in C)
    for L in lits:
        if -L not in lits:
            proof.append(indent + f"Pure literal {print_clause({L})}")
            return DPLL(assign_literal(K, L, proof, indent), proof, depth)

    L = next(iter(K[0]))   
    proof.append(indent + f"Split on {print_clause({L})}")

    sat, proof = DPLL(assign_literal(K, L, proof, indent), proof, depth + 1)
    if sat:
        return True, proof

    sat, proof = DPLL(assign_literal(K, -L, proof, indent), proof, depth + 1)
    return sat, proof


def assign_literal(K, literal, proof, indent):
    K2 = []
    for C in K:
        if literal in C:
            proof.append(indent + f"Clause satisfied by {print_clause({literal})}: {print_clause(C)}")
            continue
        if -literal in C:
            C2 = C - {-literal}
            proof.append(indent + f"Remove {print_clause({-literal})} from {print_clause(C)} → {print_clause(C2)}")
            K2.append(C2)
        else:
            K2.append(C)
    return K2



if __name__ == "__main__":

    K = [
        {1, -2, 3},
        {-1, 3, 4},
        {3, -6},
        { -3, -4, 1 },
        {-2, -5},
        {-2, 5},
        {-3, 6}
    ]

    sat, proof = DP(K)
    print("=== DP RESULT ===")
    print("SATISFIABLE" if sat else "UNSATISFIABLE")
    print("\n".join(proof))

    sat, proof = DPLL(K)
    print("\n=== DPLL RESULT ===")
    print("SATISFIABLE" if sat else "UNSATISFIABLE")
    print("\n".join(proof))

from typing import List, Tuple, Callable
from compsoc.profile import Profile
from compsoc.voter_model import get_profile_from_model, generate_distorted_from_normal_profile
from compsoc.voting_rules.borda import borda_rule
from compsoc.voting_rules.borda_gamma import get_borda_gamma
from compsoc.voting_rules.copeland import copeland_rule
from compsoc.voting_rules.dowdall import dowdall_rule
from compsoc.voting_rules.simpson import simpson_rule
from voting_rules.dictatorship import dictatorship_rule
from voting_rules.oligarchies import oligarchies_rule
from voting_rules.unanimity import unanimity_rule
from voting_rules.plurality import plurality_rule
from criteria.anonymity import anonymity_check
from criteria.neutrality import neutrality_check
from criteria.monotonicity import monotonicity_check
from criteria.pareto import pareto_check
from criteria.unanimity import unanimity_check
from criteria.ni import ni_check
import global_value as g



borda_rule.__name__ = "Borda"
copeland_rule.__name__ = "Copel"
dictatorship_rule.__name__="Dicta"
oligarchies_rule.__name__="Oliga"
plurality_rule.__name__="Plura"
unanimity_rule.__name__="Unani"

rules=[unanimity_rule,plurality_rule,oligarchies_rule,dictatorship_rule,borda_rule,copeland_rule]
#rules=[borda_rule,plurality_rule]

R=len(rules)
all_results=[["***"]]+[[rule.__name__] for rule in rules]
criteria=["anonymity","neutrality","monotonicity","pareto","unanimity","non-imposition"]
#criteria=["neutrality"]
C=len(criteria)
for ari in all_results:
    ari +=["---" for _ in range(C)]
for i in range(C):
    all_results[0][i+1]=criteria[i]
def ooz(b):
    if b:
        return 1
    else:
        return 0
rep=1000
candidatess=[6]
voterss=[1000]
topns=[1]
voter_models=["unani"]
distortions=[0.2]
verbose=False

g.neu=False
g.ano=False
for voters in voterss:
    for candidates in candidatess:
        for topn in topns:
            for voter_model in voter_models:
                for distortion in distortions:
                    for c in criteria:
                        if c=="anonymity":
                            all_results=anonymity_check(rules,all_results,rep,candidates,voters,topn,voter_model,distortion,verbose)
                        elif c=="neutrality":
                            all_results=neutrality_check(rules,all_results,rep,candidates,voters,topn,voter_model,distortion,verbose)
                        elif c=="monotonicity":
                            all_results=monotonicity_check(rules,all_results,rep,candidates,voters,topn,voter_model,distortion,verbose)
                        elif c=="pareto":
                            all_results=pareto_check(rules,all_results,rep,candidates,voters,topn,voter_model,distortion,verbose)
                        elif c=="unanimity" and voter_model=="unani":
                            all_results=unanimity_check(rules,all_results,rep,candidates,voters,topn,voter_model,distortion,verbose)
                        elif c=="non-imposition":
                            all_results=ni_check(rules,all_results,rep,candidates,voters,topn,voter_model,distortion,verbose)
                    print("rep:",rep,", candidates:",candidates,", voters:",voters,", topn:",topn,", voter_model:",voter_model,", distortion:",distortion,", verbose:",verbose,sep="")
                    output="[*******"
                    for ri in all_results[0][1:]:
                        output+=",'"+ri[:3]+"'"
                    print(output+"]")
                    for r in all_results[1:]:
                        print(r)

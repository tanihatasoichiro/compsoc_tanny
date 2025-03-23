from compsoc.profile import Profile
import random
import global_value as g
def dictatorship_rule(profile: Profile, candidate: int) -> int:
    
    top_score = len(profile.candidates) - 1
    # Get pairwise scores
    scores = 0
    dictator=list(profile.pairs)[g.num]
    #print(dictator,g.num)
    po=dictator[1]
    if g.neu:
        po=[g.nsigma[i] for i in po]
        if g.nsigma[candidate] in po:
                    scores += (top_score - po.index(g.nsigma[candidate]))
    else:
        if candidate in po:
                    scores += (top_score - po.index(candidate))
        
    return scores

"""
Computes the Borda score for a candidate.
"""
from compsoc.profile import Profile
import global_value as g
import random
def plurality_rule(profile: Profile, candidate: int) -> int:
    
    top_score = len(profile.candidates) - 1

    # Get pairwise scores
    scores = 0
    
    if g.ano:
            ps=random.sample(list(profile.pairs),len(profile.pairs))
    else:
            ps=profile.pairs
    
    
#     if g.neu:
#           for pair in ps:
#                 po=[g.nsigma[i] for i in pair[1]]
#                 if candidate in po:
#                         scores += pair[0] * (top_score - po.index(candidate))
#     else:
          
    for pair in ps:
                if candidate==pair[1][0]:
                        scores += pair[0]
    
    # return the total score
    return scores

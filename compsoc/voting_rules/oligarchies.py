from compsoc.profile import Profile
import global_value as g
def oligarchies_rule(profile: Profile, candidate: int) -> int:
    #An easy way is to pick a subset of voters k from [1…n] with top_k(P)=x and make V(P)=x
    top_score = len(profile.candidates) - 1
    # Get pairwise scores
    scores = 0
    oligarchy=list(profile.pairs)[g.num]
    #oligarchies=[i for i in oligarchy if i[1][0]==oligarchy[g.num][1][0]]
    if candidate in oligarchy[1]:
        scores += (top_score - oligarchy[1].index(candidate))
    
    return scores
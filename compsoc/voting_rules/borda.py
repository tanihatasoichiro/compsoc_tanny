"""
Computes the Borda score for a candidate.
"""
from compsoc.profile import Profile
import global_value as g
import random
def borda_rule(profile: Profile, candidate: int) -> int:
    """
    Calculates the Borda score for a candidate based on a profile.

    :param profile: The voting profile.
    :type profile: VotingProfile
    :param candidate: The base candidate for scoring.
    :type candidate: int
    :return: The Borda score for the candidate.
    :rtype: int
    """
    # Max score to be applied with borda count
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
                if candidate in pair[1]:
                        scores += pair[0] * (top_score - pair[1].index(candidate))
    
    # return the total score
    return scores

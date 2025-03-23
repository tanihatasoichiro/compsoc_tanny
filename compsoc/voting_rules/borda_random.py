"""
Borda random
"""
import random
from compsoc.profile import Profile
import global_value as g

def borda_random_gamma(profile: Profile, candidate: int) -> float:
    """
    Calculates the Borda random decay (gamma) score for a
    candidate based on a profile.
    Author: Shunsuke O.

    :param profile: The voting profile.
    :type profile: VotingProfile
    :param candidate: The base candidate for scoring.
    :type candidate: int
    :return: The Borda random gamma score for the candidate.
    :rtype: float
    """
    
    if g.ano:
            ps=random.sample(list(profile.pairs),len(profile.pairs))
    else:
            ps=profile.pairs
    gamma = random.random()
    if g.neu:
            scores=[]
            for pair in ps:
                po=[g.nsigma[i] for i in pair[1]]
                scores.append(pair[0] * (gamma ** po.index(candidate) if candidate in pair[1] else 0.0))
    else:
            scores = [pair[0] * (gamma ** pair[1].index(candidate) if candidate in pair[1] else 0.0)
                    for pair in ps]
    return sum(scores)

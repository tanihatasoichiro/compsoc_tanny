"""
Computes the Dowdall score for a candidate.
"""
from compsoc.profile import Profile
import global_value as g
import random

def dowdall_rule(profile: Profile, candidate: int) -> int:
    """
    Calculates the Dowdall score for a candidate based on a profile.

    :param profile: The voting profile.
    :type profile: VotingProfile
    :param candidate: The base candidate for scoring.
    :type candidate: int
    :return: The Dowdall score for the candidate.
    :rtype: int
    """
    top_score = len(profile.candidates) - 1
    # Get pairwise scores
    
    if g.ano:
            ps=random.sample(list(profile.pairs),len(profile.pairs))
    else:
            ps=profile.pairs
    if g.neu:
        candidate=g.nsigma[candidate]
        
    scores = [pair[0] * ((top_score - pair[1].index(candidate)) / (
                pair[1].index(candidate) + 1)) if candidate in pair[1] else 0.0
                for pair in ps]
    # Return the total score
    return sum(scores)

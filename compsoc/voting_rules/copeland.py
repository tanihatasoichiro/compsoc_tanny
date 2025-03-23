"""
Computes the Copeland score for a candidate.
"""
import numpy as np
from compsoc.profile import Profile
import global_value as g

def copeland_rule(profile: Profile, candidate: int) -> int:
    """
    Calculates the Copeland score for a candidate based on a profile.

    :param profile: The voting profile.
    :type profile: VotingProfile
    :param candidate: The base candidate for scoring.
    :type candidate: int
    :return: The Copeland score for the candidate.
    :rtype: int
    """
    scores = []
    for m in profile.candidates:
        if g.neu:
            preference = profile.get_net_preference(g.nsigma[candidate],
                                                g.nsigma[m])  # preference over m
        else:
            preference = profile.get_net_preference(candidate,
                                                m)  # preference over m
        scores.append(np.sign(preference))  # win or not
    # Return the total score
    return sum(scores)

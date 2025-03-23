"""
Computes the Simpson score for a candidate.
"""

from compsoc.profile import Profile
import global_value as g

def simpson_rule(profile: Profile, candidate: int) -> int:
    """
    Calculates the minimum pairwise score of a candidate using the Simpson rule.

    :param profile: The voting profile.
    :type profile: VotingProfile
    :param candidate: The base candidate for scoring.
    :type candidate: int
    :return: The minimum pairwise score of the candidate among all other candidates.
    :rtype: int
    """
    # Get pairwise scores
    if g.neu:
        scores = [profile.get_net_preference(g.nsigma[candidate], g.nsigma[m]) for m in
              profile.candidates - {g.nsigma[candidate]}]
    else:
        scores = [profile.get_net_preference(candidate, m) for m in
              profile.candidates - {candidate}]
    # Return the minimum score in scores
    return min(scores)

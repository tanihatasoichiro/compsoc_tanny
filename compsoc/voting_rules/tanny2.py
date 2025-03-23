"""
Computes the Borda score for a candidate.
"""
from compsoc.profile import Profile
import numpy as np
def tanny2_rule(profile: Profile, candidate: int) -> int:
    top_score = len(profile.candidates) - 1
    # Get pairwise scores
    para=10.5
    scores = [pair[0] * ((top_score - pair[1].index(candidate)+(top_score - pair[1].index(candidate))//para) / (pair[1].index(candidate) + para)) if candidate in pair[1] else 0.0 for pair in profile.pairs]
    # Return the total score
    return sum(scores)
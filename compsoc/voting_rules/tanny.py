"""
Computes the Borda score for a candidate.
"""
from compsoc.profile import Profile
import math
import numpy as np

def tanny_rule(profile: Profile, candidate: int) -> int:
    top_score = len(profile.candidates) - 1
    # Get pairwise scores
    para=5
    scores = [pair[0] * ((top_score - para*(pair[1].index(candidate)//para))/ ((pair[1].index(candidate))*para+1)) if candidate in pair[1] else 0 for pair in profile.pairs]
    # Return the total score
    return sum(scores)
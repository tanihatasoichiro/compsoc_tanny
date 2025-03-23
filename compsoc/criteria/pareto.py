from typing import List, Tuple, Callable
from compsoc.profile import Profile
from compsoc.voter_model import get_profile_from_model, generate_distorted_from_normal_profile
import random
import global_value as g

def voter_subjective_utility_for_elected_candidate(elected: List[int], vote: Tuple[int],
                                                   topn: int) -> tuple:
    # Gain, based on original vote (utility) and elected candidate
    # Given a particular vote structure (ranking), return its utility
    # knowing the elected candidate
    num_candidates = len(elected)
    utility_increments = [(num_candidates - i) / (num_candidates * 1.0) for i in range(num_candidates)]
    
    my_best = vote[0]  # utility for the top only
    utility_for_top = utility_increments[elected.index(my_best)]
    # Utility for my top n candidate
    total_utility = 0.0
    for i in range(min(topn, len(vote))):
        total_utility += utility_increments[elected.index(vote[i])]
    return utility_for_top, total_utility

def get_ranking(profile: Profile,
                     rule: Callable[[Profile, int], any],
                     topn: int,
                     verbose=False):
    g.ano=False
    g.neu=False
    rule_name = rule.__name__
    ranking = profile.ranking(rule)
    
    elected_candidates = [c[0] for c in ranking]
    if verbose:
        print(f"Ranking based on '{rule_name}' gives {ranking} with winners {elected_candidates}")
        print("======================================================================")
    total_u, total_u_n = 0., 0.
    """if verbose:
        print("Counts \t Ballot \t Utility of first")"""
    for pair in profile.pairs:

        u, u_n = voter_subjective_utility_for_elected_candidate(elected_candidates, pair[1],topn=topn)
        """if verbose:
            print(f"{pair[0]} \t {pair[1]} \t {u}")"""
        total_u += pair[0] * u
        total_u_n += pair[0] * u_n
    if verbose:
        print("Total : ", total_u)
    return [rule_name,elected_candidates]

def pareto_check(rules: list,all_result: list,rep,num_candidates: int,
                          num_voters: int,
                          topn: int,
                          voters_model: str,
                          distortion_ratio: float = 0.0,
                          verbose: bool = False
                          ) -> dict[str, dict[str, float]]:
 
    tf_s=[[rule.__name__,True] for rule in rules]
    s="pareto"
    profile = get_profile_from_model(num_candidates, num_voters, voters_model)
    profile.distort(distortion_ratio)
    g.num=random.randrange(0,len(profile.pairs))

    for _ in range(rep):
        profile = get_profile_from_model(num_candidates, num_voters, voters_model)
        profile.distort(distortion_ratio)
        if verbose:
            print(profile.pairs)
        pre=set(list(range(num_candidates)))
        result=[get_ranking(profile, rule, topn, verbose) for rule in rules]
        for i in range(len(result)):
            winner=result[i][1][0]
            for pair in profile.pairs:
                if winner in pair[1]:
                    index=pair[1].index(winner)
                else:
                    index=-1
                pre &=set(pair[1][:index])
                if len(pre)==0:
                    break
            tf_s[i][1]=len(pre)==0
    n=all_result[0].index(s)
    for i in range(len(rules)):
        all_result[i+1][n]=tf_s[i][1]
    return all_result

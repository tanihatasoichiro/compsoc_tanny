
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

def get_rule_utility(profile: Profile,
                     rule: Callable[[Profile, int], any],
                     topn: int,
                     verbose=False):
    """
    Calculates the total utility and "top n" utility for a given rule.

    :param profile: The voting profile.
    :type profile: Profile
    :param rule: The voting rule function.
    :type rule: Callable[[int], int],# | float],
    :param topn: The number of top candidates to consider for utility calculation.
    :type topn: int
    :param verbose: Print additional information if True, defaults to False.
    :type verbose: bool, optional
    :return: A dictionary containing the total utility for the top candidate and the total utility for top n candidates.
    :rtype: dict[str, float]
    """
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
        # Utility of the ballot given elected_candidates, multipled by its counts
        u, u_n = voter_subjective_utility_for_elected_candidate(elected_candidates, pair[1],topn=topn)
        """if verbose:
            print(f"{pair[0]} \t {pair[1]} \t {u}")"""
        total_u += pair[0] * u
        total_u_n += pair[0] * u_n
    if verbose:
        print("Total : ", total_u)
    #print("r",[rule_name,elected_candidates])
    return [rule_name,elected_candidates]

def monotonicity_check(rules: list,all_result: list,rep,num_candidates: int,
                          num_voters: int,
                          topn: int,
                          voters_model: str,
                          distortion_ratio: float = 0.0,
                          verbose: bool = False
                          ) -> dict[str, dict[str, float]]:
    profile = get_profile_from_model(num_candidates, num_voters, voters_model)
    profile.distort(distortion_ratio)
    """print(len(profile.pairs))
    print(g.num)"""
    result=[]
    for rule in rules:
            result.append(get_rule_utility(profile, rule, topn, verbose))
    winners=[result[i][1][0] for i in range(len(rules))]
    #print(winners)
    tf_s=[[rule.__name__,True] for rule in rules]
    s="monotonicity"
    g.num=random.randrange(0,len(profile.pairs))
    for _ in range(rep):
        
        new_profile=profile#何らかの手段でwinnerがより上位にあるようなprofileを作れたとする。
        new_result=[]
        for rule in rules:
            new_result.append(get_rule_utility(new_profile, rule, topn, verbose))
        new_winners=[new_result[i][1][0] for i in range(len(rules))]
        for i in range(len(rules)):
            tf_s[i][1] &= new_winners[i]==winners[i]
                
    n=all_result[0].index(s)
    for i in range(len(rules)):
        all_result[i+1][n]=tf_s[i][1]
    return all_result
    
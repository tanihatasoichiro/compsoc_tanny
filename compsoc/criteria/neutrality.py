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
                     topn: int,n_sigma,
                     verbose=False):
    g.ano=False
    rule_name = rule.__name__
    ranking = profile.ranking(rule)
    #print(ranking)
    
    elected_candidates = [n_sigma[c[0]] for c in ranking]
    
    if verbose:
        print(f"Ranking based on '{rule_name}' gives {ranking} with winners {elected_candidates}")
        print("======================================================================")
    total_u, total_u_n = 0., 0.
    for pair in profile.pairs:
        n_pair=[]
        for pi in pair[1]:
            n_pair.append(n_sigma[pi])
        u, u_n = voter_subjective_utility_for_elected_candidate(elected_candidates, n_pair,topn=topn)
        """if verbose:
            print(f"{pair[0]} \t {pair[1]} \t {u}")"""
        total_u += pair[0] * u
        total_u_n += pair[0] * u_n
    if verbose:
        print("Total : ", total_u)
    
    return [rule_name,elected_candidates]

def neutrality_check(rules: list,all_result: list,rep,num_candidates: int,
                          num_voters: int,
                          topn: int,
                          voters_model: str,
                          distortion_ratio: float = 0.0,
                          verbose: bool = False
                          ) -> dict[str, dict[str, float]]:
 
 
    profile = get_profile_from_model(num_candidates, num_voters, voters_model)
    profile.distort(distortion_ratio)


    if verbose:
        print(profile.pairs)

    tf_s=[[rule.__name__,True] for rule in rules]
    s="neutrality"
    g.num=random.randrange(0,len(profile.pairs))
    for _ in range(rep):
        
        sigma=list(range(num_candidates))
        #n_sigma=random.sample(sigma,len(sigma))
        n_sigma=list(reversed(sigma))
        g.nsigma=n_sigma
        
        g.neu=True
        r_result=[]
        for i in range(len(rules)):
            r_result.append(get_ranking(profile, rules[i], topn,n_sigma, verbose)[1])
        l_result=[]
        g.neu=False

        for rule in rules:
            ga=get_ranking(profile, rule, topn,sigma, verbose)[1]
            l_result.append([n_sigma[i] for i in ga])

        for i in range(len(rules)):
            tf_s[i][1] &=r_result[i]==l_result[i]
    n=all_result[0].index(s)
    for i in range(len(rules)):
        all_result[i+1][n]=tf_s[i][1]
    return all_result

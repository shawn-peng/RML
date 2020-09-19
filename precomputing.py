
def precompute(precomp_rule_f, facts_rel):
    precomp_rules = list(open(precomp_rule_f))
    print(precomp_rules)
    print(eval("".join(precomp_rules)))
    __import__()


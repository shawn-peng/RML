
#num_of_smoking_friends(x, n) :-
#   friends(x, y),
#   countUniqueBindings((friends(x,z)^smokes(z)), n).

print(fact_rels)
# print(globals()[''])
# print(friends.get_values(1))

def num_of_smoking_friends(x):
    z = var()
    # return (countUniqueBindings, z, ((friends,x,z), (smokes, z)), n)
    return count_binding_set(z, ((friends,x,z), (smokes,z)), fact_rels)

x = var()
n = var()
#print(locals())
# args_list = [(_x, print(locals())) for _x in run(0, x, (friends, x, var()))]
args_list = []
for _x in friends.get_values(1):
    args_list.append((_x,))
# args_list = [(_x, n) for _x in friends.get_values(1)]
print('persons', args_list)
func2facts(num_of_smoking_friends, args_list, fact_rels)


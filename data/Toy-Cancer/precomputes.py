
#num_smoking_friends(x, n) :-
#   friends(x, y),
#   countUniqueBindings((friends(x,z)^smokes(z)), n).

print(fact_rels)
# print(globals()[''])
# print(friends.get_values(1))

def relation_function(f):
    def inner(*args):
        def goal(s):
            return s
        return goal
    return inner

# @relation_function
def num_smoking_friends(x):
    z = TypedVar('Person', 'z')
    # return (countUniqueBindings, z, ((friends,x,z), (smokes, z)), n)
    # return count_binding_set(z, (friends(x,z), smokes(z)), fact_rels)
    return count_binding_set((z,), (friends(x,z), smokes(z)))

x = TypedVar('Person', 'x')
n = TypedVar('n', 'n')
#print(locals())
# args_list = [(_x, print(locals())) for _x in run(0, x, (friends, x, var()))]
# args_list = []
# for _x in friends.get_values(1):
#     args_list.append((_x,))
# args_list = [(_x, n) for _x in friends.get_values(1)]

args = (x,)
# print('persons', args_list)
print('persons', x.type.get_values())

rel_type = rel_types['num_smoking_friends']
func2facts(num_smoking_friends, rel_type, args, fact_rels)
print('fact_rels[nsf]', fact_rels['num_smoking_friends'].facts)

# fact( num_smoking_friends('Alice', 2) )
# exit()


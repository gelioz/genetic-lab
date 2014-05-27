from ga_core import GACore
import ga_core
import functions

def run_test(func_name, expected, func, min_arg, max_arg, args_number, optimum):
    tester = GACore(args_number, func, optimum)
    result = tester.find_extremum(min_arg, max_arg)
    print("{0} for [{1}, {2}]".format(func_name, min_arg, max_arg))
    print("Expected: {0}".format(expected))
    print("Real: {0}".format(str(result)))
    #print(func(result))
    print()

# Test suit
print("Running tests with next settings:")
print("Binary string length = " + str(ga_core.Gene.BIT_LEN))
print("Population = " + str(ga_core.GACore.POPULATION))
print("Mutation rate = " + str(ga_core.GACore.MUTATION_RATE))
print()

# Test for De Jong function
run_test("De Jong", "(1, 1)", \
         functions.de_jong, -2.048, 2.048, 2, functions.DE_JONG_OPTIMUM)

# Test for Goldstein and Price function
run_test("Goldstain and Price", "(0, -1)", \
         functions.goldstein_and_price, -2, 2, 2, \
         functions.GOLDSTEIN_AND_PRICE_OPTIMUM)

# Test for Branin function
run_test("Brinan", "(-3.143, 12.275) or (3.143, 2.275) or (9.429, 2.475)", \
         functions.branin, -5, 15, 2, functions.BRANIN_OPTIMUM)

# Test for Martin and Gaddy function
run_test("Martin and Gaddy", "(5, 5)", \
         functions.martin_and_gaddy, 0, 10, 2, \
         functions.MARTIN_AND_GADDY_OPTIMUM)

# Test for Rozenbrock 1 function
run_test("Rozenbrock 1 (a)", "(1, 1)", \
         functions.rosenbrock_1, -1.2, 1.2, 2, functions.ROSENBROCK_1_OPTIMUM)
run_test("Rozenbrock 1 (b)", "(1, 1)", \
         functions.rosenbrock_1, -10, 10, 2, functions.ROSENBROCK_1_OPTIMUM)

# Test for Rozenbrock 2 function
run_test("Rozenbrock 2", "(1, 1, 1, 1)", \
         functions.rosenbrock_2, -1.2, 1.2, 4, functions.ROSENBROCK_2_OPTIMUM)

# Test for Hyper sphere function
run_test("Hyper sphere", "(0, 0, 0, 0, 0, 0)", \
         functions.hyper_sphere, -5.12, 5.12, 6, functions.HYPER_SPHERE_OPTIMUM)

# Test for Griewangk function
run_test("Griewangk", "(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)", \
         functions.griewangk, -512, 512, 10, functions.GRIEWANGK_OPTIMUM)

import math


DE_JONG_OPTIMUM = 3905.93
def de_jong(args):
    x1 = args[0]
    x2 = args[1]
    return 3905.93 - 100 * (x2 - x1**2)**2 - (1 - x1)**2

GOLDSTEIN_AND_PRICE_OPTIMUM = 3
def goldstein_and_price(args):
    x1 = args[0]
    x2 = args[1]
    return (1 + (x1 + x2 + 1)**2 * (19 - 14*x1 + 3*(x1**2) - 14*x2 + 6*x1*x2 \
            + 3*(x2**2))) * (30 + (2*x1 - 3*x2)**2 * (18 - 32*x1 + 12*(x1**2) \
            + 48*x2 - 36*x1*x2 + 27*(x2**2)))

BRANIN_OPTIMUM = 0.397887
def branin(args):
    x1 = args[0]
    x2 = args[1]
    return (x2 - 0.12918450914398066 * x1**2 + 1.5915494309189535 * x1 - 6)**2 \
            + 9.602112642270262 * math.cos(x1) + 10
    #return (x2 - 5.1 / (4 * math.pi**2) * x1**2 + 5 / math.pi * x1 - 6)**2 \
    #        + 10 * (1 - 1 / (8 * math.pi)) * math.cos(x1) + 10

MARTIN_AND_GADDY_OPTIMUM = 0
def martin_and_gaddy(args):
    x1 = args[0]
    x2 = args[1]
    return (x1 - x2)**2 + ((x1 + x2 - 10) / 3)**2

ROSENBROCK_1_OPTIMUM = 0
def rosenbrock_1(args):
    x1 = args[0]
    x2 = args[1]
    return (1 - x1)**2 + 100 * (x2 - x1**2)**2

ROSENBROCK_2_OPTIMUM = 0
def rosenbrock_2(args):
    result = 0
    for i in range(len(args) - 1):
        result += rosenbrock_1(args[i:i+2])
    return result

HYPER_SPHERE_OPTIMUM = 0
def hyper_sphere(args):
    result = 0
    for x in args:
        result += x**2
    return result

GRIEWANGK_OPTIMUM = 0
def griewangk(args):
    sub_sum = 0
    sub_mult = 1
    for i in range(1, len(args) + 1):
        sub_sum += args[i-1]**2 / 4000 
        sub_mult *= math.cos(args[i-1] / math.sqrt(i))
    return sub_sum - sub_mult + 1

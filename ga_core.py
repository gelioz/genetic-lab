import random
import math


class Gene:
    '''Representaton of gene that used in genetic algorithms'''
    BIT_LEN = 16
    MIN_VALUE = 0
    MAX_VALUE = 2 ** BIT_LEN - 1
    
    def __init__(self, number):
        self.code = number

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, number):
        if number < Gene.MIN_VALUE or number > Gene.MAX_VALUE:
            raise ValueError("Wrong value for gene: " + str(number))
        self._code = number

    def combine(self, other, bit_pos):
        '''bit_pos is position starting from left'''
        if 0 <= bit_pos < Gene.BIT_LEN:
            other_mask = 2 ** (Gene.BIT_LEN - bit_pos) - 1
            other_part = other.code & other_mask
            self_mask = Gene.MAX_VALUE - other_mask
            self_part = self.code & self_mask
            self.code = self_part + other_part

    def clone(self):
        return Gene(self.code)

    def __str__(self):
        bin_str = []
        rest = self.code
        rated_value = 2 ** (Gene.BIT_LEN - 1)
        for i in range(Gene.BIT_LEN):
            if rest // rated_value:
                bin_str.append('1')
                rest -= rated_value
            else:
                bin_str.append('0')
            rated_value = rated_value // 2        
        return ''.join(bin_str)


class Chromosome:
    '''Chromosome that used in genetic algorithms. Consists of genes.'''
    def __init__(self, genes_number, min_limit, max_limit, genes = None):
        self.genes_number = genes_number
        self.min_limit = min_limit
        self.max_limit = max_limit
        if genes:
            self.genes = genes
        else:
            self.genes = self._fill_randomly()
        self.fitness = None

    def _fill_randomly(self):
        genes = []
        for i in range(self.genes_number):
            genes.append(Gene(random.randint(Gene.MIN_VALUE, Gene.MAX_VALUE)))
        return genes

    def get_limited_values(self):
        limited_values = []
        for gene in self.genes:
            limits_interval = self.max_limit - self.min_limit
            limited = gene.code * limits_interval / (Gene.MAX_VALUE + 1) \
                      + self.min_limit
            limited_values.append(limited)
        return tuple(limited_values)

    def combine(self, other, dots):
        if not len(dots):
            raise ValueError("'dots' should contain 1 or more dots")
        elif len(self.genes) != len(other.genes):
            raise ValueError("Chromosomes have different number of genes")

        dot_lst = sorted(dots)
        dot_idx = 0
        curr_chrm = self
        next_chrm = other
        new_genes = []
        
        for idx in range(len(self.genes)):
            new_genes.append(curr_chrm.genes[idx].clone())

            while dot_idx < len(dot_lst):
                pos_in_chrm = dot_lst[dot_idx] // Gene.BIT_LEN
                if pos_in_chrm > idx:
                    break
                pos_in_gene = dot_lst[dot_idx] % Gene.BIT_LEN
                new_genes[idx].combine(next_chrm.genes[idx], pos_in_gene)
                curr_chrm, next_chrm = next_chrm, curr_chrm
                dot_idx += 1
                
        return Chromosome(self.genes_number, self.min_limit, self.max_limit,
                          genes = new_genes)
    
    def __str__(self):
        return '.'.join(str(gene) for gene in self.genes)


class GACore:
    '''
    Genetic algorithm runner. Works with specified function and
    specified number of function arguments (number of genes).
    '''
    MUTATION_RATE = 0.05
    POPULATION = 250
    ELITISM_RATE = 0.1
    BEST_PARENTS = round(POPULATION * ELITISM_RATE)
    MAX_COUNTS = 25
    
    def __init__(self, args_number, func, global_optimum):
        self.func = func
        self.args_number = args_number
        self.generation = []
        self.global_optimum = global_optimum
        self.best_descendant = None

    def find_extremum(self, min_value, max_value):
        self._create_new_generation(min_value, max_value)
        self.best_descendant = self.generation[random.randint(0, GACore.POPULATION - 1)]
        self._count_and_set_population_fitness(self.generation)
        counter = 0
        best_one = self.best_descendant

        while counter < GACore.MAX_COUNTS:
            selected = self._tournament_select()
            new_generation = self._cross_over(selected)
            new_generation += self._best_parents()
            self._mutate(new_generation, min_value, max_value)
            self._count_and_set_population_fitness(new_generation)
            best_one = sorted(new_generation, key=lambda chrm: chrm.fitness)[0]
            if best_one.fitness < self.best_descendant.fitness:
                self.best_descendant = best_one
                counter = 0
            else:
                counter += 1
            self.generation = new_generation
            
        return self.best_descendant.get_limited_values()
        

    def _create_new_generation(self, min_val, max_val):
        self.generation.clear()
        for i in range(GACore.POPULATION):
            self.generation.append(Chromosome(self.args_number, min_val, max_val))

    def _count_and_set_fitness(self, chrm):
        func_value = self.func(chrm.get_limited_values())
        chrm.fitness = abs(self.global_optimum - func_value)

    def _count_and_set_population_fitness(self, generation):
        for chrm in generation:
            self._count_and_set_fitness(chrm)

    def _tournament_select(self):
        selected = []
        for i in range(GACore.POPULATION):
            applicants = (random.choice(self.generation) for i in range(2))
            selected.append(min(applicants, key=lambda chrm: chrm.fitness))
        return selected

    def _combine_randomly(self, chrm1, chrm2):
        point1 = random.randint(1, chrm1.genes_number * Gene.BIT_LEN - 2)
        point2 = random.randint(point1, chrm1.genes_number * Gene.BIT_LEN - 1)
        return chrm2.combine(chrm1, [point1, point2])

    def _cross_over(self, selected):
        new_generation = []
        for i in range(GACore.POPULATION - GACore.BEST_PARENTS):
            father = random.choice(selected)
            mother = random.choice(selected)
            new_generation.append(self._combine_randomly(father, mother))
        return new_generation

    def _best_parents(self):
        return sorted(self.generation, key=lambda chrm: chrm.fitness)[0:GACore.BEST_PARENTS]

    def _mutate(self, new_generation, min_value, max_value):
        if random.random() < GACore.MUTATION_RATE:
            chrm_idx = random.randint(0, GACore.POPULATION - 1)
            mutagen = Chromosome(self.args_number, min_value, max_value)
            mutant = self._combine_randomly(self.generation[chrm_idx], mutagen)
            self.generation[chrm_idx] = mutant
            

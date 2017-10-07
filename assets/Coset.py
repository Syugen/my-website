from itertools import permutations

class Permutation:
    def __init__(self, d, size):
        self.size = size
        self.d = d
    
    def __eq__(self, other):
        if type(other) != Permutation: raise Exception('Type error')
        return self.size == other.size and self.d == other.d
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        if self == get_identity(self.size): return 'e'
        cycles = []
        d = {key: value for key, value in self.d.items() if key != value}
        digits = list(sorted(d.keys()))
        while len(digits) > 0:
            cycles.append([])
            digit = digits.pop(0)
            cycles[-1].append(digit)
            while d[digit] not in cycles[-1]:
                cycles[-1].append(d[digit])
                digit = d[digit]
                digits.remove(digit)
        string = ''
        for cycle in cycles:
            string += '(' + ''.join([str(digit) for digit in cycle]) + ')'
        return string
    
    def composite(self, other):
        """ Note: self.composite(other) <==> self o other
        """
        d = {}
        for key in self.d:
            d[key] = self.d[other.d[key]]
        return Permutation(d, self.size)      
            
def get_identity(size):
    return Permutation({i: i for i in range(1, size + 1)}, size)

def get_all_permutations(size):
    all_permutations = []
    for t in permutations('123456789'[:size], size):
        p = Permutation({i + 1: int(t[i]) for i in range(size)}, size)
        all_permutations.append(p)
    return all_permutations

def validate(permutation):
    expect_digit = False
    exp = None
    p = ''
    cycles = [[]]
    for char in permutation:
        if expect_digit:
            if char.isdigit():
                exp = 0 if exp is None else exp
                time = 9 * exp + int(char)
                exp = 10 * exp + int(char)
                for i in range(exp - 1):
                    cycles.append(cycles[-1][:])
            else:
                if exp is None or char != '*':
                    return False, 'Exponent error'
                expect_digit = False
        if not expect_digit:
            if char == '(':
                if len(p) == 0 or p[-1] == ')':
                    p += char
                    cycles[-1].append([])
                else:
                    return False, 'Invalid left parenthesis position'
            elif char == ')':
                if len(p) > 0 and p[-1] == '(':
                    p += char
                else:
                    return False, 'Invalid right parenthesis position'
            elif char == '*':
                if len(p) > 0 and p[-1] == ')':
                    cycles.append([])
                else:
                    return False, 'Invalid binary operator position'
            elif char == '^':
                if len(p) > 0 and p[-1] == ')':
                    expect_digit = True
                else:
                    return False, 'Invalid exponent operator position'                
            elif '1' <= char <= str(size):
                if len(p) > 0 and p[-1] == '(':
                    cycles[-1][-1].append(int(char))
                else:
                    return False, 'Invalid digit position'
            else:
                return False, 'Invalid input character'    
    return True, cycles

def form_permutations(cycles, size):
    for i in range(len(cycles)):
        d = {}
        for j in range(len(cycles[i])):
            for k in range(len(cycles[i][j])):
                if cycles[i][j][k] not in d:
                    d[cycles[i][j][k]] = cycles[i][j][(k+1)%len(cycles[i][j])]
                else:
                    return False, str(cycles[i][j][k]) + ' appears more than once'
        
        for j in range(1, size + 1):
            if j not in d: d[j] = j
        cycles[i] = Permutation(d, size)
    return True, cycles

def validate_and_form_permutations(permutation, size):
    valid, cycles = validate(permutation)
    if not valid:
        return False, cycles
    return form_permutations(cycles, size)

def calculate(permutation):
    while len(permutation) > 1:
        p1 = permutation.pop()
        p2 = permutation.pop()
        p3 = p2.composite(p1)
        permutation.append(p3)
    return permutation[0]

def get_permutation(hint="calculation"):
    permutation = None
    while permutation is None:
        permutation = input('Input your expression for ' + hint + ': ')
        valid, result = validate_and_form_permutations(permutation, size)
        if not valid: 
            print(result + '. Please try again.')
            permutation = None
        else:
            permutation = calculate(result)   
    return permutation

def generate(generator):
    subgroup = [generator]
    cur = generator
    while cur != get_identity(generator.size):
        cur = generator.composite(cur)
        subgroup.append(cur)
    return subgroup
    
if __name__ == '__main__':
    size = None
    print('Permutation (Group Theorem) Calculator')
    while size is None:
        size = input('Input size (1-9): ')
        if size.isdigit() and 1 <= int(size) <= 9: size = int(size)
        else:
            print('Invalid input. Please try again.')
            size = None
    print('1. Given expression, calculate expression')
    print('2. Given expression of generator, generate subgroup.')
    print('3. Given g and generator of subgroup H, calculate gH.')
    print('4. Given generator of subgroup H, calculate all gH for g in Sn')
    print('5. Given generator of subgroup H, calculate all Hg for g in Sn')
    while True:
        selection = None
        while selection is None:
            selection = input('Input your selection: ')
            if selection.isdigit() and 1 <= int(selection) <= 5: 
                selection = int(selection)
            else:
                print('Invalid input. Please try again.')
                selection = None
        if selection == 1:
            print('Result is:', get_permutation())        
        elif selection == 2:
            generator = get_permutation('generator')
            print('Generator is:', generator)        
            subgroup = generate(generator)
            print('Subgroup is: ', subgroup)
        elif selection == 3:
            g = get_permutation('g')
            generator = get_permutation('generator of H')
            print('g =', g)
            H = generate(generator)
            print('H =', H)
            gH = [g.composite(h) for h in H]
            print('gH =', gH)
        elif selection == 4 or selection == 5:
            H = generate(get_permutation('generator of H'))
            print('H =', H)        
            Sn = get_all_permutations(size)
            gH_all = []
            print('All gH:')
            while len(Sn) != 0:
                gH = [Sn[0].composite(h) for h in H] if selection == 4 else \
                     [h.composite(Sn[0]) for h in H]
                for p in gH: Sn.remove(p)
                if selection == 4:
                    print(''.join([str(gh) + 'H = ' for gh in gH]), end='')
                else:
                    print(''.join(['H' + str(gh) + ' = ' for gh in gH]), end='')
                gH_all.append(gH)
                print(gH)
    
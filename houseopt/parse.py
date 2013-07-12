def positive_int(s):
    i = int(s)
    if i < 0:
        raise ValueError('Not a positive integer: {}'.format(i))
    return i

def parse_houses(problem, houses):
    result = []
    for line in houses:
        if not line.strip() or line[0] == '#':
            continue

        line = line.strip()

        if len(line.split(' ')) != 2:
            raise ValueError('Invalid house line {!r}'.format(line))

        name, count = line.split(' ')
        result.append(name)
            
        problem.add_house(name.encode('utf-8'), positive_int(i))

    return result

def read_lines_file(lf, house_types):
    result = []

    for line in lf:
        if not line.strip() or line[0] == '#':
            continue

        parts = line.strip().split(' ')
        if len(parts) != len(house_types):
            raise ValueError('Invalid house line {!r}'.format(line))

        first = [(n.encode('utf-8'),positive_int(i))
                      for (n,i) in zip(house_types,parts)]
        result.append((sum(c for n,c in first), first))

    return result
        
def parse_customers(problem, customers, houses, min_pref, max_pref):
    for line in customers:
        line = line.strip()
        
        if not line:
            continue

        parts = line.split(' ')
        name = parts[0]
        prefs = parts[1:]

        try:
            problem.add_customer(name.encode('utf-8'), {
                house.encode('utf-8'): int(pref)
                for (house,pref) in zip(houses,prefs)
                if min_pref <= int(pref) <= max_pref})
            
        except ValueError:
            raise ValueError('Invalid customer line {!r}'.format(line))

def parse_houses(problem, houses):
    result = []
    for line in houses:
        line = line.strip()
        
        if not line:
            continue

        if len(line.split(' ')) != 2:
            raise ValueError('Invalid house line {!r}'.format(line))

        name, count = line.split(' ')
        result.append(name)

        try:
            count_i = int(count)
            assert count_i >= 0
        except Exception:
            raise ValueError('Not a positive number: {!r}'.format(count))
            
        problem.add_house(name.encode('utf-8'), count_i)

    return result

def parse_customers(problem, customers, houses, min_pref, max_pref):
    for line in customers:
        line = line.strip()
        
        if not line:
            continue

        name, *prefs = line.split(' ')

        try:
            problem.add_house(name.encode('utf-8'), {
                house.encode('utf-8'): int(pref)
                for (house,pref) in zip(houses,prefs)
                if min_pref <= int(pref) <= max_pref})
            
        except ValueError:
            raise ValueError('Invalid customer line {!r}'.format(line))

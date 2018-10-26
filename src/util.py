import json
import shapely
import shapely.geometry


def load(src):
    with open(src, 'r') as f:
        x = f.read()
        x = json.loads(x)
    return x


def regions(src, region_key):
    l = []
    x = load(src)
    for f in x['features']:
        props = f['properties']
        if region_key not in props:
            raise ValueError('{} not in props.'.format(region_key))
        name = props[region_key]
        short_name = name[name.rfind(' ')+1:]
        short_name = short_name[:3].upper()
        s = shapely.geometry.shape(f['geometry'])
        l.append({'name': name, 's_name': short_name, 'geom': s})
    return l


def neighbours(region_list):
    def adjacent(g1, g2):
        return g1.touches(g2) or g1.intersects(g2)

    n = []
    # for i=0, j=i+1...
    #   0 1 2 3
    # 0   x x x  
    # 1     x x
    # 2       x
    # 3
    #import itertools
    #for i, j in itertools.combinations(range(0, len(region_list)), r=2):
    rl_len = len(region_list)
    for i in range(0, rl_len):
        src = region_list[i]['geom'] 
        for j in range(i+1, rl_len):
            dst = region_list[j]['geom']
            if adjacent(src, dst): 
                n.append((i, j))
    return n


def conf(region_list, adjacency_list):
    return dict(regions=region_list, neighbours=adjacency_list)


def load_conf(src, region_key):
    l = regions(src, region_key)
    n = neighbours(l)
    return conf(l, n)    


if __name__ == '__main__':
    # python3 ./read.py geojson/counties.geojson Name
    import sys
    src, region_key = sys.argv[1:]
    r = regions(src, region_key)
    n = neighbours(r)
    for i, region in enumerate(r):
        j = 0
        for x, y in n:
            if i == x:
                print('{} ({}) -> {} ({})'.format(region['s_name'], region['name'], r[y]['s_name'], r[y]['name']))
                j += 1
            elif i == y:
                print('{} ({}) -> {} ({})'.format(region['s_name'], region['name'], r[x]['s_name'], r[x]['name']))
                j += 1
        print('{} = {} neighbours'.format(region['s_name'], j))
    print('total relations = {}'.format(len(n)))

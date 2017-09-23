import json
import shapely.geometry

def load(src):
    with open(src, 'r') as f:
        x = f.read()
        x = json.loads(x)
    return x


def neighbours(src, region_key):
    x = load(src)
    # enumerate features in FeatureCollection
    for f in x['features']:
        props = f['properties']
        if region_key not in props:
            raise ValueError('{} not in props.'.format(region_key))
        name = props[region_key]
        short_name = name.replace(" ", "")
        short_name = short_name[:3].upper()
        s = shapely.geometry.shape(f['geometry'])
        print(type(s))


if __name__ == '__main__':
    # python3 ./read.py geojson/constituencies.geojson pcon16nm
    import sys
    src, region_key = sys.argv[1:]
    neighbours(src, region_key)

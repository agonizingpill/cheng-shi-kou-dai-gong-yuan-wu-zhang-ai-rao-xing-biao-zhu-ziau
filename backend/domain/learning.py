from sklearn.preprocessing import MultiLabelBinarizer

def calculate(data):
    profile, entrances = data['profile'], data['entrances']
    mlb = MultiLabelBinarizer()
    vectors = mlb.fit_transform([profile['avoid']]+[r['tags'] for r in entrances])
    weights = [profile['weights'].get(x,0) for x in mlb.classes_]
    total = sum(weights)
    ranked = []
    for record, bits in zip(entrances, vectors[1:]):
        overlap = sum(weight*int(bit) for weight,bit in zip(weights,bits))
        ranked.append({'entry':record['code'],'score':round(1-overlap/total,4),'ramp':record['ramp']})
    return {'classes':mlb.classes_.tolist(),'ranked':sorted(ranked,key=lambda r:(-r['score'],not r['ramp'],r['entry']))}

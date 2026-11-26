from sklearn.preprocessing import MultiLabelBinarizer

from domain.trials_scoring import score_pending

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

def dispatch(payload):
    if isinstance(payload, dict) and payload.get('kind') == 'weight_trial_scoring':
        return score_pending(payload['trial'])
    return calculate(payload)

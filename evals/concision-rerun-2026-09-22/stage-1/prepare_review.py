import json,random,re
from pathlib import Path
R=Path(__file__).resolve().parent
cases=json.loads((R/'heldout-cases.json').read_text()); byid={c['id']:c for c in cases}
rows=[];blind=[];key={};rng=random.Random(79422)
for a in ['none','old','candidate']:
 for rep in [1,2]:
  for d in json.loads((R/f'{a}-{rep}-output.json').read_text())['outputs']:
   c=byid[d['id']];checks={f'exact_span_{j}':s in d['text'] for j,s in enumerate(c['exact_spans'])}
   if c['word_range']:
    lo,hi=c['word_range']; checks['word_range']=lo<=len(d['text'].split())<=hi
   if d['id']=='c03':checks['punctuation_only']=re.findall(r'\w+',c['source'])==re.findall(r'\w+',d['text'])
   rows.append({'id':d['id'],'arm':a,'repetition':rep,'text':d['text'],'checks':checks})
rng.shuffle(rows)
for j,row in enumerate(rows):
 bid=f'sample-{j+1:03}';key[bid]={k:row[k] for k in ['id','arm','repetition']}
 c=byid[row['id']]
 blind.append({'sample_id':bid,'request':c['request'],'source':c['source'],'proposed_required_content':c['must_preserve'],'draft':row['text']})
(R/'blinded-review.json').write_text(json.dumps(blind,indent=2))
(R/'blind-key.json').write_text(json.dumps(key,indent=2))
(R/'experiment.json').write_text(json.dumps({'repetitions':2,'cases':cases,'outputs':rows},indent=2))
print('Prepared',len(rows),'blinded drafts')

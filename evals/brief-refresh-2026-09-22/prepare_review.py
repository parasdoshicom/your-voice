from pathlib import Path
import json,random
R=Path(__file__).resolve().parent
cases=json.loads((R/'heldout-cases.json').read_text());byid={c['id']:c for c in cases}
rows=[]
for arm in ['none','old','candidate']:
 for rep in [1,2]:
  for o in json.loads((R/f'{arm}-{rep}-output.json').read_text())['outputs']:
   c=byid[o['id']];checks={f'exact_span_{i}':s in o['text'] for i,s in enumerate(c['exact_spans'])}
   if c['word_range']:
    a,b=c['word_range'];checks['word_range']=a<=len(o['text'].split())<=b
   rows.append({'id':o['id'],'arm':arm,'repetition':rep,'text':o['text'],'checks':checks})
random.Random(83601).shuffle(rows);blind=[];key={}
for i,o in enumerate(rows):
 sid=f'sample-{i+1:03}';key[sid]={k:o[k] for k in ['id','arm','repetition']};c=byid[o['id']]
 blind.append({'sample_id':sid,'request':c['request'],'source':c['source'],'must_preserve':c['must_preserve'],'draft':o['text']})
(R/'blinded-review.json').write_text(json.dumps(blind,ensure_ascii=False,indent=2));(R/'blind-key.json').write_text(json.dumps(key,indent=2));(R/'experiment.json').write_text(json.dumps({'repetitions':2,'cases':cases,'outputs':rows},ensure_ascii=False,indent=2))
print('prepared',len(rows),'drafts')

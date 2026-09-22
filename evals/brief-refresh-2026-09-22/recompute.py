"""Recompute recorded exploratory counts; not a writing-quality gate."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
x=json.loads((ROOT/'experiment.json').read_text())
cs={c['id']:c for c in x['cases']}
assert len(cs)==10
seen=set();summary={a:{'drafts':0,'deterministic_assertions':0,'deterministic_failures':0,'meaning_failures':0,'contract_failures':0} for a in ['none','old','candidate']}
for row in x['outputs']:
    key=(row['id'],row['arm'],row['repetition'])
    assert key not in seen;seen.add(key)
    c=cs[row['id']];checks=[s in row['text'] for s in c['exact_spans']]
    if c['word_range']:
        lo,hi=c['word_range'];checks.append(lo<=len(row['text'].split())<=hi)
    out=summary[row['arm']];out['drafts']+=1
    out['deterministic_assertions']+=len(checks)
    out['deterministic_failures']+=sum(not v for v in checks)
    for field in ['meaning','contract']:
        assert row[field]['label'] in ['Pass','Fail'] and row[field]['evidence']
        out[field+'_failures']+=row[field]['label']=='Fail'
assert seen=={(i,a,r) for i in cs for a in summary for r in [1,2]}
if '--check' in sys.argv:
    assert summary==json.loads((ROOT/'summary.json').read_text()), 'Stored summary differs'
    print('Stored counts match raw drafts and recorded reviews; this is not human calibration.')
else:print(json.dumps(summary,indent=2))

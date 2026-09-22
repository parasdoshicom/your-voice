"""Verify archived regression records; not a behavioral quality gate."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
read = lambda name: json.loads((root / name).read_text())
manifest = read('manifest.json')
assert hashlib.sha256((root / 'heldout-cases.json').read_bytes()).hexdigest() == manifest['case_sha256']
cases = {c['id']: c for c in read('heldout-cases.json')}
outputs = {}
for run in manifest['runs']:
    name = run['name']
    assert hashlib.sha256((root / (name + '-prompt.txt')).read_bytes()).hexdigest() == run['prompt_sha256']
    rows = read(name + '-output.json')['outputs']
    assert len(rows) == len(cases) and {r['id'] for r in rows} == set(cases)
    for row in rows:
        outputs[name, row['id']] = row['text']
key = read('blind-key.json')
blinded = {r['label']: r for r in read('blind-review.json')}
review = read('blind-judgments.json')
assert set(key) == set(blinded) == {j['label'] for j in review['judgments']}
assert len(key) == len(outputs) == 24
assert len({(v['run'], v['case_id']) for v in key.values()}) == 24
counts = {a: {'pass': 0, 'fail': 0} for a in ['none', 'old', 'candidate']}
for judgment in review['judgments']:
    label = judgment['label']
    identity = key[label]
    assert blinded[label]['text'] == outputs[identity['run'], identity['case_id']]
    assert blinded[label]['case'] == cases[identity['case_id']]
    result = judgment['overall_preservation'].lower()
    assert result in ['pass', 'fail']
    counts[identity['run'].rsplit('-', 1)[0]][result] += 1
assert sum(c['pass'] for c in counts.values()) == review['pass_count']
assert sum(c['fail'] for c in counts.values()) == review['fail_count']
print(json.dumps(counts, indent=2))
print('Archive integrity verified; model judgments are not human calibration.')

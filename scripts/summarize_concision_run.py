#!/usr/bin/env python3
"""Recompute a three-arm writing experiment; missing reviews cannot pass."""
from __future__ import annotations
import argparse
import json
import statistics
import re
from pathlib import Path

ARMS = ('none', 'old', 'candidate')

def summarize(data):
    cases = {c['id']: c for c in data['cases']}
    if len(cases) != len(data['cases']):
        raise ValueError('duplicate case id')
    rows = {}
    for row in data['outputs']:
        key = (row['id'], row['repetition'], row['arm'])
        if key in rows:
            raise ValueError('duplicate output')
        if row['id'] not in cases or row['arm'] not in ARMS:
            raise ValueError('unknown case or arm')
        rows[key] = row
    reps = data['repetitions']
    expected = {(i, r, a) for i in cases for r in range(1, reps + 1) for a in ARMS}
    if set(rows) != expected:
        raise ValueError('incomplete or unexpected output coverage')
    def words(row):
        return len(row['text'].split())
    def eligible(row):
        case = cases[row['id']]
        exact_ok = all(span in row['text'] for span in case.get('exact_spans', []))
        bounds = case.get('word_range')
        range_ok = not bounds or bounds[0] <= words(row) <= bounds[1]
        request = case.get('request', '').lower()
        punctuation_ok = True
        if 'punctuation only' in request or 'punctuation-only' in request:
            punctuation_ok = re.findall(r'\w+', case['source']) == re.findall(r'\w+', row['text'])
        return (exact_ok and range_ok and punctuation_ok and row.get('meaning', {}).get('label') == 'Pass'
                and row.get('human_intent', {}).get('label') == 'Pass'
                and all(row.get('checks', {}).values()))
    result = {'case_count': len(cases), 'output_count': len(rows), 'categories': {}, 'review_failures': []}
    for row in rows.values():
        for field in ('meaning', 'human_intent'):
            if row.get(field, {}).get('label') != 'Pass':
                result['review_failures'].append({k: row[k] for k in ('id','repetition','arm')} | {'dimension': field, 'review': row.get(field)})
    for cat in sorted({c['category'] for c in cases.values()}):
        ids = [i for i,c in cases.items() if c['category'] == cat]
        totals = {a: sum(words(rows[i,r,a]) for i in ids for r in range(1,reps+1)) for a in ARMS}
        comparisons = {}
        for baseline in ('none', 'old'):
            pairs = []
            for i in ids:
                for r in range(1,reps+1):
                    b, c = rows[i,r,baseline], rows[i,r,'candidate']
                    bw, cw = words(b), words(c)
                    pairs.append({'id':i, 'repetition':r, 'baseline_words':bw, 'candidate_words':cw,
                                  'candidate_valid':eligible(c),
                                  'half_length_success':bw > 0 and cw <= bw / 2 and eligible(c),
                                  'ratio':cw / bw if bw else None})
            ratios = [p['ratio'] for p in pairs if p['ratio'] is not None]
            comparisons[baseline] = {'pairs':len(pairs), 'half_length_successes':sum(p['half_length_success'] for p in pairs),
                'half_length_rate':sum(p['half_length_success'] for p in pairs)/len(pairs),
                'median_word_ratio':statistics.median(ratios) if ratios else None,
                'total_word_reduction':1-totals['candidate']/totals[baseline] if totals[baseline] else None,
                'details':pairs}
        result['categories'][cat] = {'words':totals, 'comparisons':comparisons}
    primary_category = data.get('primary_category', 'condense')
    result['primary_category'] = primary_category
    primary = result['categories'].get(primary_category,{}).get('comparisons',{}).get('old',{})
    all_candidate_valid = all(eligible(row) for row in rows.values() if row['arm']=='candidate')
    result['proposed_target_met'] = bool(primary.get('half_length_rate',0) >= .8 and all_candidate_valid)
    result['candidate_all_reviewed_and_valid'] = all_candidate_valid
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--check-summary',type=Path,help='Fail if a saved summary differs from recomputation')
    args=parser.parse_args()
    result=summarize(json.loads(args.input.read_text()))
    if args.check_summary:
        if result != json.loads(args.check_summary.read_text()):
            raise SystemExit('Saved summary differs from recomputed results')
        print('Saved summary matches recomputed results; this does not assert the behavioral target passed.')
    else:
        print(json.dumps(result,indent=2))

if __name__ == '__main__': main()

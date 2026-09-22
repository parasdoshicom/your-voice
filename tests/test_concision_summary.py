import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('summary',Path(__file__).parents[1]/'scripts/summarize_concision_run.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def fixture():
    return {'repetitions':1,'cases':[{'id':'x','category':'condense'}], 'outputs':[
        {'id':'x','repetition':1,'arm':arm,'text':text,'meaning':{'label':'Pass'},'human_intent':{'label':'Pass'},'checks':{}}
        for arm,text in [('none','one two three four'),('old','one two three four'),('candidate','one two')]]}

class SummaryTests(unittest.TestCase):
    def test_half_length_means_half_with_quality_gate(self):
        d=fixture(); self.assertTrue(m.summarize(d)['proposed_target_met'])
        d['outputs'][2]['meaning']['label']='Fail'
        self.assertFalse(m.summarize(d)['proposed_target_met'])
        self.assertEqual(m.summarize(d)['categories']['condense']['comparisons']['old']['half_length_successes'],0)
    def test_missing_review_does_not_pass(self):
        d=fixture(); del d['outputs'][2]['human_intent']
        self.assertFalse(m.summarize(d)['proposed_target_met'])
    def test_incomplete_or_duplicate_outputs_rejected(self):
        d=fixture(); d['outputs'].pop()
        with self.assertRaises(ValueError): m.summarize(d)
        d=fixture(); d['outputs'].append(d['outputs'][0])
        with self.assertRaises(ValueError): m.summarize(d)
    def test_controls_do_not_count_toward_compression_target(self):
        d=fixture(); d['cases'][0]['category']='control'
        self.assertFalse(m.summarize(d)['proposed_target_met'])
    def test_failed_exact_check_cannot_pass(self):
        d=fixture(); d['outputs'][2]['checks']={'command':False}
        self.assertFalse(m.summarize(d)['proposed_target_met'])

    def test_exact_spans_are_recomputed(self):
        d=fixture(); d['cases'][0]['exact_spans']=['untouched-command']
        d['outputs'][2]['checks']={'command':True}
        self.assertFalse(m.summarize(d)['proposed_target_met'])
    def test_primary_category_is_explicit(self):
        d=fixture(); d['cases'][0]['category']='generate'
        d['primary_category']='generate'
        self.assertTrue(m.summarize(d)['proposed_target_met'])

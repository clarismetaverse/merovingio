"""Panoptikon v1.3: geometry vs support graph vs temporal precedence.

All Jev judgments are typed and non-generative. Identical final geometry,
roles, supports and non-temporal DAG edges for both geneaologies. Only the
precedence edge and relative timestamps change in the temporal condition.
"""
from __future__ import annotations
import hashlib
import json
import math
import os
from pathlib import Path
import random
import sys
import requests

MODEL = 'jev-1.14.0'
A=(0.,0.)
B=(10.,0.)
SHAPES={
    'iso_low':(5.,4.),
    'iso_high':(5.,8.),
    'scalene_left':(3.2,6.4),
    'scalene_right':(7.1,5.2),
}
HISTORIES=('upper_first','lower_first')
PRESENTATIONS=('canonical','reversed','shuffled')
CONDITIONS=('final','supports','chronology')


def distance(p,q):
    return math.hypot(p[0]-q[0],p[1]-q[1])


def geometric_oracle(shape):
    C=SHAPES[shape]
    angle_foot=(10.*distance(A,C)/(distance(A,C)+distance(B,C)),0.)
    right_foot=(C[0],0.)
    iso=abs(distance(A,C)-distance(B,C)) < 1e-9
    shared=distance(angle_foot,right_foot) < 1e-9
    if iso!=shared:raise AssertionError('Angle/normal geometry inconsistent')
    if not 0<angle_foot[0]<10 or not 0<right_foot[0]<10:
        raise AssertionError('Foot out of AB')
    return {'upper_support':'CD' if shared else 'CE',
            'lower_support':'CD' if shared else 'CH',
            'shared_carrier':shared,
            'cross_pair_metric_equality':False,
            'point_set':({'A':A,'B':B,'C':C,'D':right_foot} if shared else
                         {'A':A,'B':B,'C':C,'E':angle_foot,'H':right_foot})}


def final_state(shape):
    g=geometric_oracle(shape)
    return {
      'points':sorted(g['point_set']),
      'base':{'id':'AB','from':'A','to':'B'},
      'angular_pair_at_apex':{
          'id':'S_UPPER','vertex':'C',
          'pair':'two adjoining angular sectors of equal internal measure',
          'carrier_id':g['upper_support']},
      'right_angle_pair_at_base':{
          'id':'S_LOWER',
          'pair':'two adjoining right angles formed against AB',
          'carrier_id':g['lower_support']},
      'restrictions':'These pair-wise equalities imply NO cross-pair equality of angle measures.',
    }


def graph(shape,history,include_time=False):
    """Support graph is constant across histories; time is the only treatment."""
    if history not in HISTORIES:raise ValueError(history)
    geo=geometric_oracle(shape)
    nodes=[
      {'id':'W0','kind':'material_workspace', 'supports':['AB','AC','BC']},
      {'id':'U','kind':'partition', 'produces':'S_UPPER',
       'depends_on':['W0'], 'carrier_id':geo['upper_support']},
      {'id':'L','kind':'partition', 'produces':'S_LOWER',
       'depends_on':['W0'], 'carrier_id':geo['lower_support']},
      {'id':'F','kind':'state', 'depends_on':['U','L']},
    ]
    edges=[{'from':'W0','to':'U','relation':'required'},
           {'from':'W0','to':'L','relation':'required'},
           {'from':'U','to':'F','relation':'constitutes'},
           {'from':'L','to':'F','relation':'constitutes'}]
    if include_time:
        before,after=('U','L') if history=='upper_first' else ('L','U')
        times={'W0':0,'F':3,before:1,after:2}
        nodes=[{**n,'step':times[n['id']]} for n in nodes]
        edges.append({'from':before,'to':after,'relation':'happens_before'})
    return {'nodes':nodes,'edges':edges,
            'interpretation':('Event step numbers and typed edges define chronology, never list placement' if include_time else 'Only material support/dependency relations; list placement is not evidence of time')}


def permute_graph(g,presentation,shape,history,condition):
    if presentation not in PRESENTATIONS:raise ValueError(presentation)
    output={'nodes':[dict(v) for v in g['nodes']],
            'edges':[dict(v) for v in g['edges']],
            'interpretation':g['interpretation']}
    if presentation=='reversed':
        output['nodes'].reverse()
        output['edges'].reverse()
    elif presentation=='shuffled':
        seed=(20261017 + 13*list(SHAPES).index(shape)
              + 31*PRESENTATIONS.index(presentation))
        # History and treatment deliberately excluded: the permutation is matched.
        rng=random.Random(seed)
        rng.shuffle(output['nodes'])
        rng.shuffle(output['edges'])
    return output


def canonical_signature(g):
    obj={'nodes':sorted(g['nodes'],key=lambda v:v['id']),
         'edges':sorted(g['edges'],key=lambda e:(e['from'],e['to'],e['relation']))}
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def make_payload(shape,condition,history='upper_first',presentation='canonical'):
    if condition not in CONDITIONS:raise ValueError(condition)
    state={
        'geometric_workspace':final_state(shape),
        'epistemic_scope':'Structural roles and measured angles are distinct; no theorem target or proof is supplied.',
    }
    if condition!='final':
        state['support_graph']=permute_graph(
            graph(shape,history,include_time=condition=='chronology'),
            presentation,shape,history,condition)
    questions={
        'shared_carrier':{
            'type':'noul',
            'instructions':'Are the two angle-pair Mental Spaces supported by one and the same physical carrier?',
            'criteria':{
                'true':'Exactly one material carrier is shared by both pairs',
                'false':'The pair partitions use distinct material carriers'}
        },
        'false_metric_transfer':{
            'type':'noul',
            'instructions':'Must each half-angle at the apex equal a corresponding right angle at the base in measure?',
            'criteria':{
                'true':'Cross-level measures necessarily coincide',
                'false':'No cross-level measure equality follows'}
        },
        'exploratory_focus':{
            'type':'choice',
            'instructions':(
                'Choose one structurally promising reading to explore next in this workspace. '
                'Every reading is potentially meaningful and NO unique objectively optimal answer '
                'is known. Prioritize a useful future line of attention; avoid inferring a theorem.'),
            'criteria':{
                'apex':'Investigate the upper pair as a partition at the apex',
                'base':'Investigate the two right angles at the base',
                'joint':'Investigate a joint correspondence of upper and lower pairs',
                'separate':'Investigate the two partitions as distinct Mental Spaces',
            }
        },
    }
    if condition=='chronology':
        questions['last_emergence']={
            'type':'choice',
            'instructions':(
                'Based on step numbers and happens_before edges, which of the two '
                'angular-partition spaces was created later? Ignore array order.'),
            'criteria':{
                'upper':'The upper apex partition appeared later',
                'lower':'The lower right-angle pair appeared later'},
        }
    return {'model':MODEL,'state':state,'questions':questions}


def schedule():
    result=[]
    for shape in SHAPES:
        # Baseline repeated twice for noise estimation.
        for repeat in (0,1):
            result.append({'shape':shape,'condition':'final','repeat':repeat})
        for history in HISTORIES:
            for presentation in PRESENTATIONS:
                for cond in ('supports','chronology'):
                    result.append({'shape':shape,'history':history,
                                   'presentation':presentation,'condition':cond})
    return result


def request_jev(payload):
    key=os.environ.get('TYPESAFE_API_KEY')
    if not key:raise RuntimeError('TYPESAFE_API_KEY is not configured')
    response=requests.post('https://api.typesafe.ai/v1/systemone',json=payload,
                           headers={'Authorization':'Bearer '+key},timeout=90)
    if response.status_code!=200:
        # Avoid emitting error body containing possible account details.
        raise RuntimeError('Jev HTTP '+str(response.status_code))
    data=response.json()
    answers=data.get('answers',{})
    if not all(k in answers for k in payload['questions']):
        raise RuntimeError('Incomplete typed response')
    out={}
    for name in ('shared_carrier','false_metric_transfer'):
        v=answers[name].get('noul')
        if not isinstance(v,(float,int)) or not 0<=v<=1:
            raise RuntimeError('Invalid Noul response')
        out[name]=float(v)
    for name in ('exploratory_focus','last_emergence'):
        if name in answers:
            item=answers[name]
            allowed=payload['questions'][name]['criteria']
            if item.get('choice') not in allowed:
                raise RuntimeError('Unknown choice')
            out[name]={'choice':item['choice'],'probabilities':item.get('probabilities'),
                       'confidence':item.get('confidence')}
    out['usage']=data.get('usage')
    out['model']=data.get('model')
    return out


def p_joint(record):
    p=record['response']['exploratory_focus'].get('probabilities') or {}
    return p.get('joint') if isinstance(p,dict) else None


def produce_report(destination):
    if not os.environ.get('TYPESAFE_API_KEY'):
        raise SystemExit('Missing TYPESAFE_API_KEY: no live calls made')
    destination=Path(destination)
    destination.mkdir(parents=True,exist_ok=True)
    trials=[]
    for item in schedule():
        shape=item['shape'];cond=item['condition']
        h=item.get('history','upper_first')
        presentation=item.get('presentation','canonical')
        response=request_jev(make_payload(shape,cond,h,presentation))
        oracle=geometric_oracle(shape)
        record={**item,'response':response,
                'oracle_shared_carrier':oracle['shared_carrier'],
                'shared_correct':(response['shared_carrier']>=0.5)==oracle['shared_carrier'],
                'cross_metric_rejection_correct':response['false_metric_transfer']<0.5}
        if cond=='chronology':
            later='lower' if h=='upper_first' else 'upper'
            record['later_expected_offline']=later
            record['later_correct']=response['last_emergence']['choice']==later
            record['graph_signature']=canonical_signature(graph(shape,h,True))
        elif cond=='supports':
            record['graph_signature']=canonical_signature(graph(shape,h,False))
        trials.append(record)
        print(f'{shape}/{cond}/{h}/{presentation}: shared={record["shared_correct"]} p_joint={p_joint(record)}',flush=True)
    agg={}
    for cond in CONDITIONS:
        subset=[x for x in trials if x['condition']==cond]
        agg[cond]={
            'n':len(subset),
            'shared_correct':sum(x['shared_correct'] for x in subset),
            'metric_reject_correct':sum(x['cross_metric_rejection_correct'] for x in subset),
            'mean_joint_probability':round(sum(p_joint(x) or 0 for x in subset)/len(subset),5),
            'input_tokens':sum((x['response']['usage'] or {}).get('input_tokens',0) for x in subset),
            'output_tokens':sum((x['response']['usage'] or {}).get('output_tokens',0) for x in subset),
        }
    agg['chronology']['later_correct']=sum(x.get('later_correct',False) for x in trials)
    agg['chronology']['later_tested']=sum('later_correct' in x for x in trials)
    paired=[]
    for shape in SHAPES:
        for presentation in PRESENTATIONS:
            def vals(cond,h):
                return [p_joint(r) for r in trials if r['shape']==shape and
                        r['condition']==cond and r.get('presentation')==presentation and
                        r.get('history')==h][0]
            base_up=vals('supports','upper_first')
            base_low=vals('supports','lower_first')
            time_up=vals('chronology','upper_first')
            time_low=vals('chronology','lower_first')
            paired.append({'shape':shape,'presentation':presentation,
                           'support_replication_gap':round(base_up-base_low,5),
                           'chronology_direction_delta':round(time_up-time_low,5),
                           'difference_in_differences':round((time_up-time_low)-(base_up-base_low),5)})
    report={'experiment':'Panoptikon v1.3 factorial causal genealogy ablation',
            'conditions':{'final':'geometry only',
                          'supports':'geometry plus support DAG, no time/order',
                          'chronology':'same support DAG with timestamps and one temporal edge'},
            'scope':'Only ranking of pre-authored Mental Spaces, not spontaneous discovery or proof.',
            'summary':agg,'matched_differences':paired,
            'trials':trials}
    (destination/'jev_causal_ablation_v13.json').write_text(
        json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print('Wrote sanitized report',agg,flush=True)
    return report

if __name__=='__main__':
    produce_report(sys.argv[1] if len(sys.argv)>1 else 'output')
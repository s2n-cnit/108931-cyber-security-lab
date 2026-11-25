"""Flow-level IDS evaluation; unique directional tuples in supplied datasets."""
import argparse, csv, json

def key(row):
    return (row['src_ip'],int(row['src_port']),row['dest_ip'],int(row['dest_port']),row['proto'].upper())

def evaluate(labels, events, sid):
    truth={}
    for row in labels:
        k=key(row)
        if k in truth: raise ValueError('Duplicate label tuple')
        if row['label'] not in ('0','1'): raise ValueError('Expected binary label')
        truth[k]=int(row['label'])
    alerted=set()
    for event in events:
        if event.get('event_type')=='alert' and event.get('alert',{}).get('signature_id')==sid:
            alerted.add(key(event))
    tp=sum(v==1 and k in alerted for k,v in truth.items()); tn=sum(v==0 and k not in alerted for k,v in truth.items())
    fp=sum(v==0 and k in alerted for k,v in truth.items()); fn=sum(v==1 and k not in alerted for k,v in truth.items())
    def ratio(n,d): return n/d if d else None
    return dict(TP=tp,TN=tn,FP=fp,FN=fn,accuracy=ratio(tp+tn,len(truth)),precision=ratio(tp,tp+fp),recall=ratio(tp,tp+fn),fpr=ratio(fp,fp+tn),f1=ratio(2*tp,2*tp+fp+fn),unmatched_alert_tuples=len(alerted-truth.keys()))

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--labels',required=True); p.add_argument('--eve',required=True); p.add_argument('--sid',type=int,default=1000001); a=p.parse_args()
    with open(a.labels) as f,open(a.eve) as e:
        print(json.dumps(evaluate(csv.DictReader(f),(json.loads(l) for l in e if l.strip()),a.sid),indent=2))
if __name__=='__main__': main()

"""Group numeric CSV data; approximate t critical values via conservative df lookup."""
import argparse,csv,statistics,math,json
from collections import defaultdict
# 95% two-sided t critical values, use nearest lower df conservatively.
T={1:12.706,2:4.303,3:3.182,4:2.776,5:2.571,6:2.447,7:2.365,8:2.306,9:2.262,10:2.228,12:2.179,15:2.131,20:2.086,25:2.060,29:2.045,30:2.042,40:2.021,60:2.000,120:1.980}
def summarize(values):
    n=len(values)
    if not n: raise ValueError('Empty sample')
    mean=statistics.mean(values); sd=statistics.stdev(values) if n>1 else None
    half=T[max(k for k in T if k<=n-1)]*sd/math.sqrt(n) if n>1 else None
    return dict(n=n,mean=mean,median=statistics.median(values),sd=sd,ci95=[mean-half,mean+half] if half is not None else None)
def main():
    p=argparse.ArgumentParser(); p.add_argument('csv'); p.add_argument('--group',required=True); p.add_argument('--value',required=True); a=p.parse_args(); groups=defaultdict(list)
    with open(a.csv) as f:
        for row in csv.DictReader(f):
            if row[a.value].strip(): groups[row[a.group]].append(float(row[a.value]))
    print(json.dumps({k:summarize(v) for k,v in groups.items()},indent=2))
if __name__=='__main__': main()

import argparse, csv, subprocess, random
from pathlib import Path

def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',required=True); p.add_argument('--samples',type=int,default=30); a=p.parse_args()
    if a.samples<1: p.error('samples must be positive')
    modes=['HTTP','TLS1.2','TLS1.3']*a.samples; random.Random(42).shuffle(modes)
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    with open(a.output,'w',newline='') as f:
        w=csv.writer(f); w.writerow(['mode','tcp_ms','handshake_ms','total_ms'])
        for mode in modes:
            port=80 if mode=='HTTP' else 443
            cmd=['curl','--noproxy','*','--fail','--silent','--show-error','--max-time','5','--resolve',f'web.lab.test:{port}:10.0.20.10','-o','/dev/null','-w','%{time_connect},%{time_appconnect},%{time_total}']
            if mode!='HTTP':
                v=mode[3:]; cmd+=['--cacert','work/lab-ca.crt','--tlsv'+v,'--tls-max',v]
            cmd += [f'{"http" if port==80 else "https"}://web.lab.test/']
            tcp,tls,total=map(float,subprocess.check_output(cmd,text=True).split(','))
            w.writerow([mode,tcp*1000,'' if port==80 else (tls-tcp)*1000,total*1000]); f.flush()
if __name__=='__main__': main()

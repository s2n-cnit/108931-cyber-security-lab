"""Deterministic synthetic Ethernet/IPv4/TCP/UDP PCAPs. No external traffic."""
import argparse,csv,struct,socket,random
from pathlib import Path
SRC='10.0.10.10'; DST='10.0.20.10'; MARK='/lab5-test-marker'
def checksum(data):
    if len(data)%2: data+=b'\0'
    s=sum(struct.unpack('!%dH'%(len(data)//2),data))
    while s>>16: s=(s&65535)+(s>>16)
    return (~s)&65535

def frame(src,dst,sport,dport,payload=b'',seq=0,ack=0,flags=0x18,proto=6):
    a,b=socket.inet_aton(src),socket.inet_aton(dst)
    if proto==6:
        seg=struct.pack('!HHIIBBHHH',sport,dport,seq,ack,0x50,flags,64240,0,0)+payload
        c=checksum(a+b+struct.pack('!BBH',0,proto,len(seg))+seg)
        seg=seg[:16]+struct.pack('!H',c)+seg[18:]
    else:
        seg=struct.pack('!HHHH',sport,dport,8+len(payload),0)+payload
        c=checksum(a+b+struct.pack('!BBH',0,proto,len(seg))+seg)
        seg=seg[:6]+struct.pack('!H',c or 65535)+seg[8:]
    ip=struct.pack('!BBHHHBBH4s4s',0x45,0,20+len(seg),1,0x4000,64,proto,0,a,b)
    ip=ip[:10]+struct.pack('!H',checksum(ip))+ip[12:]
    mac=lambda x: bytes([2,0,0,0,int(x.split('.')[2]),int(x.split('.')[3])])
    return mac(dst)+mac(src)+b'\x08\x00'+ip+seg

def tcp_flow(port,path):
    req=f'GET {path} HTTP/1.1\r\nHost: web.lab.test\r\nConnection: close\r\n\r\n'.encode()
    resp=b'HTTP/1.1 200 OK\r\nContent-Length: 3\r\nConnection: close\r\n\r\nOK\n'
    x,y=1000,5000
    def c(seq,ack,flags,p=b''): return frame(SRC,DST,port,80,p,seq,ack,flags)
    def s(seq,ack,flags,p=b''): return frame(DST,SRC,80,port,p,seq,ack,flags)
    xe=x+1+len(req); ye=y+1+len(resp)
    return [c(x,0,2),s(y,x+1,18),c(x+1,y+1,16),c(x+1,y+1,24,req),s(y+1,xe,16),s(y+1,xe,24,resp),c(xe,ye,16),s(ye,xe,17),c(xe,ye+1,17),s(ye+1,xe+1,16)]

def dns_frames():
    q=b'\x03web\x03lab\x04test\x00'+struct.pack('!HH',1,1)
    query=struct.pack('!HHHHHH',123,0x0100,1,0,0,0)+q
    reply=struct.pack('!HHHHHH',123,0x8180,1,1,0,0)+q+b'\xc0\x0c'+struct.pack('!HHIH',1,1,60,4)+socket.inet_aton(DST)
    return [frame(SRC,'10.0.10.1',53000,53,query,proto=17),frame('10.0.10.1',SRC,53,53000,reply,proto=17)]

def write_pcap(path,frames):
    with path.open('wb') as f:
        f.write(struct.pack('<IHHIIII',0xa1b2c3d4,2,4,0,0,65535,1))
        for i,p in enumerate(frames):
            f.write(struct.pack('<IIII',1700000000+i//100,10000*(i%100),len(p),len(p))); f.write(p)

def ids(out,name,start,counts,seed):
    paths=[(MARK,1)]*counts[0]+[(MARK+'-preview',0)]*counts[1]+[('/index',0)]*counts[2]
    random.Random(seed).shuffle(paths); frames=[]; rows=[]
    for i,(path,label) in enumerate(paths):
        port=start+i; frames.extend(tcp_flow(port,path)); rows.append([SRC,port,DST,80,'TCP',label])
    write_pcap(out/'pcap'/f'{name}.pcap',frames)
    with (out/'labels'/f'{name}.csv').open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['src_ip','src_port','dest_ip','dest_port','proto','label']); w.writerows(rows)

def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',default='datasets'); a=p.parse_args(); out=Path(a.output)
    for d in ['pcap','labels']: (out/d).mkdir(parents=True,exist_ok=True)
    write_pcap(out/'pcap/lab01-baseline.pcap',dns_frames()+sum((tcp_flow(30000+i,'/index') for i in range(3)),[]))
    write_pcap(out/'pcap/lab01-investigation.pcap',dns_frames()+sum((tcp_flow(31000+i,MARK if i>=3 else '/index') for i in range(15)),[]))
    ids(out,'ids-calibration',32000,(10,5,35),42)
    ids(out,'ids-test',34000,(20,8,72),99)
if __name__=='__main__': main()

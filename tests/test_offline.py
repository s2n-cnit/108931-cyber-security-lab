import unittest, csv, struct, tempfile, subprocess, sys
from pathlib import Path
from tools.ids_metrics import evaluate
from tools.stats import summarize
from tools.generate_datasets import checksum,frame
ROOT=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
    def test_metrics(self):
        labels=[dict(src_ip='a',src_port=i,dest_ip='b',dest_port=80,proto='TCP',label=str(i<2 and 1 or 0)) for i in range(4)]
        events=[dict(labels[i],event_type='alert',alert={'signature_id':1}) for i in (0,0,2)]
        r=evaluate(labels,events,1)
        self.assertEqual([r[k] for k in ('TP','TN','FP','FN')],[1,1,1,1]); self.assertEqual(r['f1'],.5)
    def test_undefined(self):
        self.assertIsNone(evaluate([],[],1)['accuracy'])
    def test_stats(self):
        r=summarize([1,2,3]); self.assertEqual(r['mean'],2); self.assertEqual(r['sd'],1); self.assertEqual(r['median'],2)
    def test_checksums(self):
        p=frame('10.0.10.10','10.0.20.10',30000,80,b'hello'); ip=p[14:34]; tcp=p[34:]
        self.assertEqual(checksum(ip),0); self.assertEqual(checksum(ip[12:20]+struct.pack('!BBH',0,6,len(tcp))+tcp),0)
    def test_pcaps(self):
        for name,count in [('lab01-baseline',32),('lab01-investigation',152),('ids-calibration',500),('ids-test',1000)]:
            data=(ROOT/'datasets/pcap'/f'{name}.pcap').read_bytes(); self.assertEqual(data[:4],b'\xd4\xc3\xb2\xa1'); pos=24; n=0
            while pos<len(data):
                _,_,size,wire=struct.unpack_from('<IIII',data,pos); self.assertEqual(size,wire); pos+=16+size; n+=1
            self.assertEqual(pos,len(data)); self.assertEqual(n,count)
    def test_labels(self):
        for name,count,pos in [('ids-calibration',50,10),('ids-test',100,20)]:
            with (ROOT/'datasets/labels'/f'{name}.csv').open() as f: rows=list(csv.DictReader(f))
            self.assertEqual(len(rows),count); self.assertEqual(sum(int(r['label']) for r in rows),pos); self.assertEqual(len({r['src_port'] for r in rows}),count)
    def test_reproducibility(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run([sys.executable,str(ROOT/'tools/generate_datasets.py'),'--output',d],check=True)
            for folder in ('pcap','labels'):
                for path in (ROOT/'datasets'/folder).iterdir(): self.assertEqual(path.read_bytes(),(Path(d)/folder/path.name).read_bytes())
if __name__=='__main__': unittest.main()

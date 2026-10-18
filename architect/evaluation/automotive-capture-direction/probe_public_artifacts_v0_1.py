#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, subprocess, urllib.parse, urllib.request
from pathlib import Path

OUT=Path('/tmp/automotive-capture-artifacts'); OUT.mkdir(parents=True,exist_ok=True)
CASES=[
 {'id':'S_BUICK_REFLECTION','title':'File:1937 Buick Limited.jpg','kind':'image'},
 {'id':'S_DODGE_REFLECTION','title':'File:1968 Dodge Dart GTS (5279696196).jpg','kind':'image'},
 {'id':'V_GREEN_EXPO','title':'File:Green Vehicle Expo 2025 (Bangalore International Exhibition Centre).webm','kind':'video'},
 {'id':'V_AIXAM_EXPO','title':"File:Aixam Crossline - Mondial de l'Automobile de Paris 2014 - 002.webm",'kind':'video'},
]

def info(title):
 q=urllib.parse.urlencode({'action':'query','format':'json','prop':'imageinfo','iiprop':'url|sha1|size|mime|extmetadata','titles':title})
 req=urllib.request.Request('https://commons.wikimedia.org/w/api.php?'+q,headers={'User-Agent':'professional-ai-agents-eval/1.0'})
 with urllib.request.urlopen(req,timeout=60) as r: p=json.loads(r.read().decode())
 page=next(iter(p['query']['pages'].values())); ii=page['imageinfo'][0]
 return ii

def dl(url,path):
 req=urllib.request.Request(url,headers={'User-Agent':'professional-ai-agents-eval/1.0'})
 with urllib.request.urlopen(req,timeout=180) as r, open(path,'wb') as f:
  while True:
   b=r.read(1024*1024)
   if not b: break
   f.write(b)

def sha256(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def duration(path):
 s=subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(path)],text=True).strip()
 return float(s)

rows=[]
for c in CASES:
 ii=info(c['title']); ext='.jpg' if c['kind']=='image' else '.webm'; media=OUT/(c['id']+ext); dl(ii['url'],media)
 row={'id':c['id'],'title':c['title'],'kind':c['kind'],'commons_sha1':ii.get('sha1'),'download_sha256':'sha256:'+sha256(media),'bytes':media.stat().st_size,'mime':ii.get('mime'),'width':ii.get('width'),'height':ii.get('height'),'source_page':'https://commons.wikimedia.org/wiki/'+urllib.parse.quote(c['title'].replace(' ','_'))}
 if c['kind']=='image':
  thumb=OUT/(c['id']+'-preview.jpg')
  subprocess.check_call(['ffmpeg','-loglevel','error','-y','-i',str(media),'-vf','scale=960:-2',str(thumb)])
  row['preview_sha256']='sha256:'+sha256(thumb)
 else:
  d=duration(media); row['duration_seconds']=d; frames=[]
  for j,fraction in enumerate((0.12,0.35,0.58,0.82),1):
   frame=OUT/(f"{c['id']}-f{j}.jpg")
   subprocess.check_call(['ffmpeg','-loglevel','error','-y','-ss',str(max(0,d*fraction)),'-i',str(media),'-frames:v','1','-vf','scale=640:-2',str(frame)])
   frames.append(frame)
  sheet=OUT/(c['id']+'-contact.jpg')
  cmd=['ffmpeg','-loglevel','error','-y']
  for f in frames: cmd += ['-i',str(f)]
  cmd += ['-filter_complex','[0:v][1:v]hstack=inputs=2[top];[2:v][3:v]hstack=inputs=2[bottom];[top][bottom]vstack=inputs=2[out]','-map','[out]',str(sheet)]
  subprocess.check_call(cmd)
  row['contact_sheet_sha256']='sha256:'+sha256(sheet)
 rows.append(row)
(OUT/'manifest.json').write_text(json.dumps({'schema_version':'0.1.0','candidate_calls':0,'judge_calls':0,'artifacts':rows},indent=2)+'\n')
print(json.dumps({'status':'PASS','artifact_count':len(rows),'out':str(OUT)}))

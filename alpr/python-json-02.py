import json
result = open('result02.json','r')
l = result.read()
result.close()
l = l.replace("'",'"')
l = l.replace('False','false')
l = l.replace('True','true')

obj = json.loads(l)

print(json.dumps(obj, sort_keys=True, indent=4))

for r in obj['results']:
   p = str(r['plate'])
  # print(json.dump(r['plate'],sort_keys=True,indent=4))
   print('print=',p)
   v = r['vehicle']
   color = v['color']
   make = v['make']
   model = v['body_type']
   for m in make:
       if m['confidence'] > 50:
           print('Make:',m['name'],m['confidence'])

   for c in color:
       if c['confidence'] > 30:
           print('Color:',c['name'],c['confidence'])
   
   for mo in model:
       if mo['confidence'] > 50:
           print('model:',mo['name'],mo['confidence'])
#!/usr/bin/python

```
usage: python make_sub_file.py format command
```

#read format
format = []
for line in open(sys.argv[1], 'r'):
  format.append(line.strip())
  
#read command
for n, line in enumerate(open(sys.argv[2],'r')):
  filename = "sub"+str(n)+".sub"
  fwrite = open(filename, 'w')
  fwrite.write('\n'.join(format))
  fwrite.write(line)
  fwrite.close()

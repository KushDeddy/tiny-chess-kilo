# Tiny Chess Engine v3 - Ultra Compact Alpha-Beta
import sys,time as T
PI={ord(c):0 for c in 'pnqrk'};PI.update({ord(c.upper()):1 for c in 'pnqrk'})
PV=[0,100,320,330,500,900,20000]*2
PS=[[0]*64 for _ in range(12)]
for i in range(8):PS[0][i*8+3]+=20;PS[0][i*8+4]+=20
for i in range(8):PS[1][i*8+2]+=15;PS[1][i*8+5]+=15
for i in range(8):PS[2][i*8+3]+=15;PS[2][i*8+4]+=15
for i in range(8):PS[3][i*8+i]+=10;PS[3][i*8+7-i]+=10
for i in range(8):PS[4][i*8+3]+=10;PS[4][i*8+4]+=10
def parse(fen):bd=[0]*120;r=c=0
 for ch in fen:
  if ch.isdigit():c+=int(ch)
  elif ch=='/':r+=1;c=0
  elif ch in PI:bd[r*10+c]=PI[ch]
 return bd
def at(b,r,c):return b[r*10+c]if 0<=r<8and 0<=c<8else-1
def gm(b,cl):ms=[];en=1-cl
 for r in range(8):
  for c in range(8):
   t=at(b,r,c);pc=t%7
   if not t or pc==6 and cl!=t>0:continue
   if pc==6:
    for dr in(-1,0,1):
     for dc in(-1,0,1):
      if not(dr or dc):continue
      nr,nc=r+dr,c+dc
      if 0<=nr<8and 0<=nc<8:
       u=at(b,nr,nc)
       if not u or(u%7==6 and u%7!=pc):ms.append((r,c,nr,nc,0))
   elif pc<5:
    d=((0,1),(0,-1),(0,2),(0,-2),(1,0),(-1,0))[pc] if pc<3 else((1,1),(1,-1),(-1,1),(-1,-1))[pc-3] if pc<5 else((1,2),(2,1),(2,-1),(1,-2),(-1,2),(-2,1),(-2,-1),(-1,-2))[pc-5]
    for dr,dc in(d if pc<3 else((1,1),(1,-1),(-1,1),(-1,-1))if pc<5 else((1,2),(2,1),(2,-1),(1,-2),(-1,2),(-2,1),(-2,-1),(-1,-2))[pc-5]):
     nr,nc=r+dr,c+dc
     if not(0<=nr<8and 0<=nc<8):continue
     u=at(b,nr,nc)
     if pc<3:
      if u:break
      if pc==0 and nr==r and(not u or u%7==6):
       if nr==0 or nr==7:
        for p in[4,2,3,1]:ms.append((r,c,nr,nc,p))
       else:ms.append((r,c,nr,nc,4))
       if pc==0 and((cl==0 and r==1)or(cl==1 and r==6))and not at(b,r+dr*2,dc+c):ms.append((r,c,r+dr*2,dc+c,4))
      continue
     if pc==4:
      if u%7==6:ms.append((r,c,nr,nc,0))
      break
     if u%7!=en:ms.append((r,c,nr,nc,0))
     break
 return ms
def cp(b,m):return at(b,m[2],m[3])
def evl(b):s=0
 for r in range(8):
  for c in range(8):
   t=b[r*10+c]
   if t:s+=PV[t%7]*(t>0)+PS[t%7][r*8+c]*(t>0)
 return s
TT={};TM=0
def ab(b,d,a,bt,mx):
 global TM;TM+=1
 if d==0:return evl(b)
 k=str(b)[:64];k=k[:128]
 if k in TT and TT[k][1]>=d:return TT[k]
 ms=gm(b,mx)
 if not ms:return 0if d>1else(-100000if mx else 100000)
 cv=[(-cp(b,m)+100)for m in ms];ms=sorted(ms,key=lambda x:cv[ms.index(x)],reverse=True)
 v=-200000
 for m in ms:
  nb=list(b);nb[m[2]*10+m[3]]=nb[m[0]*10+m[1]];nb[m[0]*10+m[1]]=0
  if cp(b,m)==5:nb[m[2]*10+m[3]]=12if mx else6
  elif cp(b,m)==11:nb[m[2]*10+m[3]]=4if mx else10
  elif m[4]:nb[m[2]*10+m[3]]=5if mx else11
  v2=-ab(nb,d-1,-bt,-max(v,-bt),1-mx)
  if v2>v:v=v2
  if v>a:a=v
  if a>=bt:TT[k]=(a,d);return a
 TT[k]=(v,d);return v
def go(fen,tm=3000):
 b=parse(fen);mx=1;dp=1;st=T.time()
 while T.time()-st<tm/1000:
  dp+=1;res=ab(b,dp,-200000,200000,mx)
  ms=gm(b,mx)
  cv=[(-cp(b,m)+100)for m in ms];ms=sorted(ms,key=lambda x:cv[ms.index(x)],reverse=True)
  best=None;bv=-200001
  for m in ms:
   nb=list(b);nb[m[2]*10+m[3]]=nb[m[0]*10+m[1]];nb[m[0]*10+m[1]]=0
   if cp(b,m)==5:nb[m[2]*10+m[3]]=12if mx else6
   elif cp(b,m)==11:nb[m[2]*10+m[3]]=4if mx else10
   elif m[4]:nb[m[2]*10+m[3]]=5if mx else11
   v2=-ab(nb,dp-1,-200000,200000,1-mx)
   if v2>bv:bv=v2;best=m
   if T.time()-st>tm/1000:break
  if best:
   fr,fc,tr,tc=best[0],best[1],best[2],best[3]
   pm='';p=best[4]
   if p==1:pm='p'
   elif p==2:pm='n'
   elif p==3:pm='r'
   elif p==4:pm='q'
   sys.stdout.write(chr(97+fc)+chr(49-fr)+chr(97+tc)+chr(49-tr)+pm+'\n')
   sys.stdout.flush();b=nb[:];mx=1-mx
if __name__=='__main__':
 fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
 while True:
  ln=sys.stdin.readline().strip()
  if not ln:break
  if ln=='uci':print('id name TinyChess\nid author Auto\nuciok')
  elif ln=='isready':print('readyok')
  elif ln.startswith('position'):fen=ln.split()[1]
  elif ln=='go':go(fen)
  elif ln=='quit':break

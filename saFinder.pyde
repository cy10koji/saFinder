# Strange attractor finder basically based on  Sprott’s algorithm.
# Programmed by Koji Saito ( @KojiSaito / Twitter )
#
# Added to the calculation of logical fractal dimension,
# the fractal dimension calculation in screen space has been added, too.
 
import math

InitX=InitY=.05
X=[0]*500;Y=[0]*500
N1=N2=1

def init():
    global XE,YE,Lsum,Xmin,Xmax,Ymin,Ymax,N1,N2
    YE=.05;XE=InitX+.000001
    Lsum=0;N1=N2=1 # due to avoid divide by zero.
    Xmin=Ymin=1000000;Xmax=Ymax=-Xmin
    id=[int(random(25)) for i in range(12)]
    coef=[(t-12)*.1 for t in id]
    idStr=""
    for c in id:idStr+=chr(ord('A')+c)
    return coef,idStr

def next(coef,x,y):
    xNew=coef[0]+x*(coef[1]+coef[2]*x+coef[3]*y)+y*(coef[ 4]+coef[ 5]*y)
    yNew=coef[6]+x*(coef[7]+coef[8]*x+coef[9]*y)+y*(coef[10]+coef[11]*y)
    return xNew,yNew

def updateBound(x,y):
    global Xmin,Xmax,Ymin,Ymax
    Xmin=min(x,Xmin);Xmax=max(x,Xmax)
    Ymin=min(y,Ymin);Ymax=max(y,Ymax)

def LyapunovExponent(coef,x,y,n):
    global XE,YE,Lsum
    tx,ty=next(coef,XE,YE)
    dLx=tx-x;dLy=ty-y
    dL2=dLx*dLx+dLy*dLy
    df=1e12*dL2;rs=1/sqrt(df)
    XE=x+rs*(tx-x);YE=y+rs*(ty-y)
    Lsum+=log(df)
    return .721347*Lsum/n # L=Lyapunov exponent

# in logical space (no resolution)
def updateN1N2(x,y,i):
    global N1,N2
    d2max=(Xmax-Xmin)**2+(Ymax-Ymin)**2
    t=(i+int(random(480)))%500
    d2=(x-X[t])**2+(y-Y[t])**2
    r2=(.1)**2*d2max
    if d2<r2:N2=N2+1
    if d2<r2/4:N1=N1+1

# in screen space (image space) 
def updateN1N2onFs(x,y,i):
    global N1,N2
    t=(i+int(random(480)))%500
    d2=(x-X[t])**2+(y-Y[t])**2
    r2=10**2    # 10 pixel
    if d2<r2:N2=N2+1
    if d2<r2/4:N1=N1+1

fractalDimension=lambda:log(N2/float(N1))/log(2)
    
kFractalDimensionThreshold=0.1

def search():
    f=0
    found=False
    while not(found): # or f<kFractalDimensionThreshold:
        coef,idStr=init()
        x,y=InitX,InitY
        found=True
        for i in range(1000):
            x,y=next(coef,x,y)
            if abs(x)+abs(y)>1e6:found=False;break
            X[i%500]=x;Y[i%500]=y
        if not(found):continue
        for i in range(10000):
            x,y=next(coef,x,y)
            if abs(x)+abs(y)>1e6:found=False;break
            updateBound(x,y)
            n=i+1000
            l=LyapunovExponent(coef,x,y,n)
            if i>1500:updateN1N2(x,y,n)
            X[n%500]=x;Y[n%500]=y
            # original Sprott's program threshold is .005
            if l<.005:found=False;break # threshold backup .002
        # if found:f=fractalDimension()
    return coef,idStr
    
def calcScale(coef,w,h):
    init()
    x,y=InitX,InitY
    for i in range(1000):x,y=next(coef,x,y);updateBound(x,y)
    dx=.1*(Xmax-Xmin);dy=.1*(Ymax-Ymin)
    xl=Xmin-dx;xh=Xmax+dx
    yl=Ymin-dy;yh=Ymax+dy
    sx=w/(xh-xl);sy=h/(yh-yl)
    return sx,sy,xl,yl

def setColor(idStr):
    colorH=538
    for c in idStr:colorH=ord(c)+colorH*33
    colorH%=251
    s=[0]*3;t=colorH%3
    s[t]=3;s[(t+1)%3]=1.5;s[(t+2)%3]=.8
    colorMode(HSB,250);c=color(colorH,190,200) # make color here
    colorMode(RGB,255);blendMode(ADD);
    plotColor=color(s[0]*(red(c)+40),s[1]*(green(c)+40),s[2]*(blue(c)+40))
    stroke(plotColor)
    return plotColor

IdStt=""
Coef=[]
PlotColor=0
N=90000

# calc fractal dimension in screen space
def screenSpaceFractalDimension(sx,sy,tx,ty,ioGrid):
    x,y=InitX,InitY
    for i in range(1000):x,y=next(Coef,x,y)
    N1=N2=1
    uSum=vSum=0
    totalNum=10000
    numThreshold=1500
    for i in range(totalNum):
        x,y=next(Coef,x,y)
        u=(x-tx)*sx;v=(y-ty)*sy
        n=i+1000
        if i>numThreshold:updateN1N2onFs(u,v,n);uSum+=u;vSum+=v
        X[n%500]=u;Y[n%500]=v
        ix=int(u/50);iy=int(v/50)
        if ix<0 or 10<=ix or iy<0 or 10<=iy:continue
        ioGrid[iy*10+ix]+=1
    nForAve=totalNum-numThreshold
    return fractalDimension(),uSum/nForAve,vSum/nForAve

def screenSpaceCorrelation(sx,sy,tx,ty,meanX,meanY):
    x,y=InitX,InitY
    for i in range(1000):x,y=next(Coef,x,y)
    s=sigmaX=sigmaY=0
    totalNum=10000
    numThreshold=1500
    for i in range(totalNum):
        x,y=next(Coef,x,y)
        u=(x-tx)*sx;v=(y-ty)*sy
        if i<=numThreshold:continue
        s+=(u-meanX)*(v-meanY)
        sigmaX+=(u-meanX)**2
        sigmaY+=(v-meanY)**2
    n=totalNum-numThreshold
    return (s/n)/(sqrt(sigmaX/n)*sqrt(sigmaY/n))

def screenSpaceFractalDimensionByBoxCounting():
    loadPixels()
    count=0
    for v in range(50):
        top=v*10
        for u in range(50):
            left=u*10
            for i in range(100): # grid size 10x10
                y=top+i//10
                x=left+i%10
                c=pixels[x+y*width]
                if c&0xFFFFFF!=0:
                    count+=1
                    break
    # print('count='+str(count))
    return log(count)/log(50)

def drawSA(w,h):
  global Coef,IdStr,PlotColor,N1,N2
  clear()
  found=False
  while not(found):
    Coef,IdStr=search()
    PlotColor=setColor(IdStr)
    sx,sy,tx,ty=calcScale(Coef,w,h)
    grid=[0]*100
    fs,meanX,meanY=screenSpaceFractalDimension(sx,sy,tx,ty,grid)
    found=fs>kFractalDimensionThreshold
    if not(found):continue
    r=screenSpaceCorrelation(sx,sy,tx,ty,meanX,meanY)    
    sum=0.0
    n=len(grid)
    ave=100 # =10000/100 # =sum/float(n)
    t=0
    for i in range(n):t+=(grid[i]-ave)**2
    sigma2=t/float(n)
    cv2=sigma2/(ave**2) # cv = Coefficient of Variation
    numOfZeroGrid=0
    for g in grid:
        if g==0:numOfZeroGrid+=1
    found=found and sqrt(cv2)<4 and abs(r)<.92 and numOfZeroGrid<70  # 2.5
    
  print("ID="+IdStr+" Fs="+str(fs),"cv="+str(sqrt(cv2)),'R='+str(r),'Gz='+str(numOfZeroGrid))
  drawInBlendMode()

def drawInBlendMode():
    clear()
    blendMode(ADD)
    sx,sy,tx,ty=calcScale(Coef,width,height)
    stroke(PlotColor)
    x,y=InitX,InitY
    for _ in range(N):x,y=next(Coef,x,y);point((x-tx)*sx,(y-ty)*sy)

def render(fileName):
    w=h=2000
    hiResImage=createImage(w,h,RGB)
    sx,sy,tx,ty=calcScale(Coef,w,h)
    x,y=InitX,InitY
    for i in range(N*w/width*h/height):
        x,y=next(Coef,x,y)
        u,v=int(sx*(x-tx)),int(sy*(y-ty))
        if u<0 or w<=u or v<0 or h<=v:continue
        c=hiResImage.pixels[w*v+u]
        hiResImage.pixels[w*v+u]=color(red(c)+red(PlotColor),
                                       green(c)+green(PlotColor),
                                       blue(c)+blue(PlotColor))
    hiResImage.save(fileName)

Mode=+1
def setup():size(500,500);drawSA(width,height)
def keyPressed():
    global Mode
    if key==' ':
        print('searching...');
        while(True):
            drawSA(width,height)
            f=screenSpaceFractalDimensionByBoxCounting()
            if f<1.6:
                print("SEARCH AGAIN")
            else:
                break
        print('F-Dim by BoxCounting='+str(f))
    if key=='s':
        print("Generating Hi-Res Image: "+IdStr+".png ...")
        render(IdStr+'.png')
        # save(IdStr+'.jpg') # if you need...
        print("Done.")
    if key=='t':genTweet()
    if key=="T":printTweetPaperAndInk()
    if key=="p":drawPaperAndInk()
    if key=='r':drawInBlendMode()
    if ('0'<=key and key<='9') or ('a'<=key and key<'c'):explorer(key)
    if key=='+':Mode=+1;print("Mode PLUS")
    if key=='-':Mode=-1;print("Mode MINUS")

def draw():random(1);

CoefStr=["-1.2","-1.1","-1",
         "-.9","-.8","-.7","-.6","-.5","-.4","-.3","-.2","-.1","+0",
         "+.1","+.2","+.3","+.4","+.5","+.6","+.7","+.8","+.9","+1",
         "+1.1","+1.2"]
def genTweet():
    print("------------------")
    print("#StrAttrCat #StrangeAttractor Catalog")
    print("# ID: "+IdStr)
    print("size(500,500)")
    print("clear()")    
    print("stroke("+str(int(red(PlotColor)))+","
                   +str(int(green(PlotColor)))+","
                   +str(int(blue(PlotColor)))+")")
    print("blendMode(ADD)")
    print("x=y=.05")
    codeStr="for _ in range(5**7):"
    codeStr+=genUpdateCode("u=",0)+";"
    codeStr+=genUpdateCode("v=",6)+";"
    sx,sy,tx,ty=calcScale(Coef,width,height)
    pointStr="point("+str(int(sx))+"*(u"+'{:+.1f}'.format(-tx)+"),"
    pointStr+=str(int(sy))+"*(v"+'{:+.1f}'.format(-ty)+"))"
    codeStr+=pointStr+";x,y=u,v"
    print(codeStr)
    
def genTweetPaperAndInk():
    codeStr="for _ in [0]*(6**7):"
    codeStr+="S(255,199);P(R(700),R(700));S(0,0,80,99);"
    codeStr+=genUpdateCode("u=",0)+";"
    codeStr+=genUpdateCode("v=",6)+";"
    sx,sy,tx,ty=calcScale(Coef,width,height)
    pointStr="P("+str(int(sx))+"*(u"+'{:+.1f}'.format(-tx)+"),"
    pointStr+=str(int(sy))+"*(v"+'{:+.1f}'.format(-ty)+"))"
    codeStr+=pointStr+";x,y=u,v"
    return codeStr
def printTweetPaperAndInk():
    codeStr=genTweetPaperAndInk()
    print("------------------")
    print("#StrAttrCat")
    print("# ID: "+IdStr+" (paper&ink)")
    print("size(500,500)")
    print("P=point;R=random;S=stroke")
    print("x=y=.05")
    print(codeStr)
def drawPaperAndInk():
    P=point;R=random;S=stroke
    x=y=.05
    codeStr=genTweetPaperAndInk()
    background(200)
    blendMode(REPLACE)
    exec(codeStr)

def genUpdateCode(initStr,t):
    ret=initStr
    ordA=ord('A')
    ret+=CoefStr[ord(IdStr[t+0])-ordA]
    ret+="+x*("+CoefStr[ord(IdStr[t+1])-ordA]
    ret+=CoefStr[ord(IdStr[t+2])-ordA]+"*x"
    ret+=CoefStr[ord(IdStr[t+3])-ordA]+"*y)+y*("
    ret+=CoefStr[ord(IdStr[t+4])-ordA]
    ret+=CoefStr[ord(IdStr[t+5])-ordA]+"*y)"
    return ret
def explorer(c):
    global IdStr,Coef,PlotColor
    if '0'<=c and c<='9':t=ord(c)-ord('0')
    if 'a'==c or c=='b':t=ord(c)-ord('a')+10
    IdStr=IdStr[:t]+chr((ord(IdStr[t])-ord('A')+Mode+25)%25+ord('A'))+IdStr[t+1:]
    print('IdStr='+IdStr)
    Coef=[(ord(c)-ord('A')-12)*.1 for c in IdStr]
    clear()
    PlotColor=setColor(IdStr)
    sx,sy,tx,ty=calcScale(Coef,width,height)
    x,y=InitX,InitY
    for i in range(N):x,y=next(Coef,x,y);point((x-tx)*sx,(y-ty)*sy)

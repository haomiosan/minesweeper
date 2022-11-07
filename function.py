import random as r

alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n',
            'o','p','q','r','s','t','u','v','w','x','y','z']

def start():                            #请先阅读readme
    with open("readme.txt",'r',encoding="UTF-8") as f:
        temp=f.readline()
        if temp=="false\n":
            print("\n开始游玩前请确认已经阅读过readme.txt")
            return 1
    return 0

def pre():                              #获取雷盘数据
    print("\n请选择难度：\n1.eazy\n2.normal\n3.hard\n4.custom")
    while True:
        dif=int(input("请输入难度前序号："))
        if dif==1 or dif==2 or dif==3 or dif==4:
            break
        else:
            print("输入不符合规范")
    if dif==1:
        return 9,9,10
    elif dif==2:
        return 16,16,40
    elif dif==3:
        return 16,30,99
    else:
        return custom()
    
def custom():                           #获取自定义雷盘数据
    while True:
        n=int(input("请输入纵向长度[9-24]："))
        if 8<n<25:
            break
        else:
            print("输入不符合规范")
    while True:
        m=int(input("请输入横向长度[9-30]："))
        if 8<m<31:
            break
        else:
            print("输入不符合规范")
    b=int(input("请输入雷数[10-[0.9*格数]]："))
    if 9<b<int(0.9*n*m)+1:
        pass
    else:
        print("输入不符合规范，系统将自动贴合上边界或下边界")
        if b<10:
            b=10
        else:
            b=int(0.9*n*m)
    return n,m,b

def create(n,m,b,x,y):                  #生成雷盘
    mine=[]
    boom=0
    while True:
        mine,boom=summon(mine,n,m,b,boom)
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if i<0 or i>=n or j<0 or j>=m:
                    continue
                if mine[i][j]==1:
                    mine[i][j]=0
                    boom-=1
        if boom!=b:
            continue
        else:
            return mine

def summon(mine,n,m,b,boom):            #生成雷盘
    grids=n*m
    if mine==[]:
        for i in range(n):
            mine.append([])
            for _ in range(m):
                mine[i].append(0)
    if boom==0:
        for i in range(n):
            for j in range(m):
                isboom=r.randint(0,grids-i*m-j)
                if isboom<b-boom:
                    mine[i][j]=1
                    boom+=1
                else:
                    mine[i][j]=0
    else:
        tempboom=0
        for i in range(n):
            for j in range(m):
                if mine[i][j]==1:
                    tempboom+=1
                    continue
                isboom=r.randint(0,grids-i*m-j-(b-tempboom)+1)
                if isboom<b-boom:
                    mine[i][j]=1
                    boom+=1
                    tempboom+=1
                else:
                    mine[i][j]=0


    return mine,boom

def showcreate(n,m):                    #生成显示棋盘
    showmine=[]
    for i in range(n):
        showmine.append([])
        for _ in range(m):
               showmine[i].append(0)
    return showmine

def explain():                          #操作指令介绍
    print("\n注意事项：")
    print("由于开发者技术力不够，本程序无法进行图形交互，相关操作需要使用命令行执行")
    print("使用\"-1 纵坐标+横坐标\"执行排雷操作，例如：-1 d6")
    print("使用\"-2 纵坐标+横坐标\"执行插旗或拔旗操作，例如：-2 d6")
    print("两种操作均支持多格操作，例如：-2 d6 f7 e8")
    print("不建议排雷操作使用过多格，除非十分确定")
    print("支持两种操作同时操作，例如：-1 d6 -2 e7 f8")
    print("两种操作可以互相穿插，例如：-2 d6 -1 e7 -2 f8")
    print("两种操作同时执行时默认优先执行插旗操作")
    print("第一次操作请输入只包含一格操作格的排雷操作")
    print("每次输入操作摁下enter前请检查是否存在语法错误，本程序已避免因输入越界而造成错误")
    print("如因语法错误导致错误，请用户自己承担，例如马上解完但语法错误导致整盘无效")
    print("如已知晓请摁下enter键\n")
    input()

def cut(opt):                           #切分命令行
    if opt[0]=='-':
        return [int(opt[1])]
    else:
        return [opt[0],int(opt[1:])]

def opt1(mine,showmine,exploered,n,m,x,y):        #扫雷操作
    boom=judge(mine,n,m,x,y)
    if boom!=0:
        showmine[x][y]=boom
        return showmine,exploered+1
    templist=[]
    templist=exploer(mine,templist,n,m,x,y)
    for i in range(len(templist)):
        if i%2==1:
            continue
        if templist[i+1]==0:
            templist[i+1]=9
        showmine[templist[i][0]][templist[i][1]]=templist[i+1]
    return showmine,exploered+len(templist)/2

def exploer(mine,templist,n,m,x,y):     #深搜大面积开图
    if [x,y] in templist:
        return templist
    templist.append([x,y])
    templist.append(0)
    for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if i<0 or i>=n or j<0 or j>=m:
                    continue
                boom=judge(mine,n,m,i,j)
                if boom==0:
                    templist=exploer(mine,templist,n,m,i,j)
                else:
                    templist.append([i,j])
                    templist.append(boom)
    return templist

def judge(mine,n,m,x,y):                #判断对应格显示
    boom=0
    for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if i<0 or i>=n or j<0 or j>=m:
                    continue
                if mine[i][j]==1:
                    boom+=1
    return boom

def opt2(showmine,flag,x,y):            #插旗或拔旗操作
    if showmine[x][y]==0:
        showmine[x][y]=10
        flag+=1
    elif showmine[x][y]==10:
        showmine[x][y]=0
        flag-=1
    return showmine,flag

def show(mine,n,m,b,flag):              #显示雷盘
    print('\n'*30)
    print("当前剩余雷数：%3d"%(b-flag))
    print("   ",end='')
    for i in range(m):
        if i<10:
            print('',i+1,'',end='')
        else:
            print('',i+1,'',end='')
    print("")
    for i in range(n):
        print('',alphabet[i],'',end='')
        for j in range(m):
            if mine[i][j]==0:
                print(" ■ ",end='')     #未挖格
            elif mine[i][j]==9:
                print(" □ ",end='')     #已挖格
            elif mine[i][j]==10:
                print(" X ",end='')     #插旗格
            else:
                print('',mine[i][j],end=' ')
        print('')
    print('')
    print("请输入下一次操作:")

def lose(showmine,mine,n,m,x,y):
    for i in range(n):
        for j in range(m):
            if mine[i][j]==1:
                if showmine[i][j]==0:       #未标旗的雷
                    showmine[i][j]=11   
            else:
                if showmine[i][j]==10:      #标错的旗
                    showmine[i][j]=12
    showmine[x][y]=13                       #引炸的雷
    print("")
    for i in range(n):
        print('',alphabet[i],'',end='')
        for j in range(m):
            if showmine[i][j]==0:
                print(" ■ ",end='')
            elif showmine[i][j]==9:
                print(" □ ",end='')
            elif showmine[i][j]==10:
                print(" \033[0;32mX\033[0m ",end='')
            elif showmine[i][j]==11:
                print(" \033[0;37mX\033[0m ",end='')
            elif showmine[i][j]==12:
                print(" \033[1;31mX\033[0m ",end='')
            elif showmine[i][j]==13:
                print(" \033[1;30;41mX\033[0m ",end='')
            else:
                print('',showmine[i][j],end=' ')
        print('')
    print("BOOM!\nYou are lose.")
    print("绿x代表标对的旗，红x代表标错的旗，红底黑x代表挖炸的雷")
    input("如想重新游玩，请摁下enter键之后重新启动")

def win(showmine,mine,n,m):
    print("Congradulations!")
    print("虽然不知道你能否从此程序获得成就感")
    print("But,whatever.感谢游玩")
    input("摁下enter即可退出")
    pass

def savedata():                         #储存胜负数据
    #反正也没人会长期玩，懒得写了
    pass

if __name__=="__main__":
    print("请使用main.py启动")

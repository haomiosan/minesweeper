from function import *

alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n',
            'o','p','q','r','s','t','u','v','w','x','y','z']

if __name__=="__main__":
    if start():
        exit()
    n,m,b=pre()                                 #获取地图大小及雷数
    flag,exploered=0,0
    showmine=showcreate(n,m)
    explain()                                   #显示注意事项
    show(showmine,n,m,b,flag)                   #显示未开图雷盘
    opts=list(map(cut,input().split()))         #接受第一次开图操作行
    x,y=alphabet.index(opts[1][0]),opts[1][1]-1
    mine=create(n,m,b,x,y)
    showmine,exploered=opt1(mine,showmine,exploered,n,m,x,y)
    show(showmine,n,m,b,flag)                   #显示初始雷盘
    while True:                                 #循环输入操作行
        command=[[],[]]
        isflag=[]
        outcome,over,t=0,0,0
        opts=list(map(cut,input().split()))
        for i in opts:                          #接受并切分操作行并判断越界
            if len(i)==1:
                opt=i[0]
            else:
                i[0],i[1]=alphabet.index(i[0]),i[1]-1
                if i[0]>=n or i[1]>=m:
                    over+=1
                    break
                command[opt-1].append(i)
        if over!=0:                             #如操作格越界则进行下一次输入
            print(str(over)+"个操作格不在范围内，请全部重新输入：",end='')
            continue
        for i in command[1]:                    #执行插旗插旗操作
            showmine,flag=opt2(showmine,flag,i[0],i[1])
        for i in command[0]:                    #执行排雷操作并判断是否引炸
            if showmine[i[0]][i[1]]==10:
                isflag.append([alphabet[i[0]],str(i[1]+1)])
                t+=1
                continue
            if mine[i[0]][i[1]]==1:
                lose(showmine,mine,n,m,i[0],i[1])
                outcome=1
                break
            showmine,exploered=opt1(mine,showmine,exploered,n,m,i[0],i[1])
        if outcome==1:                          #如已引炸则停止游戏
            break
        show(showmine,n,m,b,flag)               #显示操作后雷盘
        if t!=0:                                #输出已插旗但被执行排雷操作的格
            if t==1:
                print(isflag[0][0]+isflag[0][1]+"已插旗，如需取消该格旗，请使用：-2 "+isflag[0][0]+isflag[0][1])
            else:
                print(isflag[0][0]+isflag[0][1]+"等共"+str(t)+"已插旗，如需取消该格旗，请使用例如：-2 "+isflag[0][0]+isflag[0][1])
        if flag==b:                             #如旗数等于雷数且没有未插旗空位则胜利
            if flag+exploered==n*m:
                win(showmine,mine,n,m)       
                break
    exit()
import functions

binary = ['128','64','32','16','8','4','2','1','0']
jg = []
ad = 257
#print binary
for i in range(9):
    numb = int(binary[i])
    if ad == numb:       # 当输入的值跟binary列表中的值一样，表示直接用个1就可以表示了， 后面就不会继续获取了，剩下的位置需要用0来补充
        jg.append('1')
        jg.append((len(binary)-i-1)*'0')    # binary 列表的长度 - 当前的下标 - 1, 下标从0 开始的，所有需要多减一个1, 减完后表示后面需要补充的0
        break

    elif ad > numb:     # 当输入的值大于当前值，需要做个减法，把余下的值继续做匹配， 同时添加一个1，
        ad = ad - numb
        jg.append('1')
    else:               # 当输入值小于当前值，用0填充，不写也行
        jg.append('0')
print(''.join(jg))
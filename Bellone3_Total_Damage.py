import math
import numpy as np
import matplotlib.pyplot as plt

def is_int_or_int_str(x):
    if isinstance(x, int):
        return True
    if isinstance(x, str):
        try:
            int(x)
            return True
        except ValueError:
            return False
    return False

def Bellone3_Total_Damage(Elite, Lv, Mod, Pt, HP, Df, hp_sk, T1_Stack):
    #Elite精英化等级2
    #Lv等级1-90
    #Mod模组等级0-3
    #Pt潜能1-6
    #HP敌方单位最大血量
    #Df防御（计入所有除了贝洛内自身第一天赋的buff）
    #hp_sk技能开启时已造成的伤害
    #T1_Stack技能开启时目标身上第一天赋的叠层
    if Elite==0:
        return 'Not applicable for E0.' #不适用于无精
    elif Elite==1:
        return 'Not applicable for E1.' #不适用于精一
    elif Elite>2 or (not is_int_or_int_str(Elite)):
        return 'Error in entry Elite. Enter 2.'
    elif Lv<1 or Lv>90 or (not is_int_or_int_str(Lv)):
        return 'Error in entry Lv. Enter an integer in range [1,90].'
    elif Mod<0 or Mod>3 or (not is_int_or_int_str(Mod)):
        return 'Error in entry Mod. Enter an integer in range [0,3].'
    elif Pt<1 or Pt>6 or (not is_int_or_int_str(Pt)):
        return 'Error in entry Pt. Enter an integer in range [1,6].'
    elif T1_Stack<0 or (not is_int_or_int_str(T1_Stack)):
        return 'Error in entry T1_Stack. Enter a non-negative integer.'
    else:
        atk=(550+round((Lv-1)*115/89))+(Mod>0)*(Mod*15+35)+(Pt>3)*24 #攻击力
        Ign_Df=0.07+(Mod==3)*0.01 #降低防御
        Bonus_Damage=0.28+(Mod>1)*0.14+(Pt>4)*0.08 #残血增伤；之前是Damage_Inc，后来看到Arknights Wiki上写的Bonus Damage就改过来了，希望我全改了
        Total_Hits=55+(Mod>0)*4
        
        Db_atk=atk*2.7 #技能期面板攻击
        St_crit=max(Db_atk*1.85-Df*(1-Ign_Df*5),Db_atk*1.85*0.05) #标准暴击伤害
        St_ncrit=max(Db_atk-Df*(1-Ign_Df*5),Db_atk*0.05) #标准非暴击伤害
        FullT1_exp=St_crit*(1+Bonus_Damage)*0.5+St_ncrit*(1+Bonus_Damage)*0.5 #叠满第一天赋增伤后每hit期望伤害
        THR=0.8*HP #残血阈值
        r_crit=1+St_crit*Bonus_Damage/THR #暴击公比
        r_ncrit=1+St_ncrit*Bonus_Damage/THR #非暴击公比
        T1_StReg=min(T1_Stack,4) #标准化第一天赋叠的额外层数至4

        S=0

        def count_crit(x,S0):
            return max(math.ceil(math.log((THR+THR/Bonus_Damage)/((S0+THR/Bonus_Damage)*r_ncrit**x),r_crit/r_ncrit)),0) #在受到S0的伤害之后，如果要在x次攻击后过阈值，则至少要暴击多少次
        
        for n in range(2**(4-T1_StReg)):
            Stage1_Damage=hp_sk #减防期间伤害
            for i in range(4-T1_StReg):
                Crit_State=int((bin(n)[2:].zfill(4-T1_StReg))[i]) #第i次是否暴击
                Stage1_Damage+=max(Db_atk*(1+Crit_State*0.85)-Df*(1-(i+1+T1_StReg)*Ign_Df),Db_atk*(1+Crit_State*0.85)*0.05)*(1+Bonus_Damage*min(Stage1_Damage/THR,1)) #叠满减防之前的伤害
                
            n_min=math.ceil(math.log((THR+THR/Bonus_Damage)/(Stage1_Damage+THR/Bonus_Damage),r_crit)) #至少多少hit过阈值=刚好过阈值时至多暴击多少次
            n_max=math.ceil(math.log((THR+THR/Bonus_Damage)/(Stage1_Damage+THR/Bonus_Damage),r_ncrit)) #至多多少hit过阈值
            Crit_Situ=[] #统计所有的过阈值暴击情况
            for i in range(n_min,min(51+(Mod>0)*4+T1_StReg,n_max)+1): #过阈值时多少hit
                for j in range((count_crit(i,Stage1_Damage))*(i!=51+(Mod>0)*4+T1_StReg),min(count_crit(i-1,Stage1_Damage),i)+1): #其中多少hit是暴击
                    Crit_Situ.append((i,j,j==count_crit(i-1,Stage1_Damage))) #最后一个argument是这一hit是否暴击
                    
            Sub_Exp=0 #将每一种过阈值情况对应的伤害按概率加权加进期望伤害里
            for i in Crit_Situ:
                Sub_Exp+=((Stage1_Damage+THR/Bonus_Damage)*r_crit**i[1]*r_ncrit**(i[0]-i[1])-THR/Bonus_Damage)*(math.comb(i[0]-i[2],i[1]-i[2])/2**i[0]) #进阈值之前的伤害
                Sub_Exp+=((51+(Mod>0)*4+T1_StReg-i[0])*FullT1_exp)*(math.comb(i[0]-i[2],i[1]-i[2])/2**i[0]) #进阈值之后的（期望）伤害
            S+=Sub_Exp
            
        S/=2**(4-T1_StReg)
        return S

#计算总伤：用二分法解HP=Bellone3_Total_Damage(...,HP,...)这个方程。
#函数连续性不好不能迭代、容易进入循环，但是大体上是单调的，所以零点应该只有一个。可以通过matplotlib画图验证
#所以需要提前找好对应的两个端点，这个就需要自己估摸一下搞一搞了；以下给出了四个常用的配置，对应满潜/无潜+满模组/无模组，对应的端点在最后。

def f1(x):
    return Bellone3_Total_Damage(2,90,3,6,x,0,0,0)

def f2(x):
    return Bellone3_Total_Damage(2,90,0,6,x,0,0,0)

def f3(x):
    return Bellone3_Total_Damage(2,90,3,1,x,0,0,0)

def f4(x):
    return Bellone3_Total_Damage(2,90,0,1,x,0,0,0)

def Bisect(left,right,funct_for_att): #二分法；left左端点，right右端点，funct_for_att对应配置的函数
    for i in range(50):
        mid=(left+right)/2
        if (funct_for_att(mid)-mid)*(funct_for_att(left)-left)>0:
            left=mid
        elif (funct_for_att(mid)-mid)*(funct_for_att(left)-left)<0:
            right=mid
        else:
            return mid
    return mid

print(Bisect(220000,230000,f1))
print(Bisect(170000,180000,f2))
print(Bisect(200000,210000,f3))
print(Bisect(160000,170000,f4))

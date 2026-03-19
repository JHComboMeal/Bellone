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

def Bellone2_Total_Damage(Elite, Lv, Mod, Pt):
    #Elite精英化等级1，2
    #Lv等级1-90
    #Mod模组等级0-3
    #Pt潜能1-6
    if Elite==0:
        return 'Not applicable for E0.' #不适用于无精
    elif Elite>2 or (not is_int_or_int_str(Elite)):
        return 'Error in entry Elite. Enter 1 or 2.'
    elif Lv<1 or Lv>90 or (not is_int_or_int_str(Lv)) or (Elite==1 and Lv>80):
        return 'Error in entry Lv. Enter an integer in range [1,90] for Elite 2, or [1,80] for Elite 1.'
    elif Mod<0 or Mod>3 or (not is_int_or_int_str(Mod)) or (Elite==1 and Mod>0):
        return 'Error in entry Mod. Enter an integer in range [0,3] for Elite 2, or 0 for Elite 1.'
    elif Pt<1 or Pt>6 or (not is_int_or_int_str(Pt)):
        return 'Error in entry Pt. Enter an integer in range [1,6].'
    else:
        atk=(427+(123+round((Lv-1)*115/89))*(Elite==2)+round((Lv-1)*123/79)*(Elite==1))+(Mod>0)*(Mod*15+35)+(Pt>3)*24 #攻击力
        Damage_Inc=0.2+(Elite==2)*0.08+(Mod>1)*0.14+(Pt>4)*0.08 #残血增伤
        Damage_Perc=1+Damage_Inc

        def f(r,k):
            return (r**k-1)+(1+Damage_Inc)*(r-1)*(51+(Mod>0)*4-k)-Damage_Inc/0.8

        #解方程：(r^n-1)+(1+D_Inc)(r-1)(55-n)=D_Inc/0.8 且r^(n-1)<1+D_Inc<=r^n.
        for n in range(2,56):
            if f(Damage_Perc**(1/(n-1)),n)*f(Damage_Perc**(1/n),n)>0:
                pass
            elif f(Damage_Perc**(1/(n-1)),n)==0:
                HP=atk*2.5*Damage_Inc/(Damage_Perc**(1/(n-1))-1)
                return HP
            elif f(Damage_Perc**(1/(n)),n)==0:
                HP=atk*2.5*Damage_Inc/(Damage_Perc**(1/(n))-1)
                return HP
            else:
                l=Damage_Perc**(1/(n-1))
                r=Damage_Perc**(1/(n))
                for i in range(100):
                    m=(l+r)/2
                    if f(m,n)*f(l,n)<0:
                        r=m
                    elif f(m,n)*f(l,n)>0:
                        l=m
                    elif f(m,n)==0:
                        HP=atk*2.5*Damage_Inc/(m-1)
                        return HP
                HP=atk*2.5*Damage_Inc/(m-1)
                return HP

a=Bellone2_Total_Damage(2, 90, 0, 6)
print(a)
            
        

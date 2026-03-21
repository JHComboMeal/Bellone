# Bellone
## Overview
Bellone is a playable character in the game Arknights (CN), an operator in the class of Guard and branch of Fighter. This repository is dedicated to calculating damage-related stats of Bellone, mainly dealing with Skill 2 and 3.
Bellone3_Total_Damage calculates the total damage of S3 under different attributes and enemy conditions, including HP and def. When Module>0 we assume the attackspeed +10 buff is always on.
Bellone2 calculates the total damage of S2 under different attributes. Enemy conditions hasn't been added.

## Theory
We basically calculate the HP of an enemy with 0 def and art resistence that Bellone is just able to kill in expectation.
We notice that when the reduction in def in T1 is stacked to max and the enemy's HP is above 20%, the damage dealt is only dependent on the number of critical hits and is independent of the order of the critical hits.
Then everything collasped into solving a recursive formula for damage dealt before the enemy's HP drops below 20%, and separating each case of number of critical hits and total hits.
For the first at-most-4 hits when the reduction in def is still stacking, we basically separate each of the at-most-16 cases out and calculate the expectation in each case.

##Todo
Bellone S2: Add enemy conditions
Bellone S3: Calculate prob of killing enemy; Calculate expected number of hits of killing enemy

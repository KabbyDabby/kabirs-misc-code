# from random import randint

# max_trial = 0
# max_score = 0
# for trial in range(2**7):
#     player_guess = [trial%2==1, trial%4>=2, trial%8>=4, trial%16>=8, trial%32>=16, trial%64>=32, trial%128>=64]

#     count = 0

#     for i in range(100000):
#         a_wins = 0
#         b_wins = 0

#         i = 0

#         score = 0
#         while a_wins<4 and b_wins<4:
#             win = randint(0,1)
#             if win:
#                 a_wins+=1
#                 if player_guess[i]:
#                     score+=1
#             else:
#                 b_wins+=1
#                 if not player_guess[i]:
#                     score+=1

#             i+=1
        
#         if score>=3:
#             count+=1

#         if score = max_score
    
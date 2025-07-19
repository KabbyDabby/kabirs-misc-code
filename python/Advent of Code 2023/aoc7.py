from aoc7input import test_input
from aoc7input import actual_input

def sort_cards(cards):
    answer = ''
    hand = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(cards)):
        if cards[i].isdecimal():
            hand[int(cards[i])-2] += 1
        elif cards[i] == 'T':
            hand[8] += 1
        elif cards[i] == 'J':
            hand[9] += 1
        elif cards[i] == 'Q':
            hand[10] += 1
        elif cards[i] == 'K':
            hand[11] += 1
        elif cards[i] == 'A':
            hand[12] += 1

    if 5 in hand: 
        answer = '7'
    elif 4 in hand:
        answer = '6'
    elif 3 in hand:
        if 2 in hand:
            answer = '5'
        else:
            answer = '4'
    elif 2 in hand:
        two_count = 0
        for ha in hand:
            if ha == 2:
                two_count+=1
        
        if two_count == 2:
            answer = '3'
        else:
            answer = '2'
    elif 1 in hand:
        answer = '1'
    else:
        print("SHOULD NEVER HAPPEN FIX UR CRAP CODE")
    
    for j in range(len(cards)):
        if cards[j] == 'A':
            answer = answer + "14"
        elif cards[j] == 'K':
            answer = answer + "13"
        elif cards[j] == 'Q':
            answer = answer + "12"
        elif cards[j] == 'J':
            answer = answer + "11"
        elif cards[j] == 'T':
            answer = answer + "10"
        elif cards[j].isdecimal():
            answer = answer + cards[j].zfill(2)
    if len(answer) !=11:
        print(hand)
        print(cards)
        print(answer)
    return int(answer)

def part1(input):
    lines = input.split('\n')
    cards =[]
    bets = []
    for line in lines:
        stuff = line.split(' ')
        cards.append(stuff[0])
        bets.append(int (stuff[1]))
    cards_to_bets = {}
    for i in range(len(cards)):
        cards_to_bets[cards[i]] = bets[i]

    cards.sort(key=sort_cards)
    #print(cards)
    bets.clear()
    for card in cards:
        bets.append(cards_to_bets[card])
    #print(bets)

    total = 0
    for k in range(len(cards)):
        total+= (k+1)*cards_to_bets[cards[k]]
        #print(str(k+1)+'*'+str(cards_to_bets[cards[k]]))
    print(total)

def sort_cards_p2(cards):
    answer = ''
    hand = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    j_count = 0
    for i in range(len(cards)):
        if cards[i].isdecimal():
            hand[int(cards[i])-2] += 1
        elif cards[i] == 'T':
            hand[8] += 1
        elif cards[i] == 'J':
            j_count+=1
        elif cards[i] == 'Q':
            hand[10] += 1
        elif cards[i] == 'K':
            hand[11] += 1
        elif cards[i] == 'A':
            hand[12] += 1
    max = 0
    index = -1
    for i in range(len(hand)):
        if hand[i]>max:
            max = hand[i]
            index = i
    hand[index] += j_count

    
    sum = 0
    for ha in hand:
        sum+=ha
    if sum != 5:
        print(cards)
        print(hand)
        print("fix your goddamn code")
    

    if 5 in hand: 
        answer = '7'
    elif 4 in hand:
        answer = '6'
    elif 3 in hand:
        if 2 in hand:
            answer = '5'
        else:
            answer = '4'
    elif 2 in hand:
        two_count = 0
        for ha in hand:
            if ha == 2:
                two_count+=1
        
        if two_count == 2:
            answer = '3'
        else:
            answer = '2'
    elif 1 in hand:
        answer = '1'
    else:
        print("SHOULD NEVER HAPPEN FIX UR CRAP CODE")
    
    for j in range(len(cards)):
        if cards[j] == 'A':
            answer = answer + "14"
        elif cards[j] == 'K':
            answer = answer + "13"
        elif cards[j] == 'Q':
            answer = answer + "12"
        elif cards[j] == 'J':
            answer = answer + "1".zfill(2)
        elif cards[j] == 'T':
            answer = answer + "10"
        elif cards[j].isdecimal():
            answer = answer + cards[j].zfill(2)
    if len(answer) !=11:
        print(hand)
        print(cards)
        print(answer)
    return int(answer)
#part1(test_input)
#part1(actual_input)

def part2(input):
    lines = input.split('\n')
    cards =[]
    bets = []
    for line in lines:
        stuff = line.split(' ')
        cards.append(stuff[0])
        bets.append(int (stuff[1]))
    cards_to_bets = {}
    for i in range(len(cards)):
        cards_to_bets[cards[i]] = bets[i]

    cards.sort(key=sort_cards_p2)
    #print(cards)
    bets.clear()
    for card in cards:
        bets.append(cards_to_bets[card])
    #print(bets)

    total = 0
    for k in range(len(cards)):
        total+= (k+1)*cards_to_bets[cards[k]]
        #print(str(k+1)+'*'+str(cards_to_bets[cards[k]]))
    print(total)
#part2(test_input)
part2(actual_input)
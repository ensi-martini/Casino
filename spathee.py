from easygui import *
from objects import *

deck = Deck(1)
deck.shuffle()

player_hands = []
player_stashes = []
player_points = []
player_clubs = []
player_names = ['first', 'second', 'third', 'fourth']

field = Hand()

tutorial = boolbox('Would you like a tutorial?', 'Spathee')

if tutorial:
    msgbox('Spathee is a game about adding up cards in your hand and the field to equal numbers, then "claiming" them to your pile. If you cannot make a claim, you must "tribute" a card from your hand by adding it to the field for anyone, even yourself on a different turn, to claim.\nThere are five points for determining who wins; the player with the most points at the end wins the game.\n2 points are won by having the largest pile of "claimed" cards, 1 point is for the player who claims the most clubs (\u2663), 1 point for the player who claimed the 2 of clubs (2\u2663), and 1 point for the player who claims the 10 of diamonds (10\u2666).', 'Basics')
    
    msgbox('There are between 2 and 4 players for each game. The field is made up of 4 cards, and each player is dealt from the deck 4 cards each round. Players take turns in a circle, and each player can make one "claim" when it is their turn.\nAn ace is worth 1, 2-9 are 2-9 respectively, and face cards are not considered numbers; they can only be matched with an equal face card (J for J, Q for Q, K for K).\nSuits do not matter when matching numbers.\nWhen it is a player\'s turn, they can add up any cards on the field to match the value of a card in their hand, then adds those cards to their pile.', 'Mechanics')
    
    msgbox("For example, if I have a hand of ['A\u2660', 'A\u2663', '7\u2666', 'J\u2665'], and the field is ['8\u2660', '2\u2665', 'J\u2666', '5\u2665'], I have several options;\n -I can claim the 2\u2665 and the 5\u2665 on the field with my 7\u2666\n -I can claim the J\u2666 on the field with my J\u2665\nHowever, I cannot;\n -Claim the 2\u2665 on the field with my A\u2660 and my A\u2663\n -Claim the 8\u2660 with my A\u2663 and 7\u2666", 'Examples')

players = buttonbox('How many players? (2 - 4)', 'Spathee', (2, 3, 4))

for card in range (4):
    field.append(deck.deal())

for player in range(players):
    
    player_points.append(0)
    player_clubs.append(0)
    player_hands.append(Hand())
    player_stashes.append(Hand())    
    
    
#These variable is used later to determine the player(s) with the largest pile of cards and most club suit cards, respectivly.
largest_pile = 0
most_clubs = 0
#This variable is used to determine who the last player to make a claim was
last_claim = 0

while len(deck) > 0:
    
    if len(player_hands[-1]) == 0:
        
        msgbox('Dealing each player 4 cards...', 'Spathee')
        
        #Dealing each player 4 cards
        for player in range(len(player_hands)):
            for card in range (4):
                player_hands[player].append(deck.deal())   
            
    for player in range(len(player_hands)):     
        
        if len(field) > 0:
            choice = buttonbox('The field is {}. You have {}. Would you like to make a claim or tribute a card?'.format(field.str_list(),  player_hands[player].str_list()), 'Spathee', ('Claim', 'Tribute'))
        
        if choice == 'Claim':
            #This variable is used to evaluate whether a claim is valid or not
            sum_bool = False 
            
            while sum_bool == False:
                
                match_list = field[:]
                match_list.append('Done')
                addend_cards = Hand()
                
                matches = buttonbox("{} player's turn.\nWhat cards would you like to add up?".format(player_names[player].capitalize()), 'Spathee', (match_list))
        
                while type(matches) == Card:
                    
                    addend_cards.append(matches)
                    match_list.remove(matches)
                        
                    matches = buttonbox("Any other cards?", 'Spathee', (match_list))                
                    
                match_list.pop(-1)
                
                match_list = player_hands[player]
                
                sum_card = buttonbox('Which card would you like to claim?', 'Spathee', (match_list))
                
                if len(addend_cards) == 1 and addend_cards[0].number == sum_card.number:
                    sum_bool = True
                    
                elif addend_cards.value() == sum_card.value() and sum_card.number not in 'JQK':
                    sum_bool = True
                
            player_stashes[player].append(sum_card)
                                
            for card in addend_cards:
                player_stashes[player].append(card)
                field.remove(card)
                
            player_hands[player].remove(sum_card)
                
            msgbox('{} has been claimed by the {} player with {}.\nYou now have {} cards in your pile'.format(sum_card, player_names[player], addend_cards.str_list(), len(player_stashes[player])), 'Spathee')
            
            last_claim = player
            
        elif choice == 'Tribute' or len(field) == 0:
            
            tribute = buttonbox('Which card would you like to tribute?', 'Spathee', (player_hands[player]))
            field.append(tribute)
            player_hands[player].remove(tribute)
            
#Giving the last player to make a claim all the remaining cards on the field            
if len(field) > 0:
    for card in field:
        player_stashes[last_claim].append(card)
        
#Calculating the score of each player and determining the winner            
for player in range(len(player_hands)):
    
    for card in player_hands[player]:
        
        if card == Card('2', '\u2663'):
            player_points[player] += 1
            
        if card == Card('10', '\u2666'):
            player_points[player] += 1
            
        if card.suit == '\u2663':
            player_clubs[player] += 1   
            
    if len(player_hands[player]) > len(player_hands[largest_pile]):
        largest_pile = player
        
    elif len(player_hands[player]) == len(player_hands[largest_pile]):
        #Since there are only 2 points to give out, first two players to meet this requirement get a point each
        player_points[largest_pile] += 1
        player_points[player] += 1
        
    if player_clubs[player] > player_clubs[most_clubs]:
        most_clubs = player     
           
player_points[most_clubs] += 1

msgbox('{} player is the winner, with {} points!'.format(player_names[player_points.index(max(player_points)).capitalize(), max(player_points)], 'Spathee'))

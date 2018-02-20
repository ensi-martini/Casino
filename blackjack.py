#Task 2 Blackjack

from objects import *
from easygui import *

msgbox('Welcome to Blackjack! Rules: Dealers stand on all 17s, blackjacks pay 3:2, you can only split once, split blackjacks do not count as real blackjacks.', 'Blackjack')
money = 100

amount = buttonbox('How many decks will we be playing with?', 'Blackjack', (1,2,3,4,5,6,7,8))
decks = Deck(amount)
decks.shuffle()

bet = ''

while money > 0 and bet != None:

    choice = ''
    p_hand = Hand()
    d_hand = Hand()

    bet = enterbox('How much would you like to bet?\nYou have ${}'.format(money), 'Blackjack')

    if bet != None:

        while bet.isnumeric() == False or int(bet) > money:
            bet = enterbox('Sorry, but that was not a valid entry\nHow much would you like to bet?\nYou have ${}'.format(money), 'Blackjack')

        bet = int(bet)

        #Cards are dealt the same way they would be in a physical game
        p_hand.append(decks.deal())
        d_hand.append(decks.deal())
        p_hand.append(decks.deal())
        d_hand.append(decks.deal())

        if d_hand[0].number == 'A':

            insurance_choice = buttonbox('Dealer has [{}, ?], and you have {}.\nWould you like to buy insurance (${})?'.format(d_hand[0], p_hand.str_list(), bet/2), 'Blackjack', ('Yes', 'No'))

            if insurance_choice == 'Yes':
                insurance = bet / 2

                if d_hand.blackjack():
                    msgbox('Dealer has a blackjack. You win insurance! (+${})'.format(insurance))
                    money += insurance

                else:
                    msgbox('Dealer does not have a blackjack. You lose insurance! (-${})'.format(insurance))
                    money -= insurance

        if p_hand.blackjack() and d_hand.blackjack():
            msgbox('You have {} and dealer has {}. Push!'.format(p_hand.str_list(), d_hand.str_list()), 'Blackjack')

        elif p_hand.blackjack():
            msgbox('Blackjack! You win ${}'.format(bet * 1.5), 'Blackjack')
            money += bet * 1.5

        while p_hand.value() < 21 and choice != 'Surrender' and choice != 'Stand' and choice != 'Split' and choice != 'Double Down' and p_hand.blackjack() == False:

            message = 'Dealer has [{}, ?].\nYou have {}, which has a value of {}.\nYour bet is ${}'.format(d_hand[0], p_hand.str_list(), p_hand.value(), bet)

            #If player has a pair and it's their first move and they can afford to double down or split
            if len(p_hand) == 2 and bet * 2 <= money and p_hand[0].value() == p_hand[1].value():
                choice = buttonbox(message, 'Blackjack', ('Hit', 'Stand', 'Surrender', 'Double Down', 'Split'))

            #If it's a player's first move and they can afford to double down
            elif len(p_hand) == 2 and bet * 2 <= money:
                choice = buttonbox(message, 'Blackjack', ('Hit', 'Stand', 'Surrender', 'Double Down'))

            #If it's a player's first move
            elif len(p_hand) == 2:
                choice = buttonbox(message, 'Blackjack', ('Hit', 'Stand', 'Surrender'))

            else:
                choice = buttonbox(message, 'Blackjack', ('Hit', 'Stand'))

            if choice == 'Hit' or choice == 'Double Down':

                if choice == 'Double Down':
                    bet *= 2

                p_hand.append(decks.deal())

                if p_hand.value() <= 21:
                    msgbox('{}! You now have {}, which has a value of {}.'.format(p_hand[-1], p_hand.str_list(), p_hand.value()))

                else:
                    msgbox('{}! You now have {}, which has a value of {}. Bust!\nYou lose! (-${})'.format(p_hand[-1], p_hand.str_list(), p_hand.value(), bet))
                    money -= bet

            elif choice == 'Split':

                first_hand = Hand([p_hand[0], decks.deal()])
                second_hand = Hand([p_hand[1], decks.deal()])

                handlist = [first_hand, second_hand]

                for pos in range(2):

                    hand = handlist[pos]

                    split_choice = ''

                    if handlist.index(hand) == 0:
                        name = 'first'

                    else:
                        name = 'second'

                    while split_choice != 'Stand' and hand.value() < 21:

                        if len(hand) == 2 and (bet * 3) <= money:
                            split_choice = buttonbox('Your {} hand is {}, which has a value of {}.\nYour bet is (${}).'.format(name, hand.str_list(), hand.value(), bet), 'Blackjack', ('Hit', 'Stand', 'Double Down'))

                        else:
                            split_choice = buttonbox('Your {} hand is {}, which has a value of {}.\nYour bet is (${}).'.format(name, hand.str_list(), hand.value(), bet), 'Blackjack', ('Hit', 'Stand'))

                        hand_bet = bet

                        #These are being added to the list for reference later if the hands do not bust and the player chooses to double down
                        handlist.append(hand_bet)

                        if split_choice == 'Hit' or split_choice == 'Double Down':

                            if split_choice == 'Double Down':
                                hand_bet *= 2

                            hand.append(decks.deal())

                            if hand.value() <= 21:
                                msgbox('{}! Your {} hand is {}, which has a value of {}.\nYour bet is (${})'.format(hand[-1], name, hand.str_list(), hand.value(), hand_bet), 'Blackjack')

                            else:
                                msgbox('{}! Your {} hand is {}, which has a value of {}.\nBust!(-${})'.format(hand[-1], name, hand.str_list(), hand.value(), hand_bet), 'Blackjack')
                                money -= hand_bet

            elif choice == 'Surrender':
                msgbox('You surrendered! You lose half your original bet (-${}) and you forfeit the hand!'.format(bet/2), 'Blackjack')
                money -= bet / 2

        if (choice != 'Split' and choice != 'Surrender' and p_hand.blackjack() == False and p_hand.value() <= 21) or (choice == 'Split' and (handlist[0].value() <= 21 or handlist[1].value() <= 21)):

            message = 'Dealer has {}\n'.format(d_hand.str_list())

            while d_hand.value() < 17:

                d_hand.append(decks.deal())
                message += '{}! Dealer now has {}, which has a value of {}\n'.format(d_hand[-1], d_hand.str_list(), d_hand.value())

            msgbox(message.rstrip(), 'Blackjack')

            if choice != 'Split':

                if d_hand.value() > 21:
                    msgbox('Dealer busts on {}, which has a value of {}. You win! (+${})'.format(d_hand.str_list(), d_hand.value(), bet), 'Blackjack')
                    money += bet

                elif d_hand.blackjack():
                    msgbox('Dealer has {}, a blackjack!\nYou have {}, which has a value of {}. You lose! (-{})'.format(d_hand.str_list(), p_hand.str_list(), p_hand.value(), bet))
                    money -= bet

                elif p_hand.value() > d_hand.value():
                    msgbox('Dealer stands on {}, which has a value of {}.\nYou have {}, which has a value of {}. You win! (+${})'.format(d_hand.str_list(), d_hand.value(), p_hand.str_list(), p_hand.value(), bet), 'Blackjack')
                    money += bet

                elif p_hand.value() == d_hand.value():
                    msgbox('Dealer stands on {}, which has a value of {}.\nYou have {}, which has a value of {}. Push!'.format(d_hand.str_list(), d_hand.value(), p_hand.str_list(), p_hand.value()), 'Blackjack')

                elif p_hand.value() < d_hand.value():
                    msgbox('Dealer stands on {}, which has a value of {}.\nYou have {}, which has a value of {}. You lose! (-${})'.format(d_hand.str_list(), d_hand.value(), p_hand.str_list(), p_hand.value(), bet), 'Blackjack')
                    money -= bet

            else:

                for pos in range(2):

                    hand = handlist[pos]

                    if handlist.index(hand) == 0:
                        name = 'first'

                    else:
                        name = 'second'

                    if hand.value() <= 21:

                        if d_hand.value() > 21:
                            msgbox('Dealer busts on {}, which has a value of {}.\nYour {} hand wins! (+${})'.format(d_hand.str_list(), d_hand.value(), name, handlist[pos + 2]), 'Blackjack')
                            money += handlist[pos + 2]

                        elif hand.value() > d_hand.value():
                            msgbox('Dealer stands on {}, which has a value of {}.\nYour {} hand is {}, which has a value of {}. You win! (+${})'.format(d_hand.str_list(), d_hand.value(), name, hand.str_list(), hand.value(), handlist[pos + 2]), 'Blackjack')
                            money += handlist[pos + 2]

                        elif hand.value() == d_hand.value():
                            msgbox('Dealer stands on {}, which has a value of {}.\nYour {} hand is {}, which has a value of {}. Push!'.format(d_hand.str_list(), d_hand.value(), name, hand.str_list(), hand.value()), 'Blackjack')

                        elif hand.value() < d_hand.value():
                            msgbox('Dealer stands on {}, which has a value of {}.\nYour {} hand is {}, which has a value of {}. You lost! (-${})'.format(d_hand.str_list(), d_hand.value(), name, hand.str_list(), hand.value(), handlist[pos + 2]), 'Blackjack')
                            money -= handlist[pos + 2]


        if len(decks) <= 10:
            msgbox('Shuffling...', 'Blackjack')
            decks.reset()
            decks.shuffle()

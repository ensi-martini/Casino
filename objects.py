import random

class Card(object):
    
    def __init__(self, number, suit):
        '''A class that models a playing card with a suit and a number'''
        self.number = number
        self.suit = suit
    
    def value(self):
        '''C.value() --> int
        Returns the integer value of the card'''
        if self.number in '2345678910':
            return int(self.number)
        
        elif self.number in 'JQK':
            return 10
    
        return 1
        
    def __eq__(self, other):
        '''C.__eq__(C2) <==> C == C2 --> bool
        Returns True if the two cards compared have the same number, False otherwise'''
        return self.number == other.number
        
    def __gt__(self, other):
        '''C.__gt__(C2) <==> C > C2 --> bool
        Returns True if the number value of C is greater than that of C2, False otherwise'''
        if self.number == 'A' and other.number != 'A':
            return True
        
        elif self.number in 'JQK' and other.number not in 'AJQK':
            return True
        
        elif self.number in 'JQK' and other.number in 'JQK' and 'JQK'.find(self.number) > 'JQK'.find(other.number):
                return True
        
        elif self.number in '2345678910' and other.number in '2345678910' and '2345678910'.find(self.number) > '2345678910'.find(other.number):
                return True
            
        return False
    
    def __lt__(self, other):
        '''C.__lt__(C2) <==> C < C2 --> bool
        Returns True if the number value of C is less than that of C2, False otherwise'''
        if self.number != 'A' and other.number == 'A':
            return True
        
        elif self.number not in 'AJQK' and other.number in 'JQK':
            return True
        
        elif self.number in 'JQK' and other.number in 'JQK' and 'JQK'.find(self.number) < 'JQK'.find(other.number):
                return True
            
        elif self.number in '2345678910' and other.number in '2345678910' and '2345678910'.find(self.number) < '23456788910'.find(other.number):
                return True
        
        return False
    
    def __str__(self):
        '''C.__str__() <==> str(C) --> str
        Returns a string representation of Card, in the form "(number)(suit)"'''
        return '{}{}'.format(self.number, self.suit)    
    
    
class Deck(list):
    
    def __init__(self, decks):
        '''A class that models a deck of cards, with a list of all the cards in said deck'''
        list.__init__(self)
        
        self.decks = decks
        
        for deck in range (decks):
            for suit in ['\u2660', '\u2663', '\u2665', '\u2666']:
                for number in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
                    self.append(Card(number, suit))
    
    def reset(self):
        '''D.reset() --> Deck
        Resets the deck to it's original condition, regardless of which cards are left'''
        self[:] = []
        
        for deck in range (self.decks):
            for suit in ['\u2660', '\u2663', '\u2665', '\u2666']:
                for number in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
                    self.append(Card(number, suit))  
                    
    def str_list(self):
        '''D.str_list() --> str
        Returns Deck in the form of a list of the string representations of all the cards in Deck'''
        str_list = self[:]
        
        for pos in range(len(self)):
            str_list[pos] = str(str_list[pos])

        return '{}'.format(str_list)
    
    def deal(self):
        '''D.deal() --> Card
        Returns one card from the deck, and removes it'''
        card = self[0]
        self.pop(0)
        
        return card
    
    def shuffle(self):
        '''D.shuffle() --> None
        Shuffles the deck'''
        random.shuffle(self)        
        
        '''FOSTER'S EARLY CHRISTMAS PRESENT'''
        
        #return_deck = self[:]
        
        #for card in range(len(self)):
            #pos = randint(0, len(return_deck) - 1)
            #self[card] = return_deck[pos]
            #return_deck.pop(pos)
            
        #self = return_deck
        
        
class Hand(list):
    
    def __init__(self, cards=[]):
        '''A class that models a hand of cards, with a list of said cards in the hand'''
        list.__init__(self)        
        
        for card in cards:
            self.append(card)

    def str_list(self):
        '''H.str_list() --> list
        Returns Hand in the form of a list of string representations of the cards in Hand'''
        str_list = self[:]
                
        for pos in range(len(self)):
            str_list[pos] = str(str_list[pos])
            
        return '{}'.format(str_list)        
    
    def blackjack(self):
        '''H.blackjack() --> bool
        Evaluates if a hand is a blackjack, and returns True if it is, False otherwise'''
        if len(self) == 2:
            if self[0].number == 'A' or self[1].number == 'A':
                if self.value() == 21:
                    return True
                
        return False
        
    def value(self):
        '''H.value() --> int
        Returns an integer that is the value of a blackjack hand'''
        counter = 0
        aces = 0    
        
        #Copy the hand and sort it so that all the aces are at the end
        copy_hand = self[:]
        copy_hand.sort()                                 
        
        for card in copy_hand:
            
            #This uses Card's value method, and evaluates an ace as 1
            counter += card.value()
                
            if card.number == 'A':
                aces += 1
        
        #If we can turn an ace from a 1 into an 11 without busting the hand, do it
        if 21 - counter >= 10 and aces > 0:
            counter += 10
            
        return counter
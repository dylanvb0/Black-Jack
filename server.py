import socket
import sys
import random
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('10.0.41.116', 10000)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)
# Listen for incoming connections
sock.listen(5)

while True:

    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            deck = []
            hand = []
            dealer_hand = []


            def rec_data(max_len):
                data_len = 0
                str = ""
                while data_len < max_len:
                    data = connection.recv(1).decode()
                    #print >> sys.stderr, 'received "%s"' % data
                    if data:
                        str += data
                        data_len += str.__len__()
                    else:
                        print('no more data from', client_address)
                        break
                return str

            def hit(is_player):
                if is_player:
                    deal_card = deck.pop(0)
                    hand.append(deal_card)
                else:
                    deal_card = deck.pop(0)
                    dealer_hand.append(deal_card)

            def total(hand):
                points = 0
                numOfAces = 0
                for card in hand:
                    if isinstance(card[0], int):
                        points += card[0]
                    elif(card[0] == "Ace"):
                        points += 11
                        numOfAces += 1
                    else:
                        points += 10
                for i in range(0, numOfAces):
                    if(points > 21):
                        points -= 10
                return points

            def find_winner():
                if(total(dealer_hand)) > 21:
                    connection.send(("Dealer Bust\nYou: %02d\nDealer: %02d\nYou Win!" % (total(hand), total(dealer_hand))).encode())
                elif total(hand) > 21:
                    connection.send(("You Bust\nYou: %02d\nDealer: %02d\nDealer Wins!" % (total(hand), total(dealer_hand))).encode())
                elif total(hand) > total(dealer_hand):
                    connection.send(("You: %02d\nDealer: %02d\nYou Win!" % (total(hand), total(dealer_hand))).encode())
                elif total(hand) < total(dealer_hand):
                    connection.send(("You: %02d\nDealer: %02d\nDealer Wins!" % (total(hand), total(dealer_hand))).encode())
                else:
                    connection.send(("You: %02d\nDealer: %02d\nTie!" % (total(hand), total(dealer_hand))).encode())
                connection.send("\nPlay again?".encode())
                response = rec_data(1)
                if response == 'y':
                    return True
                else:
                    return False


            def display_cards(is_player):
                if is_player:
                    hand_string = (', '.join([str(x) for x in hand]))
                    hand_string = "Your hand is" + hand_string + "\n"
                    connection.send(hand_string.encode())
                else:
                    dealer_string = (', '.join([str(x) for x in dealer_hand]))
                    dealer_string = ("Dealer hand is: " + dealer_string + "\n")
                    connection.send(dealer_string.encode())


            def deck_shuffle():
                for suit in ["Clubs", "Diamonds", "Hearts", "Spades"]:
                    for face in ["Jack", "Queen", "King", "Ace"]:
                        deck.append([face, suit])
                    for num in range(2, 11):
                        deck.append([num, suit])
                random.shuffle(deck)
                return deck


            def deal_cards():
                for x in range(0, 2):
                    deal_card = deck.pop(0)
                    hand.append(deal_card)
                    deal_card = deck.pop(0)
                    dealer_hand.append(deal_card)

            deck_shuffle()
            deal_cards()

            display_cards(True)
            display_cards(False)




            while 1:
                if total(hand) > 21:
                    if find_winner():
                        break
                    else:
                        connection.close()
                        sys.exit(0)

                elif total(hand) == 21:
                    while total(dealer_hand) < 17:
                        hit(False)
                    display_cards(False)
                    if find_winner():
                        break
                    else:
                        connection.close()
                        sys.exit(0)

                else:
                    connection.send("Hit or Stay?".encode())
                    response = rec_data(1)
                    if response == 'h':
                        hit(True)
                        display_cards(True)
                    else:
                        while total(dealer_hand) < 17:
                            hit(False)
                        display_cards(False)
                        if find_winner():
                            break
                        else:
                            connection.close()
                            sys.exit(0)




    finally:
        # Clean up the connection
        connection.close()
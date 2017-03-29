import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('10.0.41.116', 10000)
print ('connecting to %s port %s' % server_address)
sock.connect(server_address)
try:

    # Send data
    #message = input('Please type a message: ')
    #print >> sys.stderr, 'sending "%s"' % message
    #sock.sendall(message)

    # Look for the response
    amount_received = 0
    #amount_expected = len(message)

    while 1:
        data = sock.recv(1600).decode()
        amount_received += len(data)
        #str = data.decode('utf-8')
        if 'Hit or Stay?' in data:
            print('%s' % data)
            sock.sendall((input("(h/s)")).encode())
        elif 'Play again?' in data:
            print('%s' % data)
            response = input("(y/n)")
            if response == 'n':
                break
            sock.sendall(response.encode())
        else:
            print('%s' % data)
finally:
    print('closing socket')
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
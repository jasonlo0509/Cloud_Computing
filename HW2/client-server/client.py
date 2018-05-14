import os
import optparse

from twisted.internet import reactor, protocol, stdio, defer
from twisted.protocols import basic
from twisted.internet.protocol import ClientFactory

from common import COMMANDS, display_message, validate_file_md5_hash, get_file_md5_hash, read_bytes_from_file, clean_and_split_input

import time
import pyinotify
from multiprocessing import Process, Queue

class FileTransferProtocol(basic.LineReceiver):
    delimiter = '\n'

    def connectionMade(self):
        self.buffer = []
        self.file_handler = None
        self.file_data = ()
        
        print 'Connected to the server'
        
    def connectionLost(self, reason):
        self.file_handler = None
        self.file_data = ()
        
        print 'Connection to the server has been lost'
        reactor.stop()
    
    def lineReceived(self, line):
        print(line)
        if line == 'ENDMSG':
            print self.buffer
            if 'Welcome' in self.buffer:
                file_path = os.path.join(self.factory.files_path, self.factory.sendfile)
                self.transport.write('PUT %s %s\n' % (self.factory.sendfile, get_file_md5_hash(file_path)))
                self.setRawMode()
                
                for bytes in read_bytes_from_file(file_path):
                    self.transport.write(bytes)
                
                self.transport.write('\r\n')   
                
                # When the transfer is finished, we go back to the line mode 
                self.setLineMode()
                self.buffer = []
            elif 'File was successfully transfered and saved' in self.buffer:
                self.buffer = []
                if '.java' in self.factory.sendfile:
                    self.transport.write('GET %s\n' % (self.factory.sendfile.split('.')[0]+'.class'))
                else:
                    self.transport.write('GET %s\n' % (self.factory.sendfile.split('.')[0]))
            else:
                self.buffer = []
                if '.java' in self.factory.sendfile:
                    self.transport.write('GET %s\n' % (self.factory.sendfile.split('.')[0]+'.class'))
                else:
                    self.transport.write('GET %s\n' % (self.factory.sendfile.split('.')[0]))
        elif line.startswith('HASH'):
            # Received a file name and hash, server is sending us a file
            data = clean_and_split_input(line)

            filename = data[1]
            file_hash = data[2]
            
            self.file_data = (filename, file_hash)
            self.setRawMode()
        else:
            self.buffer.append(line)
        
    def rawDataReceived(self, data):
        filename = self.file_data[0]
        file_path = os.path.join(self.factory.files_path, filename)
        
        print 'Receiving file chunk (%d KB)' % (len(data))
        
        if not self.file_handler:
            self.file_handler = open(file_path, 'wb')
            
        if data.endswith('\r\n'):
            # Last chunk
            data = data[:-2]
            self.file_handler.write(data)
            self.setLineMode()
            
            self.file_handler.close()
            self.file_handler = None
            
            if validate_file_md5_hash(file_path, self.file_data[1]):
                print 'File %s has been successfully transfered and saved' % (filename)
            else:
                os.unlink(file_path)
                print 'File %s has been successfully transfered, but deleted due to invalid MD5 hash' % (filename)
        else:
            self.file_handler.write(data)


class FileTransferClientFactory(protocol.ClientFactory):
    protocol = FileTransferProtocol
    
    def __init__(self, files_path, sendfile):
        self.files_path = files_path
        self.sendfile = sendfile

# run reactor many times
def run_reactor(ip_address, port, path, file):
    def f(q):
        try:
            reactor.connectTCP(ip_address, port, FileTransferClientFactory(path, file))
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

# Monitor the code close event in folder
class FileSaveEventHandler(pyinotify.ProcessEvent):
	def process_IN_CLOSE_WRITE(self, event):
		if event.pathname.endswith('.c') or event.pathname.endswith('.cpp') or event.pathname.endswith('.java'):
			print "CLOSE_WRITE event:", event.pathname.split('/')[-1]
			print 'Client started, incoming files will be saved to %s' % (options.path)
			run_reactor(options.ip_address, options.port, options.path, event.pathname.split('/')[-1])

if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option('--ip', action = 'store', type = 'string', dest = 'ip_address', default = '127.0.0.1', help = 'server IP address')
	parser.add_option('-p', '--port', action = 'store', type = 'int', dest = 'port', default = 1234, help = 'server port')
	parser.add_option('--path', action = 'store', type = 'string', dest = 'path', help = 'directory where the incoming files are saved')
	parser.add_option('--file', action = 'store', type = 'string', dest = 'file', help = 'file to be sent')
    
	(options, args) = parser.parse_args()
	# watch manager
	wm = pyinotify.WatchManager()
	wm.add_watch(options.path, pyinotify.ALL_EVENTS, rec=False)

	# event handler
	eh = FileSaveEventHandler()

    # notifier
	notifier = pyinotify.Notifier(wm, eh)
	notifier.loop()

from pymodbus.client.sync import ModbusSerialClient
import time
import sys
totalport=8
monitor_port=[1,3,5]
modport='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AI04UGGP-if00-port0'
mymodbus=ModbusSerialClient(method='rtu',port=modport,baudrate=9600)
mymodbus.read_coils(0,count=totalport,unit=1)
mymodbus.socket.timeout=.1
print 'test can begin'
sys.stdout.flush()
class DI():
	status=[]
	counter=[]
	prestatus=[]
	for i in range (0,totalport):
		status.append(0)
		counter.append(0)
		prestatus.append(0)
	def read(self):
		self.status_all=mymodbus.read_coils(0,count=totalport,unit=1)
		for i in range(0,totalport):
			self.status[i]=self.status_all.bits[i]
	def write(self):
		for i in range(0,totalport):
			if self.status[i]==True:
				if self.status[i]!=self.prestatus[i]:
					self.counter[i]+=1
					counter_all=''
					for j in monitor_port:
						counter_all+='port'+str(j)+':'+str(self.counter[j])+' '
					print 'LED%d is on,Total: '%i + counter_all
					sys.stdout.flush()
		for i in range(0,totalport):
			self.prestatus[i]=self.status[i]

if __name__=='__main__':
	di=DI()

	while (1):
		di.read()
		di.write()

import os

def getConnections():

	connection = os.popen("cat /tmp/dhcp.leases").read()
	dhcpList = connection.split("\n")[:-1]

	connectionsList = []
	for item in dhcpList:
		connectionsList.append(item.split(" ")[1:4])
	return connectionsList

def getListMacsFromFirewall(string):
	firewall = os.popen("cat /etc/config/firewall").read()
	blocks = firewall.split("\n\n")[:-1]

	listFromBlock = []

	for i in range(0, len(blocks)):
		block = blocks[i].split("\n")
		for j in range(0, len(block)):
			if string in block[j]:
				listFromBlock = blocks[i].split("\n")
				break

	MACsList = []

	for i in range(0, len(listFromBlock)):
		tmp = listFromBlock[i].split(" ")
		if tmp[0].strip("\t") in "list" and tmp[1] in "src_mac":
			mac = tmp[2].strip("'")
			MACsList.append(mac)

	return(MACsList)

if __name__ == '__main__':
	getConnections()
	print(getListMacsFromFirewall("\toption name 'Gera'"))




import os

test = "./check_add_ssh_pub.sh"
answ = os.popen(test).read()

print(answ)

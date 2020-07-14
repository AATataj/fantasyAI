import  subprocess 
import os

getIP = """ 
        docker inspect mysql-server | grep '"IPAddress"' | head -n 1 
        """

os.system('sudo /home/slick/fantasy/fantasyAI/sqlStart.sh')
print(os.getegid())

# p = subprocess.Popen([getIP], shell=True, stdin=None, stdout=subprocess.PIPE, stderr=None, close_fds=True)
# ipAddr, err = p.communicate()
# ipAddr = str(ipAddr)
# ipAddr = ipAddr.replace('"IPAddress": "', "")
# ipAddr = ipAddr.replace("b'", "")
# ipAddr = ipAddr.replace('",\\n', "")
# ipAddr = ipAddr.replace("'", "")
# ipAddr = ipAddr.strip()

# print (ipAddr)

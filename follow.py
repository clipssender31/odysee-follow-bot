import httpx, time, pyfiglet, os; from itertools import cycle; from concurrent.futures import ThreadPoolExecutor

user = input("Username: ")
claim = input("Claim ID: ")

class bcolors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def GetProxy():
    with open('./proxies.txt', 'r') as temp_file:
        proxy = [line.rstrip('\n') for line in temp_file]
    return proxy

proxy = GetProxy()
proxy_pool = cycle(proxy)

def GetProxies():
    proxy = next(proxy_pool)
    if len(proxy.split(':')) == 4:
        splitted = proxy.split(':') 
        return f"http://{splitted[2]}:{splitted[3]}@{splitted[0]}:{splitted[1]}" # Converts ip:port:user:pass format to user:pass@ip:port
    return 'http://'+proxy
def follow():
  while True:
    try:
      client = httpx.Client(proxies=GetProxies())
      response = client.get('https://api.odysee.com/user/new')
      token = response.json()['data']['auth_token']
      res = client.get(f'https://api.odysee.com/subscription/new?auth_token={token}&channel_name=%40{user}&claim_id={claim}&notifications_disabled=true')
      if res.status_code==200:
        print(f"{bcolors.RED}[!]{bcolors.RESET} Followed {user}")
      else:
        print(f"{bcolors.RED}[!]{bcolors.RESET} Failed to follow {user}")
    except Exception as e:
      print(e)
if __name__ == "__main__":
    os.system("cls")
    print(pyfiglet.figlet_format(f"Clips Odysee Follow"))
    threadAmount=input(f'Thread Amount: ')
    os.system("cls")
    threadAmount = 1 if threadAmount == "" else int(threadAmount)
    threads = []
    with ThreadPoolExecutor(max_workers=threadAmount) as tello:
        for x in range(threadAmount):
            tello.submit(follow)

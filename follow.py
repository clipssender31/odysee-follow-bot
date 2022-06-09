import httpx, time, pyfiglet, os; from itertools import cycle; from concurrent.futures import ThreadPoolExecutor; from random_user_agent.user_agent import UserAgent; from random_user_agent.params import SoftwareName, OperatingSystem
claim = "5ff8f59cbf15a19c2b1d9cb8gf112741a0207f33" # change this if the script is not working

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

def GetProxies():
    with open("proxies.txt", "r") as temp_file:
        proxies = [line.rstrip("\n") for line in temp_file]
    return proxies
proxies = GetProxies()
proxy_pool = cycle(proxies)
def GetProxy():
    proxy = next(proxy_pool)
    if len(proxy.split(":")) == 4:
        splitted = proxy.split(":")
        return f"{splitted[2]}:{splitted[3]}@{splitted[0]}:{splitted[1]}"
    else:
        return proxy

def follow():
  while True:
    try:
      software_names = [SoftwareName.CHROME.value]
      operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
      user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
      user_agent = user_agent_rotator.get_random_user_agent()
      print(f"{bcolors.RED}[!]{bcolors.RESET} Using UserAgent: "+user_agent)
      client = httpx.Client(headers={"user-agent": f"{user_agent}"}, proxies="http://"+GetProxy())
      response = client.get('https://api.odysee.com/user/new', timeout=30)
      token = response.json()['data']['auth_token']
      print(f"{bcolors.RED}[!]{bcolors.RESET} Got Auth Token: "+token)
      res = client.get(f'https://api.odysee.com/subscription/new?auth_token={token}&channel_name=%40{username}&claim_id={claim}&notifications_disabled=true', timeout=30)
      print(f"{bcolors.RED}[!]{bcolors.RESET} Using This Auth Token to follow: "+token)
      if res.status_code==200:
        print(f"{bcolors.GREEN}[!]{bcolors.RESET} Followed {username} Successfully: {token}")
      else:
        print(f"{bcolors.RED}[!]{bcolors.RESET} Failed to follow {username}")
    except Exception as e:
      print(e)
if __name__ == "__main__":
    os.system("cls")
    print(pyfiglet.figlet_format(f"Clips Odysee Follow Bot"))
    threadAmount=input(f'{bcolors.RED}Thread Amount: {bcolors.RESET}')
    username = input(f"{bcolors.RED}Username To Follow: {bcolors.RESET}")
    os.system("cls")
    threadAmount = 1 if threadAmount == "" else int(threadAmount)
    threads = []
    with ThreadPoolExecutor(max_workers=threadAmount) as tello:
        for x in range(threadAmount):
            tello.submit(follow)

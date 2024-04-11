import requests

def checkServiceForWord(url, keyword):
    try:
        x = requests.get(url)
        print(x.text)
        serverStatus=1
        if keyword in x.text:
            print("found keyword")
            return True
    except:
        print("error")
        return False


url = 'http://localhost:5000/getTitles'
result = checkServiceForWord(url, 'title')
print(result)


url = 'http://localhost:5000/getProducts'
result = checkServiceForWord(url, 'xxx')
print(result)
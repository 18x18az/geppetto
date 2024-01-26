from getUuid import get_uuid
from connect import get_server
def display(): 
    server, serverPort, browserPort = get_server()
    ident = get_uuid()
    urlToOpen = 'http://' + server + ':' + str(browserPort) + '/display/field/' + ident
    subprocess.call(['chromium-browser', urlToOpen,
                  '--window-size=1920,1080',
                  '--window-position=0,0',
                  '--start-fullscreen',
                  '--kiosk',
                  '--incognito',
                  '--noerrdialogs',
                  '--disable-translate',
                  '--no-first-run',
                  '--fast',
                  '--fast-start',
                  '--no-sandbox',
                  '--disable-infobars',
                  '--disable-features=TranslateUI',
                  '--disk-cache-dir=/dev/null',
                  '--overscroll-history-navigation=0',
                  '--disable-pinch']

display()
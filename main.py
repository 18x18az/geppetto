from getUuid import get_uuid
from connect import get_server
from register import register
import subprocess

server, serverPort, browserPort = get_server()

ident = get_uuid()

## Run command chromium-browser http://{server}:{browserPort}/display/field/{ident}
urlToOpen = 'http://' + server + ':' + str(browserPort) + '/display/field/' + ident
## Start x server
# ##   --window-size=1920,1080 \
#   --window-position=0,0 \
#   --start-fullscreen \
#   --kiosk \
#   --incognito \
#   --noerrdialogs \
#   --disable-translate \
#   --no-first-run \
#   --fast \
#   --fast-start \
#   --disable-infobars \
#   --disable-features=TranslateUI \
#   --disk-cache-dir=/dev/null \
#   --overscroll-history-navigation=0 \
#   --disable-pinch
subprocess.Popen(['chromium-browser', urlToOpen,
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
                  '--disable-infobars',
                  '--disable-features=TranslateUI',
                  '--disk-cache-dir=/dev/null',
                  '--overscroll-history-navigation=0',
                  '--disable-pinch']
                  )

register(server, serverPort, ident)

print(server)
print(ident)

while True:
    pass

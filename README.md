# CRX-Sandbox
A python utility for running chrome extensions with a proxy using selenium.

### Usage

```
usage: crx_sandbox.py [-h] [-p PROXY] [-f FILE] [-i ID] [-s SLEEP] [-d]

Run a browser extension in google chrome with a proxy

optional arguments:
  -h, --help            show this help message and exit
  -p PROXY, --proxy PROXY
                        Proxy for browser network traffic (default of 127.0.0.1:8080)
  -f FILE, --file FILE  Chrome extension archive or folder to run
  -i ID, --id ID        Chrome extension webstore id to download and run (instead of a file)
  -s SLEEP, --sleep SLEEP
                        Seconds to sleep before quitting chrome (default of 600)
  -d, --detach          Run the chrome extension until manually quiting (insetad of sleeping)
  ```

#### Requirements
- Selenium
- Chrome Webdriver (https://sites.google.com/a/chromium.org/chromedriver/home)

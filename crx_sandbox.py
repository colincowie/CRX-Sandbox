# Colin Cowie, 2022.
import os, time, argparse, requests, zipfile
from selenium import webdriver

class CRX_Sandbox():
    def __init__(self,args):
        self.args = args

    def download_ext(self, id):
        # Download extension webstore url
        download_url = "https://clients2.google.com/service/update2/crx?response=redirect&os=win&arch=x86-64&os_arch=x86-64&nacl_arch=x86-64&prod=chromecrx&prodchannel=unknown&prodversion=81.0.4044.138&acceptformat=crx2,crx3&x=id%3D" + str(id) + "%26uc"
        print("[*] Downloading extension with id: "+str(id))
        r = requests.get(download_url, allow_redirects=True)

        # Save output of download
        if r.status_code == 200 :
            # Save ext to .crx file
            crx_name = id+'.crx'
            open(crx_name, 'wb').write(r.content)
            print("[*] Unzipping Extension")
            try:
                with zipfile.ZipFile(crx_name, 'r') as zip_ref:
                    zip_ref.extractall(crx_name[:-4])
                os.remove(crx_name)
            except Exception as e:
                print("[-] Unzip Error")
                print(e)
                print(download_url)
                pass
            return True
        elif r.status_code == 204:
            print("[-] HTTP 204: No Content.")
            return False
        else:
            print("[-] Error! Status Code: "+str(r.status_code))
            return False

    def run(self):
        # Create the webdriver with proxy and extension
        try:
            options = webdriver.ChromeOptions()
        except Exception as e:
            print("[-] Failed to initalize the chome web driver")
            print(e)
            raise

        options.add_argument('--proxy-server='+self.args.proxy)
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--ignore-certificate-errors')

        if self.args.file is not None:
            if os.path.isdir(self.args.file):
                try:
                    options.add_argument('load-extension=' + self.args.file)
                except Exception as e:
                    print("[-] Failed to load the chrome extension: " + self.args.file)
                    raise
            else:
                try:
                    options.add_extension(self.args.file)
                except Exception as e:
                    print("[-] Failed to load the chrome extension: " + self.args.file)
                    raise
        elif self.args.id is not None:
            # Download
            print("[*] Attempting to download the chrome extension")
            ext_download = self.download_ext(self.args.id)
            # Load chrome extension
            options.add_argument('load-extension=' + self.args.id)
        if self.args.detach:
            options.add_experimental_option("detach", True)

        # options.add_argument('--no-sandbox')
        print("[*] Creating chrome driver")
        #driver = webdriver.Chrome(executable_path="/bin/chromedriver",options=options)

        try:
            driver = webdriver.Chrome(options=options)
        except Exception as e:
            print("\033[0;31m[-] Failed to start the chome web driver\033[0m")
            print(e)
            raise
        driver.get("chrome://extensions/")

        try:
            driver.get("chrome://newtab")
            print("[*] Navigated to chrome://newtab")
        except:
            failed = True
            print("[-] Erorr: unable to open chrome://newtab")

        driver.get("chrome://extensions/")
        print("[*] Navigated to chrome://extensions/")
        time.sleep(self.args.sleep)

        try:
            driver.close()
            driver.quit()
        except:
            print("[?] Error: browser is already closed")

def parse_args():
    parser = argparse.ArgumentParser(description="Run a browser extension in google chrome with a proxy")
    parser.add_argument('-p', '--proxy', help="Proxy for browser network traffic (default of 127.0.0.1:8080)", default="127.0.0.1:8080")
    parser.add_argument('-f', '--file', help="Chrome extension archive or folder to run")
    parser.add_argument('-i','--id', help="Chrome extension webstore id to download and run (instead of a file)")
    parser.add_argument('-s','--sleep', type=int, help="Seconds to sleep before quitting chrome (default of 600)", default=600)
    parser.add_argument('-d','--detach', action='store_true', help="Run the chrome extension until manually quiting (insetad of sleeping)", default=False)

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    # Create instance of the sandbox class and run with an extension id
    sandbox = CRX_Sandbox(args)
    sandbox.run()

# -*- coding: utf-8 -*-
"""
A proxy server acts as an intermediary for requests between a client and a server.
In simple, the traffic flows through the proxy server on its way to the address you requested and back.

A proxy server for automation scripts with Selenium could be helpful for:
   - Capture network traffic
   - Mock backend calls made by the website
   - Access the required website under complex network topologies or strict corporate restrictions/policies.

If you are in a corporate environment, and a browser fails to connect to a URL, this is most likely because the
environment needs a proxy to be accessed.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.proxy import Proxy, ProxyType
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


# Creating local driver proxy
def proxy_object():
    """
    Configure proxy using Selenium Proxy object attached to ChromeOptions.
    """
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = 'http://proxy:80'
    proxy.ssl_proxy = 'http://proxy:80'
    options = webdriver.ChromeOptions()
    options.proxy = proxy
    options.accept_insecure_certs = True

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    # do something
    driver.quit()


# Creating local driver proxy
def proxy_capability():
    """
    Configure proxy by setting the W3C proxy capability on ChromeOptions.
    """
    proxy = 'http://proxy:80'

    options = webdriver.ChromeOptions()
    options.set_capability('proxy', {
        'httpProxy': proxy,
        'ftpProxy': proxy,
        'sslProxy': proxy,
        'proxyType': 'manual',
    })

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    # do something
    driver.quit()


# Creating local driver proxy
def firefox_proxy_object():
    """
    Configure proxy for Firefox using Selenium Proxy object and FirefoxOptions.
    """
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = 'http://proxy:80'
    proxy.ssl_proxy = 'http://proxy:80'

    options = webdriver.FirefoxOptions()
    options.proxy = proxy
    options.accept_insecure_certs = True

    service = FirefoxService(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    # do something
    driver.quit()


# Creating local driver proxy
def edge_proxy_object():
    """
    Configure proxy for Edge using Selenium Proxy object and EdgeOptions.
    """
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = 'http://proxy:80'
    proxy.ssl_proxy = 'http://proxy:80'

    options = webdriver.EdgeOptions()
    options.proxy = proxy
    options.accept_insecure_certs = True

    service = EdgeService(executable_path=EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    # do something
    driver.quit()

if __name__ == '__main__':
    proxy_object()


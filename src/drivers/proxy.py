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
from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType


# Creating local driver proxy
def proxy_object():
    """
    Configuring proxy with Selenium's Proxy object.
    """
    capabilities = {
        'browserName': 'chrome',
        'acceptSslCerts': True
    }

    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = 'http://proxy:80'
    proxy.ssl_proxy = 'http://proxy:80'
    proxy.add_to_capabilities(capabilities)

    driver = webdriver.Chrome(desired_capabilities=capabilities)
    # do something
    driver.quit()


# Creating local driver proxy
def proxy_capability():
    """
    Configuring the driver proxy via browser capabilities.
    """
    proxy = "http://proxy:80"
    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": proxy,
        "ftpProxy": proxy,
        "sslProxy": proxy,
        "proxyType": "MANUAL",
    }

    driver = webdriver.Chrome()
    # do something
    driver.quit()


# TODO: add proxy configuration example for firefox and edge.

if __name__ == '__main__':
    proxy_object()

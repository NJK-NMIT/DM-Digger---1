# This is not the same as the supplied jsn_drop_service.
# For one thing, it has the commented out lines of code removed.

import requests 
import json 



class jsnDrop(object):

    def __init__(self) -> None:
        self.tok = "a7828c33-3ba1-4774-ad80-d7e2030dc3ea"
        self.url = "https://newsimland.com/~todd/JSON"
        # A 250ms RTT to newsimland means it takes ages to even setup a TCP 3 way handshake.
        # api.twitter.com, api.google.com, etc, are all sub 50ms !
        self.jsnStatus = ""
        self.jsnResult = {}



        # Setting up data structures for storing JsnDrop Commands
        self.decode = json.JSONDecoder().decode
        self.encode = json.JSONEncoder().encode

        self.jsnDropRecord = self.decode('{"tok":"","cmd":{}}')
        self.jsnDropCreate = self.decode('{"CREATE":"aTableName","EXAMPLE":{}}')
        self.jsnDropStore  = self.decode('{"STORE":"aTableName","VALUE":[]}')
        self.jsnDropAll    = self.decode('{"ALL":"aTableName"}')
        self.jsnDropSelect = self.decode('{"SELECT":"aTableName","WHERE":"aField = b"}')
        self.jsnDropDelete = self.decode('{"DELETE":"aTableName","WHERE":"aField = b"}')
        self.jsnDropDrop   = self.decode('{"DROP":"aTableName"}')

    def jsnDropApi(self,command):
        api_call  = self.jsnDropRecord
        api_call["tok"] = self.tok
        api_call["cmd"] = command
        payload = {'tok': self.encode(api_call)}


        # Request to the API
        # We would like to use "post" here since "get" has the following problems
        #   * Encodes stuff in URLs, which has the effect of:
        #      | A URL can/should be no longer than 2000 characters so not much data can be sent at once
        #      | Plaintext URL data may get appended to log files.  This is a security issue.
        #   * Accoring to HTTP documentation, "get" should only be used to retrieve data, _never_ change it.
        #      | Refer: https://datatracker.ietf.org/doc/html/rfc2616#page-51
        # BUT POST DOESN'T WORK!
        r = requests.get(self.url, payload)

        # Update the status and result
        jsnResponse = r.json()
        self.jsnStatus = jsnResponse["JsnMsg"]
        self.jsnResult = jsnResponse["Msg"]

        return self.jsnResult 

    
    def create(self,table_name, example):
        command = self.jsnDropCreate
        command["CREATE"] = table_name
        command["EXAMPLE"] = example
        return self.jsnDropApi(command)
        
    def store(self, table_name, value_list):
        command = self.jsnDropStore
        command["STORE"] = table_name
        command["VALUE"] = value_list
        return self.jsnDropApi(command)

    def all(self, table_name):
        command = self.jsnDropAll
        command["ALL"] = table_name
        return self.jsnDropApi(command)

    def select(self, table_name, where):
        command = self.jsnDropSelect
        command["SELECT"] = table_name
        command["WHERE"] = where
        return self.jsnDropApi(command)

    def delete(self,table_name, where):
        command = self.jsnDropDelete
        command["DELETE"] = table_name
        command["WHERE"] = where
        return self.jsnDropApi(command)

    def drop(self,table_name):
        command = self.jsnDropDrop
        command["DROP"] = table_name
        return self.jsnDropApi(command)



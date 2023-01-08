#!/usr/bin/python3
import requests
import argparse
import warnings
import json,sys
from pprint import pprint
from urllib import parse

class GraphQLDetector:
    """
    This class detects if GraphQL introspection is enabled on a given list of URLs.
    """
    def __init__(self, urlist):
        """
        Initializes the GraphQLDetector with a list of URLs to check.

        Parameters:
        - urlist (str): A file containing a list of URLs, one per line.
        """
        self.urlist = urlist
        self.paths = [
            "/graphql",
            "/v1/api/graphql",
            "/v1/graphql",
            "/v2/graphql",
            "/v4/api/graphql",
            "/api/graphql"
        ]
        self.query = """
        {__schema{queryType{name}mutationType{name}subscriptionType{name}types{...FullType}directives{name description locations args{...InputValue}}}}fragment FullType on __Type{kind name description fields(includeDeprecated:true){name description args{...InputValue}type{...TypeRef}isDeprecated deprecationReason}inputFields{...InputValue}interfaces{...TypeRef}enumValues(includeDeprecated:true){name description isDeprecated deprecationReason}possibleTypes{...TypeRef}}fragment InputValue on __InputValue{name description type{...TypeRef}defaultValue}fragment TypeRef on __Type{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name}}}}}}}}
        """

    def check_introspection(self):
        """
        Checks if GraphQL introspection is enabled on a multiple URL.

        Parameters:
        - url (str): The URL list to check.

        Returns:
        - str: A string indicating if introspection is enabled or not.
        """
        file = open("%s" %(self.urlist))
        content = file.read()
        lines = content.splitlines()

        for url in lines:
            for path in self.paths:
                endpoint = parse.urljoin(url, path)
                try:
                    warnings.simplefilter("ignore")
                    response = requests.post(endpoint, json={'query': self.query}, verify=False)
                except Exception:
                    pass
                else:
                    if response.status_code == 200:
                        try:
                            json_data = json.loads(response.text)
                            if json_data.get('data'):
                                return f'[+] Graphql Introspection Enabled On: {endpoint}'
                            else:
                                return f'[!] Graphql Introspection Not Enabled On: {endpoint}'
                        except ValueError:
                            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--urlist', help='list of target urls')
    args = parser.parse_args()
    if args.urlist:
        graphqldetector = GraphQLDetector(args.urlist)
        pprint(graphqldetector.check_introspection())

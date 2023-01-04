#!/usr/bin/python
import requests
import json
import argparse
from colorama import Fore
from core.ascii import cli
class DependencyConfusionChecker:
    def __init__(self,package_name):
        self.package_name = package_name
        self.pypi_url = "https://pypi.org/pypi/{}/json"
        self.npm_url = "https://registry.npmjs.org/{}"
        self.rubygems_url = "https://rubygems.org/api/v1/gems/{}.json"
        self.go_url = "https://proxy.golang.org/{}/@v/list"

    def check_pypi(self):
        """
        Check for potential dependency confusion vulnerabilities in a PyPI package.
        Parameters:
            - package_name: the name of the PyPI package to check
            
        Returns:
            - True if there is a potential dependency confusion vulnerability in the package,
              False otherwise.
        """
        try:
            package_url = self.pypi_url.format(self.package_name)
            response = requests.get(package_url)
            package_info = response.json()

            if "requires_dist" not in package_info["info"]:
                return False

            dependencies = package_info["info"]["requires_dist"]
            for dependency in dependencies:
                name = dependency.split(";")[0]
                if name.lower() == self.package_name.lower():
                    return True

            return False
        except Exception as e:
            print(f'An error occurred while checking PyPI package: {e}')
            return False

    def check_npm(self):
        """
        Check for potential dependency confusion vulnerabilities in an npm package.
        Parameters:
            - package_name: the name of the npm package to check
            
        Returns:
            - True if there is a potential dependency confusion vulnerability in the package,
              False otherwise.
        """
        try:
            package_url = self.npm_url.format(self.package_name)
            response = requests.get(package_url)
            package_info = response.json()

            if "dependencies" not in package_info:
                return False

            dependencies = package_info["dependencies"]
            for name in dependencies:
                if name.lower() == self.package_name.lower():
                    return True

            return False
        except Exception as e:
            print(f'An error occurred while checking Npm package: {e}')
            return False

    def check_rubygems(self):
        """
        Check for potential dependency confusion vulnerabilities in a RubyGems package.
        Parameters:
            - package_name: the name of the RubyGems package to check
            
        Returns:
            - True if there is a potential dependency confusion vulnerability in the package,
              False otherwise.
        """
        try:
            package_url = self.rubygems_url.format(self.package_name)
            response = requests.get(package_url)
            package_info = response.json()

            if "dependencies" not in package_info:
                return False

            dependencies = package_info["dependencies"]["development"]
            for dependency in dependencies:
                name = dependency["name"]
                if name.lower() == self.package_name.lower():
                    return True

            return False
        except Exception as e:
            print(f'An error occurred while checking Ruby package: {e}')
            return False           
        
    def check_go(self):
        """
        Check for potential dependency confusion vulnerabilities in a Go module.
        Parameters:
            - package_name: the name of the Go module to check
            
        Returns:
            - True if there is a potential dependency confusion vulnerability in the package,
              False otherwise.
        """
        try:     
            package_url = self.go_url.format(self.package_name)
            response = requests.get(package_url)
            version_list = response.text

            versions = version_list.split("\n")
            for version in versions:
                if version.lower() == self.package_name.lower():
                    return True

            return False
        except Exception as e:
            print(f'An error occurred while checking Golang package: {e}')
            return False

if __name__ == "__main__":
    print(cli())
    argparse = argparse.ArgumentParser()
    argparse.add_argument("-p", "--package_name", help="package name to check for dependency confusion")
    args = argparse.parse_args()
    if args.package_name:
        checker = DependencyConfusionChecker(args.package_name)
        if checker.check_pypi():
            print(f"Potential dependency confusion vulnerability found in PyPI package {checker}")
        else:
            print(f"No dependency confusion vulnerabilities found in PyPI package {checker}")

        if checker.check_npm():
            print(f"Potential dependency confusion vulnerability found in npm package {checker}")
        else:
            print(f"No dependency confusion vulnerabilities found in npm package {checker}")

        if checker.check_rubygems():
            print(f"Potential dependency confusion vulnerability found in Ruby package {checker}")
        else:
            print(f"No dependency confusion vulnerabilities found in Ruby package {checker}")

        if checker.check_go():
            print(f"Potential dependency confusion vulnerability found in go package {checker}")
        else:
            print(f"No dependency confusion vulnerabilities found in go package {checker}")            

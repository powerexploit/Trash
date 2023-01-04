package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"net/http"
	"strings"
	"os"
)

type DependencyConfusionChecker struct {
	packageName string
	pypiURL     string
}

func NewDependencyConfusionChecker(packageName string) *DependencyConfusionChecker {
	return &DependencyConfusionChecker{
		packageName: packageName,
		pypiURL: "https://pypi.org/pypi/{}/json",
	}
}

func (c *DependencyConfusionChecker) CheckPypi() bool {
	packageURL := fmt.Sprintf(c.pypiURL, c.packageName)
	response, err := http.Get(packageURL)
	if err != nil {
		fmt.Printf("An error occurred while checking PyPI package: %s\n", err)
		return false
	}
	defer response.Body.Close()

	var packageInfo map[string]interface{}
	if err := json.NewDecoder(response.Body).Decode(&packageInfo); err != nil {
		fmt.Printf("An error occurred while checking PyPI package: %s\n", err)
		return false
	}

	info, ok := packageInfo["info"].(map[string]interface{})
	if !ok {
		return false
	}

	requiresDist, ok := info["requires_dist"]
	if !ok {
		return false
	}

	// Assert that requiresDist is a slice of strings and assign it to a variable of the correct type
	dependencies, ok := requiresDist.([]string)
	if !ok {
		return false
	}

	for _, dependency := range dependencies {
		name := strings.Split(dependency, ";")[0]
		if strings.EqualFold(name, c.packageName) {
			return true
		}
	}

	return false
}

func main() {
	// Define a command line flag for the package name
	packageName := flag.String("package", "", "The name of the package to check for dependency confusion")
	flag.Parse()

	// Check that a package name was provided
	if *packageName == "" {
		fmt.Println("Please provide a package name to check for dependency confusion")
		os.Exit(1)
	}

	checker := NewDependencyConfusionChecker(*packageName)
	if checker.CheckPypi() {
		fmt.Printf("Potential dependency confusion vulnerability found in PyPI package %s\n", *packageName)
	} else {
		fmt.Printf("No dependency confusion vulnerabilities found in PyPI package %s\n", *packageName)
	}
}


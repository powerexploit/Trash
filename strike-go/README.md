<h1 align="center">Strike</h1>

## Note

Strike is an Automated tool written in golang for shodan public api to detect hostnames, open ports, and CVEs.


## Install

```
git clone https://github.com/powerexploit/Trash
cd Trash/strike-go
go install strike
```

## Usage

```
$ echo "8.8.8.8" | ./strike -json
```

```
usage: ./strike -h

options:
  -c int
        Set the concurrency level (default 20)
  -json
        Show Output as Json format
  -open
        Show Output as format 'IP:Port' only

``` 

<h1 align="center">
  <br>
  <img src="https://i.ibb.co/Z1BFTzQ/Screenshot-2022-11-21-at-10-39-06-PM.png">
  <br>
</h1>

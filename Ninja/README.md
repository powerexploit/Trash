<h1 align="center">Strike</h1>
<p align="center">
    <img src="https://img.shields.io/badge/python-v3-blue" alt="python badge">
</p>
## Note

Ninja is a cli tool to enumerate Aws Secrets with the help of AWS PoolId.

## Install

```
git clone https://github.com/powerexploit/Trash
cd Trash/Ninja
python3 -m pip install requirements.txt
```

## Usage

```
$ python3 Ninja.py --p <aws_pool_id> --r <aws_region_name>
```

```
usage: Ninja.py [-h] [--p P] [--r R]

options:                                                                                                                            
  -h, --help         show this help message exit
  --p P, --pool P    aws pool id to fetch the secrets
  --r R, --Region R  aws region name to fetch the secrets

``` 

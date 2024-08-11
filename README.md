
# Secret

^ _ ^ This is only for education purposes ^ _ ^

Basically a brute force script in generating a 16 length string that contains letters + numbers and check whether the link that has the generated string is accessible or nah. 


## Run Locally

Clone the project

```bash
  git clone https://github.com/laefy13/secret1
```

Go to the project directory

```bash
  cd secret1
```

* Docker
**Note:** Replace the /d/secret1 with your actual directory. Make sure you have a openvpn file or just remove the openvpn+sleep line together in the entrypoint.sh. And make sure that you have the arg for the --id or --url in /app/main.py.
```bash
  docker build -t vid .
  docker run -it --cap-add=NET_ADMIN --device /dev/net/tun -v /d/secret1:/app vid
```

* No docker

Install dependencies

```bash
  pip install -r requirements.txt
or 
  pip install requests
```

**Note:** --db argument is needed here, unless you actually want to generate the db in /app/file.db. Make sure that you provide the --id or --url
```bash
  python main.py --id 1 --db ./tested.db 
```




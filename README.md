# [Summer of Algorithms](https://pyjaipur-soa.herokuapp.com/)
 
## What is it?

PyJaipur "Summer of Algorithms" is a 2 month long program which is usually conducted in the month of July-August.
The aim is to have a place where all our community memebers can learn something new in these 2 months.

## How do I contribute?

There are multiple ways you can contibute to this website.

- Report bugs please!.
- Add missing documentation.
- Add/improve design and asthetics of website.
- Request/Ask/Submit new features using github's [issues](https://github.com/PyJaipur/Summer-of-Algorithm/issues).

## Local setup

1. Git clone this repo
2. Make sure you have docker running on your machine.
3. Make sure you have python poetry running on your machine.
4. Edit `soa/.dev.env` with correct credentials.

```bash
cd soa
poetry install # Install dependencies
poetry shell   # Activate virtualenv
make services  # Start postgres + redis
make web       # Start webserver
make stop      # stop services
```

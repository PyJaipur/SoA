# [Summer of Algorithms](https://soa.pyjaipur.org)
 
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
2. Install postgresql or make sure you have docker running on your machine.
3. Run postgres database. I use docker and so the command there is `docker run --rm -e "POSTGRES_PASSWORD=password" -p 5432:5432 -it postgres`.
4. Run server using `DATABASE_URL='postgres://postgres:password@localhost:5432' python -m soa`

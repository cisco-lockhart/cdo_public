# To run

We have only tested this against Mac OS X running homebrew. If you're using anything else, you're 
on your own.

## The easy way

*This is a quick hacky script. Your mileage may vary.*

Run `./setup.sh`, and then run `./cdo.py` as instructed to in the last step in the following section.

## The hard way

### Python
- Install Python 3: `brew install python3` (execute `brew upgrade python` if you have Python 2 installed using brew already)
- Install virtualenv: `pip3 install virtualenv`
- Create a virtualenv called venv: `virtualenv -p python3 venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `./cdo.py [arguments]` --- to figure out what you can execute, execute `./cdo.py -h`

### Node

Requires Node version 6.11.1


### Running the report generator
`cd node/report_generator`
Run `npm install`
`node report_generator.js /tmp/jsons/my/dir`

Note: The report generator is run by the Python script anyway.
 

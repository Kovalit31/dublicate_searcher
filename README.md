# Dublicate searcher

## About
Search dublicates in setted directory

## How works
Enter directory
       |
       V
Caching files on it
       |
       V
Read cache and getting dublicates
       |
       V
Write dublicates paths on STDOUT

### Enter directory
This step will be anytime, when you start a programm

### Caching files
The caching provides utils/cacher.py.
It create uuid for any object and write it as <two first letters of uuid>/<other letters>
Then write filename, hash and bytes uuid to one file, but bytes to other

### Read cache
See utils/cacher.py @ find_file_in_cache()

### Write dublicates paths on STDOUT

This feature is only for time, this will be overriding on remove, link or archive dublicates

## Using
`cd /path/to/repo && python3 -m dublicate_searcher "<path/to/dir/to/check>"`

## Requirments
Installed python >= 3.4

## Logs

Providing by plugins/collections.py, what implemented on my repository "python-addons" with name "text-formatter.py"
They're can be found on plugins/collections.py_data/*.log

## Note
Checking lots of file will be long time. Please get lots of coffee :)

Enjoy!

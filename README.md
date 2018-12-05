# sanename

Renames all files within a given directory to what I consider _sane_:

- No whitespace
- All lowercase
- Only a-z and 0-9

## Usage

    sanename.py path/to/directory
    
## Details

Has a list of some common latin letters that are accented or otherwise 
different from a-z, for example `á`, `ö`, `ñ` and similar. If those are 
found, they will be replaced with their a-z "lookalikes". 

Additionally, there is a list of allowed characters that will be kept. 
Currently, those are `-`, `_` and `.` - the dot being important because 
it is usually used as a file separator.

## License

sanename is free software, dedicated to the public domain. Do with it 
whatever you want, but don't hold me responsible for anything either. 

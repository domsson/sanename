# sanename

Renames all files within a given directory to what I consider _sane_:

- No whitespace
- All lowercase
- Only `a-z`, `0-9`, `-`, `_` and `.`

## Usage

    sanename.py path/to/directory
    
## Details

Has a list of some common latin letters that are accented or otherwise 
different from a-z, for example `á`, `ö`, `ñ` and similar. If those are 
found, they will be replaced with their a-z "lookalikes". 

Currently not recursive, meaning it does not rename files that are in 
subdirectories of the given directory.

## License

sanename is free software, dedicated to the public domain. Do with it 
whatever you want, but don't hold me responsible for anything either. 

# Association for Computing Machinery (ACM) PDF Maker
#### Quickly create a .pdf sign-in sheet for ACM-related events. 


Command Line Arguments
---
    help: -h, -help

    input file: [ -i, --input ] < path/to/chapter_member_listing.csv >  [ REQUIRED ]

    event name: [ -e, --event ] < string: event name >                  [ OPTIONAL ]

    event date: [ -d, --date ] < string: event date >                   [ OPTIONAL ]

    title font size: [ -tf, --title-font ] < integer >                  [ OPTIONAL ]

    cell font size: [ -cf, --cell-font ] < integer >                    [ OPTIONAL ]

    non member pages: [ -nm, --non-member ] < integer >                 [ OPTIONAL ]

    output path: [ -o, --output ] < path/to/output/folder >             [ OPTIONAL ]

    
Example Usage
---
* Sign-in sheet for a Data Science Series event on August 20, 2018. 
```console
foo@bar: $ python pdf.py -i ~/data/acm/chapter_member_listing.csv -e "Data Science Series" -d "August 20, 2018"
```

* Sign-in sheet with 5 additional non member pages and title font size of 15 px.
```console
foo@bar: $ python pdf.py -i ~/data/acm/chapter_member_listing.csv -e "Data Science Series" -d "August 20, 2018" -nm 5 -tf 15 
```

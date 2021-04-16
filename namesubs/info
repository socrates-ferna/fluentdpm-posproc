File: coreutils.info,  Node: cut invocation,  Next: paste invocation,  Up: Operating on fields

8.1 ‘cut’: Print selected parts of lines
========================================

‘cut’ writes to standard output selected parts of each line of each
input file, or standard input if no files are given or for a file name
of ‘-’.  Synopsis:

     cut OPTION... [FILE]...

   In the table which follows, the BYTE-LIST, CHARACTER-LIST, and
FIELD-LIST are one or more numbers or ranges (two numbers separated by a
dash) separated by commas.  Bytes, characters, and fields are numbered
starting at 1.  Incomplete ranges may be given: ‘-M’ means ‘1-M’; ‘N-’
means ‘N’ through end of line or last field.  The list elements can be
repeated, can overlap, and can be specified in any order; but the
selected input is written in the same order that it is read, and is
written exactly once.

   The program accepts the following options.  Also see *note Common
options::.

‘-b BYTE-LIST’
‘--bytes=BYTE-LIST’
     Select for printing only the bytes in positions listed in
     BYTE-LIST.  Tabs and backspaces are treated like any other
     character; they take up 1 byte.  If an output delimiter is
     specified, (see the description of ‘--output-delimiter’), then
     output that string between ranges of selected bytes.

‘-c CHARACTER-LIST’
‘--characters=CHARACTER-LIST’
     Select for printing only the characters in positions listed in
     CHARACTER-LIST.  The same as ‘-b’ for now, but internationalization
     will change that.  Tabs and backspaces are treated like any other
     character; they take up 1 character.  If an output delimiter is
     specified, (see the description of ‘--output-delimiter’), then
     output that string between ranges of selected bytes.

‘-f FIELD-LIST’
‘--fields=FIELD-LIST’
     Select for printing only the fields listed in FIELD-LIST.  Fields
     are separated by a TAB character by default.  Also print any line
     that contains no delimiter character, unless the ‘--only-delimited’
     (‘-s’) option is specified.

     Note ‘awk’ supports more sophisticated field processing, like
     reordering fields, and handling fields aligned with blank
     characters.  By default ‘awk’ uses (and discards) runs of blank
     characters to separate fields, and ignores leading and trailing
     blanks.
          awk '{print $2}'      # print the second field
          awk '{print $(NF-1)}' # print the penultimate field
          awk '{print $2,$1}'   # reorder the first two fields
     Note while ‘cut’ accepts field specifications in arbitrary order,
     output is always in the order encountered in the file.

     In the unlikely event that ‘awk’ is unavailable, one can use the
     ‘join’ command, to process blank characters as ‘awk’ does above.
          join -a1 -o 1.2     - /dev/null # print the second field
          join -a1 -o 1.2,1.1 - /dev/null # reorder the first two fields

‘-d INPUT_DELIM_BYTE’
‘--delimiter=INPUT_DELIM_BYTE’
     With ‘-f’, use the first byte of INPUT_DELIM_BYTE as the input
     fields separator (default is TAB).

‘-n’
     Do not split multi-byte characters (no-op for now).

‘-s’
‘--only-delimited’
     For ‘-f’, do not print lines that do not contain the field
     separator character.  Normally, any line without a field separator
     is printed verbatim.

‘--output-delimiter=OUTPUT_DELIM_STRING’
     With ‘-f’, output fields are separated by OUTPUT_DELIM_STRING.  The
     default with ‘-f’ is to use the input delimiter.  When using ‘-b’
     or ‘-c’ to select ranges of byte or character offsets (as opposed
     to ranges of fields), output OUTPUT_DELIM_STRING between
     non-overlapping ranges of selected bytes.

‘--complement’
     This option is a GNU extension.  Select for printing the complement
     of the bytes, characters or fields selected with the ‘-b’, ‘-c’ or
     ‘-f’ options.  In other words, do _not_ print the bytes, characters
     or fields specified via those options.  This option is useful when
     you have many fields and want to print all but a few of them.

‘-z’
‘--zero-terminated’
     Delimit items with a zero byte rather than a newline (ASCII LF).
     I.e., treat input as items separated by ASCII NUL and terminate
     output items with ASCII NUL. This option can be useful in
     conjunction with ‘perl -0’ or ‘find -print0’ and ‘xargs -0’ which
     do the same in order to reliably handle arbitrary file names (even
     those containing blanks or other special characters).

   An exit status of zero indicates success, and a nonzero value
indicates failure.


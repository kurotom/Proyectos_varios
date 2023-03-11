# reset_metadata_pdf

Script que permite cambiar la metadata de un fichero PDF.


# Requisitos

[Ghostscript - download](https://ghostscript.com/releases/gsdnld.html)


# Uso

```bash
./reset_metadata_pdf.sh -f pdf_original.pdf [ t | a | s | k | c | p ]
```


Obligatorio: `-f filename.pdf`

Opciones:
```
    \-t title
    \-a author
    \-s subject
    \-k keywords
    \-c creator
    \-p producer
```


* [Fuente](https://askubuntu.com/questions/27381/how-to-edit-pdf-metadata-from-command-line)

# py-great-resume

## usage

`py-great-resume` may be used within Python as a package:

```python
>>> import py_great_resume
>>> resume = py_great_resume.Resume("/path/to/resume.json", template="long")
>>> resume.validate()
>>> resume.to_pdf("/path/to/resume.pdf")
>>> resume.to_html("/path/to/resume.html")
```

It may also be used directly from the command line:

```bash
$ python -m py_great_resume --src_fpath /path/to/resume.json --tgt_fpath /path/to/resume.pdf --template long --validate
$ python -m py_great_resume --src_fpath /path/to/resume.json --tgt_fpath /path/to/resume.html --template long --validate
```

## whence "py-great-resume"?

When debugging and developing, I often use "my-great-[FOO]" when naming test files. In this case, I used "my-great-resume.json", then mixed in "py" for the Python code loading it in.

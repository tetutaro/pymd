#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re


begin_pattern = '^[`~]{3,}\s*\{\s*[pP]ython(?:(?:\s*,|\s+)(.*)|)\}\s*$'
end_pattern = '^[`~]{3,}\s*$'
python_code_begin = re.compile(begin_pattern)
python_code_end = re.compile(end_pattern)

python_begins = [
	{
		'pattern': '``',
		'expected': False,
		'expected_options': '',
	},
	{
		'pattern': '``{}',
		'expected': False,
		'expected_options': '',
	},
	{
		'pattern': '```{}',
		'expected': False,
		'expected_options': '',
	},
	{
		'pattern': '```{r}',
		'expected': False,
		'expected_options': '',
	},
	{
		'pattern': '```{pythonname,label="hoge",.class}',
		'expected': False,
		'expected_options': '',
	},
	{
		'pattern': ' ```{python name,label="hoge",.class}',
		'expected': False,
		'expected_options': '',
	},
	{
		'pattern': '	```{python name,label="hoge",.class}',
		'expected': False,
		'expected_options': '',
	},
	{
		'pattern': '```{python}',
		'expected': True,
		'expected_options': '',
	},
	{
		'pattern': '```{Python}',
		'expected': True,
		'expected_options': '',
	},
	{
		'pattern': '~~~{python}',
		'expected': True,
		'expected_options': '',
	},
	{
		'pattern': '~~~{Python}',
		'expected': True,
		'expected_options': '',
	},
	{
		'pattern': '`````{python}',
		'expected': True,
		'expected_options': '',
	},
	{
		'pattern': '`````{Python}',
		'expected': True,
		'expected_options': '',
	},
	{
		'pattern': '~~~~~{python}',
		'expected': True,
		'expected_options': '',
	},
	{
		'pattern': '~~~~~{Python}',
		'expected': True,
		'expected_options': '',
	},
	{
		'pattern': '`````  {  python   }   ',
		'expected': True,
		'expected_options': '',
	},
	{
		'pattern': '`````  {  Python   }   ',
		'expected': True,
		'expected_options': '',
	},
	{
		'pattern': '~~~~~  {  python   }   ',
		'expected': True,
		'expected_options': '',
	},
	{
		'pattern': '~~~~~  {  Python   }   ',
		'expected': True,
		'expected_options': '',
	},
	{
		'pattern': '```{python name,label="hoge",.class}',
		'expected': True,
		'expected_options': 'name,label="hoge",.class',
	},
	{
		'pattern': '```{python,name,label="hoge",.class}',
		'expected': True,
		'expected_options': 'name,label="hoge",.class',
	},
	{
		'pattern': '```{python, name,label="hoge",.class}',
		'expected': True,
		'expected_options': 'name,label="hoge",.class',
	},
	{
		'pattern': '```{Python name,label="hoge",.class}',
		'expected': True,
		'expected_options': 'name,label="hoge",.class',
	},
	{
		'pattern': '```{Python,name,label="hoge",.class}',
		'expected': True,
		'expected_options': 'name,label="hoge",.class',
	},
	{
		'pattern': '```{Python, name,label="hoge",.class}',
		'expected': True,
		'expected_options': 'name,label="hoge",.class',
	},
	{
		'pattern': '~~~{python name,label="hoge",.class}',
		'expected': True,
		'expected_options': 'name,label="hoge",.class',
	},
	{
		'pattern': '~~~{python,name,label="hoge",.class}',
		'expected': True,
		'expected_options': 'name,label="hoge",.class',
	},
	{
		'pattern': '~~~{python, name,label="hoge",.class}',
		'expected': True,
		'expected_options': 'name,label="hoge",.class',
	},
	{
		'pattern': '~~~{Python name,label="hoge",.class}',
		'expected': True,
		'expected_options': 'name,label="hoge",.class',
	},
	{
		'pattern': '~~~{Python,name,label="hoge",.class}',
		'expected': True,
		'expected_options': 'name,label="hoge",.class',
	},
	{
		'pattern': '~~~{Python, name,label="hoge",.class}',
		'expected': True,
		'expected_options': 'name,label="hoge",.class',
	},
	{
		'pattern': '`````  {  python   name  ,  label  =  "hoge"  ,   .class  }  ',
		'expected': True,
		'expected_options': 'name  ,  label  =  "hoge"  ,   .class',
	},
	{
		'pattern': '`````  {  python  ,   name  ,  label  =  "hoge"  ,   .class  }  ',
		'expected': True,
		'expected_options': 'name  ,  label  =  "hoge"  ,   .class',
	},
	{
		'pattern': '`````  {  Python   name  ,  label  =  "hoge"  ,   .class  }  ',
		'expected': True,
		'expected_options': 'name  ,  label  =  "hoge"  ,   .class',
	},
	{
		'pattern': '`````  {  Python  ,   name  ,  label  =  "hoge"  ,   .class  }  ',
		'expected': True,
		'expected_options': 'name  ,  label  =  "hoge"  ,   .class',
	},
	{
		'pattern': '~~~~~  {  python   name  ,  label  =  "hoge"  ,   .class  }  ',
		'expected': True,
		'expected_options': 'name  ,  label  =  "hoge"  ,   .class',
	},
	{
		'pattern': '~~~~~  {  python  ,   name  ,  label  =  "hoge"  ,   .class  }  ',
		'expected': True,
		'expected_options': 'name  ,  label  =  "hoge"  ,   .class',
	},
	{
		'pattern': '~~~~~  {  Python   name  ,  label  =  "hoge"  ,   .class  }  ',
		'expected': True,
		'expected_options': 'name  ,  label  =  "hoge"  ,   .class',
	},
	{
		'pattern': '~~~~~  {  Python  ,   name  ,  label  =  "hoge"  ,   .class  }  ',
		'expected': True,
		'expected_options': 'name  ,  label  =  "hoge"  ,   .class',
	},
]

python_ends = [
	{
		'pattern': ' ```',
		'expected': False,
	},
	{
		'pattern': '	```',
		'expected': False,
	},
	{
		'pattern': '```',
		'expected': True,
	},
	{
		'pattern': '~~~',
		'expected': True,
	},
	{
		'pattern': '`````  ',
		'expected': True,
	},
	{
		'pattern': '~~~~~  ',
		'expected': True,
	},
]

error_count = 0

for test_pattern in python_begins:
	pattern = test_pattern['pattern']
	expected = test_pattern['expected']
	expected_options = test_pattern['expected_options']
	is_match = python_code_begin.match(pattern) is not None
	if is_match is expected:
		options = python_code_begin.findall(pattern)
		if len(options) == 0:
			options = ''
		else:
			options = options[0].strip()
		if options != expected_options:
			print("!!! DON'T MATCH OPTION !!!")
			print(pattern)
			print("result: |%s|" % options)
			print("expected: |%s|" % expected_options)
			error_count += 1
	else:
		print("!!!DON'T MATCH!!!")
		print(pattern)
		print("result: ", is_match)
		print("expected: ", expected)
		error_count += 1

for test_pattern in python_ends:
	pattern = test_pattern['pattern']
	expected = test_pattern['expected']
	is_match = python_code_end.match(pattern) is not None
	if is_match is not expected:
		print("!!!DON'T MATCH!!!")
		print(pattern)
		error_count += 1

if error_count == 0:
	print("PASSED")

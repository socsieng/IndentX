# IndentX [![Build Status](https://travis-ci.org/socsieng/IndentX.svg)](https://travis-ci.org/socsieng/IndentX)

IndentX is a forgiving indentation plugin for Sublime Text inspired by [Indent Xml](https://sublime.wbond.net/packages/Indent%20XML), aimed primarily at preserving attribute ordering and working with *invalid* content.

Supported content types:

* XML*-like* content
* JSON-*like* content

## Usage: keyboard short-cuts

### Indenting

The *Indent* command will format both XML and JSON like content (content guess based on the first character `<` for XML) and can be accessed using the following keyboard short-cuts (think angle brackets: `control`/`command` + `<`):

* Windows: `control` + `shift` + `,`
* Mac: `command` + `shift` + `,`
* Linux: `control` + `shift` + `,`

### JSON formatting

The *Indent & format JSON* will try and indent and convert JavaScript-like objects to JSON (e.g. wrapping attributes in `"` and converting `'` strings to `"`). It can be accessed using the following keyboard short-cuts (think curly braces: `control`/`command` + `{`):

* Windows: `control` + `shift` + `[`
* Mac: `command` + `shift` + `[`
* Linux: `control` + `shift` + `[`

*JSON before and after formatting:*

![Before JSON formatting](docs/images/json_before.png)
![After JSON formatting](docs/images/json_after.png)

Note: If starting with a JavaScript object and you want to maintain the JavaScipt object format, use the [Indent](#Indenting) command instead.

## How it works

IndentX uses regular expressions (probably more than it should) to identify tokens to:

* insert new lines
* increase indentation (begin tag/object)
* decrease indentation (end tag/object)

This technique has the following benefits:

* doesn't require valid strict XML or JSON (close enough should be good enough)
* preserves attribute order

## Installation

Install using Package Control.

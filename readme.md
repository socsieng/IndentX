# IndentX

IndentX a forgiving indentation plugin for Sublime Text inspired by [Indent Xml](https://sublime.wbond.net/packages/Indent%20XML), aimed primarily at preserving attribute ordering and working with *invalid* content.

Supported content types:

* XML*-like* content
* JSON-*like* content

## Usage: keyboard short-cuts

### Indenting

The *Indent* command will format both XML and JSON like content (content guess based on the first character `<` for XML) and can be accessed using the following keyboard short-cuts:

* Windows: `control` + `shift` + `,` (think `control` + `<`)
* Mac: `command` + `shift` + `,` (think `command` + `<`)
* Linux: `control` + `shift` + `,` (think `control` + `<`)

### JSON formatting

The *Indent & format JSON* will try and indent convert JavaScript looking objects to JSON (e.g. wrapping attributes in `"`) and can be accessed using the following keyboard short-cuts:

* Windows: `control` + `shift` + `[` (think `control` + `{`)
* Mac: `command` + `shift` + `[` (think `command` + `{`)
* Linux: `control` + `shift` + `[` (think `control` + `{`)

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

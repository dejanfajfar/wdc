![LOGO](https://raw.githubusercontent.com/dejanfajfar/wdc/master/doc/logo/cover.png)

# About

## Inspiration

Every company uses its own time tracking program. Sometimes as an freelancer I have to fill out multiple at once.
If you are lucky those time tracking tools are actually useful and do not require exceeded effort to operate.

Sadly from my experience this is not always the case...

Another _inspiration_ was to answer the question: How long do I have to work today?

## Goals

**WDC** has the following goals in no particular order:

- Easy to use (if possible)
- Calculate the end time of the current work day
- Log basic work information
  - Start time
  - End time
  - A descriptive message
- Provide an easy way of grouping the logged work information
- Export the logged items

# Installation

Using ```pip```

```bash
$ pip install wdc
```

# Quick start

After installation you are able to use the **wdc** from the shell of your choice.

To log your first task simply:

```bash
$ wdc start 0900 -m 'My first task'
```

When you want to start another task simply start it, no need to end the current one.

```bash
$ wdc start 1030 -m 'Off to the next task'
```

You can also apply tags to the tasks beeing logged

```bash
$ wdc start 1030 -m 'Off to the next task' -t tag01 -t tag02
```

# Further reading

More information can be found at [the wdc wiki](https://github.com/dejanfajfar/wdc/wiki)

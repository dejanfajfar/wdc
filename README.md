![Logo](doc/logo/cover.png)

![CI](https://github.com/dejanfajfar/wdc/workflows/CI/badge.svg)
[![PyPI version](https://badge.fury.io/py/wdc.svg)](https://badge.fury.io/py/wdc)

# WDC

***Log work effortlessly***

## About

### Inspiration

Every company uses its own time tracking program. Sometimes as an freelancer I have to fill out multiple at once.
If you are lucky those time tracking tools are actually useful and do not require exceeded effort to operate.

Sadly from my experience this is not always the case...

Another _inspiration_ was to answer the question: How long do I have to work today?

### Goals

**WDC** has the following goals in no particular order:

- Easy to use (if possible)
- Calculate the end time of the current work day
- Log basic work information
  - Start time
  - End time
  - A descriptive message
- Provide an easy way of grouping the logged work information
- Export the logged items

### Description

Because this is **my** tool, I have opted for a CLI tool that can be used on all systems.
In order to achieve this **WDC** is written in python, which is readily available on all platforms.

TBD

## Changelog

The changelog can be found [here](CHANGELOG.md)

## Installation

### From source code

Clone the repository:

```bash
git clone https://github.com/dejanfajfar/wdc.git .
```

If you have [make](https://www.gnu.org/software/make/) available then simply execute the **install** target

```bash
make install
```

If make is not available on your system then you can run the underlying python command. For that you have to navigate to the directory containing the ```setup.py``` file. In that directory execute

```bash
python setup.py install
```

### Using PIP

> It is assumed that you have python and PIP installed

**WDC** is published as openly accessible package on [pypi.org/project/wdc/](https://pypi.org/project/wdc/).

Because of this it can be easilly installed using _pip_

```bash
$ pip install wdc
```

## Formatting time

In order to make **wdc** faster usable from the CLI we opted to represent time and dates is a optimized format.

Details can be read at [Date and Time format wiki page](https://github.com/dejanfajfar/wdc/wiki/time-and-date)

**Samples**

25th of October 2020 ==> 2020-10-25

11:30am ==> 1130

4:30pm ==> 1630

...

## Commands

**WDC** supports the following command:

- ```wdc calc``` - Calculate the end time of the working day.

  [Documentation](https://github.com/dejanfajfar/wdc/wiki/com-calc#calc-command) | [Samples](https://github.com/dejanfajfar/wdc/wiki/com-calc#examples)
- ```wdc start``` - Start a new work task

  [Documentation](https://github.com/dejanfajfar/wdc/wiki/com-start#start-command) | [Samples](https://github.com/dejanfajfar/wdc/wiki/com-start#examples)
- ```wdc end``` - Adds an end time to the last task of the day

  [Documentation](https://github.com/dejanfajfar/wdc/wiki/com-end#end-command) | [Samples](https://github.com/dejanfajfar/wdc/wiki/com-end#examples)
- ```wdc list``` - List logged tasks

  [Documentation](https://github.com/dejanfajfar/wdc/wiki/com-list#list-command) | [Samples](https://github.com/dejanfajfar/wdc/wiki/com-list#examples)
- ```wdc amend``` - Edit existing tasks

  [Documentation](https://github.com/dejanfajfar/wdc/wiki/com-amend#amend-command) | [Samples](https://github.com/dejanfajfar/wdc/wiki/com-amend#examples)
- ```wdc info``` - View information about logged tasks

  [Documentation](https://github.com/dejanfajfar/wdc/wiki/com-info#info-command) | [Samples](https://github.com/dejanfajfar/wdc/wiki/com-info#examples)
- ```wdc export``` - Export tasks information

  [Documentation](https://github.com/dejanfajfar/wdc/wiki/com-export#export-command) | [Samples](https://github.com/dejanfajfar/wdc/wiki/com-export#examples)

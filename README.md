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

Because this is **my** tools I have opted for a CLI tool that can be used on all systems.
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

  [Documentation]()

## calc

The calc command is used to calculate the theoretical end of the current working day.

**sample**

```bash
$ wdc calc 0800
1615
```

### Arguments

The time at which the work day started in the **hhmm** format

### Options

#### -b, --break_duration

The duration of the lunch break in minutes.

Default value is **30** minutes.

If no break was consumed can be provided as 0.

##### Examples

Working day with 30 minute break

```bash
$ wdc 0800 -b 30
```

Working day with no break

```bash
$ wdc 0800 -b 0
```

#### -d, --workday_duration

The duration of the workday in **hhmm** format

Default value is **0745**.

### Examples

An 8 hour workday starting at 8:00

```bash
$ wdc 0800 -d 0800
```

## start

Used to start a new work day task and store it.

> In order to start a new task you do not have to call an end command. Just start the new task and the old one will be automatically closed

**sample**

```bash
$ wdc start 0800 -t Customer -t Project -m The task description
```

### Arguments

The time at which the task started in the **hhmm** format

### Options

#### -t, --tag

Provide a generic tag to associate with the task.

Multiple tags can be provided, if so then each has to be provided with its own ```-t``` or ```--tag``` option.

#### -m, --message

Provide a descriptive message to associate with the task

#### -e, --end

Provide an optional end time for the task in **hhmm** format

#### -d, --date

Provide the date to which this task should be associated to.

### Examples

Start an anonymous task

```bash
$ wdc start 0800
```

Start a task with a know end time

```bash
$ wdc start 0800 -e 0900
```

Start a task for a date other than today

```bash
wdc start 0800 -d 2020-01-01
```

## end

Adds a end time to the last work task of the given day

> If no date is provided the today is takes as a default

**sample**

```bash
$ wdc end
```

### Arguments

No arguments supported by the command

### Options

#### -d, --date

Provide the optional date on which the last task should be closed

#### -e, --end

Provide an optional end time for the task in **hhmm** format

> If not provided then the current time is taken

### Examples

End current working day with by providing an end time

```bash
$ wdc end -e 1630
```

End last task from another day

```bash
$ wdc end -d 2020-10-25
```

## list

List all stored work tasks for the day

**sample**

```bash
$ wdc list
```

### Arguments

No arguments supported by the command

### Options

#### -d, --date

Provide optional date for which tasks should be listed

#### -a, --all

Flag to denote if all tasks should be shown, or not

> If set then the change history of each task will be returned

### Examples

List all tasks for today, even the internally duplicated ones

```bash
$ wdc list -a
```

List tasks for a given day

```bash
$ wdc list -d 2020-10-25
```

## info

Provides detailed information about the given task

***sample***

```bash
$ wdc info 0c3a9014
```

### Arguments

The **id** of the task already recorded

> The task ID can be retrieved with the list command

### Options

The command does not support any options at this point

### Examples

The only use case is shown in the sample.

## amend

Enables you to change an existing workday task

> The original task is not changes only a new revision added

***sample***

```bash
$ wdc amend 0c3a9014 -t my_tag
```

### Arguments

The **id** of the task to be altered

> The task ID can be retrieved with the list command

### Options

#### -s / --start

The new value of the task start time

#### -t /--tag

The new tags to be associated with the task

Multiple tags can be provided, if so then each has to be provided with its own ```-t``` or ```--tag``` option.

> Note that the new tags will override the old one, They will **NOT** be appended to the existing ones

#### -m / --message

The new message for the work task

#### -e / --end

The new value of the task end time

#### -d /--date

The new date for the work task

### Examples

Apply multiple tags to the existing task

```bash
$ wdc amend 0c3a9014 -t tag1 -t tag2
```

Update the start time, end time and the message of the task

```bash
$ wdc amend 0c3a9014 -s 0900 -e 1030 -m "Updated message"
```

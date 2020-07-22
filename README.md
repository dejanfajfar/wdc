# WDC

***Work day calculator***

![CI](https://github.com/dejanfajfar/wdc/workflows/CI/badge.svg)

![Logo](doc/logo/cover.png)

# Purpose

The purpose of **wdc** is to provide a simple _CLI_ application for time tracking.

Born out of a nuisance that I could never tell when the working day was actually over and amazed overtime with little compensation.

# Description

Trying to come up with something better than: "timetracking in the CLI"

# Changelog

The changelog can be found [here](CHANGELOG.md)

# Installation

## From source code

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

# Time format

**wdc** uses a simplified time format similar to the military (_hhmm_). This uses a 24 hour format, so not AM/PM.

The table below should provide some additional information and clarification on how this time format maps to the more standard 24 and 12 hour format

| hhmm | 24 Hour | 12 hour |
|---|---|---|
|0000|00:00|12:00 AM
|0100|01:00|01:00 AM
|0200|02:00|02:00 AM
|0300|03:00|03:00 AM
|0400|04:00|04:00 AM
|0500|05:00|05:00 AM
|0600|06:00|06:00 AM
|0700|07:00|07:00 AM
|0800|08:00|08:00 AM
|0900|09:00|09:00 AM
|1000|10:00|10:00 AM
|1100|11:00|11:00 AM
|1200|12:00|12:00 PM
|1300|13:00|01:00 PM
|1400|14:00|02:00 PM
|1500|15:00|03:00 PM
|1600|16:00|04:00 PM
|1700|17:00|05:00 PM
|1800|18:00|06:00 PM
|1900|19:00|07:00 PM
|2000|20:00|08:00 PM
|2100|21:00|09:00 PM
|2200|22:00|10:00 PM
|2300|23:00|11:00 PM

The minutes work as _expected_.

# Commands

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

# WDC

***Work day calculator***

![CI](https://github.com/dejanfajfar/wdc/workflows/CI/badge.svg)

# Purpose

The purpose of **wdc** is to provide a simple _CLI_ application for time tracking.

Born out of a nuisance that I could never tell when the working day was actually over and amazed overtime with little compensation.

# Description

TBD

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

##### Examples

An 8 hour workday starting at 8:00

```bash
$ wdc 0800 -d 0800
```
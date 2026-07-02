# SQL Injection Notes

## Overview
SQL Injection occurs when an application fails to handle user input safely in database queries.

## Core Concepts
- User-controlled data is directly embedded into a query
- Weak input validation and insufficient escaping enable exploitation
- Common techniques include UNION-based, boolean-based, and error-based injection

## Key Notes
- Simple bypasses such as `or 1=1` can be useful in the early stages of testing.
- Different responses may reveal information about the database structure or contents.
- Identifying the database type is essential for choosing the right payloads.

# JavaScript Coding Standards

Source: <https://synacor.atlassian.net/wiki/pages/viewpage.action?pageId=3502964753>

Page ID: 3502964753

Parent ID: 3502866481

---

## Introduction

This document is intended to be a living document detailing JavaScript Style Guide. Whether you are writing a back-end Node server, or working on front end code, this document should serve as a best practice reference on how to write maintainable and readable JavaScript code.

> **Info**
> 
> 

This document is not complete by definition and currently only contains guidelines based on frequent and repeating reviews comments on the recent PRs. This document aims to help developers to avoid attracting the same review comments and thus improve the quality of the PRs.

## Getting Started

### JavaScript, & Node/Browser Support

Zimbra Modern UI have support for the following:

-   **JavaScript**: ECMAScript 2015
    
-   **Browser**: Chrome, Firefox, Safari, MS Edge
    
-   **Node**: v18
    

## Tooling

-   **IDE**: [Visual Studio Code](<https://code.visualstudio.com/>)
    
-   **Linter**: Eslint
    
-   **Formatter**: Prettier
    
-   **Tests**: TestCafe for Web and Mobile, Playwright for Desktop
    
-   **Package Manager**: NPM
    

Most of these tools are setup to run automatically, please refer to the "package.json" file to reference script commands.

## Code Style

The following Code Style is not "complete" by definition.  It does not cover all bases of the JavaScript language, and allows room for developers to employ various acceptable techniques. This Style Guide focuses on key development areas to equip developers with the knowledge to deliver readable, maintainable, and scalable code.

### Naming Conventions

-   Use intention-revealing names.
    

```js
// bad
let d; // elapsed time in days  
let s; // elapsed time in seconds

// good
let elapsedTimeInDays;  
let daysSinceCreation; 
let daysSinceModification;  
let fileAgeInDays;


// bad
let cust;
let emp;

// good
let customer;
let employee;‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍


// bad
const getData = () => {};
const setData = () => {};

// good
const getSingleProductData = () => {};
const setProductName = () => {};


// bad
if(user && token) {}

// good
const isAuthenticated = user && token;
if(isAuthenticated) {}


// bad
if(forecast.getDate() !== new Date().getDate()) {}

// good
const now = new Date();
const shouldGetNewForecast = forecast.getDate() !== now.getDate();
if(shouldGetNewForecast){}‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍


// bad
const handleError = (e) => {
   console.error(e);
   location.assign("/error-page");
}

// good
const handleErrorAndRedirectTo = (e, route = DEFAULT_ERROR_PAGE) => {
   console.error(e);
   location.assign(route);
}
```

### Constants

-   Prefer usage of meaningful constants over inline strings / numbers.
    

```js
// Bad
throw TypeError("my error message that i also need for test assertions");

expect(e).toEqual("my error message that i also need for test assertions");


// Good
const ERROR_INCORRECT_VALUE = "My Error Message";

throw TypeError(ERROR_INCORRECT_VALUE);

expect(e).toEqual(ERROR_INCORRECT_VALUE);


// Bad
if(password.length > 6) {}


// Good
const MIN_PASSWORD_LENGTH = 6;

if(password.length > MIN_PASSWORD_LENGTH) {}‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍


// Bad
if(color === "#FFFFFF") {}

// Good
const WHITE = "#FFFFFF";
if(color === WHITE) {}
‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍
```

-   Prefer grouping related constants using objects over isolated constants.
    

```js
// Bad
const REPLY_ACTION = 'r';
const FORWARD_ACTION = 'f';

// Good
const MAIL_ACTIONS = {
    REPLY: 'r',
    FORWARD: 'f'
};
```

### Booleans

-   Prefix variables with "is", "has", or "should" to denote boolean values.
    

```js
// Bad
const active = true;
const error = true;

// Good
const isActive = true;
const hasError = true;
```

### Destructuring

-   Use object destructuring when using multiple properties of an object.
    

```js
// bad
function getFullName(user) {
  const firstName = user.firstName;
  const lastName = user.lastName;

  return `${firstName} ${lastName}`;
}

// good
function getFullName(user) {
  const { firstName, lastName } = user;
  return `${firstName} ${lastName}`;
}

// best
function getFullName({ firstName, lastName }) {
  return `${firstName} ${lastName}`;
}‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍
```

### Strings

-   Prefer template strings instead of concatenation.
    

```js
const name = "Jane";

// bad
const personalHello = "Hello" + firstName;

// good
const personalHello = `Hello ${firstName}`;‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍
```

### Functions

-   Prefer functions no longer than 4 arguments long.
    

```js
// bad
const myFunction = (foo, bar, baz, boz, fizz, buzz) => {
   //.. 
}

// good
const opts = {
  boz,
  fizz,
  buzz
};

const myFunction = (foo, bar, baz, opts) => {
  //..
}‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍
```

-   Use default parameter syntax over mutating an argument.
    

```js
// bad
const logWithColor = (msg: string, color: string) => {
  if (!color) {
    color = "#fff";
  }
  //
};

// good
const logWithColor = (msg: string, color = "#FFFFFF") => {
  //
};‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍
```

### Composition & Higher Order Functions

-   Avoid anonymous functions for composed functions.
    

```js
// Bad
const withFunctionLogger = (name, targetFn) => {
  return (...args) => {
    const value = targetFn(...args);
    console.log({ name, args, value });

    return value;
  };
};

// Good
const withFunctionLogger = (name, targetFn) => {
  return function functionLogger(...args) {
    const value = targetFn(...args);
    console.log({ name, args, value });

    return value;
  };
};

// or

const withFunctionLogger = (name, targetFn) => {
  const functionLogger = (...args) => {
    const value = targetFn(...args);
    console.log({ name, args, value });

    return value;
  };

  return functionLogger;
};
‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍
```

### Flow Control and Conditionals

-   Avoid unnecessary else statements.
    
-   Return as early as possible.
    

```js
// bad
const getTodaysForecast = async () => {
  let content;

  const res = await fetch(/**/).then(res => res.toJson());

  if (res.ok) {
    content = res.body;
  } else {
    content = "Error getting forecast";
  }

  return content;
};

// good
const getTodaysForecast = async () => {
  const res = await fetch(/**/).then(res => res.toJson());
  if (!res.ok) {
    return "Error getting forecast";
  }

  return res.body;
};
‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍
```

### Iteration

-   Prefer using functional prototype over "for-in" "for-of".
    
-   Avoid long iteration method chaining on large arrays.
    

```js
const numbers = [1, 2, 3, 4, 5];

// bad
let sum = 0;
for (let num of numbers) {
  sum += num;
}

// good
let sum = 0;
numbers.forEach((num) => {
  sum += num;
});

// best
const sum = numbers.reduce((total, num) => total + num, 0);

const bigNumberArray = []
‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍

// bad
const evenNumbers = [];
for (let i = 0; i < numbers.length; i++) {
    if (numbers[i] % 2 === 0) {
        evenNumbers.push(numbers[i]);
    }
}

// good
const evenNumbers = numbers.filter((num) => num % 2 === 0);
```

### Modules

-   Prefer import destructuring for named exports.
    

```js
// good
import _ from "lodash";
_.get()‍‍‍‍‍‍‍‍‍‍‍‍‍‍;

// better
import { get } from "lodash";
get();

// best
import get from "lodash/get";
get();
```

-   Prefer named exports over default.
    

```js
// ok
const foo = () => {}
export default foo

// good
export const foo = () => {}‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍
```

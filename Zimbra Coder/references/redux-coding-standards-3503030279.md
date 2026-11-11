# Redux Coding Standards

Source: <https://synacor.atlassian.net/wiki/pages/viewpage.action?pageId=3503030279>

Page ID: 3503030279

Parent ID: 3502866481

---

## Introduction

This document is intended to be a handy reference detailing how we use Redux across Zimbra Modern UI app.

> **Info**
> 
> 

This document is not complete by definition and currently only contains guidelines based on frequent and repeating reviews comments on the recent PRs. This document aims to help developers to avoid attracting the same review comments and thus improve the quality of the PRs.

### Reading values using `useSelector`

-   With useSelector(), returning a new object every time will always force a re-render by default. If you want to retrieve multiple values from the store, you can:
    
    -   Call useSelector() multiple times, with each call returning a single field value.
        
    -   Use Reselect or a similar library to create a memoized selector that returns multiple values in one object, but only returns a new object when one of the values has changed.
        
    -   Use the shallowEqual function from React-Redux as the equalityFn argument to useSelector().
        

```js
// Bad
const [userInfo, products, shoppingCart] = useSelector((state) => [
  state.userInfo,
  state.products,
  state.shoppingCart
]);

// Good
const userInfo = useSelector((state) => state.userInfo);
const products = useSelector((state) => state.products);
const shoppingCart = useSelector((state) => state.shoppingCart);
```

For more details read this document on [how to use Redux hooks](<https://react-redux.js.org/api/hooks>).

### Batch multiple dispatches into one

-   The `batch` function should be used to prevent unnecessary re-renders when dispatching multiple actions.
    

```js
// Bad
dispatch(increment());
dispatch(increment());

// Good
batch(() => {
  dispatch(increment())
  dispatch(increment())
});
```

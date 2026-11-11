# React Coding Standards

Source: <https://synacor.atlassian.net/wiki/pages/viewpage.action?pageId=3502964766>

Page ID: 3502964766

Parent ID: 3502866481

Export notes:
- Some Confluence page references have no resolvable page ID/space key; titles were preserved.

---

## Introduction

This document is intended to be a handy reference detailing React Style Guide. Although Zimbra uses Preact, the details listed below should still apply. This document should serve as a best practice reference on how to write performant and readable React code.

> **Info**
> 
> 

This document is not complete by definition and currently only contains guidelines based on frequent and repeating reviews comments on the recent PRs. This document aims to help developers to avoid attracting the same review comments and thus improve the quality of the PRs.

### Project Structure and Naming

-   **Extensions:** Use .js for React components.
    
-   **Filename:**
    
    -   Use Kebab Case for .js filenames, ex: `html-body.js`, `text-body.js`.
        

### Class vs. Function Components

> **Warning!**
> 
> -   Class components are no longer the preferred method of creating components. -- Except for components requiring **componentDidCatch**
>     
> -   Prefer Function component over Class component when creating new components.
>     

### Naming Conventions

-   Use meaningful names for Components
    

```js
// Bad
const User = () => {};

// Good
const UserInformation = () => {};
```

-   Use meaningful names for state variables and functions
    

```js
// Bad
const [data, setData] = useState();

// Good
const [messages, setMessages] = useState();
```

-   Use meaningful names for Component props
    

```js
// Bad
<ProductList data={products} />

// Good
<ProductList products={products} />
```

### Hooks

-   Always specify necessary dependencies for the useEffect, useCallback, useMemo hooks.
    

```js
// Bad
const handleClick((value) => {
  onClick(value);
}, []);

// Good
const handleClick((value) => {
  onClick(value);
}, [value, onClick]);
```

### Avoid polluting generic components.

-   Modern UI has a few generic components like `FolderList`, `FolderListItem`, `Viewer`, etc.
    
-   Generic component should not care about what they are rendering.
    
-   It's best not to pass any special prop to the child component or add any condition for special-casing the child component.
    

### Form Handling

-   Avoid using `useState` for form elements if you don't want the state to update on every interaction:
    

```js
// Bad as it re-renders the component on every key press
  const [email, setEmail] = useState();

  const handleInput = (e) => setEmail(e.target.value);

  return <input type="text" value={email} onChange={handleInput} />;

// Good as it doesn't cause re-renders. We can read the input value using `inputRef.current.value`
const inputRef = useRef(null);
return <input type="text" ref={inputRef} />
```

### Avoid wasted renders

-   Please read this document on tackling wasted renders [Confluence page reference; URL unavailable] to learn how to write performant components.
    

### Render Methods

-   Don't add unnecessary DOM nodes.
    

```js
// Bad
<div>
  <ChildComponent1 />
  <ChildComponent2 />
</div>

// Good
<Fragment>
  <ChildComponent1 />
  <ChildComponent2 />
</Fragment>
```

-   Do not nest conditional renders, return early or create sub components for complex components
    

```js
// bad
const ForecastComponent = () => {
  const [forecast, isLoading, error] = useFetch(/**/);

  return (
    <div>
      {isLoading ? (
        "Loading..."
      ) : (
        <div>
          {error ? <div>Error</div> : <div>{forecast.days.map(/**/)}</div>}
        </div>
      )}
    </div>
  );
};

// good
const ForecastComponent = () => {
  const [forecast, isLoading, error] = useFetch(/**/);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error has occured</div>;
  }

  return <div>{forecast.days.map(/**/)}</div>;
};
‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍
// great
const ForecastView = ({ forecast }) => {};
const ForecastLoading = () => {};
const ForecastError = () => {};

const ForecastComponent = () => {
  const [forecast, isLoading, error] = useFetch(/**/);

  if (isLoading) {
    return <ForecastLoading />;
  }

  if (error) {
    return <ForecastError />;
  }

  return <ForecastView forecast={forecast} />;
};‍‍‍‍‍‍‍‍‍‍‍‍‍‍
```

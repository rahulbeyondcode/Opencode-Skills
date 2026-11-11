# Frontend Code Review - Checklist 

Source: <https://synacor.atlassian.net/wiki/pages/viewpage.action?pageId=3305570360>

Page ID: 3305570360

Parent ID: 2719252502

---

Frontend code review checklist incorporating the following points along with examples:  

1.  **Component Size:**
    
    -   Keep components small. If a component exceeds 200-300 lines, consider breaking it into smaller child components.
        
    -   Example: If a "UserProfile" component handles both user information and user actions, consider splitting it into "UserInformation" and "UserActions" components.  
        
2.  **Comments:**
    
    -   Remove unnecessary comments that describe how the code works.
        
    -   Add necessary comments that describe why certain code decisions were made.
        
    -   Example:
        
        ```
        // Unnecessary comment describing what the function does:
        // Function to handle user login
        function loginUser() {
          // Code to handle user login
        }
        
        // Necessary comment explaining why a certain approach is used:
        // Using localStorage instead of cookies for authentication due to browser compatibility and security concerns.
        ```
        
3.  **Linting:**
    
    -   Ensure the code has no linter errors.
        
    -   Example: Running ESLint on the codebase and fixing any reported errors.  
        
4.  **React Warnings:**
    
    -   Resolve any React warnings reported in the console.
        
    -   Example: Adding a unique "key" prop to each element in an array to resolve the "Each child in a list should have a unique 'key'" warning.  
        
5.  **Code Reusability:**
    
    -   Avoid code repetition by abstracting common functionality into reusable functions or components.
        
    -   Example: If multiple components have similar functionality for handling form submissions, create a reusable "FormSubmitHandler" component.  
        
6.  **Code Patterns:**
    
    -   Ensure new code follows existing code patterns and conventions.
        
    -   Example: Following the naming conventions for variables and functions already established in the codebase.  
        
7.  **Unused Props:**
    
    -   Avoid passing unused props to components.
        
    -   Example: Removing any unused props being passed to a child component.  
        
8.  **Naming Conventions:**
    
    -   Follow consistent naming conventions for variables, file names, and translations.
        
    -   Example: Using camelCase for variable names and PascalCase for component names consistently throughout the codebase.  
        
9.  **Constants:**
    
    -   Avoid hardcoding values and use constants instead.
        
    -   Example: Define a constant `MAX_LOGIN_ATTEMPTS` instead of hardcoding the maximum login attempts value.  
        
10.  **Console Logs:**
     
     -   Avoid console.log statements in production code unless necessary for debugging.
         
     -   Example: Removing console.log statements used for debugging purposes before deploying to production.  
         
11.  **Promises and Async/Await:**
     
     -   Use Promises instead of Async/Await and handle API rejections gracefully.
         
     -   Example: Handling API rejections using the .catch() method of Promises.  
         
12.  **Destructuring:**
     
     -   Use destructuring assignment for arrays and objects where applicable.
         
     -   Example: Destructuring an object in a function parameter:
         
         ```
         function printUserDetails({ name, age }) {
           console.log(`${name} is ${age} years old.`);
         }
         ```
         
13.  **Custom Hooks:**
     
     -   Encapsulate reusable logic into custom hooks for better code organization and reusability.
         
     -   Example: Creating a custom hook to fetch data from an API:
         
         ```
         function useFetchData(url) {
           // Custom hook logic to fetch data from the provided URL
         }
         ```
         
14.  **useCallback with useEffect:**
     
     -   Use useCallback with useEffect for function calls with proper dependencies to optimize performance.
         
     -   Example: Using useCallback to memoize a function used as a dependency in useEffect:
         
         ```
         const fetchData = useCallback(() => {
           // Function to fetch data
         }, [dependency]);
         useEffect(() => {
           fetchData();
         }, [fetchData]);
         ```
         
15.  **Helper Functions:**
     
     -   Create helper functions (common functions) if a function is repeated elsewhere in the codebase.
         
     -   Example: Extracting a common date formatting function to avoid repetition:
         
         ```
         function formatDate(date) {
           // Function to format date
         }
         ```
         
16.  **Exception Handling:**
     
     -   Implement proper exception handling and resource cleanup to prevent memory leaks and unexpected behavior.
         
     -   Example: Using try-catch blocks to handle exceptions and clean up resources:
         
         ```
         try {
           // Code that may throw an error
         } catch (error) {
           // Error handling logic
         } finally {
           // Cleanup logic
         }
         ```
         
17.  **Avoid dangerouslySetInnerHTML:**
     
     -   Avoid using dangerouslySetInnerHTML whenever possible to mitigate XSS vulnerabilities.
         
     -   Example: Instead of setting HTML directly using dangerouslySetInnerHTML, consider using React components to render dynamic content safely.  
         
18.  **Library Size:**
     
     -   When introducing a new library for a feature, check its size to ensure it doesn't significantly impact the application's performance.
         
     -   Example: Checking the bundle size impact of adding a new library using tools like Bundlephobia or Webpack Bundle Analyzer.  
         
19.  **Timers Cleanup:**
     
     -   If any timers (e.g., setInterval) are registered during the mounting phase, ensure they are unregistered in the clean-up effects to avoid memory leaks.
         
     -   Example: Using clearInterval to unregister a setInterval timer in the clean-up effect of a useEffect hook.  
         
20.  **Image Alt Text:**
     
     -   Provide meaningful alternative text (alt attribute) for images to improve accessibility and provide context for non-visual browsers.
         
     -   Example: Adding alt text to an image tag:
         
         ```
         <img src="image.jpg" alt="Description of the image">
         ```
         
21.  **Git Commit Messages:**
     
     -   Write small and understandable Git commit messages that clearly describe the changes made.  
         
22.  **Avoid State Mutations in Reducers:**
     
     -   Ensure that reducers do not directly mutate state objects but return new state objects instead.
         
     -   Example: Using the spread operator to create a new state object in a reducer:
         
         ```
         case 'ADD_TODO':
           return [...state, action.payload];
         ```
         
23.  **Optimistic Response:**
     
     -   Instead of refetching data after a mutation, use optimisticResponse to update the cache and ensure the cached data remains accurate.
         
     -   Example: Suppose we have a GraphQL mutation to add a new todo item:
         
         ```
         mutation AddTodo($text: String!) {
           addTodo(text: $text) {
             id
             text
             completed
           }
         }
         ```
         
         In your React component using Apollo Client, you can define the mutation and the optimisticResponse like this:
         
         ```
         import { useMutation, gql } from '@apollo/client';
         
         const ADD_TODO = gql`
           mutation AddTodo($text: String!) {
             addTodo(text: $text) {
               id
               text
               completed
             }
           }
         `;
         
         const TodoForm = () => {
           const [addTodo] = useMutation(ADD_TODO);
         
           const handleSubmit = async (e) => {
             e.preventDefault();
         
             const text = e.target.elements.text.value;
         
             // Optimistically update the cache before the server response
             const optimisticTodo = {
               __typename: 'Todo',
               id: Math.round(Math.random() * -1000000), // Generate temporary ID
               text,
               completed: false,
             };
         
             try {
               await addTodo({
                 variables: { text },
                 optimisticResponse: {
                   __typename: 'Mutation',
                   addTodo: optimisticTodo,
                 },
                 // Update the cache after the server response
                 update: (cache, { data: { addTodo } }) => {
                   cache.modify({
                     fields: {
                       todos(existingTodos = []) {
                         const newTodoRef = cache.writeFragment({
                           data: addTodo,
                           fragment: gql`
                             fragment NewTodo on Todo {
                               id
                               text
                               completed
                             }
                           `,
                         });
                         return [...existingTodos, newTodoRef];
                       },
                     },
                   });
                 },
               });
             } catch (error) {
               console.error('Error adding todo:', error);
             }
         
             // Clear the input field after adding the todo
             e.target.elements.text.value = '';
           };
         
           return (
             <form onSubmit={handleSubmit}>
               <input type="text" name="text" />
               <button type="submit">Add Todo</button>
             </form>
           );
         };
         
         export default TodoForm;
         ```
         
         In this example:
         
         -   We define the mutation using gql from Apollo Client.
             
         -   Inside the handleSubmit function, we define the optimisticTodo object with the new todo item's details. This allows us to update the UI optimistically before receiving a response from the server.
             
         -   We call the addTodo mutation function with the text variable and provide the optimisticResponse option with the optimisticTodo object.
             
         -   In the update function, we manually update the cache with the new todo item after receiving a response from the server. We use cache.modify to add the new todo item to the list of existing todos.
             
         -   If an error occurs during the mutation, we catch and log the error.
             
         -   Finally, we clear the input field after successfully adding the todo item.
             
         
         Using optimisticResponse in this way allows us to provide a seamless user experience by updating the UI optimistically and maintaining consistency with the server-side data once the mutation is completed.
         

This comprehensive checklist covers various aspects of frontend code review, ensuring code quality, performance, security, and maintainability.

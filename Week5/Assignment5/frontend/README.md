# Online Food Ordering - Frontend (React + TypeScript)

## Setup
```bash
npm install
npm run dev      # http://127.0.0.1:5173
```

Make sure the backend is running on `http://127.0.0.1:5000` first
(see `../backend/README.md`) - the API base URL is set in `src/api/axiosClient.ts`.

## Project structure
```
src/
  api/
    axiosClient.ts        # axios instance, attaches JWT to every request
  types/
    index.ts               # shared TypeScript interfaces (User, Order, ...)
  context/
    AuthContext.tsx        # logged-in user + token, persisted to localStorage
    CartContext.tsx        # in-memory cart before an order is placed
  components/
    <ComponentName>/
      <ComponentName>.tsx   # markup
      use<ComponentName>.ts # the component's logic/state, as a hook
      <ComponentName>.css   # styling for that component only
  pages/
    <PageName>/             # same three-file pattern as components
  App.tsx                   # routes
  main.tsx                  # app entry point (providers + router)
```

## Pages
- `/` - Restaurants list
- `/restaurants/:id` - Menu for a restaurant + cart, place an order
- `/login`, `/register`
- `/orders` - your past orders (requires login)
- `/profile` - view/edit your profile (requires login)

Admin-only actions (creating restaurants/food items, viewing the reports in
`backend/subqueries.sql`) don't have a UI screen in this learning version -
call those endpoints directly with the admin JWT.

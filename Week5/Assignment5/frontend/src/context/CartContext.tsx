import { createContext, useContext, useState, ReactNode } from "react";
import { CartItem, FoodItem } from "../types";

interface CartContextValue {
  items: CartItem[];
  addItem: (food: FoodItem) => void;
  removeItem: (foodItemId: number) => void;
  clearCart: () => void;
  total: number;
}

const CartContext = createContext<CartContextValue | undefined>(undefined);

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([]);

  function addItem(food: FoodItem) {
    setItems((prev) => {
      const existing = prev.find((i) => i.food_item_id === food.food_item_id);
      if (existing) {
        return prev.map((i) =>
          i.food_item_id === food.food_item_id ? { ...i, quantity: i.quantity + 1 } : i
        );
      }
      return [
        ...prev,
        {
          food_item_id: food.food_item_id,
          name: food.name,
          price: food.price,
          quantity: 1,
          restaurant_id: food.restaurant_id,
        },
      ];
    });
  }

  function removeItem(foodItemId: number) {
    setItems((prev) => prev.filter((i) => i.food_item_id !== foodItemId));
  }

  function clearCart() {
    setItems([]);
  }

  const total = items.reduce((sum, i) => sum + i.price * i.quantity, 0);

  return (
    <CartContext.Provider value={{ items, addItem, removeItem, clearCart, total }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) throw new Error("useCart must be used inside CartProvider");
  return context;
}
